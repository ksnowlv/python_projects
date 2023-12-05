
import os.path
from fastapi import APIRouter, UploadFile, File, Response
from app.core.xhdfs import XHDFS
from ..models.responsemodel import ResponseBaseModel

router = APIRouter(
    prefix="/hdfs",
    tags=["hdfs"],
    responses={404: {"description": "Not found"}},
)


@router.get("/list_files")
async def list_files(directory: str):
    fs = XHDFS.hdfs()
    file_list = fs.list_dir(directory)
    return ResponseBaseModel(data={"files": file_list})


@router.post("/hdfsUploadFile/")
async def hdfs_upload_file(file: UploadFile = File(...)):
    file_content = await file.read()
    file_name = file.filename
    # 上传文件到 HDFS
    remote_path = f'/user/lvwei/{file_name}'  # 指定远程路径

    fs = XHDFS.hdfs()
    if fs.exists_file_dir(remote_path):
        return ResponseBaseModel(message=f"{file_name} 已存在")
    else:
        fs.create_file(remote_path, file_content)
        return ResponseBaseModel(message=f"{file_name} 上传成功")


@router.get("/hdfsDownloadFile/{file_path:path}")
def hdfs_download_file(file_path: str):

    file_name = os.path.basename(file_path)
    fs = XHDFS.hdfs()

    if fs.exists_file_dir(file_path):
        content = fs.read_file(file_path)
        return Response(content=content, media_type="application/octet-stream",
                        headers={"Content-Disposition": f"attachment; filename={file_path}"})
    else:
        return ResponseBaseModel(message=f"{file_name} 找不到")
