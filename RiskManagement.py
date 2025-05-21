import streamlit as st


def calculate_liquidation_price(entry_price, leverage, position_type):
    if position_type == 'long':
        return entry_price * leverage / (leverage + 1)
    elif position_type == 'short':
        return entry_price * leverage / (leverage - 1)


def calculate_take_profit(entry_price, percent, position_type):
    if position_type == 'long':
        return entry_price * (1 + percent / 100)
    elif position_type == 'short':
        return entry_price * (1 - percent / 100)


def main():
    st.title("📉 Crypto Risk Management Tool")

    st.sidebar.header("🧮 Input Parameters")
    coin_name = st.sidebar.text_input("Coin Name", value="BTC")
    portfolio_size = st.sidebar.number_input("Portfolio Size (USDT)", value=1000.0, step=100.0)
    current_price = st.sidebar.number_input("Current Price", value=30000.0, step=100.0)
    position_type = st.sidebar.selectbox("Position Type", options=["long", "short"]).lower()
    max_percent_diff = st.sidebar.slider("Max % Difference Allowed", min_value=1.0, max_value=100.0, value=25.0)

    if st.sidebar.button("Run Risk Calculation"):
        entry_percentages = [0.20, 0.30, 0.30, 0.20]
        allocations = [portfolio_size * perc for perc in entry_percentages]
        entry_prices = []
        total_allocation = 0
        total_quantity = 0

        st.subheader(f"📌 Coin: {coin_name.upper()} | Position: {position_type.capitalize()}")

        for i, (allocation, percentage) in enumerate(zip(allocations, entry_percentages), start=1):
            if i == 1:
                entry_price = current_price
            else:
                adjustment_factor = 0.80 if position_type == 'long' else 1.20
                entry_price = entry_prices[-1] * adjustment_factor

            entry_prices.append(entry_price)
            avg_entry_price = sum(entry_prices) / len(entry_prices)
            liquidation_price_3x = calculate_liquidation_price(avg_entry_price, 3, position_type)
            liquidation_price_5x = calculate_liquidation_price(avg_entry_price, 5, position_type)
            liquidation_price_10x = calculate_liquidation_price(avg_entry_price, 10, position_type)
            liquidation_price_15x = calculate_liquidation_price(avg_entry_price, 15, position_type)
            take_profit = calculate_take_profit(avg_entry_price, 5, position_type)

            quantity = allocation / entry_price
            total_quantity += quantity
            total_allocation += allocation

            st.markdown(f"""
                ### 🔹 Entry {i} ({int(percentage * 100)}%)
                - 📌 Entry Price: **{entry_price:.2f}**
                - 💰 Allocation: **{allocation:.2f} USDT**
                - 📊 Average Entry (so far): **{avg_entry_price:.2f}**
                - 🧮 Quantity: **{quantity:.4f}**
                - ⚠️ Liquidation Prices:
                    - 3x: `{liquidation_price_3x:.2f}`
                    - 5x: `{liquidation_price_5x:.2f}`
                    - 10x: `{liquidation_price_10x:.2f}`
                    - 15x: `{liquidation_price_15x:.2f}`
                - 🎯 Take Profit (5%): **{take_profit:.2f}**
            """)

        st.subheader("📊 Final Summary")
        st.markdown(f"""
            - ✅ **Average Entry Price:** `{avg_entry_price:.2f}`
            - 🪙 **Total Quantity:** `{total_quantity:.4f}`
            - 💼 **Total Allocation Used:** `{total_allocation:.2f} USDT`
        """)

        st.subheader("🛑 Stop Loss (SL) Strategy")
        entry4_price = entry_prices[3]
        if position_type == 'long':
            sl_price = entry4_price * 0.995  # 0.5% below Entry 4
            sl_note = "SL triggers if a 4h candle closes below Entry 4 price by 0.5%."
        else:
            sl_price = entry4_price * 1.005  # 0.5% above Entry 4 for short
            sl_note = "SL triggers if a 4h candle closes above Entry 4 price by 0.5%."

        st.markdown(f"""
            - 📉 **Entry 4 Price:** `{entry4_price:.2f}`
            - 🛑 **Stop Loss Trigger Price:** `{sl_price:.2f}`
            - 📘 **Condition:** {sl_note}
        """)

        st.subheader("💼 Emergency Fund Advice")
        emergency_fund = portfolio_size * 1.8
        st.info(f"💡 Keep **{emergency_fund:.2f} USDT** separately as an emergency fund outside the exchange.")

        st.markdown("---")
        st.caption("Made with ❤️ for better risk-managed trading.")


if __name__ == "__main__":
    main()
