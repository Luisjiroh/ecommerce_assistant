from flask import Flask, jsonify, render_template
import sys, os

# 👇 Agregamos la raíz del proyecto al path de Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 👇 Importamos la clase desde recommender/recommender.py
from recommender.recommender import Recommender

# 👇 Le decimos a Flask dónde están las plantillas HTML
app = Flask(__name__, template_folder="../web/templates")

# 👇 Inicializamos el recomendador con los datos
rec = Recommender(data_file="../data/products.csv")
rec.train()

@app.route("/")
def home():
    return "Bienvenido a la API de Ecommerce Assistant"

# 👇 Ruta para abrir el HTML en el navegador
@app.route("/web")
def web_home():
    return render_template("index.html")

# 👇 Nueva ruta para obtener recomendaciones
@app.route("/recommend/<int:product_index>")
def recommend(product_index):
    try:
        recommendations = rec.recommend(product_index)
        return recommendations.to_json(orient="records", force_ascii=False)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/products")
def get_products():
    try:
        return rec.data.to_json(orient="records", force_ascii=False)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    # 👇 Host=0.0.0.0 para que se pueda acceder desde cualquier lado
    app.run(debug=True, host="127.0.0.1", port=8000)