#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    :   utils.py
@Time    :   2024/09/14 01:16:28
@Author  :   lvguanjun
@Desc    :   utils.py
"""

import hashlib
import os
import random
import re

import httpx

from utils.config import OUTPUT_DIR


def get_svg_from_llm_resp(resp: str) -> str:
    """
    Get SVG from LLM response.
    """
    pattern = r"<svg.*</svg>"
    match = re.search(pattern, resp, re.DOTALL)
    if match:
        return match.group(0)
    return ""


def save_svg(word: str, svg: str):
    # 生成文件的哈希值，用于创建独特的文件名
    hash_object = hashlib.sha256(svg.encode())
    hash_hex = hash_object.hexdigest()[:6]

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # 设置 PNG 和 SVG 文件的路径
    svg_path = os.path.join(OUTPUT_DIR, f"{word}_{hash_hex}.svg")

    # 保存 SVG 文件
    with open(svg_path, "w") as svg_file:
        svg_file.write(svg)


async def save_png_by_svg(word: str, svg: str):
    # 生成文件的哈希值，用于创建独特的文件名
    hash_object = hashlib.sha256(svg.encode())
    hash_hex = hash_object.hexdigest()[:6]

    # 设置 PNG 和 SVG 文件的路径
    file_name = f"{word}_{hash_hex}"
    png_file_path = os.path.join(OUTPUT_DIR, f"{file_name}.png")
    svg_file_path = os.path.join(OUTPUT_DIR, f"{file_name}.svg")

    # 保存 SVG 文件
    with open(svg_file_path, "w") as svg_file:
        svg_file.write(svg)


def random_string(length):
    length -= 3  # 调整长度以补偿前缀
    characters = "abcdefghijklmnopqrstuvwxyz1234567890"
    prefix = "st3"
    result = prefix  # 开始时设置前缀
    for _ in range(length):
        result += random.choice(
            characters
        )  # 从字符集中随机选择一个字符并添加到结果字符串
    return result


async def svg_to_png(file_name, svg_path, png_path):
    # 发送请求
    url = "https://kirk.cdkm.com/convert/c10.php"
    random_str = random_string(32)
    payload = {
        "imagequality": "100",
        "imagesize": "option1",
        "customsize": "",
        "removeprofile": "removeprofile",
        "videostartposition": "",
        "videoendposition": "",
        "videosizetype": "0",
        "customvideowidth": "",
        "customvideoheight": "",
        "videobitratetype": "0",
        "custombitrate": "",
        "frameratetype": "0",
        "customframerate": "",
        "videoaspect": "0",
        "videoaudiobitratetype": "0",
        "customvideoaudiobitrate": "",
        "audiostartposition": "",
        "audioendposition": "",
        "audiobitratetype": "0",
        "customaudiobitrate": "",
        "audiosamplingtype": "0",
        "customaudiosampling": "",
        "fileurl": "",
        "filelocation": "local",
        "targetformat": "png",
        "code": "83000",
        "randomstr": random_str,
        "acceptterms": "",
        "warning": "We DO NOT allow using our PHP programs in any third-party websites, software or apps! We will report abuse to your server provider, Google Play and App store if illegal usage found!",
    }
    files = {
        "file": (
            f"{file_name}.svg",
            open(svg_path, "rb"),
            "application/octet-stream",
        ),
    }
    headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cache-control": "no-cache",
        "origin": "https://cdkm.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://cdkm.com/",
        "sec-ch-ua": '"Microsoft Edge";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, files=files, data=payload)
        if response.status_code == 200:
            file_name = response.json()["filename"]
            print(file_name)
            file_url = f"https://kirk.cdkm.com/convert/file/{random_str}/{file_name}"
            headers = {
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "priority": "u=0, i",
                "referer": "https://cdkm.com/",
                "sec-ch-ua": '"Microsoft Edge";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "same-site",
                "sec-fetch-user": "?1",
                "upgrade-insecure-requests": "1",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0",
            }
            response = await client.get(file_url, headers=headers)
            if response.status_code == 200:
                with open(png_path, "wb") as file:
                    file.write(response.content)
                print(f"PNG file has been created successfully at {png_path}")
                return png_path
            print(response.status_code, response.content)


if __name__ == "__main__":
    import asyncio

    asyncio.run(svg_to_png("结婚", "a.svg", "b.png"))
