from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import random

# IMPORT YOUR MODEL HERE
from model import predict_risk

app = FastAPI()

# Enable CORS so React can talk to this server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Scenario(BaseModel):
    speed: int
    roadType: str
    curvature: float
    weather: str
    lighting: str

@app.post("/predict")
def predict(scenario: Scenario):
    print(f"Received scenario: {scenario}")
    
    try:
        risk_score = predict_risk(scenario.dict())
        return {"riskScore": risk_score}
    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
