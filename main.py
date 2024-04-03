# -*- coding:utf-8 -*-

import os
import json
from fastapi import Header, FastAPI, HTTPException, status, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from utils import generate_music, get_feed, generate_lyrics, get_lyrics
from deps import get_token
import schemas

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", description="Enter your bearer token")



async def verify_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization scheme")
    token = authorization.split(" ")[1]
    if token != os.getenv("API_TOKEN"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


@app.get("/")
async def get_root(_: str = Depends(verify_token)):
    return schemas.Response()


@app.post("/generate")
async def generate(data: schemas.GenerateBase, _: str = Depends(verify_token), token: str = Depends(get_token)):
    try:
        resp = await generate_music(data.dict(), token)
        return resp
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.get("/feed/{aid}")
async def fetch_feed(aid: str, _: str = Depends(verify_token), token: str = Depends(get_token)):
    try:
        resp = await get_feed(aid, token)
        return resp
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.post("/generate/lyrics/")
async def generate_lyrics_post(request: Request, _: str = Depends(verify_token), token: str = Depends(get_token)):
    req = await request.json()
    prompt = req.get("prompt")
    if prompt is None:
        raise HTTPException(detail="prompt is required", status_code=status.HTTP_400_BAD_REQUEST)

    try:
        resp = await generate_lyrics(prompt, token)
        return resp
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.get("/lyrics/{lid}")
async def fetch_lyrics(lid: str, _: str = Depends(verify_token), token: str = Depends(get_token)):
    try:
        resp = await get_lyrics(lid, token)
        return resp
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
