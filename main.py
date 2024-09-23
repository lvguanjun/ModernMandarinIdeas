#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    :   main.py
@Time    :   2024/09/14 00:54:27
@Author  :   lvguanjun
@Desc    :   main.py
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from utils.completions import explain_word
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
    resp = await explain_word(word_data.word)
    svg = get_svg_from_llm_resp(resp)
    save_svg(word_data.word, svg)
    return {"svg": svg}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
