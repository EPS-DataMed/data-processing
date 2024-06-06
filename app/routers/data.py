from fastapi import FastAPI
from pydantic import BaseModel 
from typing import List

class formulario(BaseModel):
    peso: float
    altura: float
    imc: float
    tipo_sanguineo: str
    circunferencia_abdominal: float
    hemacias: float
    hemoglobina: float
    hematocrino: float
    hemoglobina_glicada: float
    ast: float
    alt: float
    ureia: float
    creatina: float
    alergias: str
    doecas: str
    medicacao_em_uso: str
    historico_familiar: str
    observacoes_importantes: str
    exame_de_imagem: str

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/exames/{user_id}")
async def data_processing(user_id: int, listaExames: List[int]):
    return

@app.post("/formulario/{user_id}")
async def add_formulario(user_id: int, formulario: formulario):
    return