from app import app, db
from app.models import User, Concerts, store
import arrow, threading, time

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'store': store,
        'Concert': Concerts,
    }


current_date = arrow.now().format("YYYYMMDD")
for i in Concerts.query.all():
    if int(i.date) < int(current_date):
        db.session.delete(i)
        db.session.commit()


if __name__ == '__main__':
    app.run()
