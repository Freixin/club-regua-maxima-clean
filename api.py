from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
import os
from datetime import datetime

app = FastAPI()

# Configuração do MongoDB
MONGODB_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017/club_regua_maxima")

def get_database():
    try:
        client = MongoClient(MONGODB_URL)
        return client.get_default_database()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro de conexão com o banco: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Club Régua Máxima API", "status": "online", "timestamp": datetime.now()}

@app.get("/api/health")
async def health_check():
    try:
        db = get_database()
        # Teste simples de conexão
        db.command("ping")
        return {"status": "healthy", "database": "connected", "timestamp": datetime.now()}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e), "timestamp": datetime.now()}

@app.get("/api/test")
async def test_db():
    try:
        db = get_database()
        # Teste de escrita e leitura
        test_collection = db.test
        test_doc = {"test": True, "timestamp": datetime.now()}
        result = test_collection.insert_one(test_doc)
        
        # Verifica se inseriu
        found_doc = test_collection.find_one({"_id": result.inserted_id})
        
        # Remove o documento de teste
        test_collection.delete_one({"_id": result.inserted_id})
        
        return {
            "message": "Banco de dados funcionando perfeitamente!",
            "test_result": "success",
            "timestamp": datetime.now()
        }
    except Exception as e:
        return {"error": str(e), "timestamp": datetime.now()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
