import pandas as pd
import streamlit as st
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import altair as alt


from db_utils import load_all_sales, get_engine


def main():
    st.set_page_config(
        page_title="Car Sales Dashboard",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.title("🚗 Car Sales Dashboard")
    
    # load data
    df_all = load_all_sales()
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

    # 3) Top-row Key Metrics
    total_sales = len(df)
    total_revenue = df["price"].sum()
    avg_price = df["price"].mean()

    # find the top age group
    bins = [18, 25, 35, 45, 55, 65, 100]
    labels = ["18–24", "25–34", "35–44", "45–54", "55–64", "65+"]
    df["age_group"] = pd.cut(df["customer_age"], bins=bins, labels=labels, right=False)
    age_counts = df["age_group"].value_counts()
    top_age_group = age_counts.idxmax()
    top_age_count = age_counts.max()

    # Top row: Total Sales & Revenue
    c1, c2 = st.columns(2)
    c1.metric("📅 Total Sales",   f"{total_sales:,}")
    c2.metric("💰 Total Revenue", f"${total_revenue:,.0f}")

    st.markdown("") 

    # Bottom row: Avg Price, Top Fuel, Top Age Group
    c3, c4 = st.columns(2)
    c3.metric("🔖 Avg. Price", f"${avg_price:,.0f}")
    c4.metric("👥 Top Age Group", f"{top_age_group}", f"{top_age_count:,} cars")

    st.markdown("---")

    # 4) Revenue by Make Chart
    by_make_df = (
        df.groupby("make")["price"]
        .sum()
        .reset_index(name="revenue")
        .sort_values("revenue", ascending=False)
        .head(5)
    )

    min_r, max_r = by_make_df["revenue"].min(), by_make_df["revenue"].max()

    lower = min_r * 0.99
    upper = max_r * 1.01

    fig2 = px.bar(
        by_make_df,
        x="make",
        y="revenue",
        title="Revenue by Make",
        range_y=[lower, upper],
        labels={"revenue": "Revenue ($)", "make": "Make"}
    )
    fig2.update_yaxes(tickformat="$,.0f")

    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    
    # 5) Sales vs Population using AI assistance
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
    
    st.markdown("---")
    
    # 6) fuel type distribution
    fuel_pct = (
        df["fuel_type"]
        .value_counts(normalize=True)
        .mul(100)
        .round(1)
        .reset_index(name="percent")
        .rename(columns={"index": "fuel_type"})
    )

    # 2) Build a pie chart
    fig_fuel = px.pie(
        fuel_pct,
        names="fuel_type",
        values="percent",
        title="Fuel Type Distribution (%)",
        hole=0.4,
        labels={"fuel_type": "Fuel Type", "percent": "% of Sales"}
    )

    st.plotly_chart(fig_fuel, use_container_width=True)
    
    st.markdown("---")
 
    # 7) price against gender with AI assistance
    avg_price = (
        df.groupby('gender')['price']
        .mean()
        .reset_index(name='avg_price')
    )

    counts = (
        df.groupby(['gender','payment_method'])
        .size()
        .reset_index(name='count')
        .merge(df.groupby('gender').size().reset_index(name='total'), on='gender')
        .merge(avg_price, on='gender')
    )
    counts['proportion'] = counts['count'] / counts['total']
    counts['height']     = counts['avg_price'] * counts['proportion']

    chart = (
        alt.Chart(counts)
        .mark_bar()
        .encode(
            x=alt.X('gender:N', title='Gender'),
            y=alt.Y('height:Q', title='Average Sale Price'),
            color=alt.Color('payment_method:N', title='Payment Method'),
            tooltip=[
                alt.Tooltip('count:Q', title='Count'),
                alt.Tooltip('proportion:Q', format='.0%', title='Pct of Customers'),
                alt.Tooltip('avg_price:Q', format=',.2f', title='Avg Price')
            ]
        )
        .properties(
            width=600,
            height=400,
            title='Avg Sale Price by Gender with Payment Method Breakdown'
        )
    )

    st.title('Sales Analysis Dashboard')
    st.altair_chart(chart, use_container_width=True)

    st.markdown("---")

    #  data expander + download
    with st.expander("🔽 Show sales data"):
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
