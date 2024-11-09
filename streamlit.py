import streamlit as st
import datetime
import yfinance as yf
import plotly.graph_objects as go

# Set up your web app with a wider layout and title
st.set_page_config(layout="wide", page_title="Stock Data Explorer")

# Custom CSS for styling
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f5f7fa; /* Softer light gray background */
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #ffffff, #e6ebf1); /* Gradient for the sidebar */
        padding: 20px;
        border-radius: 15px;
    }
    .sidebar .sidebar-content h1, h2, h3 {
        color: #005f73; /* Deep teal for sidebar headings */
    }
    .reportview-container .main .block-container {
        padding: 20px;
    }
    h1, h2 {
        color: #333333; /* Consistent dark gray for main headings */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

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

# Display company information with improved formatting
if stock.info:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(f"**🏢 Sector:** {stock.info.get('sector', 'N/A')}")
        st.write(f"**📉 Beta:** {stock.info.get('beta', 'N/A')}")
    with col2:
        st.write(f"**💰 Market Cap:** {stock.info.get('marketCap', 'N/A'):,}")
        st.write(f"**📊 P/E Ratio:** {stock.info.get('forwardPE', 'N/A')}")
    with col3:
        website = stock.info.get('website', 'N/A')
        st.write(f"**🌐 Website:** [{website}]({website})")
else:
    st.error("Failed to fetch company data.")

# Download historical data with a loading spinner
with st.spinner("Loading stock data..."):
    data = yf.download(symbol, start=sdate, end=edate)

# Debug message to check if data is fetched correctly
if data.empty:
    st.warning("No data found for the selected stock symbol and date range.")
    st.write("Please verify that the stock symbol is valid and that there is data available for the selected date range.")
else:
    st.write("Data successfully retrieved. Here's a sample:")
    st.write(data.head())  # Display the first few rows of data for confirmation

    # Create and display interactive line chart with improved styling
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close Price'))
    fig.update_layout(
        title=f'{symbol} Closing Prices',
        xaxis_title='Date',
        yaxis_title='Close Price',
        template='plotly_white',  # Light theme
        xaxis=dict(showgrid=True, gridcolor='LightGrey'),  # Light grid lines
        yaxis=dict(showgrid=True, gridcolor='LightGrey'),
        plot_bgcolor='rgba(255, 255, 255, 1)',  # White background
        paper_bgcolor='rgba(240, 242, 246, 1)',  # Light gray paper background
    )
    st.plotly_chart(fig, use_container_width=True)

# Footer with additional resources or credits
st.markdown("---")  # Horizontal separator
st.markdown(
    "<footer style='text-align: center; font-size: small; color: #6c757d;'>"
    "Stock data provided by Yahoo Finance | App designed by [Your Name]</footer>",
    unsafe_allow_html=True,
)
