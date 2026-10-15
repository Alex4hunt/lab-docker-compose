import os

import psycopg2
import requests
from flask import Flask, jsonify, request
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
WS_URL = os.environ["WEB_SERVICE_URL"]


def get_conn():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    )


@app.get("/api/ads")
def list_ads():
    with get_conn() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT * FROM ads ORDER BY id")
        return jsonify(cur.fetchall())


@app.post("/api/ads")
def add_ad():
    d = request.get_json()
    with get_conn() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            "INSERT INTO ads (title, category, original_price, age_months, condition) "
            "VALUES (%s, %s, %s, %s, %s) RETURNING *",
            (d["title"], d["category"], int(d["original_price"]),
             int(d["age_months"]), d["condition"]),
        )
        return jsonify(cur.fetchone()), 201


@app.delete("/api/ads/<int:ad_id>")
def delete_ad(ad_id):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("DELETE FROM ads WHERE id = %s", (ad_id,))
    return jsonify(deleted=ad_id)


@app.post("/api/recommend-all")
def recommend_all():
    """Для каждого объявления просим web-сервис посчитать цену и сохраняем в БД."""
    with get_conn() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT * FROM ads ORDER BY id")
        for ad in cur.fetchall():
            r = requests.post(
                WS_URL + "/calculate",
                json={
                    "category": ad["category"],
                    "condition": ad["condition"],
                    "original_price": ad["original_price"],
                    "age_months": ad["age_months"],
                },
                timeout=5,
            )
            r.raise_for_status()
            cur.execute(
                "UPDATE ads SET recommended_price = %s WHERE id = %s",
                (r.json()["recommended_price"], ad["id"]),
            )
    return jsonify(status="ok")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)