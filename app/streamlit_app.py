import pandas as pd
import streamlit as st
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from db_utils import load_all_sales, get_engine


def main():
    # Page configuration
    st.set_page_config(
        page_title="Car Sales Dashboard",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.title("🚗 Car Sales Dashboard")

    # 1) Load & prepare sales data
    df_all = load_all_sales()
    # ensure consistent price column
    if "price" not in df_all.columns:
        if "Sale Price" in df_all.columns:
            df_all = df_all.rename(columns={"Sale Price": "price"})
        else:
            st.error("No 'price' column found in sales data.")
            return

    df_all["date"] = pd.to_datetime(df_all["date"])
    df_all["year"] = df_all["date"].dt.year
    df_all["month"] = df_all["date"].dt.to_period("M").dt.to_timestamp()

    # 2) Sidebar filters
    st.sidebar.header("🔍 Filters")
    years = sorted(df_all["year"].unique())
    makes = sorted(df_all["make"].unique())

    selected_years = st.sidebar.multiselect("Year", options=years, default=years)
    selected_makes = st.sidebar.multiselect("Make", options=makes, default=makes)

    df = df_all[
        df_all["year"].isin(selected_years) &
        df_all["make"].isin(selected_makes)
    ]

    # 3) Top-row KPIs
    total_sales = len(df)
    total_revenue = df["price"].sum()
    avg_price = df["price"].mean()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📅 Records", f"{total_sales:,}")
    c2.metric("💰 Total Revenue", f"${total_revenue:,.0f}")
    c3.metric("🔖 Avg. Price", f"${avg_price:,.0f}")
    c4.metric("🗓 Years Shown", ", ".join(str(y) for y in selected_years))

    st.markdown("---")

    # 4) Monthly Transactions Chart
    monthly_df = (
        df.groupby("month")["price"]
          .count()
          .reset_index(name="transactions")
    )
    fig1 = px.line(
        monthly_df, x="month", y="transactions",
        title="Monthly Transactions"
    )
    st.plotly_chart(fig1, use_container_width=True)

    # 5) Revenue by Make Chart
    by_make_df = (
        df.groupby("make")["price"]
          .sum()
          .reset_index(name="revenue")
          .sort_values("revenue", ascending=False)
          .head(5)
    )
    fig2 = px.bar(
        by_make_df, x="make", y="revenue",
        title="Revenue by Make"
    )
    st.plotly_chart(fig2, use_container_width=True)

    # 6) Sales vs Population 
    engine = get_engine()
    sql = """
    WITH filtered_sales AS (
      SELECT date_trunc('month', date)::date AS month
      FROM sales
      WHERE make = ANY(%(makes)s)
        AND EXTRACT(YEAR FROM date) = ANY(%(years)s)
    )
    SELECT
      fs.month,
      COUNT(*)            AS sales_count,
      MAX(p.population)   AS population
    FROM filtered_sales fs
    LEFT JOIN population p
      ON p.date = fs.month
    GROUP BY fs.month
    ORDER BY fs.month
    """
    params = {"makes": list(selected_makes), "years": [int(y) for y in selected_years]}
    merged = pd.read_sql(sql, engine, params=params, parse_dates=["month"])
    
    # Remove outliers
    merged = merged[merged["sales_count"] >= 10000]

    # Convert population to millions (absolute)
    merged["pop_millions"] = merged["population"] / 1_000_000

    # Compute padded axis ranges
    min_sales = merged["sales_count"].min() * 0.90
    max_sales = merged["sales_count"].max() * 1.10
    min_pop = merged["pop_millions"].min() * 0.999
    max_pop = merged["pop_millions"].max() * 1.001

    fig3 = make_subplots(specs=[[{"secondary_y": True}]])
    fig3.add_trace(
        go.Scatter(x=merged["month"], y=merged["sales_count"],
                   name="Sales Count", mode="lines+markers"),
        secondary_y=False,
    )
    fig3.add_trace(
        go.Scatter(x=merged["month"], y=merged["pop_millions"],
                   name="Population (millions)", mode="lines+markers"),
        secondary_y=True,
    )
    fig3.update_layout(
        title="Sales vs Population Over Time",
        xaxis_title="Month",
        legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center"),
        margin=dict(t=60, b=40),
    )
    fig3.update_yaxes(range=[min_sales, max_sales], title_text="Sales Count", secondary_y=False)
    fig3.update_yaxes(range=[min_pop, max_pop], title_text="Population (millions)", secondary_y=True)

    st.plotly_chart(fig3, use_container_width=True)

    # 7) data expander + download
    st.markdown("---")
    with st.expander("🔽 Show raw sales data"):
        st.dataframe(df, use_container_width=True, hide_index=True)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download filtered data as CSV",
            data=csv,
            file_name="filtered_sales.csv",
            mime="text/csv",
        )


if __name__ == "__main__":
    main()
