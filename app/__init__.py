from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'secret-key'

    db.init_app(app)

    with app.app_context():
        from . import models, routes
        db.create_all()
        if not models.Admin.query.filter_by(username='admin').first():
            admin = models.Admin(username='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()

    app.register_blueprint(routes.main_bp)

    return app
