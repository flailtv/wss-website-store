from app import app, db
from app.models import User, Concerts, Store, cart, stock
import arrow, threading


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'store': Store,
        'Concert': Concerts,
        "Stock": stock,
        "Cart": cart,
    }


def algo():
    current_date = arrow.now().format("YYMMDD")
    for i in Concerts.query.all():
        t = i.thedate.strftime("%y%m%d")
        if int(t) < int(current_date):
            db.session.delete(i)
            db.session.commit()
        threading.Timer(60, algo).start()


if __name__ == '__main__':
    app.run(host="0.0.0.0")


# if __name__ == '__main__':
#     app.run()

