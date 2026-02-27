# 📊 Churn Prediction Dashboard

This is a Machine Learning web application built using **Streamlit** that predicts customer churn based on input features.

🔗 **Live App:**  
https://churn-prediction-dashboard-azcbou5rwuqembqm5go2zg.streamlit.app/

---

## 🛠️ Technologies Used

- Python  
- Streamlit  
- Scikit-learn  
- Pandas  
- NumPy  
- Matplotlib  
- Seaborn  

---

## 💻 How to Run This Project Locally

Follow these steps to run the project on your system:

### 🔹 Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/churn-prediction-dashboard.git
cd churn-prediction-dashboard
🔹 Step 2: Create Virtual Environment (Recommended)
For Windows:
python -m venv venv
venv\Scripts\activate
For Mac/Linux:
python3 -m venv venv
source venv/bin/activate
🔹 Step 3: Install Required Libraries
pip install -r requirements.txt

If requirements.txt is not available:

pip install streamlit pandas numpy scikit-learn matplotlib seaborn
🔹 Step 4: Run the Application
streamlit run app.py

After running, Streamlit will automatically open the app in your browser at:

http://localhost:8501
📁 Project Structure
churn-prediction-dashboard/
│
├── app.py
├── model.pkl
├── requirements.txt
└── README.md
📌 Notes

Make sure model.pkl file is in the same directory as app.py

Python version 3.8+ recommended

Ensure all dependencies are installed before running the app
