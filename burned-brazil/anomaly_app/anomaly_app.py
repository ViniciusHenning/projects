import pandas as pd
from statsmodels.tsa.seasonal import STL
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
from ts import AnomalyDetection
import download_link

sns.set_theme(style="darkgrid")

st.write(
"""
# Web application for anomaly detection
This app show few relevant features concerning the anomaly in timeseries,
it also corrects the anomaly(ies) as described [here].
"""
)

st.sidebar.header("Choose a dataset")
file = st.sidebar.file_uploader(label = 'Upload your file here')

freq_names = ['Daily', 'Weekly', 'Monthly']
freq_dict = {'Daily' : 365, 'Weekly' : 52, 'Monthly' : 12}
st.sidebar.header('Choose the Frequency of your data')
freq = st.sidebar.selectbox('Options', freq_names)

frequency = freq_dict[freq]

if file is not None:
    try:
        df = pd.read_csv(file, parse_dates = True)
    except:
        df = pd.read_excel(file, parse_dates = True)

if file is not None:
	st.sidebar.header('Choose the datetime column')
	date_column = st.sidebar.radio('Columns', list(df.columns))

	df = df.set_index(date_column)
	df.index = pd.to_datetime(df.index)


st.write('## Choose the options that you want to check regarding the anomalies')

option_plot = st.selectbox('Please select one of the options below',
                           ['Seasonal, Trend and residuals decomposition',
                           'The timeseries after removing the residuals',
                           'Residual analysis',
                           'Anomaly points in the timeseries',
                           'The corrected timeseries after the handling the anomalies'])
options_0 = ['Seasonal, Trend and residuals decomposition',
           'The timeseries after removing the residuals']

if option_plot not in options_0:
	n_sigma = st.slider('Choose the number of standard deviations to be used', min_value = 1., max_value = 3.5, step = 0.5, value = 3.)

corrected_dataframe = None

if file is not None:
    try:
        ad = AnomalyDetection(df, frequency)
        corrected_dataframe = ad.corrected_timeseries(n_sigma)

        if option_plot == 'Seasonal, Trend and residuals decomposition':
            st.pyplot(ad.decomposition())
        elif option_plot == 'The timeseries after removing the residuals':
            st.pyplot(ad.seasonal_trend())
        elif option_plot == 'Residual analysis':
            st.pyplot(ad.residuals_analysis(n_sigma))
        elif option_plot == 'Anomaly points in the timeseries':
            st.pyplot(ad.anomaly_points_timeseries(n_sigma))
        else:
            st.pyplot(ad.corrected_timeseries_plot(n_sigma))
    except Exception as e:
        print(e)

if corrected_dataframe is not None:
    st.write('# If you wish to downaload the corrected dataset click the button below')

    tmp_download_link = download_link.download_button(corrected_dataframe, 'corrected_dataframe.csv', 'Click here to download it')
    st.markdown(tmp_download_link, unsafe_allow_html=True)
