

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

# ----------------------------------------------------
# 3. Monthly Revenue & Orders by Age Group (Cleaned Combination Chart)
# ----------------------------------------------------
st.header("👥 3. Försäljning och order per åldersgrupp")

try:
    df_amr = pd.read_csv("data/AMRKlad.csv")

    cols_amr = list(df_amr.columns)
    age_col = cols_amr[0]
    
    online_orders_col = next((c for c in cols_amr if "online" in c.lower() and "order" in c.lower()), cols_amr[1] if len(cols_amr) > 1 else None)
    butik_orders_col = next((c for c in cols_amr if "butik" in c.lower() and "order" in c.lower()), cols_amr[2] if len(cols_amr) > 2 else None)
    online_rev_col = next((c for c in cols_amr if "online" in c.lower() and ("rev" in c.lower() or "försälj" in c.lower() or "sales" in c.lower())), cols_amr[3] if len(cols_amr) > 3 else None)
    butik_rev_col = next((c for c in cols_amr if "butik" in c.lower() and ("rev" in c.lower() or "försälj" in c.lower() or "sales" in c.lower())), cols_amr[4] if len(cols_amr) > 4 else None)

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # 1. Online Orders Bar
    fig.add_trace(
        go.Bar(
            x=df_amr[age_col],
            y=df_amr[online_orders_col],
            name="Online_orders",
            marker_color="#9ECAE1",
            text=df_amr[online_orders_col],
            textposition="inside",
            hovertemplate="<b>Online Orders</b>: %{y:,}<extra></extra>",
        ),
        secondary_y=False,
    )

    # 2. Butik Orders Bar
    fig.add_trace(
        go.Bar(
            x=df_amr[age_col],
            y=df_amr[butik_orders_col],
            name="Butik_orders",
            marker_color="#80E080",
            text=df_amr[butik_orders_col],
            textposition="inside",
            hovertemplate="<b>Butik Orders</b>: %{y:,}<extra></extra>",
        ),
        secondary_y=False,
    )

    # Clean display labels (formatted value with background box)
    online_rev_labels = [f"{val:,.0f} SEK" for val in df_amr[online_rev_col]]
    butik_rev_labels = [f"{val:,.0f} SEK" for val in df_amr[butik_rev_col]]

    # 3. Online Revenue Line (Placed Above Point with Pink Box)
    fig.add_trace(
        go.Scatter(
            x=df_amr[age_col],
            y=df_amr[online_rev_col],
            name="Online_revenue",
            mode="lines+markers+text",
            line=dict(color="#DA70D6", width=3),
            marker=dict(size=8),
            text=online_rev_labels,
            textposition="top center",
            hovertemplate="<b>Online Revenue</b>: %{y:,.0f} SEK<extra></extra>",
        ),
        secondary_y=True,
    )

    # 4. Butik Revenue Line (Placed Below Point with Yellow Box)
    fig.add_trace(
        go.Scatter(
            x=df_amr[age_col],
            y=df_amr[butik_rev_col],
            name="Butik_revenue",
            mode="lines+markers+text",
            line=dict(color="#E6C200", width=3),
            marker=dict(size=8),
            text=butik_rev_labels,
            textposition="bottom center",
            hovertemplate="<b>Butik Revenue</b>: %{y:,.0f} SEK<extra></extra>",
        ),
        secondary_y=True,
    )

    fig.update_layout(
        title_text="Försäljning och order per åldersgrupp",
        title_x=0.5,
        barmode="group",
        legend=dict(orientation="h", yanchor="top", y=-0.15, xanchor="center", x=0.5),
        template="plotly_white",
        height=600,
        hovermode="x unified", # Shows combined tooltip when hovering over any age group
    )

    fig.update_yaxes(title_text="Orders (Count)", secondary_y=False)
    fig.update_yaxes(title_text="Revenue (SEK)", secondary_y=True)

    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Could not load or parse 'data/AMRKlad.csv': {e}")