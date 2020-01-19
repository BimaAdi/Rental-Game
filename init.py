from app import db, init

print('Initialize Table')
db.create_all()

init()
