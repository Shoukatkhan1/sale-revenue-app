from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional
import joblib
import pandas as pd

app = FastAPI(
    title="SALE REVENUE Prediction Model",
    description="This model predicts sales revenue based on product and market features.",
    version="1.0.0"
)

# Load the trained model
model = None
try:
    model = joblib.load(r"best_pipeline_model.joblib")
    print("Model loaded successfully.")
except FileNotFoundError as e:
    print(f"Error loading model: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")

# Define input model
class SaleRevenueFeature(BaseModel):
    ProductCategory: str = Field(..., example="Furniture", description="Product category: Electronics, Clothing, Furniture, Toys")
    Region: str = Field(..., example="East", description="Sales region: North, South, East, West")
    CustomerSegment: str = Field(..., example="High Income", description="Customer income segment")
    IsPromotionApplied: str = Field(..., example="Yes", description="Whether promotion was applied: Yes/No")
    ProductionCost: float = Field(..., example=536.05, description="Product manufacturing cost")
    MarketingSpend: float = Field(..., example=189.27, description="Marketing expenditure")
    SeasonalDemandIndex: float = Field(..., example=1.15, description="Seasonal demand factor (1.0 = average)")
    CompetitorPrice: float = Field(..., example=220.83, description="Competitor's product price")
    CustomerRating: float = Field(..., example=4.03, description="Customer rating (1-5 scale)")
    EconomicIndex: float = Field(..., example=146.22, description="Economic conditions index")
    StoreCount: int = Field(..., example=52, description="Number of stores carrying product")
    PriceCompetitiveness: Optional[float] = Field(None, example=-100.5, description="CompetitorPrice - ProductionCost")

# Define output model
class PredictionResponse(BaseModel):
    prediction_Sale_Revenue: float = Field(..., example=2293.14, description="Predicted sales revenue")
    input_feature: dict = Field(..., example={}, description="Echo of input features")

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>Sales Revenue Predictor</title>
            <style>
                body { font-family: Arial, sans-serif; background-color: #f0f8ff; text-align: center; padding: 50px; }
                .container { background-color: #fff; padding: 30px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); max-width: 700px; margin: auto; }
                h1 { color: #007acc; }
                footer { margin-top: 40px; font-size: 0.9em; color: #555; }
                code { background: #f5f5f5; padding: 2px 5px; border-radius: 3px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🔬 Sales Revenue Prediction API</h1>
                <p>Welcome to the Sales Revenue Predictor!</p>
                <p>Send a POST request to <code>/predict</code> with input data to get predicted sales revenue.</p>
                <footer>Created by <strong>Shoukat Khan</strong> | Data Scientist & ML Engineer</footer>
            </div>
        </body>
    </html>
    """

@app.post("/predict", response_model=PredictionResponse)
async def predict_sales(features: SaleRevenueFeature):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        # Convert to DataFrame
        input_data = features.dict()
        
        # Calculate PriceCompetitiveness if not provided
        if input_data["PriceCompetitiveness"] is None:
            input_data["PriceCompetitiveness"] = input_data["CompetitorPrice"] - input_data["ProductionCost"]
            
        input_df = pd.DataFrame([input_data])
        
        # Make prediction
        prediction = model.predict(input_df)
        
        return PredictionResponse(
            prediction_Sale_Revenue=round(float(prediction[0]), 2),
            input_feature=input_data
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
