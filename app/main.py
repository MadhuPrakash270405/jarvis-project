from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

from apis.endpoints import router as endpoints_router
from frontend.routes import router as frontend_router

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(endpoints_router)
app.include_router(frontend_router)


if __name__ == "__main__":
     uvicorn.run(app, host="0.0.0.0", port=8001)
