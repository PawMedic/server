from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:5432@localhost/pawmedic'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return db