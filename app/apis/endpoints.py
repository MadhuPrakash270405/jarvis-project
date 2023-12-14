from datetime import timedelta
import os
from fastapi import Depends, HTTPException, Request
import base64
import cv2
import mediapipe as mp
import numpy as np
from fastapi import APIRouter
import face_recognition
from pydantic import BaseModel
from pyparsing import Optional
from utils.jwt_auth import ACCESS_TOKEN_EXPIRE_MINUTES, User, create_access_token, get_current_user

from utils.audio_functions import text_to_voice
from dotenv import load_dotenv
from apis.helper import process_the_audio_command
# Load the .env file
load_dotenv()

router = APIRouter()




@router.post("/register/face")
async def register_face(request: Request):
    try:
        data = await request.json()
        name=data.get('name')
        pin=data.get('pin')
        email=data.get('email')
        USER = User(username=name, email=email,pin=int(pin))
        # if 'username' in request.session:
        #     raise HTTPException(status_code=400, detail="User already registered.")
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
            cv2.imwrite(f"images/verification_image_{pin}.png", image)
            # request.session["username"] = name
            # request.session["loginPin"] = pin
            # request.session["email"] = email
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                USER, expires_delta=access_token_expires
            )
            return {"message": "Face registered successfully.",'access_token':access_token}
        else:
            raise HTTPException(status_code=400, detail="No face detected in the image.")
    except Exception as e:
        # Log the exception and return a generic error message
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred during face registration.")


@router.post("/verify/face")
async def verify_face(request: Request, current_user: User = Depends(get_current_user)):
    try:
        data = await request.json()
        loginPin = data.get('loginpin')
        image_data = data['image']
        email=data.get('emailInput')
        if not current_user and (current_user.get('pin')==loginPin and current_user.get('email')==email):
            raise HTTPException(status_code=401, detail="Unauthorized")
        image_data = image_data.split(",")[1]
        image_bytes = base64.b64decode(image_data)
        nparr = np.frombuffer(image_bytes, np.uint8)
        unknown_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        # Load the image of the registered user

        known_image = face_recognition.load_image_file(f"images/verification_image_{loginPin}.png")
        print(f'images/verification_image_{loginPin}.png')
        known_encoding = face_recognition.face_encodings(known_image)[0]
        unknown_image_rgb = cv2.cvtColor(unknown_image, cv2.COLOR_BGR2RGB)
        unknown_encoding = face_recognition.face_encodings(unknown_image_rgb)[0]
        # Compare the faces
        results = face_recognition.compare_faces([known_encoding], unknown_encoding,tolerance=0.5)
        print(results[0])
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



@router.post("/process_transcript")
async def process_transcript(request: Request, current_user: User = Depends(get_current_user)):
    try:
        if not current_user:
            raise HTTPException(status_code=401, detail="Unauthorized")
        # Load the newly captured (unknown) face image
        data = await request.json()
        transcript = data.get('transcript')
        message=process_the_audio_command(transcript)
        return {"message": message} 
    except Exception as e:
        # For any other exceptions
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred during face verification.")