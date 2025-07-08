import os
from flask import Flask, request, render_template
import psycopg2
from datetime import datetime

app = Flask(__name__)

# PostgreSQL connectie via DigitalOcean
conn = psycopg2.connect(
    host="bbl2025-db-do-user-23457648-0.k.db.ondigitalocean.com",
    port="25060",
    dbname="defaultdb",
    user="doadmin",
    password="AVNS_NkJT2sdXBKULZJk3SSD",
    sslmode="require"
)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        email = request.form.get('email')
        m2 = request.form.get('m2')

        if not email or not m2:
            return "❌ E-mail en m² zijn verplicht!", 400

        # Dummy CUFXML-inhoud
        inhoud = f"<CUFXML><m2>{m2}</m2></CUFXML>"
        naam = f"CUFXML_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xml"

        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO CUFXML_Bestanden (naam, inhoud, email, m2)
                    VALUES (%s, %s, %s, %s)
                """, (naam, inhoud, email, m2))

        return f"✅ Bestand {naam} succesvol toegevoegd!"

    return render_template("index.html")
