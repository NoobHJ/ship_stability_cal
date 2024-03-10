from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import BackgroundTasks
import os
from subprocess import run

from cal.make_xyz import make_xyz
from cal.make_offset import make_off
from cal.cal_main import cal_run
from cal.visualize import main

# 현재 스크립트의 디렉토리를 기준으로 하위 디렉토리 생성
current_directory = os.path.dirname(os.path.realpath(__file__))
upload_directory = os.path.join(current_directory, 'uploaded_stl_files')

# 디렉토리가 없으면 생성
os.makedirs(upload_directory, exist_ok=True)

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 원본 허용 (실제 배포 환경에서는 이 값을 적절히 변경하세요)
    allow_credentials=True,
    allow_methods=["*"],  # 모든 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

@app.post("/upload-stl")
async def upload_stl(file: UploadFile):
    try:
        # Save uploaded .stl file to a desired location
        with open(os.path.join(upload_directory, file.filename), "wb") as buffer:
            buffer.write(await file.read())
        
        filename_without_extension = os.path.splitext(file.filename)[0]

        xyz_result = await make_xyz("./uploaded_stl_files/" + file.filename, "./db/"+filename_without_extension+"_xyz.csv")
        off_result = await make_off("./db/"+filename_without_extension+"_xyz.csv","./db/"+filename_without_extension+"_offset.csv")
        cal_result = await cal_run("./db/"+filename_without_extension+"_offset.csv")

        combined_result = f"result(unit : mm, g): {cal_result}"

        return JSONResponse(content={"message": combined_result})
    except Exception as e:
        print(e)
        return JSONResponse(content={"message": str(e)}, status_code=500)
