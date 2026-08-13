from fastapi import FastAPI, UploadFile
from ultralytics import YOLO
import json
import time

app = FastAPI(title="Yolo Detection App")
model = YOLO("yolo26n.pt")

#health check
@app.get ("/health")
def health_check():
    return {"status":"ok"}

#detect image
@app.post ("/api/detect/image") 
async def upload_files(file: UploadFile):
    #save temporary image files
    contents = await file.read()
    print (len(contents))
    temp_path = "temp_" + file.filename
    with open (temp_path, "wb") as f:
        f.write(contents)

    #image detection process
    start_time = time.time()
    results=model(temp_path)
    boxes = results[0].boxes
    print(boxes)
    detection = []
    for i in range(len(boxes.cls)):
        cls = model.names[int(boxes.cls[i])]
        conf = boxes.conf[i].item()
        xyxy = boxes.xyxy[i].tolist()
        detection.append({"class": cls, "confidence": round(conf,2), "bbox": [round(coord,2) for coord in xyxy]})
    count = len(boxes.cls)
    end_time = time.time()
    time_result = (end_time - start_time)*1000

    #Response w/ JSON format
    response = ({
        "count": count, 
        "detection": detection,
        "time": time_result
        })
    
    return (response)