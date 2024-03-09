# ship_stability_cal

.stl로 modeling 된 hull의 형상에 open3d-pointcloud를 활용하여 1000만개의 point seed를 뿌려
해당 값들을 Offset Table로 정리하는 과정

uvicorn main:app --host 0.0.0.0 --port 8000 --reload
