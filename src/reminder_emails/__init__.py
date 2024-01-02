#!/usr/bin python3
import os
from dataclasses import dataclass

"""
Information needed by reminder modules.
"""

SENDER: str = os.environ.get("TA_REMIND_EMAIL")
PASSWORD: str = os.environ.get("GMAIL_PASSWORD")

