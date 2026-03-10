from flask import Flask
from flask_cors import CORS
from sqlalchemy import inspect, text

from .config import Config
from .extensions import db, login_manager, bcrypt
from .models import User, Role


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(
        app,
        supports_credentials=True,
        origins=["http://localhost:5173", "http://localhost:4173"]
    )

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    login_manager.login_view = 'auth.login'

    from .api import auth_bp, admin_bp, company_bp, student_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(company_bp, url_prefix='/company')
    app.register_blueprint(student_bp, url_prefix='/student')

    with app.app_context():
        db.create_all()
        upgrade_schema()
        db.create_all()
        seed_roles_and_admin()

    return app


def upgrade_schema():
    inspector = inspect(db.engine)
    existing_tables = set(inspector.get_table_names())

    if 'drives' in existing_tables:
        drive_columns = {column['name'] for column in inspector.get_columns('drives')}
        column_sql = {
            'required_skills': 'ALTER TABLE drives ADD COLUMN required_skills TEXT',
            'experience_required': 'ALTER TABLE drives ADD COLUMN experience_required TEXT',
            'benefits': 'ALTER TABLE drives ADD COLUMN benefits TEXT',
            'is_approved': 'ALTER TABLE drives ADD COLUMN is_approved BOOLEAN NOT NULL DEFAULT 0',
        }
        for column_name, sql in column_sql.items():
            if column_name not in drive_columns:
                db.session.execute(text(sql))

    db.session.commit()


def seed_roles_and_admin():
    for role_name in ['admin', 'company', 'student']:
        if not Role.query.filter_by(name=role_name).first():
            db.session.add(Role(name=role_name))

    db.session.commit()

    admin_role = Role.query.filter_by(name='admin').first()

    if not User.query.filter_by(username='admin').first():
        admin_email = 'admin@iitm.ac.in'
        admin_raw_password = 'password'
        admin_username = 'admin'
        role_id = admin_role.id

        admin = User(email=admin_email, username=admin_username, role_id=role_id)
        admin.set_password(admin_raw_password)

        db.session.add(admin)
        db.session.commit()
