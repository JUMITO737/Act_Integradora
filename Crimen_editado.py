import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import base64
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly as px
import plotly.figure_factory as ff
from bokeh.plotting import figure

df = pd.read_csv('DF_POLICE.csv')

#######Configuración de Page
st.set_page_config(
    page_title="POLICIA",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

def logo_to_base64(image):
    import base64
    from io import BytesIO
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

######Cargar logo y encabezado de tablero################
logo_path = "rb.jpg"
logo = Image.open(r"logo_poli.png")
title = "Police incident reports from 2018 to 2020 in San Francisco"
st.markdown(
    """
    <div style="display: flex; align-items: center; background-color: #0080FF; padding: 1rem; border-radius: 8px;">
        <img src="data:image/png;base64,{}" alt="Logo" style="width: 70px; height: 70px; margin-right: 40px;">
        <h1 style="color: white;"> {}</h1>
    </div>
    """.format(logo_to_base64(logo), title),
    unsafe_allow_html=True,
)

##########Creación de menú###########################

selected = option_menu(
     menu_title=None,
     options=["Inicio", "Mapa", "Grafico"],
     icons=[],
     default_index=0,
     orientation="horizontal")

############Pestañas###########
if selected == "Grafico":
    mapa = pd.DataFrame()
    mapa['Date'] = df['Incident Date']
    mapa['Day'] = df['Incident Day of Week']
    mapa['District'] = df['Police District']
    mapa['Neighbourhood'] = df['Analysis Neighborhood']
    mapa['Incident Category'] = df['Incident Category']
    mapa['Incident Subcategory'] = df['Incident Subcategory']
    mapa['Resolution'] = df['Resolution']
    mapa['lat'] = df['Latitude']
    mapa['lon'] = df['Longitude']
    mapa = mapa.dropna()

    subset_data2 = mapa
    police_district_input = st.sidebar.multiselect('Police District',
                                            mapa.groupby('District').count().reset_index()['District'].tolist())
    if len(police_district_input) > 0:
        subset_data2 = mapa[mapa['District'].isin(police_district_input)]

    subset_data1 = subset_data2
    neighbourhood_input = st.sidebar.multiselect('Neighbourhood',
                                            subset_data2.groupby('Neighbourhood').count().reset_index()['Neighbourhood'].tolist())
    if len(neighbourhood_input) > 0:
        subset_data1 = subset_data2[subset_data2['Neighbourhood'].isin(neighbourhood_input)]

    subset_data = subset_data1
    incident_input = st.sidebar.multiselect('Incident Category',
                                            subset_data1.groupby('Incident Category').count().reset_index()['Incident Category'].tolist())
    if len(incident_input) > 0:
        subset_data = subset_data1[subset_data1['Incident Category'].isin(incident_input)]
    subset_data0=subset_data

    resolution_input=st.sidebar.multiselect(
        'Resolution of crime ',
        mapa.groupby('Resolution').count().reset_index()['Resolution'].tolist())
    if len(resolution_input)>0:
        subset_data0 = mapa[mapa['Resolution'].isin(resolution_input)]
    #subset_data
    #st.map(subset_data)
    st.markdown('Crimes ocurred per day of the week')
    st.bar_chart(subset_data['Day'].value_counts())
    st.markdown('Crimes ocurred per date')
    st.bar_chart(subset_data['Date'].value_counts())
    st.markdown('Types of crimes committed')
    st.bar_chart(subset_data['Incident Category'].value_counts())

    agree = st.button('Click to see incident subcategories')
    if agree:
        st.markdown('Subtype of crimes committed')
        st.bar_chart(subset_data['Incident Subcategory'].value_counts())

    st.markdown('Resolution status')
    fig1, ax1 = plt.subplots()
    labels = subset_data['Resolution'].unique()
    ax1.pie(subset_data['Resolution'].value_counts(), labels=labels, autopct='%1.1f%%', startangle=90)
    st.pyplot(fig1)

#--------------------------------------
    st.markdown('Distribución de crímenes por día de la semana')
    st.bar_chart(subset_data['Day'].value_counts())

    st.markdown('Distribución de crímenes por categoría de incidente')
    st.bar_chart(subset_data['Incident Category'].value_counts())

    st.markdown('Distribución de resoluciones de crímenes')
    st.bar_chart(subset_data['Resolution'].value_counts())

    st.markdown('Proporción de crímenes por categoría de incidente')
    fig_pie, ax_pie = plt.subplots()
    labels_pie = subset_data['Incident Category'].unique()
    ax_pie.pie(subset_data['Incident Category'].value_counts(), labels=labels_pie, autopct='%1.1f%%', startangle=90)
    st.pyplot(fig_pie)
#-------------------------------------------------------------------------------------Mapa-------------------------------------------------------------
elif selected == "Mapa":
    mapa = pd.DataFrame()
    mapa['Date'] = df['Incident Date']
    mapa['Day'] = df['Incident Day of Week']
    mapa['District'] = df['Police District']
    mapa['Neighbourhood'] = df['Analysis Neighborhood']
    mapa['Incident Category'] = df['Incident Category']
    mapa['Incident Subcategory'] = df['Incident Subcategory']
    mapa['Resolution'] = df['Resolution']
    mapa['lat'] = df['Latitude']
    mapa['lon'] = df['Longitude']
    mapa = mapa.dropna()

    subset_data2 = mapa
    police_district_input = st.sidebar.multiselect('Police District',
                                            mapa.groupby('District').count().reset_index()['District'].tolist())
    if len(police_district_input) > 0:
        subset_data2 = mapa[mapa['District'].isin(police_district_input)]

    subset_data1 = subset_data2
    neighbourhood_input = st.sidebar.multiselect('Neighbourhood',
                                            subset_data2.groupby('Neighbourhood').count().reset_index()['Neighbourhood'].tolist())
    if len(neighbourhood_input) > 0:
        subset_data1 = subset_data2[subset_data2['Neighbourhood'].isin(neighbourhood_input)]

    subset_data = subset_data1
    incident_input = st.sidebar.multiselect('Incident Category',
                                            subset_data1.groupby('Incident Category').count().reset_index()['Incident Category'].tolist())
    if len(incident_input) > 0:
        subset_data = subset_data1[subset_data1['Incident Category'].isin(incident_input)]

    #subset_data
    st.map(subset_data)

    # Lógica para la pestaña de ventas
    # ...
#-------------------------------------------------------------------------------------Inicio-------------------------------------------------------------
elif selected == "Inicio":
    st.title('The data shown below belongs to incident reports in the City of San Francisco, from the year 2018 to 2020, woth details from each case such as date, day of the week, police district, neighbourhood in which it happened, type of incident in category and subcategory, exact location and resolution')
    mapa = pd.DataFrame()
    mapa['Date'] = df['Incident Date']
    mapa['Day'] = df['Incident Day of Week']
    mapa['District'] = df['Police District']
    mapa['Neighbourhood'] = df['Analysis Neighborhood']
    mapa['Incident Category'] = df['Incident Category']
    mapa['Incident Subcategory'] = df['Incident Subcategory']
    mapa['Resolution'] = df['Resolution']
    mapa['lat'] = df['Latitude']
    mapa['lon'] = df['Longitude']
    mapa = mapa.dropna()

    subset_data2 = mapa
    police_district_input = st.sidebar.multiselect('Police District',
                                            mapa.groupby('District').count().reset_index()['District'].tolist())
    if len(police_district_input) > 0:
        subset_data2 = mapa[mapa['District'].isin(police_district_input)]

    subset_data1 = subset_data2
    neighbourhood_input = st.sidebar.multiselect('Neighbourhood',
                                            subset_data2.groupby('Neighbourhood').count().reset_index()['Neighbourhood'].tolist())
    if len(neighbourhood_input) > 0:
        subset_data1 = subset_data2[subset_data2['Neighbourhood'].isin(neighbourhood_input)]

    subset_data = subset_data1
    incident_input = st.sidebar.multiselect('Incident Category',
                                            subset_data1.groupby('Incident Category').count().reset_index()['Incident Category'].tolist())
    if len(incident_input) > 0:
        subset_data = subset_data1[subset_data1['Incident Category'].isin(incident_input)]

    subset_data


    # Lógica para la pestaña de inicio
    # ...