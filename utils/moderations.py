#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    :   moderations.py
@Time    :   2024/09/25 07:30:57
@Author  :   lvguanjun
@Desc    :   moderations.py
"""

import httpx

from utils.config import MODERATIONS_API_KEY, MODERATIONS_BASE_URL


async def check_moderations(text: str) -> bool:
    url = MODERATIONS_BASE_URL + "/v1/moderations"
    headers = {
        "content-type": "application/json",
        "Authorization": f"Bearer {MODERATIONS_API_KEY}",
    }
    body = {"input": text}
    async with httpx.AsyncClient(timeout=120) as client:
        resp = await client.post(url, headers=headers, json=body)
        if not resp.is_success:
            raise ValueError(resp.text)
    ans = resp.json()["results"][0]["flagged"]
    return ans
