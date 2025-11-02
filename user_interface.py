from flask import Flask, render_template_string, request
from inference_engine import InferenceEngine
import os

app = Flask(__name__)

# Load rules.json
kb_path = os.path.join(os.path.dirname(__file__), "rules.json")
engine = InferenceEngine(kb_path)

# Daftar gejala
symptoms = {
    "G001": "Peka terhadap cahaya (fotofobia)",
    "G002": "Terasa nyeri",
    "G003": "Bintik nanah pada kornea",
    "G004": "Ada kotoran mata",
    "G005": "Kelopak mata membengkak",
    "G006": "Iritasi mata",
    "G007": "Benjolan pada kelopak mata",
    "G008": "Daerah kemerahan di bawah kelopak mata",
    "G009": "Bulu mata rontok",
    "G010": "Mata sulit dibuka pagi hari",
    "G011": "Alergi",
    "G012": "Mata panas",
    "G013": "Seperti kelilipan",
    "G014": "Mata berair",
    "G015": "Nyeri tepi kelopak mata",
    "G016": "Kornea keruh",
    "G017": "Konjungtiva meradang",
    "G018": "Penglihatan kabur",
    "G019": "Floaters/kilatan cahaya",
    "G020": "Kehilangan penglihatan bertahap",
    "G021": "Sulit melihat malam hari",
    "G022": "Penurunan ketajaman penglihatan",
    "G023": "Kemerahan sklera",
    "G024": "Mata menonjol",
    "G025": "Demam",
    "G026": "Bola mata bengkak",
    "G027": "Mata merah",
    "G028": "Mata gatal",
    "G029": "Mata perih",
    "G030": "Konjungtiva merah",
    "G031": "Konjungtiva bengkak",
    "G032": "Benjolan kuning",
    "G033": "Nyeri bila ditekan",
    "G034": "Gangguan penglihatan",
    "G035": "Sakit kepala",
    "G036": "Koma",
    "G037": "Kejang",
    "G038": "Sakit saat gerakkan mata",
    "G039": "Kehilangan penglihatan total",
    "G040": "Nyeri di sekitar kantung air mata",
    "G041": "Nanah",
    "G042": "Pusing",
    "G043": "Mual muntah",
    "G044": "Pupil melebar"
}

HOME_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Sistem Pakar Penyakit Mata</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background: linear-gradient(135deg, #91c9f7, #cee7ff); }
        .title-box {
            background: white;
            padding: 40px;
            border-radius: 18px;
            margin-top: 140px;
            box-shadow: 0 0 18px rgba(0,0,0,0.15);
        }
        h1 { color: #00529b; font-weight: 700; }
        p { color: #003865; }
    </style>
</head>
<body>
<div class="container text-center">
    <div class="title-box">
        <img src="https://cdn-icons-png.flaticon.com/512/159/159604.png" width="90">
        <h1 class="mt-3">Sistem Pakar<br>Diagnosa Penyakit Mata</h1>
        <p class="mt-3">Sistem ini membantu mengetahui indikasi penyakit mata berdasarkan gejala awal.</p>
        <a href="/diagnose" class="btn btn-primary btn-lg mt-3 px-5">Mulai Diagnosa</a>
    </div>
</div>
</body>
</html>
"""

DIAGNOSE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Diagnosa Penyakit Mata</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background: #f0f7ff; }
        .card { border-radius: 18px; }
        .result-box {
            border-left: 5px solid #007bff;
            border-radius: 10px;
        }
        .disease-name { color:#003e82; font-weight:700; }
    </style>
</head>
<body>
<div class="container mt-4 mb-4">
    <a href="/" class="btn btn-secondary mb-3">← Kembali</a>

    <div class="card p-4 shadow-sm">
        <h3 class="text-primary"><b>🩺 Pilih Gejala</b></h3>

        <form method="POST">
            <div class="row">
            {% for code, desc in symptoms.items() %}
                <div class="col-md-6 mb-2">
                    <input type="checkbox" class="form-check-input" name="symptoms" value="{{ code }}">
                    <label class="form-check-label">{{ desc }}</label>
                </div>
            {% endfor %}
            </div>
            <button type="submit" class="btn btn-primary w-100 mt-3">🔍 Proses Diagnosa</button>
        </form>

        {% if result %}
        <div class="mt-4">
            <h4 class="text-success"><b>📌 Hasil Diagnosa</b></h4>

            {% for r in result %}
            <div class="alert alert-info mt-3 result-box">
                <h5 class="disease-name">{{ r['name'] }} ({{ r['disease'] }})</h5>
                <p><b>Penjelasan:</b> {{ r['desc'] }}</p>
                <p><b>Solusi:</b> {{ r['solution'] }}</p>
                <p><b>Confidence:</b> {{ r['confidence'] }}% 
                    ({{ r['match_count'] }}/{{ r['total_needed'] }} gejala cocok)
                </p>
            </div>
            {% endfor %}
        </div>
        {% endif %}
    </div>
</div>

<footer class="text-center text-muted mt-4 mb-3">
    Sistem Pakar Penyakit Mata © 2025
</footer>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HOME_TEMPLATE)

@app.route("/diagnose", methods=["GET","POST"])
def diagnose():
    result = None
    if request.method == "POST":
        selected_symptoms = request.form.getlist("symptoms")
        result = engine.diagnose(selected_symptoms)
    return render_template_string(DIAGNOSE_TEMPLATE, symptoms=symptoms, result=result)

if __name__ == "__main__":
    app.run(debug=True)
