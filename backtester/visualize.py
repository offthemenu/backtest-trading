import pandas as pd
import plotly.graph_objs as go
import streamlit as st

def plot_backtest(df: pd.DataFrame, trade_log: pd.DataFrame):
    """
    Plot the backtest result using Plotly — Price, EMA, RSI, Trades
    """
    st.title("Equity Trading Backtest Visualization")

    # Price + EMA Chart
    fig_price = go.Figure()
    fig_price.add_trace(go.Candlestick(
        x=df.index,
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        name='Candles'
    ))

    # Add EMAs
    fig_price.add_trace(go.Scatter(
        x=df.index, y=df['ema10'],
        line=dict(color='blue', width=1),
        name='EMA 10'
    ))
    fig_price.add_trace(go.Scatter(
        x=df.index, y=df['ema50'],
        line=dict(color='red', width=1),
        name='EMA 50'
    ))

    # Plot Buy/Sell markers
    buy_signals = trade_log[trade_log['type'] == 'BUY']
    sell_signals = trade_log[trade_log['type'] == 'SELL']

    fig_price.add_trace(go.Scatter(
        x=buy_signals['date'], y=buy_signals['price'],
        mode='markers', marker=dict(color='blue', size=10, symbol='triangle-up'),
        name='Buy'
    ))
    fig_price.add_trace(go.Scatter(
        x=sell_signals['date'], y=sell_signals['price'],
        mode='markers', marker=dict(color='orange', size=10, symbol='triangle-down'),
        name='Sell'
    ))

    fig_price.update_layout(
        title='Price Chart with EMAs and Trade Signals',
        yaxis_title='Price',
        xaxis_title='Date',
        template='plotly_white',
        xaxis_rangeslider_visible=False
    )

    st.plotly_chart(fig_price, use_container_width=True)

    # RSI Chart
    fig_rsi = go.Figure()
    fig_rsi.add_trace(go.Scatter(
        x=df.index, y=df['rsi_14'],
        line=dict(color='purple', width=1),
        name='RSI 14'
    ))
    fig_rsi.add_hline(y=70, line=dict(color='red', dash='dash'))
    fig_rsi.add_hline(y=30, line=dict(color='green', dash='dash'))
    fig_rsi.update_layout(
        title='RSI 14',
        yaxis_title='RSI',
        template='plotly_white'
    )

    st.plotly_chart(fig_rsi, use_container_width=True)

    # NAV Curve
    st.subheader("Net Asset Value (NAV) Curve")
    fig_nav = go.Figure()
    fig_nav.add_trace(go.Scatter(
        x=trade_log['date'], y=trade_log['net_asset_value'],
        line=dict(color='black', width=2),
        name='NAV'
    ))
    fig_nav.update_layout(
        title='NAV Curve',
        yaxis_title='Net Asset Value ($)',
        template='plotly_white'
    )
    st.plotly_chart(fig_nav, use_container_width=True)

    # Drawdown Chart
    st.subheader("Drawdown (Underwater) Curve")
    nav_series = trade_log.set_index('date')['net_asset_value']
    rolling_max = nav_series.cummax()
    drawdown = (nav_series - rolling_max) / rolling_max * 100

    fig_dd = go.Figure()
    fig_dd.add_trace(go.Scatter(
        x=drawdown.index, y=drawdown,
        fill='tozeroy', line=dict(color='red'),
        name='Drawdown (%)'
    ))
    fig_dd.update_layout(
        title='Drawdown (Underwater) Chart',
        yaxis_title='Drawdown (%)',
        template='plotly_white'
    )
    st.plotly_chart(fig_dd, use_container_width=True)

    st.write("Backtest Trade Logs:")
    st.dataframe(trade_log)
