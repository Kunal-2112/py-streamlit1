import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import warnings

import html

st.set_option('deprecation.showPyplotGlobalUse', False)
warnings.filterwarnings("ignore")

# front end elements of the web page

html_temp = """
    <header style="font-size:10px;width=100">
    <div style ="background-color:#00aebd;border-style:solid;">
    <img src="https://renom.in/wp-content/uploads/2022/02/cropped-renom-logo.86b197ce-e1644472068111-1.png" style="float:Right;width:200px;height:50px;border:orange; border-width:5px; border-style:solid;">
    <h1 style ="color:black;text-align:center;">INOX TML Analysis</h1>
    <h2 style ="color:black;text-align:center;">O&M-Engineering </h2>
    <h3 style ="color:black;text-align:center;">Renom Energy Services Pvt Ltd </h3>
    <h6 style ="color:black;text-align:center;"> Preapred By-Kunal lite/Suraj Shinde</h6></header>
    </div>

    """
st.markdown(html_temp, unsafe_allow_html=True)
st.markdown("The dashboard will help a researcher to get to know \
   more about the given datasets and it's output")
# display the front end aspect
Ideal_data1 = {
    'x': [0,1,2,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10,10.5,11,11.5,12,12.5,13,13.5,14,14.5,15,15.5,16,16.5,17,17.5,18,18.5,19,19.5,20],
    'y': [0,0,0,1,34,77,141,209,272,373,496,631,776,954,1137,1340,1509,1723,1853,1935,1978,2004,2017,2031,2033,2035,2037,2037,2037,2033,2036,2036,2036,2036,2036,2036,2036,2036]}



uploaded_file = st.sidebar.file_uploader("Upload TML files", type=['xlsx'])
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    # Data Cleaning : 1.unwanted column source name deleted
    df1 = df.drop(["Source name"], axis=1)
    # Tanspose the excel file
    df2 = df1.transpose()
    df_new = df2.iloc[0]
    df2 = df2.iloc[1:]
    df2.columns = df_new
    df3 = df2.drop(["Log time (UTC)"], axis=1)
    df15=df3["Log time (Local)"].iloc[:1]
    df16=df15[0]
    st.write("You are viewing data of date-:",df16)
    df17 = df3["Wind speed - AVE [m/s]"].mean()
    st.write("Day Average Wind Speed-:", df17)


    st.sidebar.title("Select Visual Charts")
    st.sidebar.markdown("Select the Charts/Plots accordingly:")
    chart_visual = st.sidebar.selectbox('Select Charts/Plot type',
                                        ('GearBox Temperature', "Converter Temperature", "Generator Temperature",
                                         "Voltage", 'Blade KPI', "Power Chart", "Power Curve"))

    if chart_visual == 'Blade KPI':
        fig = go.Figure()
        # Voltage graph
        df21 = df3[['Angle blade 1 - AVE [°]', 'Angle blade 2 - AVE [°]', 'Angle blade 3 - AVE [°]',
                   'Wind speed - AVE [m/s]']]
        fig = px.line(df21, x=df21.index, y=df21.columns[0:4], title="Blade Angle")
        fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='Grey')
        fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='Grey')
        st.plotly_chart(fig, use_container_width=True)

        # Blade temp-
        df19 = df3[
            ['Blade 1 converter internal temperature - AVE [C]', 'Blade 2 converter internal temperature - AVE [C]',
             'Blade 3 converter internal temperature - AVE [C]',
             'Motor temp. blade 1 - AVE [C]', 'Motor temp. blade 2 - AVE [C]', 'Motor temp. blade 3 - AVE [C]',
             'Wind speed - AVE [m/s]']]
        fig = px.line(df19, x=df19.index, y=df19.columns[0:7],
                      title="Blade Temperature)")
        fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='Grey')
        fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='Grey')
        st.plotly_chart(fig, use_container_width=True)

    if chart_visual == 'GearBox Temperature':
        fig = go.Figure()

        #Gearbox temp
        df4 = df3[['Gearbox rotor bearing temp. - MAX [C]','Gearbox shaft bearing temp. 1 - MAX [C]',
                   'Gearbox shaft bearing temp. 2 - MAX [C]','Gearbox shaft bearing temp. 3 - MAX [C]',
                   'Wind speed - AVE [m/s]']]

        fig = px.line(df4, x=df4.index, y=df4.columns[0:5],title="GearBox Temperature  (Warning-85,Error-90)")
        fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='Grey')
        fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='Grey')
        fig.update_traces()
        st.plotly_chart(fig,use_container_width=True)

        # Oil temp-
        df20 = df3[
            ['Gearbox oil heater temp. - MAX [C]', 'Gearbox oil inlet temp. - MAX [C]',
             'Gearbox oil tank temp. - MAX [C]', 'Oil inlet pressure - MAX [bar]', 'Wind speed - AVE [m/s]']]
        fig = px.line(df20, x=df20.index, y=df20.columns[0:5],
                      title="Oil Temperature")
        fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='Grey')
        fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='Grey')
        st.plotly_chart(fig, use_container_width=True)

    if chart_visual == 'Generator Temperature':
        fig = go.Figure()
        df5 = df3[['Gen. winding [U] temp. - MAX [C]', 'Gen. winding [V] temp. - MAX [C]',
                   'Gen. winding [W] temp. - MAX [C]','Generator choke temp. - MAX [C]',
                   'Wind speed - AVE [m/s]']]
        fig = px.line(df5, x=df5.index, y=df5.columns[0:5],title="Winding Temperature (Warning-135,Error-140)")
        fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='Grey')
        fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='Grey')
        st.plotly_chart(fig,use_container_width=True)

    if chart_visual == 'Converter Temperature':
        fig = go.Figure()
         #IGBT temperature
        df6 = df3[
            ['Gen-side IGBT max.temp. - MAX [C]', 'Line-side IGBT max.temp. - MAX [C]', 'Cooling plate temp. - MAX [C]','Converter cab. 1 temp. - MAX [C]',
             'Wind speed - AVE [m/s]']]
        fig = px.line(df6, x=df6.index, y=df6.columns[0:5],title="IGBT Temperature   (IGBT-Warning-85,Error-90,Plate-(Warning-55,Error-60))")
        fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='Grey')
        fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='Grey')
        st.plotly_chart(fig, use_container_width=True)

        # cabinet temp-
        df18 = df3[
            ['Environment temp. - MAX [C]', 'Nacelle cab. 1 temp. - MAX [C]', 'Converter cab. 1 temp. - MAX [C]',
             'Temperature inside converter cabinet 2 - MAX [C]', 'Wind speed - AVE [m/s]']]
        fig = px.line(df18, x=df18.index, y=df18.columns[0:5],
                      title="Cabinet Temperature Converter-(Warning-60,Error-65))")
        fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='Grey')
        fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='Grey')
        st.plotly_chart(fig, use_container_width=True)

    if chart_visual == 'Voltage':
        fig = go.Figure()
        #Voltage graph
        df7 = df3[['Voltage phase 1-2 - MAX [V]', 'Voltage phase 2-3 - MAX [V]', 'Voltage phase 3-1 - MAX [V]','Wind speed - AVE [m/s]']]
        fig = px.line(df7, x=df7.index, y=df7.columns[0:5],title="Voltage  (Under voltage-660V)")
        fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='Grey')
        fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='Grey')
        st.plotly_chart(fig, use_container_width=True)

        #Active power vs Wind speed
        df8 = df3[['Active power - AVE [kW]', 'Wind speed - AVE [m/s]','DC-bus voltage - AVE [V]']]
        fig = px.line(df8, x=df8.index, y=df8.columns[0:3],title="Production (kw)")
        df8.plot(x="Wind speed - AVE [m/s]", y="Active power - AVE [kW]", kind="bar", figsize=(30, 6))
        fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='Grey')
        fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='Grey')
        st.plotly_chart(fig, use_container_width=True)

    if chart_visual == 'Power Chart':
        df8 = df3[['Active power - AVE [kW]', 'Wind speed - AVE [m/s]']]
        fig = px.scatter(df8, x=df8.index, y=df8.columns[0:2], title="Production (kw)")
        st.plotly_chart(fig)

    if chart_visual == 'Power Curve':

        #df17=df3["Wind speed - AVE [m/s]"].mean()
        #st.write("Day Average Wind Speed-:", df17)
        df18 = df3["Energy production 10min - SUM [kWh]"].sum()
        st.write("Total Day Production(KWh)-:", df18)

        plt.figure(figsize=(25,15))
        plt.plot(df3['Wind speed - AVE [m/s]'], df3['Active power - AVE [kW]'], 'o', label='Real Power')
        plt.plot(Ideal_data1['x'], Ideal_data1['y'], '-', label='Ideal_power_curve (kwh)',lw=5)
        plt.xlabel('wind speed (m/s)', size=25)
        plt.ylabel('Power Production (kw)', size=25)
        plt.title('--- Wind Turbine Power Production ---', size=30)
        plt.legend(fontsize=25)
        plt.xticks([0,2,4,6,8,10,12,14,16,18,20],size=20)
        plt.yticks([0,200,400,600,800,1000,1200,1400,1600,1800,2000,2200],size=20)
        plt.grid()
        st.pyplot()
        st.write("Welcome to Git....Code is push")




