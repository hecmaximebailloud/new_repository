# AP_Projet_code.py
import streamlit as st
import pandas as pd
import numpy as np
import os
from scripts.data_processing import preprocess_all_data, calculate_returns, calculate_volatility, fetch_latest_news

custom_css = """
<style>
body {
    background-color: #1e3d59;
    color: #ffffff;
}
.sidebar .sidebar-content {
    background-color: #1e3d59;
}
.stButton>button {
    background-color: #1e3d59;
    color: #ffffff;
}
.stTabs .stTabs__tab {
    background-color: #1e3d59;
    color: #ffffff;
}
.stTabs .stTabs__tab--selected {
    background-color: #1e3d59;
    color: #ffffff;
    border-bottom: 2px solid #ffffff;
}
</style>
"""

# Inject the custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

# Define start and end dates for the weekly data
start_date = pd.to_datetime('2011-01-09')
end_date = pd.to_datetime('2023-12-24')
keep_columns = ['Date', 'Dernier Prix']

# List of all tickers
all_data_ticker = ['AMAZON', 'APPLE', 'google', 'TESLA',
                 'GOLD', 'CL1 COMB Comdty', 'NG1 COMB Comdty', 'CO1 COMB Comdty', 
                 'DowJones', 'Nasdaq', 'S&P', 'Cac40', 'ftse', 'NKY',
                 'EURR002W', 'DEYC2Y10', 'USYC2Y10', 'JPYC2Y10', 'TED SPREAD JPN', 'TED SPREAD US', 'TED SPREAD EUR',
                 'renminbiusd', 'yenusd', 'eurodollar' ,'gbpusd',
                 'active_address_count', 'addr_cnt_bal_sup_10K', 'addr_cnt_bal_sup_100K', 'miner-revenue-native-unit', 'miner-revenue-USD', 'mvrv', 'nvt', 'tx-fees-btc', 'tx-fees-usd']

# Preprocess data
try:
    merged_df = preprocess_all_data(all_data_ticker, start_date, end_date, keep_columns)
except Exception as e:
    st.error(f"Error during preprocessing: {e}")
    st.stop()

# Calculate returns and volatilities
dataset_returns = calculate_returns(merged_df)
dataset_volatility = calculate_volatility(merged_df)

# Streamlit interface
st.set_page_config(page_title='Financial Analysis and Prediction App', layout='wide')

tabs = st.tabs(['Home', 'Prices', 'Returns', 'Volatility', 'Groups Analysis', 'Predictive Models', 'Investment Strategy', 'Correlation', 'Crypto News'])

# Home tab
with tabs[0]:
    st.title('Financial Analysis and Prediction App')
    st.write("""
        Welcome to the Financial Analysis and Prediction App. This application allows you to analyze and predict financial data using various models.
        You can explore different financial metrics, apply predictive models, and devise investment strategies based on predicted and actual prices.
    """)

# Prices tab
with tabs[1]:
    st.header('Price')
    features = merged_df.columns.tolist()
    selected_features = st.multiselect('Select Features', features, key='price_features')
    if selected_features:
        try:
            selected_price = [f"{feature}" for feature in selected_features]
            price = merged_df[selected_price]
            st.line_chart(price)
        except KeyError as e:
            st.error(f"Error selecting price columns: {e}")

# Returns tab
with tabs[2]:
    st.header('Returns')
    selected_features = st.multiselect('Select Features', merged_df.columns.tolist(), key='returns_features')
    if selected_features:
        try:
            selected_returns = [f"{feature}_returns" for feature in selected_features]
            returns = dataset_returns[selected_returns]
            st.line_chart(returns)
        except KeyError as e:
            st.error(f"Error selecting returns columns: {e}")

# Volatility tab
with tabs[3]:
    st.header('Volatility')
    selected_features = st.multiselect('Select Features', merged_df.columns.tolist(), key='volatility_features')
    if selected_features:
        try:
            selected_volatility = [f"{feature}_volatility" for feature in selected_features]
            volatility = dataset_volatility[selected_volatility]
            st.line_chart(volatility)
        except KeyError as e:
            st.error(f"Error selecting volatility columns: {e}")

# Groups tab
with tabs[4]:
  st.header('Groups Analysis')
  group_choice = st.selectbox('Select what you want to see in details', ['Groups Overview', 'Groups Importance', 'Importance Evolution'], key = 'group_choice')
  if group_choice == 'Groups Overview':
    st.header('Features and Groups')

  elif group_choice == 'Groups Importance':
    st.header('Importance of each group in the Random Forest model')
    st.image("Group's Importance.png", caption = 'Importance of each group for the Random Forest predictions', use_column_width = False)

  elif group_choice == 'Importance Evolution':
    st.header('Evolution of the two most important groups')
    st.image('Evolution of groups importance BCM and EI .png', caption = 'Evolution of their importance over time', use_column_width = False)
  



# Predictive Models tab
with tabs[5]:
    st.header('Predictive Models')
    model_choice = st.selectbox('Select Model', ['Random Forest', 'SARIMA', 'LSTM'], key='model_choice')
    if model_choice == 'Random Forest':
        st.subheader('Random Forest model details and predictions.')
        st.write('Here, you can see the comparison of the predicted prices between Bitcoin actual prices, a Random Forest using all features (34) and a Random Forest using the 5 most explicative features (selected with Recursive Features Elimination).')
        st.write('The top features are Google, Tesla, Nasdaq, S&P500, and miner revenue.')
        st.write('You will find below the accuracy comparison between both Random Forest models.')
        st.image('Screen Shot 2024-05-16 at 8.42.15 pm.png', caption='Random Forest Model', use_column_width=True)
        st.image('Accuracy Comparison between RFE and all features .png', caption = 'Accuracy of the predicted prices over time', use_column_width = False)

    elif model_choice == 'SARIMA':
        st.subheader('SARIMA model details and predictions')
        st.image('Consolidated BTC prices comparison.png', caption = 'SARIMA model', use_column_width = False)
    elif model_choice == 'LSTM':
        st.subheader('LSTM model details and predictions')
        st.write('As you can see below, the overall predicted price is quite good, but the forecasted price does not look good. I would advise you not to pay attention to this if you want to invest in Bitcoin...')  
        st.image('Screen Shot 2024-05-18 at 5.35.41 pm.png', caption = 'LSTM model', use_column_width = False)

# Investment Strategy tab
with tabs[6]:
    st.header('Investment Strategy')
    st.subheader('Moving-Average Crossover Strategy')
    st.write('The strategy selected is the Moving-Average Crossover Strategy. This strategy involves taking long and short positions based on the crossover points of short-term and long-term moving averages, we buy when we forecast a price increase (positive signal) and go short when we forecast a decrease (negative signal).')  
    st.write('Here you can choose whether the performance of the strategy, based on my predictions, or the performance with the actual prices.') 
    strategy_choice = st.selectbox('Select Strategy', ['Predicted Bitcoin Prices', 'Actual Bitcoin Prices'], key='strategy_choice')
    if strategy_choice == 'Predicted Bitcoin Prices':
        st.subheader('Investment strategy based on predicted Bitcoin prices using Recursive Features Elimination.')
        st.write(' RFE output was the 5 most explicative features concerning Bitcoin prices. The top features are Google, Tesla, Nasdaq, S&P500, and the miner revenue.')
        st.write('Following the computation of the Moving-Averages, you will find the performance of the portfolio, with a benchmark that is "Long" every period.')
        st.image('MA RFE.png', caption = 'Short and Long-term Moving Averages on predicted and forecasted prices', use_column_width = False)
        st.image('Strat perf RFE.png', caption = 'Performance of the strategy and the benchmark', use_column_width = False)

    elif strategy_choice == 'Actual Bitcoin Prices':
        st.subheader('Investment strategy based on actual Bitcoin prices')
        st.write('Following the computation of the Moving-Averages, you will find the performance of the portfolio, with a benchmark that is "Long" every period.')
        st.image('MA actual prices.png', caption = 'Short and Long-term Moving Averages on actual and forecasted prices', use_column_width = False)
        st.image('Strat perf actual prices.png', caption = 'Performance of the strategy and the benchmark', use_column_width = False)

# Correlation tab
with tabs[7]:
    st.header('Correlation')
    st.write(f'First, you need to choose which features you want to add in the correlation matrix. Then, You can customize the heatmap as you wish (color, size):')  
    features = dataset_returns.columns.tolist()
    selected_features = st.multiselect('Select Features', features, key='correlation_features')
    if selected_features:
        try:
            correlation_matrix = dataset_returns[selected_features].corr()
            st.write("Customize Heatmap")
            cmap_option = st.selectbox('Select Color Map', ['coolwarm', 'viridis', 'plasma', 'inferno', 'magma', 'cividis'])
            annot_option = st.checkbox('Show Annotations', value=True)
            figsize_width = st.slider('Figure Width', min_value=5, max_value=15, value=10)
            figsize_height = st.slider('Figure Height', min_value=5, max_value=15, value=6)
            
            # Display heatmap
            st.write("Correlation Heatmap")
            import seaborn as sns
            import matplotlib.pyplot as plt

            fig, ax = plt.subplots(figsize=(figsize_width, figsize_height))
            sns.heatmap(correlation_matrix, annot=annot_option, cmap=cmap_option, ax=ax)
            st.pyplot(fig)
        except KeyError as e:
            st.error(f"Error selecting features for correlation: {e}")

# Bitcoin News tab
with tabs[8]:
    st.header('Latest Bitcoin and Cryptocurrencies News')
    api_key = 'e2542da4e232487f8a2b6e1702e8db2f'
    news_articles = fetch_latest_news(api_key)
    if news_articles:
        for article in news_articles:
            st.subheader(article['title'])
            st.write(article['summary'])
            st.markdown(f"[Read more]({article['link']})")
    else:
        st.write("Failed to fetch the latest news.")
    
    

    




