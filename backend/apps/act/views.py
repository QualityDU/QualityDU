from flask import Blueprint, jsonify, render_template, request, flash
from flask_login import login_required
from models import Act

# TODO: pamietac o zabezpieczeniu zeby odczyt byl dla uzytownika z odpowiednimi uprawnieniami, a zapisa tylko dla admina i eksperta

act_bp = Blueprint(
    "act_bp", __name__, template_folder="templates", static_folder="static"
)


@act_bp.route("/")
@login_required
def act():
    act_id = request.args.get('id')
    if act_id:
        acts = Act.query.filter_by(act_id=act_id).all()
    else:
        acts = Act.query.all() # TODO: Add pegination???
    return render_template("act/act.html", acts=acts)


@act_bp.route('/save', methods=['POST']) # TODO: pozniej dodac parametr i na podstawie niego wybrac z bazy danych akt
def save():
    if request.method == 'POST':

        data = request.json
        text = data.get('text')
        tags = data.get('tags')

        # TODO: Zapis zmian w bazie danych

        flash('Zapisano zmiany.', category='success')
        return jsonify({"status": "success", "message": "Zapisano zmiany.", "text": text, "tags": tags}), 200

    return render_template('act/act.html')

@act_bp.route('/all', methods=['GET']) # TODO: dodac parametr dot. paginacji
def all_acts():
    ACTS = [
        {
            "id": 1,
            "title": "Obwieszczenie Marszałka Sejmu Rzeczypospolitej Polskiej z dnia 11 października 2024 r. w sprawie ogłoszenia jednolitego tekstu ustawy o emeryturach i rentach z Funduszu Ubezpieczeń Społecznych",
            "expert": "teodorPrawnik",
            "date": "2024-11-08 11:30:08",
            "link": "#"
        },
        {
            "id": 2,
            "title": "Ustawa o ochronie środowiska z dnia 10 września 2023 r.",
            "expert": "agnieszkaEkolog",
            "date": "2024-10-01 15:45:22",
            "link": "#"
        }
    ]
    return render_template('act/acts-table.html', acts=ACTS)