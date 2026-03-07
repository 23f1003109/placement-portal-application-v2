from flask import Blueprint
from flask_login import login_required, current_user

company_bp = Blueprint("company", __name__)