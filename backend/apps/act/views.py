import datetime

from flask import Blueprint, jsonify, render_template, request, flash
from flask_login import login_required
from backend.models import Act, Tag, ActTag, db
from math import ceil


# TODO: pamietac o zabezpieczeniu zeby odczyt byl dla uzytownika z odpowiednimi uprawnieniami, a zapisa tylko dla admina i eksperta

act_bp = Blueprint(
    "act_bp", __name__, template_folder="templates", static_folder="static"
)


@act_bp.route("/<int:act_id>", methods=["GET"])
@login_required
def act(act_id):
    act = Act.query.filter_by(act_id=act_id).first_or_404()
    return render_template("act/act.html", act=act)


@act_bp.route('/save', methods=['POST'])
def save():
    if request.method == 'POST':
        act_id = request.args.get('id')

        data = request.json
        text = data.get('text')
        tags = data.get('tags')

        act = Act.query.filter_by(act_id=act_id).first()
        if not act:
            return jsonify({"status": "error", "message": "Cannot find act with given ID"}), 404

        if text:
            act.text_payload = text
            act.last_edited_date = datetime.utcnow()

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
def all_acts():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    total_acts = Act.query.count()
    acts = Act.query.order_by(Act.date_scraped.desc()).paginate(page=page, per_page=per_page)

    acts_data = [
        {
            "id": act.act_id,
            "title": act.du_code,
            "expert": act.tags[0].creator.username if act.tags else "Brak eksperta",
            "date": act.date_scraped.strftime('%Y-%m-%d %H:%M:%S'),
            "link": f"/act/{act.act_id}"
        }
        for act in acts.items
    ]

    pagination_info = {
        "current_page": page,
        "per_page": per_page,
        "total_pages": ceil(total_acts / per_page),
        "total_acts": total_acts,
        "has_prev": acts.has_prev,
        "has_next": acts.has_next,
        "prev_page": page - 1 if acts.has_prev else None,
        "next_page": page + 1 if acts.has_next else None
    }

    return render_template('act/acts-table.html', acts=acts_data, pagination=pagination_info)