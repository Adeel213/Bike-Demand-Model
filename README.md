# 🚲 Bike Sharing Demand Predictor

A machine learning web app that predicts how many bikes will be rented in a given hour, based on weather and time conditions.

**Live App:** https://bike-demand-predictors.streamlit.app/

## What It Does

You enter the season, weather, temperature, humidity, windspeed, hour, month, and day — the app predicts the expected number of bike rentals for that hour.

## Dataset

- Source: [Kaggle - Bike Sharing Demand](https://www.kaggle.com/c/bike-sharing-demand/data)
- Historical hourly rental data from Capital Bikeshare (Washington D.C.)
- Features: season, weather, temperature, humidity, windspeed, datetime

## Steps Followed

1. **EDA** — studied rental patterns by hour, season, weather, and working day
2. **Feature Engineering**
   - Extracted hour, month, weekday from datetime
   - Encoded hour as sine/cosine (so 11 PM and 12 AM are treated as close)
   - Merged rare weather categories
3. **Preprocessing** — scaling and one-hot encoding wrapped in a scikit-learn pipeline
4. **Modeling** — compared Linear, Ridge, Lasso, Polynomial, SVR, Decision Tree, Random Forest, and XGBoost
5. **Tuning** — used GridSearchCV to tune the best models
6. **Final Model** — XGBoost Regressor (best performance)

## Results

| Metric | Score |
|--------|-------|
| RMSE   | 86.89 |
| MAE    | 55.31 |
| R²     | 0.841 |

## Tech Stack

- Python, Pandas, NumPy
- Scikit-learn, XGBoost
- Streamlit (frontend + deployment)

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```
