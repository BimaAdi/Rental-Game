from app import db, init

print('remove existing table')
db.drop_all()
print('Initialize Table')
db.create_all()

init()
