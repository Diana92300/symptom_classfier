from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import service
from schema import UserInput

app = FastAPI()

# Configure CORS
origins = ["http://localhost", "http://localhost:3000", "http://localhost:5173", ]

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"], )


@app.post("/")
async def process_input(data: UserInput):
    diagnosis = service.classify_disease(data.user_input)

    return diagnosis
