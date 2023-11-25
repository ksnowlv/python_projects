import http
import io
import urllib

import bson
from fastapi import APIRouter, UploadFile, Request, File
from starlette.responses import Response
from starlette.responses import StreamingResponse

from ..models.responsemodel import ResponseBaseModel, ResponseNotFoundModel
from ...core.xlogger import xlogger
from ...core.xfastdfs import XFastDFS
from ...db.xgridfs import XGridFS
from ...utils.md5utils import md5_by_data

router = APIRouter(
    prefix="/file",
    tags=["文件操作接口"],
    responses={404: {"description": "Not found"}},
)

"""
curl -X POST http://localhost:8081/create_file/upload \
-F "file=@/Users/lvwei/Documents/1.txt" \
-H "Content-Type: multipart/form-data"

curl -X POST http://localhost:8081/file/upload_file_1 \
-F "file=@/Users/ksnowlv/Documents/1.txt" \
-H "Content-Type: multipart/form-data"
"""


@router.post("/uploadFile", response_model=ResponseBaseModel)
async def upload_file(file: UploadFile = None):
    if not file:
        return ResponseBaseModel(code=http.HTTPStatus.NOT_ACCEPTABLE, message=f"文件为空，上传失败", data={
            "file_id": 0,
        })

    f = XGridFS.shared_gridfs().find_one({'filename': file.filename})
    # 如果文件存在，则返回文件id；如果不存在，则写入GridFS
    file_content = None
    if f:
        gridfs_file_content = XGridFS.shared_gridfs().gridfs().get(f._id).read()
        file_content = await file.read()
        # 比较文件是否相同
        if md5_by_data(file_content) == md5_by_data(gridfs_file_content):
            return ResponseBaseModel(message=f"文件{file.filename}已经存在", data={
                "file_id": str(f._id),
            })

    if not file_content:
        file_content = await file.read()
    # 将文件写入 GridFS 中
    file_id = XGridFS.shared_gridfs().put_file(file_content, file.filename)

    if not file_id:
        return ResponseBaseModel(message=f"文件{file.filename}上传失败", data={
            "file_id": 0,
        })

    return ResponseBaseModel(message=f"文件{file.filename}上传成功", data={
        "file_id": str(file_id),
    })


"""
         curl -X POST http://localhost:8080/file/multifileupload \
          -F "upload[]=@/Users/lvwei/Documents/1.txt" \
          -F "upload[]=@/Users/lvwei/Documents/2.txt" \
          -F "upload[]=@/Users/lvwei/Documents/3.txt" \
          -H "Content-Type: multipart/form-data"

          curl -X POST http://localhost:8080/file/multifileupload \
          -F "upload[]=@/Users/ksnowlv/Documents/1.txt" \
          -F "upload[]=@/Users/ksnowlv/Documents/2.txt" \
          -F "upload[]=@/Users/ksnowlv/Documents/3.txt" \
          -H "Content-Type: multipart/form-data"
"""


@router.post("/uploadMultipleFiles", response_model=ResponseBaseModel)
async def upload_multiple_files(files: list[UploadFile] = None):
    upload_files = []

    try:
        for file in files:
            content = await file.read()
            file_id = XGridFS.shared_gridfs().put_file(content, file.filename)
            upload_files.append({"fileId": str(file_id), "fileName": file.filename})
    except:
        return ResponseBaseModel(code=http.HTTPStatus.NOT_FOUND, message="存储服务异常")

    if len(upload_files) > 0:
        return ResponseBaseModel(data={"files": upload_files})
    else:
        return ResponseBaseModel(message="您没有上传任何文件!", data={"files": upload_files})


"""
curl -o output.file -r 2000-5000 http://127.0.0.1:8081/file/downloadFile/655d97c659b1196d5e0cc7e8

curl -o output.file -r -9000 http://127.0.0.1:8081/file/downloadFile/655d97c659b1196d5e0cc7e8

curl -o output.file -r 9000- http://127.0.0.1:8081/file/downloadFile/655d97c659b1196d5e0cc7e8

curl -o output.file  http://127.0.0.1:8081/file/downloadFile/655d97c659b1196d5e0cc7e8

"""


@router.get("/fileId/{file_id}")
async def get_file_content(file_id: str, response: Response):
    try:
        file = XGridFS.shared_gridfs().find_file(file_id)

        if file:
            content = file.read()
            # 解决文件名称为中文的情况
            encoded_filename = urllib.parse.quote(file.filename)
            response.headers["Content-Disposition"] = f'attachment; filename="{encoded_filename}"'
            return Response(content, media_type='application/octet-stream', headers=response.headers)

            # 返回上述Response或下面StreamingResponse都可以
            # file_stream = io.BytesIO(content)
            # return StreamingResponse(file_stream, media_type='application/octet-stream', headers=response.headers)
        else:
            return ResponseBaseModel(code=http.HTTPStatus.NOT_FOUND, message=f"找不到文件{file_id}")
    except:
        return ResponseBaseModel(code=http.HTTPStatus.SERVICE_UNAVAILABLE, message="存储服务异常")


# http://127.0.0.1:8081/file/downloadFile/655d97c659b1196d5e0cc7e8

@router.get("/downloadFile/{file_id}")
async def download_file(file_id: str, request: Request):
    file = XGridFS.shared_gridfs().find_one({"_id": bson.objectid.ObjectId(file_id)})
    if not file:
        return ResponseNotFoundModel()

    total_file_size = file.length
    range_header = request.headers.get("range")
    content_length = chunk_size = total_file_size
    offset = 0
    encoded_filename = urllib.parse.quote(file.filename)

    res_headers = {
        'content-disposition': f'attachment; filename="{encoded_filename}"',
        'accept-ranges': 'bytes',
        'connection': 'keep-alive',
        'content-length': str(content_length),
        # 'last-modified': time,
    }
    file_range = None

    if range_header:
        xlogger.info(f"range_header:{range_header}")
        file_range = parse_range_header(range_header, total_file_size)

        if file_range and not file_range.is_valid(total_file_size):
            return ResponseNotFoundModel(message="超出文件范围")

        res_headers.update({'content-range': file_range.content_range(total_file_size)})
        if file_range:
            offset = file_range.start
            content_length = chunk_size = file_range.stop - file_range.start
            res_headers.update({'content-length': str(content_length)})

    file.seek(offset)
    res_data = file.read(chunk_size)

    xlogger.info(f"res headers= {res_headers}")

    return Response(res_data,
                    status_code=206 if file_range and file_range.is_valid(content_length) else 200,
                    media_type='application/octet-stream',
                    headers=res_headers)
    # 使用Response或下面的StreamingResponse
    file_stream = io.BytesIO(res_data)
    return StreamingResponse(
        file_stream,
        status_code=206 if file_range and file_range.is_valid(content_length) else 200,
        media_type='application/octet-stream',
        headers=res_headers
    )


class XRange:
    def __init__(self, start=None, stop=None):
        self.start = start
        self.stop = stop

    def content_range(self, file_size):
        # Content-Range：bytes 2400-3599/5000
        if self.start is None:
            return f"bytes */{file_size}"
        elif self.stop is None:
            return f"bytes {self.start}-/{file_size}"
        else:
            return f"bytes {self.start}-{self.stop - 1}/{file_size}"

    def is_valid(self, length):
        if self.start is None:
            self.start = length - self.stop
            self.stop = length
        elif self.stop is None or self.stop > length:
            self.stop = length
        return 0 <= self.start < self.stop


def parse_range_header(range_header, length):
    if range_header is None:
        return None
    range_parts = range_header.split("=")[1].split("-")
    start, stop = [int(x) if x else None for x in range_parts]

    if start is not None and start >= length:
        return None
    if stop is not None and stop >= length:
        stop = length - 1
    return XRange(start, stop)


@router.post("/uploadFileWithFastDFS", response_model=ResponseBaseModel)
async def upload_file_fast_dfs(file: UploadFile = File(...)):
    if not file:
        return ResponseBaseModel(code=http.HTTPStatus.NOT_ACCEPTABLE, message=f"文件为空，上传失败", data={
            "file_id": 0,
        })

    file_info = XFastDFS.fast_dfs().upload_by_buffer(file.read(), file.filename)
    # 如果文件存在，则返回文件id；如果不存在，则写入GridFS

    if file_info:
        return ResponseBaseModel(message=f"文件{file.filename}上传成功", data={
            "file_id": str(file_info['Remote file_id'])})

    return ResponseBaseModel(message=f"文件{file.filename}上传失败", data={
            "file_id": 0,
        })


@router.get("/fileIdByFastFDS/{file_id}")
async def get_file_contentByFastFDS(file_id: str, response: Response):
    try:
        file_info = XFastDFS.fast_dfs().get_meta_data(file_id)

        if file_info:
            # 解决文件名称为中文的情况
            encoded_filename = urllib.parse.quote(file_info.filename)
            response.headers["Content-Disposition"] = f'attachment; filename="{encoded_filename}"'

            return Response(file_info.content, media_type='application/octet-stream', headers=response.headers)

            # 返回上述Response或下面StreamingResponse都可以
            # file_stream = io.BytesIO(content)
            # return StreamingResponse(file_stream, media_type='application/octet-stream', headers=response.headers)
        else:
            return ResponseBaseModel(code=http.HTTPStatus.NOT_FOUND, message=f"找不到文件{file_id}")
    except:
        return ResponseBaseModel(code=http.HTTPStatus.SERVICE_UNAVAILABLE, message="存储服务异常")


