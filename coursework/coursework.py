from app import app, db
from app.models import User, Concerts, Store, cart, stock


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


if __name__ == '__main__':
    app.run()
