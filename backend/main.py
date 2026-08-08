from fastapi import FastAPI, UploadFile
from ultralytics import YOLO

app = FastAPI(title="Yolo Detection App")
model = YOLO("yolo26n.pt")

#health check
@app.get ("/health")
def health_check():
    return {"status":"ok"}

#detect image
@app.post ("/api/detect/image")
def upload_files(file: UploadFile):
    return {"filename":file.filename}