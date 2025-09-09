from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pathlib import Path
from recommender.recommender import Recommender

# Inicializamos FastAPI
app = FastAPI(title="Ecommerce Assistant API")

# 📌 Ubicación del archivo CSV
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "products.csv"

# Inicializamos el recomendador
try:
    rec = Recommender(data_file=str(DATA_FILE))
    rec.train()
except Exception as e:
    rec = None
    print(f"⚠️ No se pudo cargar el modelo: {e}")

@app.get("/")
def home():
    return {"mensaje": "Bienvenido a la API de Ecommerce Assistant con FastAPI 🚀"}

# 📌 Ruta para devolver el HTML (si lo quieres servir desde templates)
@app.get("/web", response_class=HTMLResponse)
def web_home():
    try:
        html_path = BASE_DIR / "web" / "templates" / "index.html"
        if html_path.exists():
            return html_path.read_text(encoding="utf-8")
        else:
            raise HTTPException(status_code=404, detail="index.html no encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 📌 Ruta para obtener recomendaciones
@app.get("/recommend/{product_index}")
def recommend(product_index: int):
    if rec is None:
        raise HTTPException(status_code=500, detail="Modelo no cargado")
    try:
        recommendations = rec.recommend(product_index)
        return JSONResponse(content=recommendations.to_dict(orient="records"))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 📌 Ruta para obtener productos
@app.get("/products")
def get_products():
    if rec is None:
        raise HTTPException(status_code=500, detail="Datos no disponibles")
    try:
        return JSONResponse(content=rec.data.to_dict(orient="records"))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))