import pandas as pd
import streamlit as st
from db_utils import load_all_sales


def main():
    st.set_page_config(
        page_title="Car Sales Dashboard",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.title("🚗 Car Sales Dashboard")

    # Load & prepare
    df = load_all_sales()
    df["year"]  = df["date"].dt.year
    df["month"] = df["date"].dt.month_name().str.slice(0,3)
    df["make"]  = df["make"].str.title()

    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    years = sorted(df["year"].unique())
    makes = sorted(df["make"].unique())

    selected_years = st.sidebar.multiselect("Year", years, default=years)
    selected_makes = st.sidebar.multiselect("Make", makes, default=makes)

    df = df[df["year"].isin(selected_years) & df["make"].isin(selected_makes)]

    # Top‑row metrics
    total_sales = len(df)
    total_revenue = df["sale_price"].sum()
    avg_price = df["sale_price"].mean()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📅 Records", f"{total_sales:,}")
    c2.metric("💰 Total Revenue", f"${total_revenue:,.0f}")
    c3.metric("🔖 Avg. Price", f"${avg_price:,.0f}")
    c4.metric("🗓 Years Shown", ", ".join(str(y) for y in selected_years))

    st.markdown("---")

    # Charts
    st.subheader("Monthly Units Sold")
    monthly = df.groupby("month")["units_sold"].sum().reindex(
        ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    )
    st.line_chart(monthly)

    st.subheader("Sales by Make")
    by_make = df.groupby("make")["sale_price"].sum().sort_values(ascending=False)
    st.bar_chart(by_make)

    # Raw data in an expander
    with st.expander("🔽 Show raw data"):
        st.dataframe(
            df, 
            use_container_width=True,
            hide_index=True
        )


if __name__ == "__main__":
    main()
