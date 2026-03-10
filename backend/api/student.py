from flask import Blueprint, abort, request
from flask_login import current_user, login_required

from ..extensions import db
from ..helperFunctions import role_required, serialize_application, serialize_company, serialize_drive, serialize_student
from ..models import Application, Company, Drive


student_bp = Blueprint('student', __name__)


def current_student():
    student = current_user.student
    if student is None:
        abort(404)
    return student


def ensure_active_student():
    student = current_student()
    if student.is_blacklisted:
        abort(403)
    return student


def approved_drive_query():
    return Drive.query.join(Company).filter(
        Company.is_approved.is_(True),
        Company.is_blacklisted.is_(False),
        Drive.is_approved.is_(True),
        Drive.is_completed.is_(False),
    )


def serialize_student_application(application):
    payload = serialize_application(application)
    payload['drive'] = serialize_drive(application.drive)
    payload['company'] = serialize_company(application.company)
    return payload


@student_bp.route('/dashboard')
@login_required
@role_required('student')
def dashboard():
    student = ensure_active_student()
    companies = Company.query.filter_by(is_approved=True, is_blacklisted=False).order_by(Company.name.asc()).all()
    available_drives = approved_drive_query().order_by(Drive.id.asc()).all()
    applied_applications = [
        application for application in student.applications
        if application.status == 'applied'
    ]

    return {
        'student': serialize_student(student),
        'companies': [serialize_company(company) for company in companies],
        'available_drives': [serialize_drive(drive) for drive in available_drives],
        'applied_applications': [serialize_application(application) for application in applied_applications],
    }


@student_bp.route('/drives')
@login_required
@role_required('student')
def list_drives():
    ensure_active_student()
    query = approved_drive_query()
    args = request.args
    drive_name = args.get('name')
    job_title = args.get('job_title')
    company_name = args.get('company_name')
    eligibility_criteria = args.get('eligibility_criteria')
    required_skills = args.get('required_skills')

    if drive_name:
        query = query.filter(Drive.name.ilike(f'%{drive_name}%'))
    if job_title:
        query = query.filter(Drive.job_title.ilike(f'%{job_title}%'))
    if company_name:
        query = query.filter(Company.name.ilike(f'%{company_name}%'))
    if eligibility_criteria:
        query = query.filter(Drive.eligibility_criteria.ilike(f'%{eligibility_criteria}%'))
    if required_skills:
        query = query.filter(Drive.required_skills.ilike(f'%{required_skills}%'))

    drives = query.order_by(Drive.id.asc()).all()
    return [serialize_drive(drive) for drive in drives]


@student_bp.route('/profile')
@login_required
@role_required('student')
def get_profile():
    return serialize_student(current_student())


@student_bp.route('/profile', methods=['POST'])
@login_required
@role_required('student')
def update_profile():
    student = ensure_active_student()
    data = request.get_json() or {}
    editable_fields = ['name', 'department', 'degree', 'contact_number']
    errors = {}

    for field_name in editable_fields:
        if not data.get(field_name):
            errors[field_name] = ['This field is required.']

    if errors:
        return {'errors': errors}, 400

    for field_name in editable_fields:
        setattr(student, field_name, data.get(field_name))

    db.session.commit()
    return serialize_student(student)


@student_bp.route('/history')
@login_required
@role_required('student')
def view_history():
    student = ensure_active_student()
    applications = sorted(student.applications, key=lambda application: application.id)
    return [serialize_application(application) for application in applications]


@student_bp.route('/companies/<int:company_id>')
@login_required
@role_required('student')
def view_company(company_id):
    ensure_active_student()
    company = Company.query.filter_by(id=company_id, is_approved=True, is_blacklisted=False).first_or_404()
    drives = [
        serialize_drive(drive)
        for drive in company.drives
        if drive.is_approved and not drive.is_completed
    ]
    return {
        'company': serialize_company(company),
        'drives': drives,
    }


@student_bp.route('/drives/<int:drive_id>')
@login_required
@role_required('student')
def view_drive(drive_id):
    student = ensure_active_student()
    existing_application = Application.query.filter_by(student_id=student.id, drive_id=drive_id).first()
    if existing_application is not None:
        drive = existing_application.drive
    else:
        drive = approved_drive_query().filter(Drive.id == drive_id).first_or_404()

    return {
        'drive': serialize_drive(drive),
        'company': serialize_company(drive.company),
        'has_applied': existing_application is not None,
        'application_status': existing_application.status if existing_application else None,
        'application': serialize_application(existing_application) if existing_application else None,
    }


@student_bp.route('/drives/<int:drive_id>/apply', methods=['POST'])
@login_required
@role_required('student')
def apply_drive(drive_id):
    student = ensure_active_student()
    drive = approved_drive_query().filter(Drive.id == drive_id).first_or_404()
    data = request.get_json() or {}
    resume_link = data.get('resume_link')

    if not resume_link:
        return {'errors': {'resume_link': ['This field is required.']}}, 400

    existing_application = Application.query.filter_by(student_id=student.id, drive_id=drive.id).first()
    if existing_application is not None:
        return {'errors': {'_form': ['You have already applied for this drive.']}}, 400

    application = Application(
        student_id=student.id,
        drive_id=drive.id,
        resume_link=resume_link,
    )
    db.session.add(application)
    db.session.commit()
    return serialize_student_application(application), 201

