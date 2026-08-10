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
async def upload_files(file: UploadFile):
    contents = await file.read()
    print (len(contents))
    temp_path = "temp_" + file.filename
    with open (temp_path, "wb") as f:
        f.write(contents)

    results=model(temp_path)
    print(results[0].boxes)
    return {"filename":file.filename}

