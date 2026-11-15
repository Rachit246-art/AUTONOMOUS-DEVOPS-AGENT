# We are connecting all the components we've created so far and initializing our FastAPI application.
# Think of main.py as the starting point of our entire backend.


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.incidents import router as incidents_router


app = FastAPI(
    title="Autonomous DevOps Agent",
    description="API for storing and managing DevOps errors",
    version="1.0.0"
)


# CORS Configuration: Allow React Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register API Router
app.include_router(
    incidents_router,
    prefix="/api"
)


@app.get("/")
def home():
    return {
        "message": "Autonomous DevOps Agent API is running"
    }
