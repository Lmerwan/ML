import streamlit as st
import datetime
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

# Set up your web app with a wider layout and title
st.set_page_config(layout="wide", page_title="Stock Data Explorer")

# Sidebar with title and input fields
st.sidebar.title("📊 Stock Information")
symbol = st.sidebar.text_input('Enter Stock Symbol:', 'AAPL').upper()

st.sidebar.markdown("---")  # Horizontal line for separation

st.sidebar.subheader("Select Date Range")
col1, col2 = st.sidebar.columns(2)
with col1:
    sdate = st.date_input('Start Date', value=datetime.date(2023, 1, 1))
with col2:
    edate = st.date_input('End Date', value=datetime.date.today())

# Main content area with title and stock data
st.title(f"📈 Stock Data for {symbol}")

# Fetch stock data
stock = yf.Ticker(symbol)

# Download historical data with a loading spinner
with st.spinner("Loading stock data..."):
    data = yf.download(symbol, start=sdate, end=edate)

# Debugging: Check columns and convert Date column if necessary
st.write("Data Columns:", data.columns)  # Display column names to verify structure

# Ensure data is not empty
if not data.empty:
    # Reset index to convert Date to a regular column and explicitly ensure it's datetime
    data = data.reset_index()
    if 'Date' in data.columns:
        data['Date'] = pd.to_datetime(data['Date'])  # Ensure Date is in datetime format

    # Check for any NaN values in the Close column and drop them if found
    if data['Close'].isnull().any():
        st.warning("Missing values found in 'Close' column. Dropping these rows.")
        data = data.dropna(subset=['Close'])

    # Create and display interactive line chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], mode='lines', name='Close Price'))
    fig.update_layout(
        title=f'{symbol} Closing Prices',
        xaxis_title='Date',
        yaxis_title='Close Price',
        template='plotly_white',
        xaxis=dict(showgrid=True, gridcolor='LightGrey'),
        yaxis=dict(showgrid=True, gridcolor='LightGrey'),
        plot_bgcolor='rgba(255, 255, 255, 1)',
        paper_bgcolor='rgba(240, 242, 246, 1)',
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.error("No historical data found for the given symbol and date range.")

# Footer with additional resources or credits
st.markdown("---")  # Horizontal separator
st.markdown(
    "<footer style='text-align: center; font-size: small; color: #6c757d;'>"
    "Stock data provided by Yahoo Finance | App designed by [Your Name]</footer>",
    unsafe_allow_html=True,
)
