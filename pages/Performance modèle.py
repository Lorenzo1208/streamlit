from Home import load_data
import streamlit as st
import pandas as pd
from joblib import load
from sklearn.inspection import partial_dependence
import datetime
import plotly.express as px
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error

model = load('model_rf_2011.joblib')

df = load_data()
df['dteday'] = pd.to_datetime(df['dteday'])
df_predict = df[df['dteday'].dt.year == 2012].copy()

df_predict['prediction'] = model.predict(df_predict[model.feature_names_in_])

df_predict['absolute']= np.abs(df_predict['prediction'] - df_predict['cnt'])

fig = px.scatter(df_predict, x='cnt', y='prediction', trendline='ols', color='absolute')
st.plotly_chart(fig)

col1, col2, col3 = st.columns(3)
col1.metric('RMSE', round(mean_squared_error(df_predict['prediction'], df_predict['cnt'], squared=False), 2))

col2.metric('MAE', round(mean_absolute_error(df_predict['prediction'], df_predict['cnt']), 2))

col3.metric('MAPE', round(mean_absolute_percentage_error(df_predict['prediction'], df_predict['cnt']), 2))

df_cnt = df[['dteday','cnt']]
df_cnt['year'] = df_cnt['dteday'].dt.year.astype(str)
df_cnt['date_str'] = df_cnt['dteday'].dt.strftime("%m/%d")

fig = px.scatter(df_cnt, x='date_str', y='cnt', color='year', color_discrete_sequence=['red', 'blue'])
st.plotly_chart(fig)
