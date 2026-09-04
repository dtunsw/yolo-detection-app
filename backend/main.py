from fastapi import FastAPI, UploadFile, HTTPException, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from ultralytics import YOLO
import subprocess
import json
import time
import os
import cv2

app = FastAPI(title="Yolo Detection App")
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:5173"],
    allow_methods= {"*"},
    allow_headers={"*"}
)

model = YOLO("yolo26n.pt")
image_items = {"image/jpeg", "image/png"}
video_items = {"video/mp4"}

#health check
@app.get ("/health")
def health_check():
    return {"status":"ok"}

#detect image
@app.post ("/api/detect/image") 
async def upload_files(file: UploadFile = File(...)):
    if file.content_type not in image_items:
        raise HTTPException (status_code=400, detail="Invalide file type")

 #limit file size
    file.file.seek(0,2)
    file_size = file.file.tell()
    file.file.seek(0)
    if file_size > 50*1024*1024:
        raise HTTPException(status_code=400, detail="File size too large!")

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
    annotated = results[0].plot()
    output_filename = "annotated" + file.filename
    annotated_image = cv2.imwrite(filename=output_filename, img=annotated)

    #Response w/ JSON format
    response = ({
        "count": count, 
        "detection": detection,
        "time": time_result,
        "annotated_image": output_filename
        })
    os.remove (temp_path)
    return (response)


#detect videos
@app.post ("/api/detect/video")
async def detect_video(file: UploadFile):
    #file type detect
    if file.content_type not in video_items:
        raise HTTPException(status_code=400, detail="Invalid file type")

    #limit file size
    file.file.seek(0,2)
    file_size = file.file.tell()
    file.file.seek(0)
    if file_size > 100*1024*1024:
        raise HTTPException(status_code=400, detail="File's size too large")

    #save temporary file
    contents = await file.read()
    print (len(contents))
    temp_path = "temp_" + file.filename
    with open (temp_path, "wb") as f:
        f.write(contents)

    #video detection process
    result = model(temp_path)

    class_counts = {}
    output_video = cv2.VideoCapture(temp_path)
    raw_filename = "raw" + file.filename
    output_filename = "annotated" + file.filename
    annotated_video = cv2.VideoWriter(filename = raw_filename, fourcc = cv2.VideoWriter_fourcc(*'mp4v'), fps = output_video.get(cv2.CAP_PROP_FPS), frameSize = (int(output_video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(output_video.get(cv2.CAP_PROP_FRAME_HEIGHT))))
    for results in result:
        annotated_frame = results.plot()
        annotated_video.write(annotated_frame)
    output_video.release()
    annotated_video.release()
    for frame_result in result:
        frame_boxes = frame_result.boxes
        for i in range (len(frame_result.boxes)):
            class_name = model.names[int(frame_boxes.cls[i])]
            class_counts[class_name] = class_counts.get(class_name, 0) + 1

    subprocess.run([
        "ffmpeg", "-y", "-i", raw_filename,
        "-vcodec", "libx264", "-pix_fmt", "yuv420p",
        output_filename
    ], check=True)
    os.remove (temp_path)
    os.remove (raw_filename)
    return {"summary": class_counts, "annotated_video": output_filename}
    
@app.get ("/api/results/{filename}")
def get_result (filename: str):
    return FileResponse(filename)