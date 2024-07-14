from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

origins = [
    "http://localhost:5173",
    "https://fp-client-107bc916594c.herokuapp.com/",
    "https://fp-client-107bc916594c.herokuapp.com"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/events')
def events():
    # Read JSON data from the file
    with open('events.json') as json_file:
        data = json.load(json_file)
    return data