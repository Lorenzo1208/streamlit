from Home import load_data
import streamlit as st
import pandas as pd
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

st.header("Distribution du nombre de vélos loués en fonction de la température, de l'humidité et de la saison")
fig = px.scatter_3d(df_filter, x="temp", y="hum", z="cnt", color="season", color_discrete_sequence=["#00CCFF", "#33FF99", "#99FF33", "#FFFF00"])
st.plotly_chart(fig)

color_map = {'spring': 'blue', 'summer': 'green', 'fall': 'orange', 'winter': 'red'}
df_filter['color'] = df_filter['season'].map(color_map)
st.header('Distribution du nombre de vélos loués selon le jour de la semaine')
fig = px.parallel_categories(df_filter, color='color')
st.plotly_chart(fig)

st.header('Évolution du nombre de vélos loués en fonction de la date')
fig = px.scatter(df_filter, x="dteday", y="cnt")
st.plotly_chart(fig)

st.header('Distribution du nombre de vélos loués')
fig = px.histogram(df_filter, x="cnt")
st.plotly_chart(fig)

st.header('Distribution du nombre de vélos loués en fonction de la température')
fig = px.scatter(df_filter, x="temp", y="cnt", color='temp',color_continuous_scale='YlOrRd')
st.plotly_chart(fig)

st.header('Distribution du nombre de vélos loués selon le jour de la semaine')
fig = px.histogram(df_filter, x="weekday", y="cnt", color="weekday", nbins=7)
fig.update_layout(xaxis_title="Jour de la semaine", yaxis_title="Nombre de vélos loués")
st.plotly_chart(fig)

st.header('Distribution du nombre de vélos loués selon la vitesse du vent')
fig = px.scatter(df_filter, x="windspeed", y="cnt")
fig.update_layout(xaxis_title="Vitesse du vent", yaxis_title="Nombre de vélos loués", title="Distribution du nombre de vélos loués selon la vitesse du vent")
st.plotly_chart(fig)

st.header('Distribution du nombre de vélos loués selon la saison')
fig = px.box(df_filter, x="season", y="cnt")
st.plotly_chart(fig)