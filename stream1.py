import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv('PIFinal.csv')

#Función que obtiene el porcentaje de personas que fueron asignadas a su primera opción de selección
def PorcentajePrimOpcion(df):
    PO = df.apply(lambda df: int(df['OpAsig']) == 1, axis=1).sum() #Suma de personas que quedaron en su primera opción
    OO = df.apply(lambda df: int(df['OpAsig']) != 1, axis=1).sum() #Suma de personas que quedaron en otra de sus opciones 
    Porcentaje = PO/len(df['OpAsig'])*100
    return(Porcentaje)

#Función que obtiene el porcentaje de personas que estaban en programa de intercambio y el de personas en Study Abroad
def PorcentajeInt(df):
    global PorcentajeInter
    global PorcentajeStAb
    PO = df.apply(lambda df: str(df['IntVsSa']) == 'Intercambio', axis=1).sum() #Suma de personas en Intercambio
    OO = df.apply(lambda df: str(df['IntVsSa']) == 'StudyAbroad', axis=1).sum() #Suma de personas en StudyAbroad 
    PorcentajeInter = PO/len(df['OpAsig'])*100
    PorcentajeStAb = OO/len(df['OpAsig'])*100
    return(PorcentajeStAb)


st.set_page_config(layout="wide")



PO = PorcentajePrimOpcion(df)
PI = PorcentajeInt(df)

with st.container():
    cpad1, col, cpad2 = st.columns((6, 30, 2))
    with col:
        st.title('🏫 Dashboard de programas internacionales 🏫')

with st.container():

    fig_col1, fig_col2 = st.columns(2)

    with fig_col1:
        st.subheader("   Porcentaje de personas en su primera opción")
        
        fig3 = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = PO,
        gauge = {
        'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#660000"},
        'bar': {'color': "#990000"},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "gray",
        'steps': [
            {'range': [0, 250], 'color': '#660000'}],
        'threshold': {
            'line': {'color': "red", 'width': 4},
            'thickness': 0.75,
            'value': PO}}))

        fig3.update_layout(width = 600)
        st.plotly_chart(fig3)

    
    with fig_col2:
        st.subheader("   Porcentaje de personas en intercambio")
        fig4 = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = PI,
        gauge = {
        'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#660000"},
        'bar': {'color': "#990000"},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "gray",
        'steps': [
            {'range': [0, 250], 'color': '#660000'}],
        'threshold': {
            'line': {'color': "red", 'width': 4},
            'thickness': 0.75,
            'value': PI}}
    ))
        fig4.update_layout(width = 600)
        st.plotly_chart(fig4)



cpad1, col, pad2 = st.columns((7,10,10))
with col:
    #Gráfico x, gráfico de alluvial
    st.subheader('Escuela vs Opción Asignada vs Continente')
    fig = px.parallel_categories(df, dimensions=['Escuela','OpAsig','Continente'], color="OpAsig", color_continuous_scale=px.colors.diverging.RdBu, 
    labels={'Escuela':'Escuela', 'OpAsig':'Opción Asignada', 'Continente':'Continente final'})
    st.plotly_chart(fig)


cpad1, col, pad2 = st.columns((7,10,10))
with col:
    #Gráfico x, gráfico pie chart de porcentaje de intercambio vs study abroad por nivel
    st.subheader('Porcentaje de intercambio vs study abroad por nivel')
    nivel = df['Nivel'].unique()
    nivelbar = st.selectbox('Seleccionar un nivel', nivel)
    values = list(df['IntVsSa'].where(df['Nivel'] == nivelbar).value_counts())
    fig1 = px.pie(df, values= values, names= df['IntVsSa'].unique(), color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig1)



