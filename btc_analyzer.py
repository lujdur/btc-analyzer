# This script uses Streamlit to create a web app for analyzing crypto portfolios.
# To run this code, ensure you have Streamlit installed:
# pip install streamlit
# Then run: streamlit run btc_analyzer.py

import pandas as pd
import datetime

try:
    import streamlit as st
    import requests
    import plotly.graph_objs as go
    STREAMLIT_AVAILABLE = True
except ModuleNotFoundError:
    STREAMLIT_AVAILABLE = False


def fetch_btc_dominance():
    try:
        url = "https://api.coingecko.com/api/v3/global"
        response = requests.get(url)
        data = response.json()
        return data['data']['market_cap_percentage']['btc']
    except:
        return None


def fetch_macro_data():
    # Simulated macro data (replace with real APIs later)
    return {
        "Fed Rate": "5.25%",
        "CPI YoY": "3.2%",
        "Macro Risk Level": "Moderate"
    }

if STREAMLIT_AVAILABLE:
    st.set_page_config(page_title="BTC Portfolio Analyzer", layout="centered")
    st.title("\U0001F4C2 Crypto Portfolio Analyzer for BTC Stacking")

    st.markdown("""
    Upload your portfolio CSV and receive:
    - \U0001F4CA % BTC exposure
    - \u26A0\uFE0F Altcoin & risk analysis
    - \U0001F4C8 BTC Dominance trend
    - \U0001F30D Macroeconomic overview
    - \U0001F9E0 Suggestions for improving Bitcoin stacking

    **CSV format expected:**
    ```csv
    Token,Symbol,Quantity,Value (USD)
    Bitcoin,BTC,0.5,15000
    Ethereum,ETH,1.2,3500
    Solana,SOL,50,3000
    ``` 
    """)

    uploaded_file = st.file_uploader("Upload your portfolio CSV", type=["csv"])

    if uploaded_file is None:
        st.info("\U0001F447 Please upload a valid CSV file to begin.")

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            total_value = df['Value (USD)'].sum()
            df['Portfolio %'] = (df['Value (USD)'] / total_value * 100).round(2)

            btc_exposure = df.loc[df['Symbol'].str.upper() == 'BTC', 'Portfolio %'].sum()
            altcoin_exposure = 100 - btc_exposure

            risky_tokens = df[df['Value (USD)'] < 1000][['Token', 'Symbol', 'Value (USD)']]

            st.subheader("\U0001F50D Portfolio Overview")
            st.dataframe(df)

            st.markdown(f"**\U0001F4B0 Total Portfolio Value:** ${total_value:,.2f}")
            st.markdown(f"**✅ BTC Exposure:** {btc_exposure:.2f}%")
            st.markdown(f"**\u26A0\uFE0F Altcoin Exposure:** {altcoin_exposure:.2f}%")

            if not risky_tokens.empty:
                st.subheader("\U0001F6A9 Risk Flag — Small or Volatile Positions")
                st.dataframe(risky_tokens)

            st.subheader("\U0001F9E0 BTC Stacking Insight")
            if btc_exposure < 50:
                st.warning("Your BTC exposure is low. Consider reallocating from alts to stack more BTC.")
            elif btc_exposure > 75:
                st.success("Strong BTC position. You're well positioned for long-term stacking.")
            else:
                st.info("Balanced exposure. Monitor BTC dominance and macro conditions for adjustments.")

            # BTC Dominance
            st.subheader("\U0001F4C8 BTC Dominance")
            btc_dominance = fetch_btc_dominance()
            if btc_dominance:
                st.markdown(f"**Current BTC Dominance:** {btc_dominance:.2f}%")
                if btc_dominance > 50 and altcoin_exposure > 30:
                    st.warning("High BTC dominance + high altcoin exposure. Consider rotating into BTC.")
                elif btc_dominance < 45 and btc_exposure > 70:
                    st.info("Low BTC dominance. May be early alt season. Watch ETH and majors.")
            else:
                st.error("Unable to fetch BTC dominance data.")

            # Macro Overview
            st.subheader("\U0001F30D Macroeconomic Snapshot")
            macro_data = fetch_macro_data()
            st.markdown(f"**Fed Rate:** {macro_data['Fed Rate']}")
            st.markdown(f"**CPI YoY:** {macro_data['CPI YoY']}")
            st.markdown(f"**Macro Risk Level:** {macro_data['Macro Risk Level']}")

        except Exception as e:
            st.error(f"Error reading CSV: {e}")
            st.stop()

else:
    print("Streamlit is not installed in this environment. To run the app, install Streamlit with 'pip install streamlit' and run this script using 'streamlit run btc_analyzer.py'.")
