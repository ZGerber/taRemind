#!/usr/bin/env python


class Contact:
    def __init__(self, first_name, last_name, email_address, position=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address
        self.position = position

    # def __repr__(self) -> str:
    #     return f"({self.first_name}, {self.last_name}, {self.email_address}, {self.position})"


class Meeting:
    def __init__(self, meeting_name, meeting_day, meeting_time, zoom_link, passcode, position=None):
        self.meeting_name = meeting_name
        self.meeting_day = meeting_day
        self.meeting_time = meeting_time
        self.zoom_link = zoom_link
        self.position = position
        self.passcode = passcode

    # def __repr__(self) -> str:
    #     return f"({self.meeting_name}, " \
    #            f"{self.meeting_day}, " \
    #            f"{self.meeting_time}," \
    #            f" {self.zoom_link}, " \
    #            f"{self.passcode}, " \
    #            f"{self.position})"

