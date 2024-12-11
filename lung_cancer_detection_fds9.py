# -*- coding: utf-8 -*-
"""Lung Cancer Detection_FDS9.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1F3GGttdAQr8MIhj1NqdNBHehP0Cy_dPI
"""

!pip install scikit-learn pandas matplotlib mlflow streamlit pyngrok joblib

import pandas as pd

from google.colab import drive
drive.mount('/content/drive')

# Path to the dataset
dataset_path = '/content/drive/MyDrive/lung cancer detection/survey lung cancer.csv'  # Update with the actual path in your Drive

# Load dataset
data = pd.read_csv(dataset_path)
print(data.head())

print(data.info())
print(data.describe())
print(data.isnull().sum())

# Encode 'GENDER' (e.g., Male: 1, Female: 0)
data['GENDER'] = data['GENDER'].map({'M': 1, 'F': 0})

# Encode 'LUNG_CANCER' (e.g., YES: 1, NO: 0)
data['LUNG_CANCER'] = data['LUNG_CANCER'].map({'YES': 1, 'NO': 0})

# Features (all except 'LUNG_CANCER')
X = data.drop(columns=['LUNG_CANCER'])

# Target variable
y = data['LUNG_CANCER']

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Train the model
model = LogisticRegression()
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model

accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")
print(classification_report(y_test, y_pred))

!pip install mlflow

import mlflow
import mlflow.sklearn
mlflow.set_experiment("Lung Cancer Detection with Logistic Regression")
with mlflow.start_run():
  mlflow.log_param("model_type", "Logistic Regression")
  mlflow.log_metric("accuracy", accuracy)
  mlflow.sklearn.log_model(model, "model")
  print("Model logged in MLflow.")

!mlflow ui

from google.colab import output
output.serve_kernel_port_as_window(5000)

import joblib
joblib.dump(model, 'logistic_regression_model.pkl')

import streamlit as st
import numpy as np
import joblib

# Load the trained
model = joblib.load('logistic_regression_model.pkl')
# Streamlit app
st.title("Lung Cancer Detection App")
st.markdown("Predict if the cancer is **Benign (0)** or **Malignant(1)** based on clinical data.")
# Input fields
age = st.number_input("Age")
tumor_size = st.number_input("Tumor Size")
biomarker = st.number_input("Biomarker Level")
# Predict button
if st.button("Predict"):
  input_data = np.array([[age, tumor_size, biomarker]])
  prediction = model.predict(input_data)[0]
  st.write("Prediction: Malignant" if prediction == 1 else "Prediction: Benign")