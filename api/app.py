from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from recommender.recommender import Recommender

# Inicializamos FastAPI
app = FastAPI(title="Ecommerce Assistant API")

# 📌 Ubicación base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# 📌 Configuración de templates (para renderizar index.html)
templates = Jinja2Templates(directory=str(BASE_DIR / "web" / "templates"))

# 📌 Cargar datos desde el CSV
DATA_FILE = BASE_DIR / "data" / "products.csv"
try:
    rec = Recommender(data_file=str(DATA_FILE))
    rec.train()
except Exception as e:
    rec = None
    print(f"⚠️ No se pudo cargar el modelo: {e}")

# 📌 Ruta raíz
@app.get("/")
def home():
    return {"mensaje": "Bienvenido a la API de Ecommerce Assistant con FastAPI 🚀"}

# 📌 Ruta para abrir el HTML en el navegador
@app.get("/web")
def web_home(request: Request):
    try:
        return templates.TemplateResponse("index.html", {"request": request})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 📌 Ruta para obtener productos
@app.get("/products")
def get_products():
    if rec is None:
        return JSONResponse(content={"error": "Datos no disponibles"}, status_code=500)
    try:
        return JSONResponse(content=rec.data.to_dict(orient="records"))
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)

# 📌 Ruta para obtener recomendaciones
@app.get("/recommend/{product_index}")
def recommend(product_index: int):
    if rec is None:
        return JSONResponse(content={"error": "Modelo no cargado"}, status_code=500)
    try:
        recommendations = rec.recommend(product_index)
        return JSONResponse(content=recommendations.to_dict(orient="records"))
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)