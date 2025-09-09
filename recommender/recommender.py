import pandas as pd
from sklearn.neighbors import NearestNeighbors

class Recommender:
    def __init__(self, data_file="../data/products.csv"):
        # Intentamos cargar el CSV
        try:
            self.data = pd.read_csv(data_file)
        except FileNotFoundError:
            print("⚠️ No se encontró el archivo de productos.")
            self.data = pd.DataFrame()
        self.model = None

    def train(self):
        if not self.data.empty:
            features = self.data.select_dtypes(include=["number"])  # solo columnas numéricas
            self.model = NearestNeighbors(n_neighbors=3, algorithm="auto")
            self.model.fit(features)
            print("✅ Modelo de recomendación entrenado.")
        else:
            print("⚠️ No hay datos para entrenar el modelo.")

    def recommend(self, product_index=0):
        if self.model is None:
            print("⚠️ El modelo no está entrenado.")
            return []
        distances, indices = self.model.kneighbors(
            [self.data.select_dtypes(include=["number"]).iloc[product_index]]
        )
        return self.data.iloc[indices[0]]
