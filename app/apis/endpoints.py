from fastapi import HTTPException, Request
import base64
import cv2
import mediapipe as mp
import numpy as np
from fastapi import APIRouter
import face_recognition

router = APIRouter()

@router.post("/register/face")
async def register_face(request: Request):
    try:
        data = await request.json()
        image_data = data.get('image')
        image_data = image_data.split(",")[1]  # Remove the "data:image/png;base64," part
        image_bytes = base64.b64decode(image_data)
        
        # Convert bytes to numpy array and then to an image
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Initialize MediaPipe Face Detection
        mp_face_detection = mp.solutions.face_detection
        face_detection = mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5)

        # Convert the BGR image to RGB before processing
        results = face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        if results.detections:
            cv2.imwrite(f"images/user.png", image)
            return {"message": "Face registered successfully."}
        else:
            raise HTTPException(status_code=400, detail="No face detected in the image.")
    except Exception as e:
        # Log the exception and return a generic error message
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred during face registration.")


@router.post("/verify/face")
async def verify_face(request: Request):
    try:
        # Load the newly captured (unknown) face image
        data = await request.json()
        image_data = data['image']
        image_data = image_data.split(",")[1]
        image_bytes = base64.b64decode(image_data)
        nparr = np.frombuffer(image_bytes, np.uint8)
        unknown_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        cv2.imwrite(f"images/verification_image.png", unknown_image)
        # Convert the unknown image to RGB for face_recognition

        known_image = face_recognition.load_image_file("images/user.png")
        known_encoding = face_recognition.face_encodings(known_image)[0]
        unknown_image_rgb = cv2.cvtColor(unknown_image, cv2.COLOR_BGR2RGB)
        unknown_encoding = face_recognition.face_encodings(unknown_image_rgb)[0]

        # Compare the faces
        results = face_recognition.compare_faces([known_encoding], unknown_encoding)
        # return {"message": "Face verified successfully."}
        if results[0]:
            return {"message": "Face verified successfully."}
        else:
            return {"message": "Faces do not match."}
    except IndexError:
        # If no face is found in one of the images
        raise HTTPException(status_code=400, detail="Face not found in one of the images.")
    except Exception as e:
        # For any other exceptions
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred during face verification.")