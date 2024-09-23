#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    :   config.py
@Time    :   2024/09/14 00:37:50
@Author  :   lvguanjun
@Desc    :   config.py
"""


import os

from dotenv import load_dotenv

load_dotenv()

STATIC_DIR = "static/output"

OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
