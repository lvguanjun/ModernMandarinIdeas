#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    :   main.py
@Time    :   2024/09/14 00:54:27
@Author  :   lvguanjun
@Desc    :   main.py
"""

import os

import aiofiles
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from utils.completions import explain_word
from utils.config import OUTPUT_DIR
from utils.moderations import check_moderations
from utils.utils import get_svg_from_llm_resp, save_svg

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def main():
    return RedirectResponse(url="/static/index.html")


class WordData(BaseModel):
    word: str


@app.post("/explain")
async def explain(word_data: WordData):
    if await check_moderations(word_data.word):
        return JSONResponse(
            content={"error": "Please don't use sensitive words."}, status_code=400
        )
    resp = await explain_word(word_data.word)
    svg = get_svg_from_llm_resp(resp)
    if not svg or await check_moderations(svg):
        return JSONResponse(
            content={"error": "Sorry, the word is not supported."}, status_code=400
        )
    save_svg(word_data.word, svg)
    return {"svg": svg}


@app.get("/svg-list")
async def read_svg_list():
    """返回SVG文件目录中的所有文件名"""
    # 异步获取文件列表
    files = os.listdir(OUTPUT_DIR)
    svg_files = [file for file in files if file.endswith(".svg")]
    return svg_files


@app.get("/svg/{filename}")
async def read_svg(filename: str):
    """根据文件名返回SVG文件内容"""
    filepath = os.path.join(OUTPUT_DIR, filename)
    if not filepath.endswith(".svg") or not os.path.exists(filepath):
        return JSONResponse(content={"error": "File not found"}, status_code=404)
    # 异步读取文件内容
    async with aiofiles.open(filepath, mode="rb") as file:
        content = await file.read()
    return {"svg": content.decode("utf-8")}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
