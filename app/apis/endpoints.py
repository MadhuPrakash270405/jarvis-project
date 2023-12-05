from fastapi import Request
import base64
import os
from fastapi import APIRouter

router = APIRouter()

@router.post("/register/face")
async def register_face(request: Request):
    data = await request.json()
    image_data = data['image']
    image_data = image_data.split(",")[1]  # Remove the "data:image/png;base64," part
    # Convert base64 to bytes
    image_bytes = base64.b64decode(image_data)
    # Write the image to a file or process it as needed
    with open("images/face_image.png", "wb") as file:
        file.write(image_bytes)
    # Here you would add the logic to store or process the image
    return {"message": "Face registered successfully."}

# Add additional endpoints for voice registration
