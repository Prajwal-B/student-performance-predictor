# Student Performance Predictor — End-to-End ML and DS Project with Flask Deployment

Predict student math scores from demographics and prior scores with a fully scripted ML pipeline, artifact management, and a polished Flask UI for form-based inference.

## Demo
- Run locally: `python app.py` then open `http://localhost:5000`.
<img width="705" height="634" alt="Screenshot 2025-12-11 131901" src="https://github.com/user-attachments/assets/52a1ec56-8932-44ed-a6ff-e1974346e664" />


## Key Features
- **Full pipeline**: ingestion → preprocessing → model training + tuning → evaluation → artifacts → Flask serving.
- **Multiple regressors** with hyperparameter tuning and R²-based selection.
- **Training–inference parity**: persisted preprocessor and model artifacts.
- **Config-driven**: `config.yaml` for paths, train/test split, app host/port, logging.
- **Logging & artifacts**: structured logs under `logs/`; models/preprocessors/data under `artifacts/`.
- **Secure & simple UI**: form-only predictions; no input data persisted.

## Architecture
Data CSV → train/test split → preprocessing (impute + encode + scale) → model candidates + GridSearchCV → best model saved → Flask routes → form inputs → preprocessor → model → math score prediction.

## Tech Stack
Python, pandas, numpy, scikit-learn, XGBoost, CatBoost, AdaBoost, Random Forest, Gradient Boosting, Linear Regression, GridSearchCV, Flask, PyYAML, logging.

## Data & Schema
- Features: `gender` (cat), `race_ethnicity` (cat), `parental_level_of_education` (cat), `lunch` (cat), `test_preparation_course` (cat), `reading_score` (num), `writing_score` (num).
- Target: `math_score`.

## Preprocessing Techniques
- **Missing value handling**: SimpleImputer (median for numeric, most_frequent for categorical).
- **Categorical encoding**: OneHotEncoder.
- **Scaling**: StandardScaler (numeric with mean/var; categorical with `with_mean=False` after OHE).
- **ColumnTransformer** to keep pipelines parallel and persisted.
- **Persisted transformer**: saved to `artifacts/preprocessor.pkl` to ensure training–inference parity.

## Modeling & ML Techniques
- Models evaluated: **Random Forest**, **Decision Tree**, **Gradient Boosting**, **XGBoost**, **CatBoost**, **AdaBoost**, **Linear Regression**.
- **Hyperparameter tuning**: GridSearchCV for each candidate with model-specific grids.
- **Metric**: R² on held-out test data; best model selected by max R².
- **Early rejection**: if best R² < 0.6, training fails with a clear exception.
- **Persistence**: best model saved to `artifacts/model.pkl`.

## Training Pipeline (Scripted)
- Entry point: `python -m src.pipeline.train_pipeline`
  1) Ingest CSV (`notebook/data/stud.csv`), save raw/train/test to `artifacts/`.
  2) Fit/transform data with the preprocessing pipeline.
  3) Train/tune all model candidates; select best by R².
  4) Save preprocessor + best model artifacts.

## Serving Layer (Flask)
- Routes:
  - `/` → landing page with project overview.
  - `/predictdata` (GET) → form.
  - `/predictdata` (POST) → validates inputs, runs through preprocessor + model, returns predicted math score.
- Inputs are not persisted; predictions are computed in-memory.

## Configuration
- `config.yaml`: paths (data/model/preprocessor), train/test split, target column, Flask host/port/debug, logging format/level/dir.

## Logging & Artifacts
- Logs: `logs/` with timestamped files.
- Artifacts: `artifacts/` stores `model.pkl`, `preprocessor.pkl`, `train.csv`, `test.csv`, `data.csv`.

## How to Run (Local)
1) Python 3.8+; create/activate venv.
2) `pip install -r requirements.txt` 
3) Train: `python -m src.pipeline.train_pipeline`
4) Serve: `python app.py` → open `http://localhost:5000`

## Repository Structure
```
app.py                  # Flask app (form-based inference)
config.yaml             # Central config
requirements.txt        # Dependencies (pin versions)
src/
  components/           # data_ingestion, data_transformation, model_trainer
  pipeline/             # train_pipeline, predict_pipeline
  utils.py              # save/load objects, evaluate_models
  logger.py, exception.py, config.py
templates/              # index.html, home.html
artifacts/              # model + preprocessor + data splits (generated)
notebook/               # EDA/training notebooks
logs/                   # runtime logs
```


