#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    :   completions.py
@Time    :   2024/09/14 00:37:42
@Author  :   lvguanjun
@Desc    :   completions.py
"""

import httpx

from utils.config import OPENAI_API_KEY, OPENAI_BASE_URL
from utils.prompt import FEW_SHOT_PROMPT, SYSTEM_PROMPT
from utils.utils import get_svg_from_llm_resp, svg_to_png


async def explain_word(word: str) -> str:
    url = OPENAI_BASE_URL + "/v1/chat/completions"
    headers = {"Authorization": OPENAI_API_KEY}
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for prompt in FEW_SHOT_PROMPT:
        user, assistant = prompt
        messages.extend(
            [
                {"role": "user", "content": user},
                {"role": "assistant", "content": assistant},
            ]
        )
    messages.append({"role": "user", "content": word})
    async with httpx.AsyncClient(timeout=120) as client:
        body = {
            "messages": messages,
            "stream": False,
            "model": "gpt-4o",
            "temperature": 0.5,
            "presence_penalty": 0,
            "frequency_penalty": 0,
            "top_p": 1,
        }
        resp = await client.post(url, headers=headers, json=body)
        if not resp.is_success:
            raise ValueError(resp.text)
    ans = resp.json()["choices"][0]["message"]["content"]
    print(ans)
    return ans


async def generate_svg(word: str) -> bytes:
    resp = await explain_word(word)
    svg = get_svg_from_llm_resp(resp)
    ans = await svg_to_png(word, svg)
    return ans


if __name__ == "__main__":
    import asyncio

    resp = asyncio.run(generate_svg("结婚"))
    print(resp)
