from tinydb import TinyDB, Query

contact_db = TinyDB('/home/zane/software/taRemind/contacts/contact-book.json')
contact_db.default_table_name = 'contact-book'
ContactQuery = Query()
