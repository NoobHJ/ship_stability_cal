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

current_directory = os.path.dirname(os.path.realpath(__file__))
upload_directory = os.path.join(current_directory, 'uploaded_stl_files')

os.makedirs(upload_directory, exist_ok=True)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

@app.post("/upload-stl")
async def upload_stl(file: UploadFile):
    try:
        with open(os.path.join(upload_directory, file.filename), "wb") as buffer:
            buffer.write(await file.read())
        
        filename_without_extension = os.path.splitext(file.filename)[0]

        xyz_result = await make_xyz("./uploaded_stl_files/" + file.filename, "./db/"+filename_without_extension+"_xyz.csv")
        off_result = await make_off("./db/"+filename_without_extension+"_xyz.csv","./db/"+filename_without_extension+"_offset.csv")
        cal_result = await cal_run("./db/"+filename_without_extension+"_offset.csv")
        
        combined_result = f"result(unit : mm, g): {cal_result}"
        print(combined_result)
        return JSONResponse(content={"message": combined_result})
    except Exception as e:
        print(e)
        return JSONResponse(content={"message": str(e)}, status_code=500)
