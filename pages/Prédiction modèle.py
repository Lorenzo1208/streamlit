from Home import load_data
import streamlit as st
import pandas as pd
from joblib import load
from sklearn.inspection import partial_dependence
import datetime
import plotly.express as px

model = load('model_rf_2011.joblib')

if 'last_pred' not in st.session_state:
    st.session_state['last_pred'] = None

df = load_data()
df['dteday'] = pd.to_datetime(df['dteday'])

temp = st.slider('Valeur de température',  min(df['temp']), max(df['temp']))

hum = st.slider('Valeur d\'humidité', min(df['hum']), max(df['hum']))
wind = st.slider('Valeur de vent', min(df['windspeed']), max(df['windspeed']))

parameters = {}
for f in model.feature_names_in_:
    if f == 'temp':
        parameters[f] = temp
    elif f == 'hum':
        parameters[f] = hum
    elif f == 'windspeed':
        parameters[f] = wind
    else:
        parameters[f] = 0
    
pred_values = pd.DataFrame(parameters, index=[0])

predict = model.predict(pred_values)

if st.session_state['last_pred'] is None:
    delta = None
else :
    delta = predict - st.session_state['last_pred']
    delta = round(float(delta), 2) if delta is not None else None


st.metric('Prédiction', predict, delta=delta)

st.session_state['last_pred'] = predict
