from datetime import datetime
from flask import Blueprint, jsonify, render_template, request, flash
from flask_login import login_required, current_user
from backend.models import Act, Tag, ActTag, db
from flask_sqlalchemy import pagination


act_bp = Blueprint(
    "act_bp", __name__, template_folder="templates", static_folder="static"
)


@act_bp.route("/<int:act_id>", methods=["GET"])
@login_required
def act(act_id):
    act = Act.query.filter_by(act_id=act_id).first_or_404()
    tags = Tag.query.join(ActTag).filter(ActTag.act_id == act_id).all()
    act_tags = [tag.name for tag in tags]
    
    return render_template("act/act.html", act=act, act_tags=act_tags)


@act_bp.route('/save', methods=['POST'])
@login_required
def save():
    if request.method == 'POST':
        if current_user.role != 'admin' and current_user.role != 'expert':
            return jsonify({"status": "error", "message": "Nie masz uprawnień do zapisywania zmian."}), 403

        data = request.json
        act_id = data.get('act_id')
        text = data.get('text')
        tags = data.get('tags')

        print(act_id)
        act = Act.query.filter_by(act_id=act_id).first()
        if not act:
            return jsonify({"status": "error", "message": "Cannot find act with given ID"}), 404

        if text:
            act.text_payload = text
            act.last_edited_date = datetime.today()

        if tags:
            ActTag.query.filter_by(act_id=act_id).delete()

            for tag_name in tags:
                tag = Tag.query.filter_by(name=tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name, num_assigned=0, date_created=datetime.today())
                    db.session.add(tag)
                    db.session.flush()

                tag.num_assigned += 1

                act_tag = ActTag(act_id=act_id, tag_id=tag.tag_id, assigned_date=datetime.today())
                db.session.add(act_tag)

        db.session.commit()

        flash('Zapisano zmiany.', category='success')
        return jsonify({"status": "success", "message": "Zapisano zmiany.", "text": text, "tags": tags}), 200

    return render_template('act/act.html')

@act_bp.route('/all', methods=['GET'])
@login_required
def all_acts():
    page = request.args.get("page", 1, type=int)
    per_page = 15

    pagination = Act.query.order_by(Act.act_id).paginate(page=page, per_page=per_page, error_out=False)

    return render_template(
        'act/acts-table.html',
        acts=pagination.items,
        pagination=pagination   
    )