from flask import Flask, jsonify, request

app = Flask(__name__)

# Потеря стоимости в месяц (доля) по категориям
RATES = {"electronics": 0.03, "furniture": 0.015, "clothes": 0.025, "other": 0.02}
# Множитель по состоянию
CONDITION = {"excellent": 1.0, "good": 0.9, "fair": 0.75, "poor": 0.55}


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.post("/calculate")
def calculate():
    d = request.get_json()
    rate = RATES.get(d.get("category"), 0.02)
    cond = CONDITION.get(d.get("condition"), 0.75)
    factor = max(0.15, 1 - rate * int(d["age_months"]))
    price = round(int(d["original_price"]) * factor * cond)
    return jsonify(recommended_price=price)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)