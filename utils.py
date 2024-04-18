import json
import os
import time

import aiohttp
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")

COMMON_HEADERS = {
    "Content-Type": "text/plain;charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Referer": "https://suno.com",
    "Origin": "https://suno.com",
}


async def fetch(url, headers=None, data=None, method="POST"):
    if headers is None:
        headers = {}
    headers.update(COMMON_HEADERS)
    if data is not None:
        data = json.dumps(data)

    print(data, method, headers, url)

    async with aiohttp.ClientSession() as session:
        try:
            async with session.request(
                method=method, url=url, data=data, headers=headers
            ) as resp:
                return await resp.json()
        except Exception as e:
            return f"An error occurred: {e}"


async def get_feed(ids, token):
    headers = {"Authorization": f"Bearer {token}"}
    api_url = f"{BASE_URL}/api/feed/?ids={ids}"
    response = await fetch(api_url, headers, method="GET")
    return response

async def get_trending(token, interval, page=0):
    listId = "1190bf92-10dc-4ce5-968a-7a377f37f984"

    match interval:
        case "now":
            listId = "1190bf92-10dc-4ce5-968a-7a377f37f984"
        case "weekly":
            listId = "08a079b2-a63b-4f9c-9f29-de3c1864ddef"
        case "monthly":
            listId = "845539aa-2a39-4cf5-b4ae-16d3fe159a77"
        case "alltime":
            listId = "6943c7ee-cbc5-4f72-bc4e-f3371a8be9d5"

    headers = {
        "Authorization": f"Bearer {token}"
    }
    api_url = f"{BASE_URL}/api/playlist/{listId}/?page={page}"
    response = await fetch(api_url, headers, method="GET")

    modified_data = []

    for item in response['playlist_clips']:
        modified_item = item["clip"]

        new_item = {
            'id': modified_item["id"],
            'image_url': modified_item["image_url"],
            'audio_url': modified_item["audio_url"],
            'title': modified_item["title"],
            'duration': modified_item["metadata"]['duration'],
            'tags': modified_item["metadata"]['tags']
        }

        modified_data.append(new_item)

    return modified_data

async def generate_music(data, token):
    headers = {"Authorization": f"Bearer {token}"}
    api_url = f"{BASE_URL}/api/generate/v2/"
    response = await fetch(api_url, headers, data)
    return response


async def generate_lyrics(prompt, token):
    headers = {"Authorization": f"Bearer {token}"}
    api_url = f"{BASE_URL}/api/generate/lyrics/"
    data = {"prompt": prompt}
    return await fetch(api_url, headers, data)


async def get_lyrics(lid, token):
    headers = {"Authorization": f"Bearer {token}"}
    api_url = f"{BASE_URL}/api/generate/lyrics/{lid}"
    return await fetch(api_url, headers, method="GET")
