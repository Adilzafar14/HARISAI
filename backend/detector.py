import cv2
from ultralytics import YOLO

# Load YOLO model
model = YOLO('../models/yolov8n.pt')
print("✅ YOLO Model Loaded!")

def count_people(frame):
    results = model(frame, verbose=False)
    people = 0
    for r in results:
        for box in r.boxes:
            if int(box.cls) == 0:  # class 0 = person
                people += 1
                x1,y1,x2,y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,212,200),2)
                cv2.putText(frame,'Pilgrim',(x1,y1-8),
                    cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,212,200),1)
    cv2.putText(frame,f'People: {people}',(10,30),
        cv2.FONT_HERSHEY_SIMPLEX,1,(0,212,200),2)
    return frame, people

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    print("Camera ON - Press Q to quit")
    while True:
        ret, frame = cap.read()
        if not ret: break
        frame, count = count_people(frame)
        print(f"People: {count}")
        cv2.imshow('HARISAI - YOLO People Counter', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()