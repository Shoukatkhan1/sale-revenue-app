import streamlit as st
import requests

# --- Page Configuration ---
st.set_page_config(
    page_title="🔮 Sales Revenue Predictor",
    page_icon="📈",
    layout="centered"
)

# --- Header Section ---
st.markdown("""
    <h1 style='text-align: center; color: #4CAF50;'>🔮 Sales Revenue Prediction App</h1>
    <p style='text-align: center;'>Predict your sales revenue based on product and market factors!</p>
    <hr>
""", unsafe_allow_html=True)

# --- API Endpoint Configuration ---
API_URL = "http://localhost:8000/predict"  # Update with your API URL if hosted elsewhere


with st.form("prediction_form"):
    st.subheader("📋 Enter Product and Market Details:")

    col1, col2 = st.columns(2)
    
    with col1:
        ProductCategory = st.selectbox("Product Category", ["Electronics", "Clothing", "Furniture", "Toys"])
        Region = st.selectbox("Region", ["North", "South", "East", "West"])
        CustomerSegment = st.selectbox("Customer Segment", ["High Income", "Middle Income", "Low Income"])
        IsPromotionApplied = st.radio("Promotion Applied?", ["Yes", "No"])
        ProductionCost = st.number_input("Production Cost ($)", min_value=0.0, value=500.0, step=10.0)
        MarketingSpend = st.number_input("Marketing Spend ($)", min_value=0.0, value=200.0, step=10.0)

    with col2:
        SeasonalDemandIndex = st.number_input("Seasonal Demand Index", min_value=0.1, value=1.0)
        CompetitorPrice = st.number_input("Competitor Price ($)", min_value=0.0, value=250.0)
        CustomerRating = st.slider("Customer Rating (1-5)", min_value=1.0, max_value=5.0, value=4.0, step=0.1)
        EconomicIndex = st.number_input("Economic Index", min_value=0.0, value=100.0)
        StoreCount = st.number_input("Store Count", min_value=1, value=50, step=1)
        PriceCompetitiveness = st.number_input("Price Competitiveness (Optional)", value=0.0, step=0.01)

    submitted = st.form_submit_button("🚀 Predict Revenue")

if submitted:
    data = {
        "ProductCategory": ProductCategory,
        "Region": Region,
        "CustomerSegment": CustomerSegment,
        "IsPromotionApplied": IsPromotionApplied,
        "ProductionCost": ProductionCost,
        "MarketingSpend": MarketingSpend,
        "SeasonalDemandIndex": SeasonalDemandIndex,
        "CompetitorPrice": CompetitorPrice,
        "CustomerRating": CustomerRating,
        "EconomicIndex": EconomicIndex,
        "StoreCount": StoreCount,
        "PriceCompetitiveness": PriceCompetitiveness if PriceCompetitiveness != 0.0 else None
    }

    with st.spinner("⏳ Predicting..."):
        response = requests.post(API_URL, json=data)

    if response.status_code == 200:
        result = response.json()
        st.success(f"💰 **Predicted Sales Revenue: ${result['prediction_Sale_Revenue']}**")
        
        with st.expander("See Details of Input Data Sent to API"):
            st.json(result['input_feature'])
    else:
        st.error(f"❌ Failed to get prediction: {response.text}")

# --- Footer ---
st.markdown("""
    <hr>
    <p style='text-align: center;'>
    Developed by <strong>Shoukat Khan</strong> | Data Scientist & ML Engineer
    </p>
""", unsafe_allow_html=True)
