import pandas as pd
import streamlit as st
from statsmodels.tsa.seasonal import STL
import seaborn as sns
import matplotlib.pyplot as plt
from ts import AnomalyDetection
import download_link

sns.set_theme(style="darkgrid")

st.markdown(
"""
# Web application for anomaly detection
This app show few relevant features concerning the anomaly in timeseries,
it also corrects the anomaly(ies) as described [here](https://github.com/ViniciusHenning/projects/blob/master/burned-brazil/tidied-up-pm.ipynb)
""")


st.sidebar.header("Choose a dataset")
file = st.sidebar.file_uploader(label = 'Upload your file here')

freq_names = ['Daily', 'Semimonthly', 'Monthly']
#freq_dict = {'Daily' : 365, 'Weekly' : 52, 'Monthly' : 12}
freq_dict = {'Daily' : 365, 'Semimonthly' : 24, 'Monthly' : 12}
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


if file is not None:
    st.write('## Choose the options that you want to check regarding the anomalies')


    options_list =  ['Seasonal, Trend and Residuals decomposition',
                     'The timeseries after removing the residuals',
                     'Residual analysis',
                     'Anomaly points in the timeseries',
                     'The corrected timeseries after the handling the anomalies']

    option_plot = st.selectbox('Please select one of the options below', options_list)

    corrected_dataframe = None

    ad = AnomalyDetection(df, frequency)

    if option_plot != options_list[0] and option_plot != options_list[1]:
        n_sigma = st.slider('Choose how many standard deviation should be used in the analysis', min_value  = 1.0, max_value = 3.5, step = 0.5)

    if option_plot == 'Seasonal, Trend and Residuals decomposition':
        st.pyplot(ad.decomposition())
    elif option_plot == 'The timeseries after removing the residuals':
        st.pyplot(ad.seasonal_trend())
    elif option_plot == 'Residual analysis':
        st.pyplot(ad.residuals_analysis(n_sigma))
    elif option_plot == 'Anomaly points in the timeseries':
        st.pyplot(ad.anomaly_points_timeseries(n_sigma))
    else:
        st.pyplot(ad.corrected_timeseries_plot(n_sigma))


if file is not None:
    st.write('### If you wish to download the dataset where the anomalies are corrected, click the button below!')
    n_sigma = st.slider('Choose how many standard deviation should be used to correct the timeseries', min_value  = 1.0, max_value = 3.5, step = 0.5)
    corrected_timeseries = ad.corrected_timeseries(n_sigma)
    tmp_download_link = download_link.download_button(corrected_timeseries, 'corrected_dataframe.csv', 'Click here to download it')
    st.markdown(tmp_download_link, unsafe_allow_html=True)
