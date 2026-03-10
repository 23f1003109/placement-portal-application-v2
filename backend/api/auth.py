from flask import Blueprint, request
from flask_login import login_required, current_user, login_user, logout_user

from ..extensions import db
from ..models import Company, Role, Student, User


auth_bp = Blueprint("auth", __name__)


def serialize_auth_user(user):
    payload = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role.name,
    }

    if user.company is not None:
        payload['company'] = {
            'id': user.company.id,
            'is_approved': user.company.is_approved,
            'is_blacklisted': user.company.is_blacklisted,
        }

    if user.student is not None:
        payload['student'] = {
            'id': user.student.id,
            'is_blacklisted': user.student.is_blacklisted,
        }

    return payload


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return {
            'errors': {
                '_form': ['JSON body required.']
            }
        }, 400

    errors = {}
    username = data.get('username')
    password = data.get('password')

    if not username:
        errors['username'] = ['This field is required.']
    if not password:
        errors['password'] = ['This field is required.']

    if errors:
        return {'errors': errors}, 400

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return {
            'errors': {
                '_form': ['Invalid credentials.']
            }
        }, 401

    login_user(user)
    return {
        'message': 'login success',
        'user': serialize_auth_user(user),
    }


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return {'message': 'logout success'}, 200


@auth_bp.route('/me')
@login_required
def me():
    return serialize_auth_user(current_user)


@auth_bp.route('/register/student', methods=['POST'])
def register_student():
    data = request.get_json()

    if not data:
        return {
            'errors': {
                '_form': ['JSON body required.']
            }
        }, 400

    required_fields = [
        'username',
        'email',
        'password',
        'name',
        'department',
        'degree',
        'contact_number',
    ]

    errors = {}
    missing_fields = [field for field in required_fields if not data.get(field)]
    for field in missing_fields:
        errors[field] = ['This field is required.']

    if User.query.filter_by(email=data.get('email')).first():
        errors['email'] = ['Email already registered.']

    if User.query.filter_by(username=data.get('username')).first():
        errors['username'] = ['Username already taken.']

    if errors:
        return {'errors': errors}, 400

    role = Role.query.filter_by(name='student').first()
    user = User(
        username=data['username'],
        email=data['email'],
        role_id=role.id,
    )
    user.set_password(data['password'])
    db.session.add(user)
    db.session.flush()

    student = Student(
        user_id=user.id,
        name=data['name'],
        department=data['department'],
        degree=data['degree'],
        contact_number=data['contact_number'],
    )

    db.session.add(student)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return {'errors': {'_form': ['Database error.']}}, 500

    return {'message': 'student registered'}, 201


@auth_bp.route('/register/company', methods=['POST'])
def register_company():
    data = request.get_json()

    if not data:
        return {
            'errors': {
                '_form': ['JSON body required.']
            }
        }, 400

    required_fields = [
        'username',
        'email',
        'password',
        'name',
        'industry',
        'hr_name',
        'hr_email',
        'hr_contact',
    ]

    errors = {}
    missing_fields = [field for field in required_fields if not data.get(field)]
    for field in missing_fields:
        errors[field] = ['This field is required.']

    if User.query.filter_by(email=data.get('email')).first():
        errors['email'] = ['Email already registered.']

    if User.query.filter_by(username=data.get('username')).first():
        errors['username'] = ['Username already taken.']

    if Company.query.filter_by(name=data.get('name')).first():
        errors['name'] = ['Company name already taken.']

    if errors:
        return {'errors': errors}, 400

    role = Role.query.filter_by(name='company').first()
    user = User(
        username=data.get('username'),
        email=data.get('email'),
        role_id=role.id,
    )
    user.set_password(data['password'])

    db.session.add(user)
    db.session.flush()

    company = Company(
        user_id=user.id,
        name=data['name'],
        industry=data['industry'],
        hr_name=data['hr_name'],
        hr_email=data['hr_email'],
        hr_contact=data['hr_contact'],
        description=data.get('description'),
        location=data.get('location'),
        website=data.get('website'),
    )

    db.session.add(company)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return {'errors': {'_form': ['Database error.']}}, 500

    return {'message': 'company registered and awaiting admin approval'}, 201
