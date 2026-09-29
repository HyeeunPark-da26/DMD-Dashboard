import os
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

    # 채널명 텍스트 정리 (대소문자 맞춤)
    df_channel[channel_col] = df_channel[channel_col].astype(str).str.strip().str.capitalize()

    # ✨ 1. 데이터 순서를 Online -> Butik 순으로 정렬
    df_channel[channel_col] = pd.Categorical(df_channel[channel_col], categories=["Online", "Butik"], ordered=True)
    df_channel = df_channel.sort_values(channel_col)

    # ✨ 색상 및 카테고리 순서 정의
    color_map = {
        "Online": "#636EFA", # 파란색
        "Butik": "#EF553B"   # 주황색
    }
    cat_orders = {channel_col: ["Online", "Butik"]} # ✨ 순서 고정 설정

    col1, col2, col3 = st.columns(3)

    if num_sales_col:
        with col1:
            fig1 = px.pie(
                df_channel, 
                values=num_sales_col, 
                names=channel_col, 
                title="Number of Sales (Count)", 
                hole=0.3, 
                color=channel_col,
                color_discrete_map=color_map,
                category_orders=cat_orders # ✨ 범례 순서 고정
            )
            fig1.update_traces(textposition="inside", textinfo="value+label", sort=False) # ✨ sort=False로 순서 유지
            st.plotly_chart(fig1, use_container_width=True)

    if total_sales_col:
        with col2:
            fig2 = px.pie(
                df_channel, 
                values=total_sales_col, 
                names=channel_col, 
                title="Total Revenue Share (%) & Amount", 
                hole=0.3, 
                color=channel_col,
                color_discrete_map=color_map,
                category_orders=cat_orders # ✨ 범례 순서 고정
            )
            fig2.update_traces(textposition="inside", texttemplate="%{label}<br>%{percent}<br>(%{value:,.0f} SEK)", sort=False)
            st.plotly_chart(fig2, use_container_width=True)

    if avg_sales_col:
        with col3:
            fig3 = px.pie(
                df_channel, 
                values=avg_sales_col, 
                names=channel_col, 
                title="Average Order Value (SEK)", 
                hole=0.3, 
                color=channel_col,
                color_discrete_map=color_map,
                category_orders=cat_orders # ✨ 범례 순서 고정
            )
            fig3.update_traces(textposition="inside", textinfo="value+label", sort=False)
            st.plotly_chart(fig3, use_container_width=True)

except Exception as e:
    st.error(f"Could not load 'data/revenue_by_channel.csv': {e}")

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
        df_raw = pd.read_csv("data/AMRKlad.csv", header=None)
    else:
        df_raw = pd.read_csv("AMRKlad.csv", header=None)

    # 숫자로 변환 불가능한 행 제외하고 첫 4개 컬럼 추출
    df_amr = df_raw.iloc[:, :4].copy()
    df_amr.columns = ["Age", "Channel", "Orders", "Revenue"]

    # 숫자로 강제 변환
    df_amr["Orders"] = pd.to_numeric(df_amr["Orders"], errors="coerce")
    df_amr["Revenue"] = pd.to_numeric(df_amr["Revenue"], errors="coerce")

    # 헤더 및 결측치 행 제거
    df_amr = df_amr.dropna(subset=["Orders", "Revenue"])

    # 연령대 이름 표준화 매핑
    age_map = {
        "under20": "Under 20", "under 20": "Under 20",
        "20s": "20s", "20-29": "20s",
        "30s": "30s", "30-39": "30s",
        "40s": "40s", "40-49": "40s",
        "50s": "50s", "50-59": "50s",
        "over 60": "over 60", "over60": "over 60", "60+": "over 60",
        "unknown": "Unknown"
    }

    df_amr["Age"] = df_amr["Age"].apply(lambda x: age_map.get(str(x).strip().lower(), str(x).strip()))
    df_amr["Channel"] = df_amr["Channel"].apply(lambda x: str(x).strip().capitalize())

    # Online / Butik 데이터 분리
    df_online = df_amr[df_amr["Channel"] == "Online"].set_index("Age")
    df_butik = df_amr[df_amr["Channel"] == "Butik"].set_index("Age")

    # 정렬할 연령대 순서
    age_order = ["Under 20", "20s", "30s", "40s", "50s", "over 60", "Unknown"]

    # 순서에 맞춰 데이터 재정렬
    df_online = df_online.reindex(age_order).fillna(0)
    df_butik = df_butik.reindex(age_order).fillna(0)

    fig_dual = make_subplots(specs=[[{"secondary_y": True}]])

    # 1. Online_orders
    fig_dual.add_trace(
        go.Bar(
            x=age_order,
            y=df_online["Orders"],
            name="Online_orders",
            marker_color="#a6c9ec",
            text=df_online["Orders"].astype(int),
            textposition="inside",     # ✨ 위치는 무조건 막대 내부(상단)
            insidetextanchor="end",    # ✨ 막대 안쪽 상단에 바짝 붙임
            textangle=0,               # ✨ 글자는 무조건 0도 (수평)
            constraintext="none",      # ✨ 핵심! 공간 부족해도 회전시키지 않고 밖으로 넘치게 허용
            textfont=dict(size=11, color="black"),
        ),
        secondary_y=False,
    )

    # 2. Butik_orders (막대 안쪽 안겹치게 표시)
    fig_dual.add_trace(
        go.Bar(
            x=age_order,
            y=df_butik["Orders"],
            name="Butik_orders",
            marker_color="#8ed973",
            text=df_butik["Orders"].astype(int),
            textposition="inside", # ✨ 막대 내부 상단에 배치
            insidetextanchor="end",
            textfont=dict(size=11, color="black"),
        ),
        secondary_y=False,
    )

    # 3. Online_revenue (분홍색 꺾은선 -> 라벨을 금액 단위만 깔끔하게 표시)
    online_labels = [f"{int(rev):,} SEK" if rev > 0 else "" for rev in df_online["Revenue"]]
    fig_dual.add_trace(
        go.Scatter(
            x=age_order,
            y=df_online["Revenue"],
            name="Online_revenue",
            mode="lines+markers+text",
            line=dict(color="#d068c2", width=3.5),
            marker=dict(size=6, color="#d068c2"),
            text=online_labels,
            textposition="top center", # ✨ 점 위쪽에 배치
            textfont=dict(size=11, color="black"),
        ),
        secondary_y=True,
    )

    # 4. Butik_revenue (노란색 꺾은선 -> 라벨을 금액 단위만 깔끔하게 표시)
    butik_labels = [f"{int(rev):,} SEK" if rev > 0 else "" for rev in df_butik["Revenue"]]
    fig_dual.add_trace(
        go.Scatter(
            x=age_order,
            y=df_butik["Revenue"],
            name="Butik_revenue",
            mode="lines+markers+text",
            line=dict(color="#e3df3b", width=3.5),
            marker=dict(size=6, color="#e3df3b"),
            text=butik_labels,
            textposition="bottom center", # ✨ 점 아래쪽에 배치하여 분홍선과 충돌 방지
            textfont=dict(size=11, color="black"),
        ),
        secondary_y=True,
    )

    # Y축 범위 조정 (꺾은선 라벨이 차트 상단 밖으로 나가지 않도록 범위 여유 확보)
    fig_dual.update_yaxes(range=[0, 160], dtick=20, secondary_y=False, showgrid=True, gridcolor="#e5e5e5")
    fig_dual.update_yaxes(range=[-5000, 100000], dtick=20000, secondary_y=True, showgrid=False)

    # 레이아웃 설정
    fig_dual.update_layout(
        title_text="Försäljning och order per åldersgrupp",
        title_x=0.5,
        title_font=dict(size=18),
        barmode="group",
        plot_bgcolor="white",
        paper_bgcolor="white",
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font=dict(size=12)
        ),
        margin=dict(l=40, r=40, t=60, b=80),
    )

    st.plotly_chart(fig_dual, use_container_width=True)

except Exception as e:
    st.error(f"Error loading demographic data: {e}")