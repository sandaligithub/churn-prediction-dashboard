# ==========================================
# ENTERPRISE CHURN INTELLIGENCE (FULL TASK VERSION)
# ==========================================

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Enterprise Churn Intelligence",
    page_icon="📊",
    layout="wide"
)

# ==========================================
# CLEAN PROFESSIONAL CSS
# ==========================================

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}
section[data-testid="stSidebar"] {
    background-color: #111827;
}
.metric-card {
    background: linear-gradient(145deg, #1f2937, #111827);
    padding: 22px;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0px 6px 20px rgba(0,0,0,0.5);
}
.section-card {
    background: #1e293b;
    padding: 30px;
    border-radius: 18px;
    margin-bottom: 25px;
}
.stButton>button {
    background: linear-gradient(90deg, #ff512f, #dd2476);
    color: white;
    font-weight: bold;
    border-radius: 12px;
    height: 52px;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# LOAD MODEL + PREPROCESSOR
# ==========================================

model = joblib.load("xgb_model.pkl")
preprocessor = joblib.load("preprocessor.pkl")

# 🔹 IMPORTANT: Replace these with your real metrics from notebook
MODEL_ACCURACY = 0.82
MODEL_AUC = 0.88
MODEL_F1 = 0.79
MODEL_PRECISION = 0.81
MODEL_RECALL = 0.77

# ==========================================
# HEADER
# ==========================================

st.markdown("""
<h1 style='text-align:center;'>🏢 Enterprise Customer Churn Intelligence</h1>
<h4 style='text-align:center; color:lightgray;'>
Strategic Retention & Revenue Risk Analytics Platform
</h4>
<hr>
""", unsafe_allow_html=True)

# ==========================================
# TABS
# ==========================================

tab1, tab2, tab3 = st.tabs(["📊 Overview", "🎯 Prediction Engine", "📈 Model Analytics"])

# ==========================================
# OVERVIEW TAB
# ==========================================

with tab1:

    col1, col2, col3 = st.columns(3)

    col1.markdown("<div class='metric-card'><h3>XGBoost</h3><p>Primary Model</p></div>", unsafe_allow_html=True)
    col2.markdown("<div class='metric-card'><h3>Customer Churn</h3><p>Target Variable</p></div>", unsafe_allow_html=True)
    col3.markdown("<div class='metric-card'><h3>End-to-End ML</h3><p>Pipeline</p></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class='section-card'>
    This enterprise system predicts churn probability using engineered RFM features,
    service usage patterns, tenure metrics, and payment behavior.
    It also quantifies revenue exposure and provides AI-driven retention recommendations.
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# PREDICTION TAB
# ==========================================

with tab2:

    st.sidebar.header("Customer Input Panel")

    gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
    SeniorCitizen = st.sidebar.selectbox("Senior Citizen", [0, 1])
    Partner = st.sidebar.selectbox("Partner", ["Yes", "No"])
    Dependents = st.sidebar.selectbox("Dependents", ["Yes", "No"])
    tenure = st.sidebar.slider("Tenure (Months)", 0, 72, 12)

    PhoneService = st.sidebar.selectbox("Phone Service", ["Yes", "No"])
    MultipleLines = st.sidebar.selectbox("Multiple Lines", ["No", "Yes", "No phone service"])

    InternetService = st.sidebar.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
    OnlineSecurity = st.sidebar.selectbox("Online Security", ["Yes", "No", "No internet service"])
    OnlineBackup = st.sidebar.selectbox("Online Backup", ["Yes", "No", "No internet service"])
    DeviceProtection = st.sidebar.selectbox("Device Protection", ["Yes", "No", "No internet service"])
    TechSupport = st.sidebar.selectbox("Tech Support", ["Yes", "No", "No internet service"])
    StreamingTV = st.sidebar.selectbox("Streaming TV", ["Yes", "No", "No internet service"])
    StreamingMovies = st.sidebar.selectbox("Streaming Movies", ["Yes", "No", "No internet service"])

    Contract = st.sidebar.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
    PaperlessBilling = st.sidebar.selectbox("Paperless Billing", ["Yes", "No"])

    PaymentMethod = st.sidebar.selectbox("Payment Method", [
        "Electronic check",
        "Mailed check",
        "Bank transfer (automatic)",
        "Credit card (automatic)"
    ])

    MonthlyCharges = st.sidebar.number_input("Monthly Charges", 0.0, 200.0, 70.0)
    TotalCharges = st.sidebar.number_input("Total Charges", 0.0, 10000.0, 1000.0)

    # Engineered Features
    Recency = tenure
    service_values = [
        PhoneService, MultipleLines, InternetService,
        OnlineSecurity, OnlineBackup, DeviceProtection,
        TechSupport, StreamingTV, StreamingMovies
    ]

    Frequency = sum([1 for val in service_values if val in ["Yes", "DSL", "Fiber optic"]])
    Monetary = MonthlyCharges
    Tenure_Ratio = tenure / 72
    Service_Bundle_Score = Frequency
    Payment_Reliability_Score = 1 if PaymentMethod in [
        "Bank transfer (automatic)", "Credit card (automatic)"
    ] else 0

    input_data = pd.DataFrame({
        "gender":[gender], "SeniorCitizen":[SeniorCitizen],
        "Partner":[Partner], "Dependents":[Dependents],
        "tenure":[tenure], "PhoneService":[PhoneService],
        "MultipleLines":[MultipleLines], "InternetService":[InternetService],
        "OnlineSecurity":[OnlineSecurity], "OnlineBackup":[OnlineBackup],
        "DeviceProtection":[DeviceProtection], "TechSupport":[TechSupport],
        "StreamingTV":[StreamingTV], "StreamingMovies":[StreamingMovies],
        "Contract":[Contract], "PaperlessBilling":[PaperlessBilling],
        "PaymentMethod":[PaymentMethod],
        "MonthlyCharges":[MonthlyCharges], "TotalCharges":[TotalCharges],
        "Recency":[Recency], "Frequency":[Frequency],
        "Monetary":[Monetary], "Tenure_Ratio":[Tenure_Ratio],
        "Service_Bundle_Score":[Service_Bundle_Score],
        "Payment_Reliability_Score":[Payment_Reliability_Score]
    })

    if st.button("🚀 Run Churn Risk Analysis"):

        processed = preprocessor.transform(input_data)
        probability = model.predict_proba(processed)[0][1]

        # Risk Segment
        if probability > 0.75:
            segment = "Critical Risk"
            strategy = "Immediate retention discount + senior relationship manager intervention."
        elif probability > 0.5:
            segment = "High Risk"
            strategy = "Personalized loyalty discount + proactive customer outreach."
        elif probability > 0.3:
            segment = "Moderate Risk"
            strategy = "Targeted engagement campaign and service upgrade recommendation."
        else:
            segment = "Low Risk"
            strategy = "Maintain engagement via rewards and upsell premium bundles."

        st.markdown("## 📊 Executive Risk Intelligence")

        r1, r2 = st.columns(2)
        r1.markdown(f"<div class='metric-card'><h2>{segment}</h2><p>Risk Segment</p></div>", unsafe_allow_html=True)
        r2.markdown(f"<div class='metric-card'><h2>{probability:.2%}</h2><p>Churn Probability</p></div>", unsafe_allow_html=True)

        st.progress(float(probability))

        monthly_risk = MonthlyCharges * probability
        annual_risk = monthly_risk * 12

        st.markdown("### 💰 Financial Risk Exposure")

        f1, f2 = st.columns(2)
        f1.markdown(f"<div class='metric-card'><h2>${monthly_risk:.2f}</h2><p>Monthly Revenue at Risk</p></div>", unsafe_allow_html=True)
        f2.markdown(f"<div class='metric-card'><h2>${annual_risk:.2f}</h2><p>Annual Revenue at Risk</p></div>", unsafe_allow_html=True)

        # Retention Recommendation
        st.markdown("### 🎯 AI Retention Recommendation")
        st.markdown(f"<div class='section-card'>{strategy}</div>", unsafe_allow_html=True)

# ==========================================
# MODEL ANALYTICS TAB
# ==========================================

with tab3:

    st.subheader("📈 Model Performance Metrics")

    m1, m2, m3, m4, m5 = st.columns(5)

    m1.metric("Accuracy", MODEL_ACCURACY)
    m2.metric("ROC-AUC", MODEL_AUC)
    m3.metric("F1 Score", MODEL_F1)
    m4.metric("Precision", MODEL_PRECISION)
    m5.metric("Recall", MODEL_RECALL)

    st.markdown("---")

    st.subheader("🔍 Feature Importance")

    feature_names = preprocessor.get_feature_names_out()
    importances = model.feature_importances_

    feat_imp = pd.DataFrame({
        "Feature": feature_names,
        "Importance": importances
    }).sort_values(by="Importance", ascending=False).head(10)

    fig, ax = plt.subplots()
    ax.barh(feat_imp["Feature"], feat_imp["Importance"])
    ax.invert_yaxis()
    st.pyplot(fig)

st.markdown("<hr><p style='text-align:center; color:gray;'>Enterprise ML Churn Platform</p>", unsafe_allow_html=True)