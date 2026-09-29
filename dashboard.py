import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(page_title="Klädbutik Dashboard", layout="wide")

st.title("👗 Klädbutik Sales & Customer Analysis Dashboard")
st.write(
    "Interactive dashboard presenting channel performance, monthly trends, and demographic sales breakdown."
)

st.markdown("---")

# ----------------------------------------------------
# 1. Channel Performance Comparison (3 Pie Charts)
# ----------------------------------------------------
st.header("📊 1. Sales Channel Performance Comparison")

try:
    df_channel = pd.read_csv("data/revenue_by_channel.csv")

    cols = list(df_channel.columns)
    channel_col = next((c for c in cols if "channel" in c.lower()), df_channel.columns[0])
    num_sales_col = next((c for c in cols if "number" in c.lower() or "count" in c.lower()), df_channel.columns[1] if len(cols) > 1 else None)
    total_sales_col = next((c for c in cols if "total" in c.lower() or "sum" in c.lower()), df_channel.columns[2] if len(cols) > 2 else None)
    avg_sales_col = next((c for c in cols if "avg" in c.lower() or "average" in c.lower()), df_channel.columns[3] if len(cols) > 3 else None)

    col1, col2, col3 = st.columns(3)

    if num_sales_col:
        with col1:
            fig1 = px.pie(df_channel, values=num_sales_col, names=channel_col, title="Number of Sales (Count)", hole=0.3, color_discrete_sequence=["#636EFA", "#EF553B"])
            fig1.update_traces(textposition="inside", textinfo="value+label")
            st.plotly_chart(fig1, use_container_width=True)

    if total_sales_col:
        with col2:
            fig2 = px.pie(df_channel, values=total_sales_col, names=channel_col, title="Total Revenue Share (%) & Amount", hole=0.3, color_discrete_sequence=["#636EFA", "#EF553B"])
            fig2.update_traces(textposition="inside", texttemplate="%{label}<br>%{percent}<br>(%{value:,.0f} SEK)")
            st.plotly_chart(fig2, use_container_width=True)

    if avg_sales_col:
        with col3:
            fig3 = px.pie(df_channel, values=avg_sales_col, names=channel_col, title="Average Order Value (SEK)", hole=0.3, color_discrete_sequence=["#636EFA", "#EF553B"])
            fig3.update_traces(textposition="inside", textinfo="value+label")
            st.plotly_chart(fig3, use_container_width=True)

except Exception as e:
    st.error(f"Could not load 'data/revenue_by_channel.csv': {e}")

st.markdown("---")

# ----------------------------------------------------
# 2. Monthly Orders & Average Order Value (Two Separate Bar Charts)
# ----------------------------------------------------
st.header("📈 2. Monthly Orders & Average Order Value")

try:
    df_monthly = pd.read_csv("data/totalorder_avg_by_month.csv")

    m_cols = list(df_monthly.columns)
    month_col = next((c for c in m_cols if "month" in c.lower()), m_cols[0])
    orders_col = next((c for c in m_cols if "order" in c.lower() and "avg" not in c.lower()), m_cols[1] if len(m_cols) > 1 else None)
    avg_val_col = next((c for c in m_cols if "avg" in c.lower() or "krona" in c.lower()), m_cols[2] if len(m_cols) > 2 else None)

    chart_col1, chart_col2 = st.columns(2)

    if orders_col:
        with chart_col1:
            st.subheader("Total Orders by Month")
            fig_bar1 = px.bar(df_monthly, x=month_col, y=orders_col, text_auto=True, color_discrete_sequence=["#636EFA"])
            fig_bar1.update_layout(xaxis_title="Sale Month", yaxis_title="Total Orders (Count)")
            st.plotly_chart(fig_bar1, use_container_width=True)

    if avg_val_col:
        with chart_col2:
            st.subheader("Average Sales per Order (SEK)")
            fig_bar2 = px.bar(df_monthly, x=month_col, y=avg_val_col, text_auto=".2f", color_discrete_sequence=["#00CC96"])
            fig_bar2.update_layout(xaxis_title="Sale Month", yaxis_title="Avg Sale (SEK)")
            st.plotly_chart(fig_bar2, use_container_width=True)

except Exception as e:
    st.error(f"Could not load 'data/totalorder_avg_by_month.csv': {e}")

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

    # CSV 데이터 컬럼명 유연 파싱 (대소문자/공백 처리)
    cols = {c.lower().strip(): c for c in df_amr.columns}

    # 연령대 컬럼 찾기
    age_col = [c for k, c in cols.items() if "age" in k][0]

    # 각 채널별 Orders / Revenue 컬럼 자동 매핑
    online_orders_col = [
        c
        for k, c in cols.items()
        if "online" in k and ("order" in k or "count" in k)
    ][0]
    butik_orders_col = [
        c
        for k, c in cols.items()
        if ("butik" in k or "store" in k) and ("order" in k or "count" in k)
    ][0]
    online_rev_col = [
        c
        for k, c in cols.items()
        if "online" in k and ("rev" in k or "sale" in k)
    ][0]
    butik_rev_col = [
        c
        for k, c in cols.items()
        if ("butik" in k or "store" in k) and ("rev" in k or "sale" in k)
    ][0]

    fig_dual = make_subplots(specs=[[{"secondary_y": True}]])

    # 1. Online Orders (파란색 막대)
    fig_dual.add_trace(
        go.Bar(
            x=df_amr[age_col],
            y=df_amr[online_orders_col],
            name="Online_orders",
            marker_color="#a2c4ec",
            text=df_amr[online_orders_col],
            textposition="inside",
        ),
        secondary_y=False,
    )

    # 2. Butik Orders (연두색 막대)
    fig_dual.add_trace(
        go.Bar(
            x=df_amr[age_col],
            y=df_amr[butik_orders_col],
            name="Butik_orders",
            marker_color="#8be082",
            text=df_amr[butik_orders_col],
            textposition="inside",
        ),
        secondary_y=False,
    )

    # 3. Online Revenue (분홍색 꺾은선)
    fig_dual.add_trace(
        go.Scatter(
            x=df_amr[age_col],
            y=df_amr[online_rev_col],
            name="Online_revenue",
            mode="lines+markers+text",
            line=dict(color="#d962ca", width=3),
            marker=dict(size=7),
            text=[f"{x:,.0f}" for x in df_amr[online_rev_col]],
            textposition="top center",
        ),
        secondary_y=True,
    )

    # 4. Butik Revenue (노란색 꺾은선)
    fig_dual.add_trace(
        go.Scatter(
            x=df_amr[age_col],
            y=df_amr[butik_rev_col],
            name="Butik_revenue",
            mode="lines+markers+text",
            line=dict(color="#d4d137", width=3),
            marker=dict(size=7),
            text=[f"{x:,.0f}" for x in df_amr[butik_rev_col]],
            textposition="bottom center",
        ),
        secondary_y=True,
    )

    # 레이아웃 설정 (막대를 병렬로 배치 barmode='group')
    fig_dual.update_layout(
        title_text="Försäljning och order per åldersgrupp",
        barmode="group",
        legend=dict(
            orient="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5
        ),
        margin=dict(l=20, r=20, t=50, b=80),
    )

    fig_dual.update_xaxes(title_text="Åldersgrupp")
    fig_dual.update_yaxes(title_text="Orders (Count)", secondary_y=False)
    fig_dual.update_yaxes(title_text="Revenue (SEK)", secondary_y=True)

    st.plotly_chart(fig_dual, use_container_width=True)

except Exception as e:
    st.error(f"Error loading demographic data: {e}")