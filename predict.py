"""Inference using the unchanged Module 8 Trial 4 weights."""
from pathlib import Path
import json
import os
os.environ.setdefault('TF_CPP_MIN_LOG_LEVEL', '2')
import joblib
import numpy as np
import pandas as pd
import tensorflow as tf

ROOT = Path(__file__).resolve().parent
META = json.loads((ROOT / 'artifacts/metadata.json').read_text())
FEATURES = META['features']
PREPROCESSOR = joblib.load(ROOT / 'artifacts/preprocessor.joblib')
MODEL = tf.keras.models.load_model(ROOT / 'artifacts/model.keras', compile=False)

def predict_record(record):
    if set(record) != set(FEATURES):
        raise ValueError('Provide exactly the 23 required features.')
    row = pd.DataFrame([record], columns=FEATURES).astype(float)
    if not np.isfinite(row.to_numpy()).all():
        raise ValueError('All inputs must be finite numbers.')
    allowed = {'SEX': {1, 2}, 'EDUCATION': set(range(7)),
               'MARRIAGE': set(range(4))}
    allowed.update({c: set(range(-2, 9)) for c in FEATURES if c.startswith('PAY_') and not c.startswith('PAY_AMT')})
    for column, codes in allowed.items():
        if row.at[0, column] not in codes:
            raise ValueError(f'Invalid category code for {column}.')
    if row.at[0, 'AGE'] < 18 or row.at[0, 'AGE'] > 120 or row.at[0, 'AGE'] % 1:
        raise ValueError('Age must be a whole number from 18 to 120.')
    if row.at[0, 'LIMIT_BAL'] <= 0 or (row.filter(regex='^PAY_AMT') < 0).any().any():
        raise ValueError('Credit limit must be positive and payment amounts nonnegative.')
    row['EDUCATION'] = row['EDUCATION'].replace({5: 0, 6: 0})
    values = PREPROCESSOR.transform(row)
    if hasattr(values, 'toarray'):
        values = values.toarray()
    probability = float(MODEL(np.asarray(values, dtype=np.float32), training=False).numpy()[0, 0])
    return {'default_probability': probability,
            'prediction': int(probability >= META['threshold']),
            'threshold': META['threshold']}
