from flask import Blueprint, render_template
from flask_login import login_required

core_bp = Blueprint(
    "core_bp", __name__, template_folder="templates", static_folder="static"
)


@core_bp.route("/")
@login_required
def home():
    return render_template("core/home.html")