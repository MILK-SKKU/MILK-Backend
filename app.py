from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import k_dictionary as kd
import json
from problem import get_similar_word, quiz_generator

class Item(BaseModel):
    data : str

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/dict/{word}')
async def dictionary(word : str):
    return kd.search_word(word)


@app.post('/createquiz')
async def createquiz(item : Item):
    return quiz_generator(item.data)


@app.get('/similarword/{word}')
async def similarword(word : str):
    return get_similar_word(word)