
from fastapi import APIRouter, File, UploadFile

file_routers = APIRouter()
"""
curl -X POST http://localhost:8081/create_file/upload \
-F "file=@/Users/lvwei/Documents/1.txt" \
-H "Content-Type: multipart/form-data"

curl -X POST http://localhost:8081/file/upload \
-F "file=@/Users/ksnowlv/Documents/1.txt" \
-H "Content-Type: multipart/form-data"
"""
@file_routers.post("/create_file/")
async def create_file(file: bytes | None = File(default=None)):
    if not file:
        return {"message": "No file sent"}
    else:
        return {"file_size": len(file)}

@file_routers.post("/create_upload_file/")
async def create_upload_file(file: UploadFile | None = None):
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
@file_routers.post("/create_files/")
async def create_files(files: list[bytes] = File()):
    return {"file_sizes": [len(file) for file in files]}


@file_routers.post("/create_upload_files/")
async def create_upload_files(files: list[UploadFile]):
    return {"filenames": [file.filename for file in files]}
