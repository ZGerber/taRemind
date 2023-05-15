from tinydb import TinyDB, Query

meeting_db = TinyDB('/home/zane/software/taRemind/meetings/meeting-book.json')
meeting_db.default_table_name = 'meeting-book'
MeetingQuery = Query()
