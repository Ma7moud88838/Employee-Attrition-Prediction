
import streamlit as st
import numpy as np
import joblib

@st.cache_resource
def Load_Models():
    Model = joblib.load('attrition_model.pkl')
    Scaler = joblib.load('scaler.pkl')
    Label_encoders = joblib.load('label_encoders.pkl')
    Feature_names = joblib.load('feature_names.pkl')
    return Model, Scaler, Label_encoders, Feature_names

model, scaler, label_encoders, feature_names = Load_Models()

st.title("Employee Attrition Prediction")

# Create inputs for each feature
user_input = {}
for feature in feature_names:
    if feature in label_encoders:
        options = list(label_encoders[feature].classes_)
        user_input[feature] = st.selectbox(f"{feature}", options)
    else:
        user_input[feature] = st.text_input(f"{feature}")

if st.button("Predict"):
    # Preprocess the input data
    input_data = []
    for feature in feature_names:
        if feature in label_encoders:
            input_data.append(label_encoders[feature].transform([user_input[feature]])[0])
        else:
            input_data.append(float(user_input[feature]))

    input_data = np.array(input_data).reshape(1, -1)
    input_data = scaler.transform(input_data)

    # Make the prediction
    prediction = model.predict(input_data)

    st.write(f"Employer {'Stayed' if prediction[0] == 1 else 'left'}")
