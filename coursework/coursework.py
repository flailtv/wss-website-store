from app import app, db
from app.models import User, Concerts, Store, cart, stock
from flask_wtf import CSRFProtect


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

csrf = CSRFProtect()

if __name__ == '__main__':
    app.run(host="0.0.0.0")
    # app.run(host="80.80.80.80")
    # app.run()
