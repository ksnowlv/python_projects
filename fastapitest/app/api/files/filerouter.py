from fastapi import APIRouter, File, UploadFile

router = APIRouter(
    prefix="/file",
    tags=["文件操作接口"],
    responses={404: {"description": "Not found111"}},
)


@router.post("/upload_file")
async def upload_file(file: bytes | None = File(default=None)):
    if not file:
        return {"message": "No file sent"}
    else:
        return {"file_size": len(file)}


"""
curl -X POST http://localhost:8081/create_file/upload \
-F "file=@/Users/lvwei/Documents/1.txt" \
-H "Content-Type: multipart/form-data"

curl -X POST http://localhost:8081/file/upload \
-F "file=@/Users/ksnowlv/Documents/1.txt" \
-H "Content-Type: multipart/form-data"
"""


@router.post("/upload_file/")
async def upload_file(file: UploadFile | None = None):
    if not file:
        return {"message": "No upload file sent"}
    else:
        return {"filename": file.filename}


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


@router.post("/upload_files/")
async def upload_files(files: list[bytes] = File()):
    return {"file_sizes": [len(file) for file in files]}


@router.post("/create_upload_files/")
async def create_upload_files(fileList: list[UploadFile]):
    return {"filenames": [file.filename for file in fileList]}

# class FileRouter(APIRouter):
#
#     def __init__(self):
#         super().__init__()
#
#         @self.post("/upload_file")
#         async def upload_file(file: bytes | None = File(default=None)):
#             if not file:
#                 return {"message": "No file sent"}
#             else:
#                 return {"file_size": len(file)}
#
#         """
#         curl -X POST http://localhost:8081/create_file/upload \
#         -F "file=@/Users/lvwei/Documents/1.txt" \
#         -H "Content-Type: multipart/form-data"
#
#         curl -X POST http://localhost:8081/file/upload \
#         -F "file=@/Users/ksnowlv/Documents/1.txt" \
#         -H "Content-Type: multipart/form-data"
#         """
#
#         @self.post("/upload_file/")
#         async def upload_file(file: UploadFile | None = None):
#             if not file:
#                 return {"message": "No upload file sent"}
#             else:
#                 return {"filename": file.filename}
#
#         """
#         		 curl -X POST http://localhost:8080/file/multifileupload \
#         		  -F "upload[]=@/Users/lvwei/Documents/1.txt" \
#         		  -F "upload[]=@/Users/lvwei/Documents/2.txt" \
#         		  -F "upload[]=@/Users/lvwei/Documents/3.txt" \
#         		  -H "Content-Type: multipart/form-data"
#
#         		  curl -X POST http://localhost:8080/file/multifileupload \
#         		  -F "upload[]=@/Users/ksnowlv/Documents/1.txt" \
#         		  -F "upload[]=@/Users/ksnowlv/Documents/2.txt" \
#         		  -F "upload[]=@/Users/ksnowlv/Documents/3.txt" \
#         		  -H "Content-Type: multipart/form-data"
#         """
#
#         @self.post("/upload_files/")
#         async def upload_files(files: list[bytes] = File()):
#             return {"file_sizes": [len(file) for file in files]}
#
#         @self.post("/create_upload_files/")
#         async def create_upload_files(fileList: list[UploadFile]):
#             return {"filenames": [file.filename for file in fileList]}
