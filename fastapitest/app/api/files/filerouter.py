import http
import urllib

from fastapi import APIRouter, File, UploadFile, Response
from fastapi.responses import FileResponse
from starlette.responses import Response
from starlette.responses import StreamingResponse
import io
from ...db.xgridfs import XGridFS
from ..models.responsemodel import ResponseBaseModel
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
async def upload_file(file: UploadFile=None):
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

