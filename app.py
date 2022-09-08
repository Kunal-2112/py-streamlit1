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
st.set_page_config(layout="wide")

# front end elements of the web page

html_temp = """
    <header style="font-size:10px;width=100">
    <div style ="background-color:#00aebd;border-style:solid;">
    <img src="https://renom.in/wp-content/uploads/2022/02/cropped-renom-logo.86b197ce-e1644472068111-1.png" style="float:Right;width:200px;height:50px;border:orange; border-width:5px; border-style:solid;">
    <a href="https://renom.in/" target="blank" > Click here to view Renom Page </a>
    <h1 style ="color:black;text-align:center;">INOX TML Analysis</h1>
    <h2 style ="color:black;text-align:center;"> Renom Energy Services Pvt Ltd </h2>
    <h3 style ="color:black;text-align:center;">Engineering/SCADA</h3>
    </header>
    </div>
    """
st.markdown(html_temp, unsafe_allow_html=True)
st.markdown("The dashboard will help a researcher to get to know \
   more about the given datasets and it's output")
# display the front end aspect
Ideal_data1 = {
   'x': [3,3.1,3.2,3.3,3.4,3.5,3.6,3.7,3.8,3.9,4,4.1,4.2,4.3,4.4,4.5,4.6,4.7,4.8,4.9,5,5.1,5.2,5.3,5.4,5.5,5.6,5.7,5.8,5.9,6,6.1,6.2,6.3,6.4,6.5,6.6,6.7,6.8,6.9,7,7.1,7.2,7.3,7.4,7.5,7.6,7.7,7.8,7.9,8,8.1,8.2,8.3,8.4,8.5,8.6,8.7,8.8,8.9,9,9.1,9.2,9.3,9.4,9.5,9.6,9.7,9.8,9.9,10,10.1,10.2,10.3,10.4,10.5,10.6,10.7,10.8,10.9,11,11.1,11.2,11.3,11.4,11.5,11.6,11.7,11.8,11.9,12,12.1,12.2,12.3,12.4,12.5,12.6,12.7,12.8,12.9,13,13.1,13.2,13.3,13.4,13.5,13.6,13.7,13.8,13.9,14,14.1,14.2,14.3,14.4,14.5,14.6,14.7,14.8,14.9,15,15.1,15.2,15.3,15.4,15.5,15.6,15.7,15.8,15.9,16,16.1,16.2,16.3,16.4,16.5,17,17.5,18,18.5,19,19.5,20],
    'y': [-7.09,-1.45,4.19,9.83,15.47,21.11,28.004,34.898,41.792,48.686,55.58,67.438,79.296,91.154,103.012,114.87,128.55,142.23,155.91,169.59,183.27,191.914,200.558,209.202,217.846,226.49,243.486,260.482,277.478,294.474,311.47,333.736,356.002,378.268,400.534,422.8,447.654,472.508,497.362,522.216,547.07,570.836,594.602,618.368,642.134,665.9,699.404,732.908,766.412,799.916,833.42,865.564,897.708,929.852,961.996,994.14,1031.954,1069.768,1107.582,1145.396,1183.21,1220.566,1257.922,1295.278,1332.634,1369.99,1419.218,1468.446,1517.674,1566.902,1616.13,1649.25,1682.37,1715.49,1748.61,1781.73,1804.518,1827.306,1850.094,1872.882,1895.67,1907.264,1918.858,1930.452,1942.046,1953.64,1961.228,1968.816,1976.404,1983.992,1991.58,1993.522,1995.464,1997.406,1999.348,2001.29,2006.798,2012.306,2017.814,2023.322,2028.83,2029.432,2030.034,2030.636,2031.238,2031.84,2031.922,2032.004,2032.086,2032.168,2032.25,2033.2,2034.15,2035.1,2036.05,2037,2037.124,2037.248,2037.372,2037.496,2037.62,2038.294,2038.968,2039.642,2040.316,2040.99,2038.544,2036.098,2033.652,2031.206,2028.76,2030.294,2031.828,2033.362,2034.896,2036.43,2036,2036,2036,2036,2036,2036,2036]}



uploaded_file = st.sidebar.file_uploader("Upload TML files", type=['xlsx'])
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    #Renaming Columns names
    def renaming_fun(x):
        if "C11_CON/.Glo.Con.LscIgbTemMax - AVE [C]" in x or "Line-side IGBT max.temp. - AVE [C]" in x or"LSC IGBT temp. - AVE [C]" in x:
            return "LSC IGBT Temp[AVE]"
        elif "C11_CON/.Glo.Con.GscIgbTemMax - AVE [C]" in x or "Gen-side IGBT max.temp. - AVE [C]" in x or"GSC IGBT temp. - AVE [C]" in x:
            return "GSC IGBT Temp[AVE]"
        elif "Energy production 10min - SUM [kWh]" in x or "@Cnt10mProPow - SUM [kWh]" in x or "Energy production 10min - SUM [kWh]"in x:
            return "Total Day Power Production[kWh]"
        elif "C11/.Glo.Gri.PowAct - AVE [kW]" in x or "Active power - AVE [kW]" in x or "C11_5/.Glo.Gri.PowActNet - AVE [kW]"in x :
            return "Active power - AVE [kW]"

        return x

    # Data Cleaning : 1.unwanted column source name deleted
    df1 = df.drop(["Source name"], axis=1)
    # Tanspose the excel file
    df2 = df1.transpose()
    df_new = df2.iloc[0]
    df2 = df2.iloc[1:]
    df2.columns = df_new
    df300 = df2.drop(["Log time (UTC)"], axis=1)
    df3 = df300.rename(columns=renaming_fun)
    df15=df3["Log time (Local)"].iloc[:1]
    df16=df15[0]
    st.write("You are viewing data of date-:",df16)
    df17 = (df3["Wind speed - AVE [m/s]"].mean())
    df30=(df17.round(2))
    st.write("Day Average Wind Speed [m/s]-:", df30)


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
        st.plotly_chart(fig, use_container_width=True, Width=00)

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
            ['GSC IGBT Temp[AVE]', 'LSC IGBT Temp[AVE]', 'Cooling plate temp. - MAX [C]','Converter cab. 1 temp. - MAX [C]',
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

        #fig = px.bar(df8, x='Wind speed - AVE [m/s]', y='Active power - AVE [kW]', title="Production (kw)")
        fig=df8.plot(x="Wind speed - AVE [m/s]", y="Active power - AVE [kW]", kind="bar", figsize=(30, 6))
        #st.plotly_chart(fig)
        st.pyplot()

        fig = px.line(df8, x=df8.index, y=df8.columns[0:2])
        fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='Grey')
        fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='Grey')
        fig.update_traces()
        st.plotly_chart(fig, use_container_width=True)



    if chart_visual == 'Power Curve':

        #df17=df3["Wind speed - AVE [m/s]"].mean()
        #st.write("Day Average Wind Speed-:", df17)
        df18 = df3["Total Day Power Production[kWh]"].sum()
        df32=(round(df18,2));
        st.write("Total Day Production [KWh]-:",df32,size=20)

        plt.figure(figsize=(15,8))
        plt.plot(df3['Wind speed - AVE [m/s]'], df3['Active power - AVE [kW]'], 'o',label='Real Power')
        plt.plot(Ideal_data1['x'], Ideal_data1['y'], '-', label='Ideal Power Curve (kwh)',lw=4)
        plt.xlabel('wind speed (m/s)', size=10)
        plt.ylabel('Power Production (kw)', size=10)
        plt.title('--- Wind Turbine Power Production ---', size=15)
        plt.legend(fontsize=15)
        plt.xticks([0,2,4,6,8,10,12,14,16,18,20],size=12)
        plt.yticks([0,200,400,600,800,1000,1200,1400,1600,1800,2000,2200],size=12)
        plt.grid()
        st.pyplot()
        df333=df3[['Wind speed - AVE [m/s]','Active power - AVE [kW]','PLC state - MAX','Converter state - MAX','Yaw state - MAX']]
        st.write(df333)
