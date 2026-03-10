from functools import wraps
from flask_login import current_user
from flask import abort


def role_required(role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)

            if current_user.role.name != role:
                abort(403)

            return fn(*args, **kwargs)
        return wrapper
    return decorator


def bool_parser(value):
    if value is None:
        return None
    return value.lower() in {"true", "yes", "1"}


def serialize_company(company):
    return {
        "id": company.id,
        "name": company.name,
        "industry": company.industry,
        "hr_name": company.hr_name,
        "hr_email": company.hr_email,
        "hr_contact": company.hr_contact,
        "description": company.description,
        "location": company.location,
        "website": company.website,
        "is_approved": company.is_approved,
        "is_blacklisted": company.is_blacklisted,
        "user_id": company.user_id,
    }


def serialize_student(student):
    return {
        "id": student.id,
        "name": student.name,
        "department": student.department,
        "degree": student.degree,
        "contact_number": student.contact_number,
        "is_blacklisted": student.is_blacklisted,
        "user_id": student.user_id,
    }


def serialize_drive(drive):
    return {
        "id": drive.id,
        "company_id": drive.company_id,
        "company_name": drive.company.name if drive.company else None,
        "name": drive.name,
        "job_title": drive.job_title,
        "job_description": drive.job_description,
        "job_location": drive.job_location,
        "eligibility_criteria": drive.eligibility_criteria,
        "required_skills": getattr(drive, 'required_skills', None),
        "experience_required": getattr(drive, 'experience_required', None),
        "benefits": getattr(drive, 'benefits', None),
        "application_deadline": drive.application_deadline.isoformat() if drive.application_deadline else None,
        "salary": drive.salary,
        "is_completed": drive.is_completed,
        "is_approved": getattr(drive, 'is_approved', False),
    }


def serialize_application(application):
    interview = getattr(application, 'interview_schedule', None)
    placement = getattr(application, 'placement', None)

    return {
        "id": application.id,
        "student_id": application.student_id,
        "student_name": application.student.name if application.student else None,
        "drive_id": application.drive_id,
        "drive_name": application.drive.name if application.drive else None,
        "company_id": application.company.id if application.company else None,
        "company_name": application.company.name if application.company else None,
        "application_date": application.application_date.isoformat() if application.application_date else None,
        "status": application.status,
        "resume_link": application.resume_link,
        "remark": application.remark,
        "interview_date": interview.interview_date.isoformat() if interview and interview.interview_date else None,
        "interview_mode": interview.mode if interview else None,
        "interview_location": interview.location if interview else None,
        "interview_feedback": interview.feedback if interview else None,
        "placement_position": placement.position if placement else None,
        "placement_salary": placement.salary if placement else None,
        "joining_date": placement.joining_date.isoformat() if placement and placement.joining_date else None,
        "offer_letter_link": placement.offer_letter_link if placement else None,
        "is_placed": placement is not None,
    }
