from datetime import date

from flask import Blueprint, abort, request
from flask_login import current_user, login_required

from ..extensions import db
from ..helperFunctions import role_required, serialize_application, serialize_company, serialize_drive, serialize_student
from ..models import Application, Drive, InterviewSchedule, Placement


company_bp = Blueprint('company', __name__)

VALID_APPLICATION_STATUSES = {'applied', 'shortlisted', 'selected', 'rejected'}


def current_company():
    company = current_user.company
    if company is None:
        abort(404)
    return company


def ensure_company_access(allow_unapproved=False):
    company = current_company()
    if company.is_blacklisted:
        return None, ({'error': 'Your company account has been blacklisted.'}, 403)
    if not allow_unapproved and not company.is_approved:
        return None, ({'error': 'Your company profile is awaiting admin approval.'}, 403)
    return company, None


def serialize_company_drive(drive):
    payload = serialize_drive(drive)
    payload['application_count'] = len(drive.applications)
    return payload


def serialize_company_application_detail(application):
    payload = serialize_application(application)
    payload['student'] = serialize_student(application.student)
    payload['drive'] = serialize_company_drive(application.drive)
    return payload


def parse_date(raw_value, field_name, errors):
    if raw_value in (None, ''):
        return None
    try:
        return date.fromisoformat(raw_value)
    except (TypeError, ValueError):
        errors[field_name] = ['This field must be a valid date.']
        return None


def parse_positive_int(raw_value, field_name, errors):
    if raw_value in (None, ''):
        return None
    try:
        value = int(raw_value)
    except (TypeError, ValueError):
        errors[field_name] = ['This field must be a number.']
        return None
    if value <= 0:
        errors[field_name] = ['This field must be positive.']
        return None
    return value


def parse_drive_payload(data, is_create=False):
    errors = {}
    values = {}
    text_fields = [
        'name',
        'job_title',
        'job_description',
        'job_location',
        'eligibility_criteria',
        'required_skills',
        'experience_required',
        'benefits',
    ]
    required_fields = {'name', 'job_title', 'job_location', 'salary', 'application_deadline'}

    for field_name in text_fields:
        raw_value = data.get(field_name)
        if raw_value in (None, ''):
            if is_create and field_name in required_fields:
                errors[field_name] = ['This field is required.']
            continue
        values[field_name] = raw_value

    salary = parse_positive_int(data.get('salary'), 'salary', errors)
    if salary is not None:
        values['salary'] = salary
    elif is_create:
        errors.setdefault('salary', ['This field is required.'])

    application_deadline = parse_date(data.get('application_deadline'), 'application_deadline', errors)
    if application_deadline is not None:
        values['application_deadline'] = application_deadline
    elif is_create:
        errors.setdefault('application_deadline', ['This field is required.'])

    return values, errors


@company_bp.route('/dashboard')
@login_required
@role_required('company')
def dashboard():
    company, error = ensure_company_access()
    if error:
        return error

    ongoing_drives = Drive.query.filter_by(company_id=company.id, is_completed=False).order_by(Drive.id.asc()).all()
    completed_drives = Drive.query.filter_by(company_id=company.id, is_completed=True).order_by(Drive.id.asc()).all()

    return {
        'company': serialize_company(company),
        'ongoing_drives': [serialize_company_drive(drive) for drive in ongoing_drives],
        'completed_drives': [serialize_company_drive(drive) for drive in completed_drives],
    }


@company_bp.route('/profile')
@login_required
@role_required('company')
def get_profile():
    company, error = ensure_company_access(allow_unapproved=True)
    if error:
        return error
    return serialize_company(company)


@company_bp.route('/profile', methods=['POST'])
@login_required
@role_required('company')
def update_profile():
    company, error = ensure_company_access(allow_unapproved=True)
    if error:
        return error

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
        return {'errors': errors}, 400

    for field_name in editable_fields:
        if field_name in data:
            setattr(company, field_name, data.get(field_name))

    db.session.commit()
    return serialize_company(company)


@company_bp.route('/drives', methods=['POST'])
@login_required
@role_required('company')
def create_drive():
    company, error = ensure_company_access()
    if error:
        return error

    data = request.get_json() or {}
    values, errors = parse_drive_payload(data, is_create=True)
    if errors:
        return {'errors': errors}, 400

    drive = Drive(company_id=company.id, is_approved=False, **values)
    db.session.add(drive)
    db.session.commit()
    return serialize_company_drive(drive), 201


@company_bp.route('/drives')
@login_required
@role_required('company')
def fetch_drives():
    company, error = ensure_company_access()
    if error:
        return error

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
    company, error = ensure_company_access()
    if error:
        return error

    drive = Drive.query.filter_by(id=drive_id, company_id=company.id).first_or_404()
    return serialize_company_drive(drive)


@company_bp.route('/drives/<int:drive_id>', methods=['POST'])
@login_required
@role_required('company')
def update_drive(drive_id):
    company, error = ensure_company_access()
    if error:
        return error

    drive = Drive.query.filter_by(id=drive_id, company_id=company.id).first_or_404()
    data = request.get_json() or {}
    values, errors = parse_drive_payload(data, is_create=False)
    if errors:
        return {'errors': errors}, 400

    for field_name, value in values.items():
        setattr(drive, field_name, value)

    if values:
        drive.is_approved = False

    db.session.commit()
    return serialize_company_drive(drive)


@company_bp.route('/drives/<int:drive_id>/toggle', methods=['POST'])
@login_required
@role_required('company')
def toggle_drive_status(drive_id):
    company, error = ensure_company_access()
    if error:
        return error

    drive = Drive.query.filter_by(id=drive_id, company_id=company.id).first_or_404()
    drive.is_completed = not drive.is_completed
    db.session.commit()
    return serialize_company_drive(drive)


@company_bp.route('/drives/<int:drive_id>/applications')
@login_required
@role_required('company')
def fetch_applications(drive_id):
    company, error = ensure_company_access()
    if error:
        return error

    drive = Drive.query.filter_by(id=drive_id, company_id=company.id).first_or_404()
    applications = Application.query.filter_by(drive_id=drive.id).order_by(Application.id.asc()).all()
    return {
        'drive': serialize_company_drive(drive),
        'applications': [serialize_application(application) for application in applications],
    }


@company_bp.route('/applications/<int:application_id>')
@login_required
@role_required('company')
def fetch_application(application_id):
    company, error = ensure_company_access()
    if error:
        return error

    application = Application.query.join(Drive).filter(
        Application.id == application_id,
        Drive.company_id == company.id,
    ).first_or_404()
    return serialize_company_application_detail(application)


@company_bp.route('/applications/<int:application_id>/status', methods=['POST'])
@login_required
@role_required('company')
def update_application_status(application_id):
    company, error = ensure_company_access()
    if error:
        return error

    application = Application.query.join(Drive).filter(
        Application.id == application_id,
        Drive.company_id == company.id,
    ).first_or_404()

    data = request.get_json() or {}
    errors = {}
    status = data.get('status')

    if status not in VALID_APPLICATION_STATUSES:
        errors['status'] = ['Select a valid status.']

    interview_date = parse_date(data.get('interview_date'), 'interview_date', errors)
    joining_date = parse_date(data.get('joining_date'), 'joining_date', errors)
    placement_salary = parse_positive_int(data.get('placement_salary'), 'placement_salary', errors)

    if errors:
        return {'errors': errors}, 400

    application.status = status
    application.remark = data.get('remark') or 'None'

    interview_fields_present = any(
        data.get(field) not in (None, '')
        for field in ['interview_date', 'interview_mode', 'interview_location', 'interview_feedback']
    )
    if interview_fields_present:
        interview = application.interview_schedule or InterviewSchedule(application=application)
        interview.interview_date = interview_date
        interview.mode = data.get('interview_mode') or None
        interview.location = data.get('interview_location') or None
        interview.feedback = data.get('interview_feedback') or None
        db.session.add(interview)

    placement_fields_present = any(
        data.get(field) not in (None, '')
        for field in ['placement_position', 'placement_salary', 'joining_date', 'offer_letter_link']
    )
    if placement_fields_present:
        placement = application.placement or Placement(
            application=application,
            student_id=application.student_id,
            company_id=application.company.id,
            position=data.get('placement_position') or application.drive.job_title,
        )
        placement.position = data.get('placement_position') or placement.position or application.drive.job_title
        placement.salary = placement_salary if placement_salary is not None else placement.salary
        placement.joining_date = joining_date if joining_date is not None else placement.joining_date
        placement.offer_letter_link = data.get('offer_letter_link') or placement.offer_letter_link
        db.session.add(placement)

    db.session.commit()
    return serialize_company_application_detail(application)
