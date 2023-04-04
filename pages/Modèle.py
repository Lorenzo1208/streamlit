from Home import load_data
import streamlit as st
import pandas as pd
from joblib import load
from sklearn.inspection import partial_dependence
import datetime
import plotly.express as px

df = load_data()

df['dteday'] = pd.to_datetime(df['dteday'])
df_filter = df[df['dteday'] <= pd.Timestamp(datetime.date(2011, 12, 31))]
# print(df_filter.dtypes)
# st.dataframe(df_filter)

temp_range = st.sidebar.slider('Températures', min(df['temp']), max(df['temp']), [min(df['temp']), max(df['temp'])])
humidity_range = st.sidebar.slider('Humidité', min(df['hum']), max(df['hum']), [min(df['hum']), max(df['hum'])])
day_of_week = st.sidebar.multiselect('Jour de la semaine', df['weekday'].unique(), default=df['weekday'].unique())

df_filter = df.loc[    (df['temp'].between(temp_range[0], temp_range[1])) &
    (df['hum'].between(humidity_range[0], humidity_range[1])) &
    (df['weekday'].isin(day_of_week)) &
    (df['dteday'].dt.year == 2011)
]

model = load('model_rf_2011.joblib')

df_filter = df_filter[model.feature_names_in_]

features = pd.DataFrame({'feature':model.feature_names_in_,'importance':model.feature_importances_})
st.dataframe(features)

var = st.selectbox('Sélectionnez la variable :', model.feature_names_in_ )

values = partial_dependence(model, df_filter,var, kind='average')

values_df = pd.DataFrame({var:values['values'][0],
                        'average_prediction': values['average'][0]})

fig = px.line(values_df, x=var, y='average_prediction')
st.plotly_chart(fig)
