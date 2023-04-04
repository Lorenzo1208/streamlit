import streamlit as st
import pandas as pd
from Home import load_data
import streamlit as st
import pandas as pd
from joblib import load
from sklearn.inspection import partial_dependence
import datetime
import plotly.express as px
# import wandb

# wandb.init()
# wandb.login()

st.title('BikeSharing')
st.write("""Bike sharing systems are new generation of traditional bike rentals where whole process from membership, rental and return back has become automatic. Through these systems, user is able to easily rent a bike from a particular position and return back at another position. Currently, there are about over 500 bike-sharing programs around the world which is composed of over 500 thousands bicycles. Today, there exists great interest in these systems due to their important role in traffic, environmental and health issues.""")

@st.cache_data
def load_data():
    day = pd.read_csv('day_clean.csv')
    day = day.drop('Unnamed: 0', axis=1)
    return day

day = load_data()

# Afficher le DataFrame dans Streamlit
st.dataframe(day)
