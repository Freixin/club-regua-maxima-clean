from fastapi import FastAPI
import os

# Criar aplicação FastAPI
app = FastAPI(title="Club Régua Máxima - Sistema de Agendamento")

@app.get("/")
def root():
    return {
        "message": "Club Régua Máxima - Sistema de Agendamento",
        "status": "online",
        "version": "1.0.0"
    }

@app.get("/api")
def api_root():
    return {
        "api": "Club Régua Máxima API",
        "status": "working",
        "endpoints": ["/", "/api", "/api/health", "/api/test"]
    }

@app.get("/api/health")
def health():
    db_connection = os.environ.get('DATABASE_URL', 'not configured')
    return {
        "status": "healthy",
        "api": "operational",
        "database": "configured" if db_connection != 'not configured' else "not configured",
        "timestamp": "2025-01-09"
    }

@app.get("/api/test")
def test():
    return {
        "test": "success",
        "deploy": "working",
        "message": "API funcionando perfeitamente!"
    }
