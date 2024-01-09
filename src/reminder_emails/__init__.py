#!/usr/bin python3
import os

"""
Information needed by reminder modules.
"""

SENDER: str = os.environ.get("TA_REMIND_EMAIL")
PASSWORD: str = os.environ.get("GMAIL_PASSWORD")

