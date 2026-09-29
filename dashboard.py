import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(page_title="Klädbutik Dashboard", layout="wide")

st.title("👕 Klädbutik Sales & Customer Analysis Dashboard")
st.write(
    "Interactive dashboard presenting channel performance, monthly trends, and demographic breakdown."
)

st.markdown("---")

# -----------------------------------------------------------------------------
# 1. Channel Performance Comparison (3 Pie Charts)
# -----------------------------------------------------------------------------
st.header("📊 1. Sales Channel Performance Comparison")

try:
    if os.path.exists("data/revenue_by_channel.csv"):
        df_channel = pd.read_csv("data/revenue_by_channel.csv")
    else:
        df_channel = pd.read_csv("revenue_by_channel.csv")

    col1, col2, col3 = st.columns(3)

    with col1:
        fig_rev = px.pie(
            df_channel,
            names="Channel",
            values="Revenue",
            title="Total Revenue Share",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel,
        )
        fig_rev.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig_rev, use_container_width=True)

    with col2:
        fig_ord = px.pie(
            df_channel,
            names="Channel",
            values="Order_Count",
            title="Total Orders Share",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel,
        )
        fig_ord.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig_ord, use_container_width=True)

    with col3:
        fig_cust = px.pie(
            df_channel,
            names="Channel",
            values="Customer_Count",
            title="Unique Customers Share",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel,
        )
        fig_cust.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig_cust, use_container_width=True)

except Exception as e:
    st.error(f"Error loading channel performance data: {e}")

st.markdown("---")

# -----------------------------------------------------------------------------
# 2. Monthly Performance Trends (2 Bar Charts)
# -----------------------------------------------------------------------------
st.header("📈 2. Monthly Performance Trends")

try:
    if os.path.exists("data/totalorder_avg_by_month.csv"):
        df_monthly = pd.read_csv("data/totalorder_avg_by_month.csv")
    else:
        df_monthly = pd.read_csv("totalorder_avg_by_month.csv")

    col_m1, col_m2 = st.columns(2)

    with col_m1:
        fig_m_ord = px.bar(
            df_monthly,
            x="Month",
            y="Order_Count",
            title="Monthly Total Orders",
            text="Order_Count",
            color_discrete_sequence=["#2b5c8f"],
        )
        fig_m_ord.update_traces(textposition="outside")
        fig_m_ord.update_layout(xaxis_title="Month", yaxis_title="Total Orders")
        st.plotly_chart(fig_m_ord, use_container_width=True)

    with col_m2:
        fig_m_val = px.bar(
            df_monthly,
            x="Month",
            y="Avg_Order_Value",
            title="Monthly Average Order Value (SEK)",
            text="Avg_Order_Value",
            color_discrete_sequence=["#e07a5f"],
        )
        fig_m_val.update_traces(texttemplate="%{text:.1f}", textposition="outside")
        fig_m_val.update_layout(xaxis_title="Month", yaxis_title="Avg Value (SEK)")
        st.plotly_chart(fig_m_val, use_container_width=True)

except Exception as e:
    st.error(f"Error loading monthly trend data: {e}")

st.markdown("---")

# -----------------------------------------------------------------------------
# 3. Customer Demographics & Performance (Dual-Axis Chart)
# -----------------------------------------------------------------------------
st.header("👥 3. Customer Demographics & Performance")

try:
    if os.path.exists("data/AMRKlad.csv"):
        df_amr = pd.read_csv("data/AMRKlad.csv")
    else:
        df_amr = pd.read_csv("AMRKlad.csv")

    # Grouping data by Age_Group
    df_age = (
        df_amr.groupby("Age_Group")
        .agg(
            Total_Revenue=("Revenue", "sum"),
            Avg_Order_Value=("Avg_Order_Value", "mean"),
        )
        .reset_index()
    )

    fig_dual = make_subplots(specs=[[{"secondary_y": True}]])

    # Bar chart for Total Revenue
    fig_dual.add_trace(
        go.Bar(
            x=df_age["Age_Group"],
            y=df_age["Total_Revenue"],
            name="Total Revenue (SEK)",
            marker_color="#2b5c8f",
            text=df_age["Total_Revenue"],
            textposition="inside",
            texttemplate="%{text:,.0f}",
        ),
        secondary_y=False,
    )

    # Line chart for Avg Order Value
    fig_dual.add_trace(
        go.Scatter(
            x=df_age["Age_Group"],
            y=df_age["Avg_Order_Value"],
            name="Avg Order Value (SEK)",
            mode="lines+markers+text",
            line=dict(color="#e07a5f", width=3),
            marker=dict(size=8),
            text=df_age["Avg_Order_Value"],
            textposition="top center",
            texttemplate="%{text:.1f}",
        ),
        secondary_y=True,
    )

    fig_dual.update_layout(
        title_text="Total Revenue vs. Average Order Value by Age Group",
        legend=dict(orient="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    fig_dual.update_xaxes(title_text="Age Group")
    fig_dual.update_yaxes(title_text="Total Revenue (SEK)", secondary_y=False)
    fig_dual.update_yaxes(title_text="Avg Order Value (SEK)", secondary_y=True)

    st.plotly_chart(fig_dual, use_container_width=True)

except Exception as e:
    st.error(f"Error loading demographic data: {e}")