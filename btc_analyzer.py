# This script uses Streamlit to create a web app for analyzing crypto portfolios.
# To run this code, ensure you have Streamlit installed:
# pip install streamlit
# Then run: streamlit run btc_analyzer.py

import pandas as pd

try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except ModuleNotFoundError:
    STREAMLIT_AVAILABLE = False

if STREAMLIT_AVAILABLE:
    st.set_page_config(page_title="BTC Portfolio Analyzer", layout="centered")
    st.title("📂 Crypto Portfolio Analyzer for BTC Stacking")

    st.markdown("""
    Upload your portfolio CSV and receive:
    - 📊 % BTC exposure
    - ⚠️ Altcoin & risk analysis
    - 🧠 Suggestions for improving Bitcoin stacking

    **CSV format expected:**
    ```csv
    Token,Symbol,Quantity,Value (USD)
    Bitcoin,BTC,0.5,15000
    Ethereum,ETH,1.2,3500
    Solana,SOL,50,3000
    ``` 
    """)

    uploaded_file = st.file_uploader("Upload your portfolio CSV", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        total_value = df['Value (USD)'].sum()
        df['Portfolio %'] = (df['Value (USD)'] / total_value * 100).round(2)

        btc_exposure = df.loc[df['Symbol'].str.upper() == 'BTC', 'Portfolio %'].sum()
        altcoin_exposure = 100 - btc_exposure

        risky_tokens = df[df['Value (USD)'] < 1000][['Token', 'Symbol', 'Value (USD)']]

        st.subheader("🔍 Portfolio Overview")
        st.dataframe(df)

        st.markdown(f"**💰 Total Portfolio Value:** ${total_value:,.2f}")
        st.markdown(f"**✅ BTC Exposure:** {btc_exposure:.2f}%")
        st.markdown(f"**⚠️ Altcoin Exposure:** {altcoin_exposure:.2f}%")

        if not risky_tokens.empty:
            st.subheader("🚩 Risk Flag — Small or Volatile Positions")
            st.dataframe(risky_tokens)

        st.subheader("🧠 BTC Stacking Insight")
        if btc_exposure < 50:
            st.warning("Your BTC exposure is low. Consider reallocating from alts to stack more BTC.")
        elif btc_exposure > 75:
            st.success("Strong BTC position. You're well positioned for long-term stacking.")
        else:
            st.info("Balanced exposure. Monitor BTC dominance and macro conditions for adjustments.")
else:
    print("Streamlit is not installed in this environment. To run the app, install Streamlit with 'pip install streamlit' and run this script using 'streamlit run btc_analyzer.py'.")
