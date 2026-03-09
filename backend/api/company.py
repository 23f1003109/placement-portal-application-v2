from datetime import date

from flask import Blueprint, abort, request
from flask_login import current_user, login_required

from ..extensions import db
from ..helperFunctions import role_required, serialize_application, serialize_company, serialize_drive, serialize_student
from ..models import Application, Drive

company_bp = Blueprint("company", __name__)

VALID_APPLICATION_STATUSES = {"applied", "shortlisted", "selected", "rejected"}


def current_company():
    company = current_user.company
    if company is None:
        abort(404)
    return company


def serialize_company_drive(drive):
    payload = serialize_drive(drive)
    payload["application_count"] = len(drive.applications)
    return payload


def serialize_company_application_detail(application):
    payload = serialize_application(application)
    payload["remark"] = application.remark
    payload["student"] = serialize_student(application.student)
    payload["drive"] = serialize_company_drive(application.drive)
    return payload


def parse_drive_payload(data, is_create=False):
    errors = {}
    values = {}

    fields = {
        "name": str,
        "job_title": str,
        "job_description": str,
        "job_location": str,
        "eligibility_criteria": str,
        "salary": int,
        "application_deadline": "date",
    }

    required_fields = {"name", "job_title", "job_location", "salary", "application_deadline"}

    for field_name, field_type in fields.items():
        raw_value = data.get(field_name)

        if raw_value in (None, ""):
            if is_create and field_name in required_fields:
                errors[field_name] = ["This field is required."]
            continue

        if field_type is int:
            try:
                value = int(raw_value)
            except (TypeError, ValueError):
                errors[field_name] = ["This field must be a number."]
                continue
            if value <= 0:
                errors[field_name] = ["This field must be positive."]
                continue
            values[field_name] = value
            continue

        if field_type == "date":
            try:
                values[field_name] = date.fromisoformat(raw_value)
            except (TypeError, ValueError):
                errors[field_name] = ["This field must be a valid date."]
            continue

        values[field_name] = raw_value

    return values, errors


@company_bp.route('/dashboard')
@login_required
@role_required('company')
def dashboard():
    company = current_company()
    ongoing_drives = Drive.query.filter_by(company_id=company.id, is_completed=False).order_by(Drive.id.asc()).all()
    completed_drives = Drive.query.filter_by(company_id=company.id, is_completed=True).order_by(Drive.id.asc()).all()

    return {
        "company": serialize_company(company),
        "ongoing_drives": [serialize_company_drive(drive) for drive in ongoing_drives],
        "completed_drives": [serialize_company_drive(drive) for drive in completed_drives],
    }


@company_bp.route('/profile')
@login_required
@role_required('company')
def get_profile():
    return serialize_company(current_company())


@company_bp.route('/profile', methods=['POST'])
@login_required
@role_required('company')
def update_profile():
    company = current_company()
    data = request.get_json() or {}

    editable_fields = [
        'name',
        'industry',
        'hr_name',
        'hr_email',
        'hr_contact',
        'description',
        'location',
        'website',
    ]

    errors = {}
    for field_name in ['name', 'industry', 'hr_name', 'hr_email', 'hr_contact']:
        if not data.get(field_name):
            errors[field_name] = ['This field is required.']

    if errors:
        return {"errors": errors}, 400

    for field_name in editable_fields:
        if field_name in data:
            setattr(company, field_name, data.get(field_name))

    db.session.commit()
    return serialize_company(company)


@company_bp.route('/drives', methods=['POST'])
@login_required
@role_required('company')
def create_drive():
    company = current_company()
    data = request.get_json() or {}
    values, errors = parse_drive_payload(data, is_create=True)

    if errors:
        return {"errors": errors}, 400

    drive = Drive(company_id=company.id, **values)
    db.session.add(drive)
    db.session.commit()

    return serialize_company_drive(drive), 201


@company_bp.route('/drives')
@login_required
@role_required('company')
def fetch_drives():
    company = current_company()
    status = request.args.get('status')
    query = Drive.query.filter_by(company_id=company.id)

    if status == 'completed':
        query = query.filter_by(is_completed=True)
    elif status == 'ongoing':
        query = query.filter_by(is_completed=False)

    drives = query.order_by(Drive.id.asc()).all()
    return [serialize_company_drive(drive) for drive in drives]


@company_bp.route('/drives/<int:drive_id>')
@login_required
@role_required('company')
def fetch_drive(drive_id):
    drive = Drive.query.filter_by(id=drive_id, company_id=current_company().id).first_or_404()
    return serialize_company_drive(drive)


@company_bp.route('/drives/<int:drive_id>', methods=['POST'])
@login_required
@role_required('company')
def update_drive(drive_id):
    drive = Drive.query.filter_by(id=drive_id, company_id=current_company().id).first_or_404()
    data = request.get_json() or {}
    values, errors = parse_drive_payload(data, is_create=False)

    if errors:
        return {"errors": errors}, 400

    for field_name, value in values.items():
        setattr(drive, field_name, value)

    db.session.commit()
    return serialize_company_drive(drive)


@company_bp.route('/drives/<int:drive_id>/toggle', methods=['POST'])
@login_required
@role_required('company')
def toggle_drive_status(drive_id):
    drive = Drive.query.filter_by(id=drive_id, company_id=current_company().id).first_or_404()
    drive.is_completed = not drive.is_completed
    db.session.commit()
    return serialize_company_drive(drive)


@company_bp.route('/drives/<int:drive_id>/applications')
@login_required
@role_required('company')
def fetch_applications(drive_id):
    drive = Drive.query.filter_by(id=drive_id, company_id=current_company().id).first_or_404()
    applications = Application.query.filter_by(drive_id=drive.id).order_by(Application.id.asc()).all()

    return {
        "drive": serialize_company_drive(drive),
        "applications": [serialize_application(application) for application in applications],
    }


@company_bp.route('/applications/<int:application_id>')
@login_required
@role_required('company')
def fetch_application(application_id):
    application = Application.query.join(Drive).filter(
        Application.id == application_id,
        Drive.company_id == current_company().id,
    ).first_or_404()
    return serialize_company_application_detail(application)


@company_bp.route('/applications/<int:application_id>/status', methods=['POST'])
@login_required
@role_required('company')
def update_application_status(application_id):
    application = Application.query.join(Drive).filter(
        Application.id == application_id,
        Drive.company_id == current_company().id,
    ).first_or_404()
    data = request.get_json() or {}
    status = data.get('status')

    if status not in VALID_APPLICATION_STATUSES:
        return {"errors": {"status": ["Select a valid status."]}}, 400

    application.status = status
    if 'remark' in data:
        application.remark = data.get('remark') or 'None'

    db.session.commit()
    return serialize_company_application_detail(application)
