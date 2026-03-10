from datetime import date

from .constraints import *
from sqlalchemy import CheckConstraint
from .extensions import db, bcrypt, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(MAX_ROLE_LENGTH), unique=True)


class User(db.Model, UserMixin):
    __tablename__ = "users"
    __exposed_fields__ = {
        "id": "ID",
        "role_id": "Role Id",
        "username": "Username",
        "email": "Email"
    }

    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    role = db.relationship('Role')

    username = db.Column(db.String(MAX_USERNAME_LENGTH), unique=True, nullable=False, index=True)
    email = db.Column(db.String(MAX_EMAIL_LENGTH), unique=True, nullable=False, index=True)
    hashed_password = db.Column(db.String(PASSWORD_HASH_LENGTH), nullable=False)

    student = db.relationship('Student', back_populates='user', uselist=False, cascade='all, delete-orphan')
    company = db.relationship('Company', back_populates='user', uselist=False, cascade='all, delete-orphan')

    @classmethod
    def exposed_fields(cls):
        return cls.__exposed_fields__

    def set_password(self, raw_password):
        self.hashed_password = bcrypt.generate_password_hash(raw_password).decode('utf-8')

    def check_password(self, raw_password):
        return bcrypt.check_password_hash(self.hashed_password, raw_password)


class Student(db.Model):
    __tablename__ = "students"
    __exposed_fields__ = {
        "id": "ID",
        "name": "Name",
        "department": "Department",
        "degree": "Degree",
        "contact_number": "Contact Number"
    }

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(MAX_NAME_LENGTH))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    user = db.relationship('User', back_populates='student')

    department = db.Column(db.String(MAX_DEPARTMENT_NAME_LENGTH), nullable=False)
    degree = db.Column(db.String(MAX_DEGREE_NAME_LENGTH), nullable=False)
    contact_number = db.Column(db.String(MAX_CONTACT_NUMBER_LENGTH), nullable=False)
    is_blacklisted = db.Column(db.Boolean, default=False)

    applications = db.relationship('Application', back_populates='student', cascade='all, delete-orphan')
    placements = db.relationship('Placement', back_populates='student', cascade='all, delete-orphan')

    @classmethod
    def exposed_fields(cls):
        return cls.__exposed_fields__


class Company(db.Model):
    __tablename__ ="companies"
    __exposed_fields__ = {
        "id": "ID",
        "name": "Name",
        "industry": "Industry",
        "user_id": "User ID",
        "hr_name": "H.R. Name",
        "hr_email": "H.R. Email",
        "hr_contact": "H.R. Contact",
        "description": "Description",
        "location": "Location",
        "website": "Website"
    }

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(MAX_NAME_LENGTH), nullable=False, unique=True)
    industry = db.Column(db.String(MAX_NAME_LENGTH), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    user = db.relationship('User', back_populates='company', uselist=False)

    hr_name = db.Column(db.String(MAX_NAME_LENGTH), nullable=False)
    hr_email = db.Column(db.String(MAX_EMAIL_LENGTH), nullable=False)
    hr_contact = db.Column(db.String(MAX_CONTACT_NUMBER_LENGTH), nullable=False)

    description = db.Column(db.Text)
    location = db.Column(db.Text)
    website = db.Column(db.Text)
    is_approved = db.Column(db.Boolean, default=False)
    is_blacklisted = db.Column(db.Boolean, default=False)

    drives =db.relationship('Drive', back_populates='company', cascade='all, delete-orphan')
    placements = db.relationship('Placement', back_populates='company', cascade='all, delete-orphan')

    @classmethod
    def exposed_fields(cls):
        return cls.__exposed_fields__


class Drive(db.Model):
    __tablename__ = "drives"
    __exposed_fields__ = {
        "id": "ID",
        "company_id": "Company ID",
        "name": "Name",
        "job_title": "Job Title",
        "job_description": "Job Description",
        "job_location": "Job Location",
        "eligibility_criteria": "Eligibility Criteria",
        "required_skills": "Required Skills",
        "experience_required": "Experience Required",
        "benefits": "Benefits",
        "application_deadline": "Application Deadline",
        "salary": "Salary"
    }

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    name = db.Column(db.String(MAX_NAME_LENGTH), nullable=False, unique=True)

    job_title = db.Column(db.String(MAX_NAME_LENGTH), nullable=False)
    job_description = db.Column(db.Text)
    job_location = db.Column(db.Text)
    eligibility_criteria = db.Column(db.Text)
    required_skills = db.Column(db.Text)
    experience_required = db.Column(db.Text)
    benefits = db.Column(db.Text)
    application_deadline = db.Column(db.Date, nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    is_completed = db.Column(db.Boolean, nullable=False, default=False)
    is_approved = db.Column(db.Boolean, nullable=False, default=False)

    company = db.relationship('Company', back_populates='drives')
    applications = db.relationship('Application', back_populates='drive', cascade='all, delete-orphan')

    @classmethod
    def exposed_fields(cls):
        return cls.__exposed_fields__


class Application(db.Model):
    __tablename__ = "applications"
    __exposed_fields__ = {
        "id": "ID",
        "student_id": "Student ID",
        "drive_id": "Drive ID",
        "application_date": "Application Date",
        "status": "Status",
        "resume_link": "Resume Link"
    }

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    student = db.relationship('Student', back_populates='applications')

    drive_id = db.Column(db.Integer, db.ForeignKey('drives.id'), nullable=False)
    drive = db.relationship('Drive', back_populates='applications')

    application_date = db.Column(db.Date, default=date.today)
    status = db.Column(db.String(MAX_STATUS_TEXT_LENGTH), default="applied")
    remark = db.Column(db.Text, default='None')
    resume_link = db.Column(db.Text, nullable=False)

    interview_schedule = db.relationship('InterviewSchedule', back_populates='application', uselist=False, cascade='all, delete-orphan')
    placement = db.relationship('Placement', back_populates='application', uselist=False, cascade='all, delete-orphan')

    __table_args__ = (
        db.UniqueConstraint('student_id', 'drive_id', name='unique_application'),
        CheckConstraint('status IN ("applied", "shortlisted", "selected", "rejected")', name="check_valid_status"),
    )

    @property
    def company(self):
        return self.drive.company

    @classmethod
    def exposed_fields(cls):
        return cls.__exposed_fields__


class InterviewSchedule(db.Model):
    __tablename__ = 'interview_schedules'

    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'), nullable=False, unique=True)
    interview_date = db.Column(db.Date)
    mode = db.Column(db.String(MAX_NAME_LENGTH))
    location = db.Column(db.Text)
    feedback = db.Column(db.Text)

    application = db.relationship('Application', back_populates='interview_schedule')


class Placement(db.Model):
    __tablename__ = 'placements'

    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'), nullable=False, unique=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    position = db.Column(db.String(MAX_NAME_LENGTH), nullable=False)
    salary = db.Column(db.Integer)
    joining_date = db.Column(db.Date)
    offer_letter_link = db.Column(db.Text)

    application = db.relationship('Application', back_populates='placement')
    student = db.relationship('Student', back_populates='placements')
    company = db.relationship('Company', back_populates='placements')
