import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from db_utils import get_engine, get_available_years, load_sales

load_dotenv()


def main():
    st.title("🚗 Car Sales Dashboard")

    years = get_available_years()
    current_year = pd.Timestamp.now().year
    default_idx = years.index(current_year) if current_year in years else len(years) - 1
    year = st.sidebar.selectbox("Select year", years, index=default_idx)

    df = load_sales(year)

    total_sales = len(df)
    total_revenue = df["sale_price"].sum()
    avg_price = df["sale_price"].mean()
    pop = df["population"].iloc[0] if not df["population"].isna().all() else None
    sales_per_capita = total_sales / pop if pop else None

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Sales", f"{total_sales:,}")
    k2.metric("Total Revenue", f"£{total_revenue:,.0f}")
    k3.metric("Avg Sale Price", f"£{avg_price:,.0f}")
    k4.metric("Sales per Capita", f"{sales_per_capita:.3f}" if sales_per_capita else "N/A")

    st.markdown("---") 

    makes = sorted(df["make"].unique())
    selected_makes = st.sidebar.multiselect("Filter by Make", makes, default=makes[:5])
    if selected_makes:
        df = df[df["make"].isin(selected_makes)]

    df["month"] = df["date"].dt.month
    df["units_sold"] = 1
    monthly = df.groupby("month")["units_sold"].sum().reset_index()
    st.subheader("Monthly Sales Count")
    st.line_chart(monthly.set_index("month"))

    st.subheader("Top Makes by Sales Volume")
    top_makes = (
        df.groupby("make")["units_sold"]
          .sum()
          .nlargest(10)
          .reset_index()
          .rename(columns={"units_sold": "sales_count"})
    )
    st.bar_chart(top_makes.set_index("make"))

    st.subheader("Detailed Data")
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name=f"sales_{year}.csv",
        mime="text/csv"
    )

    # --- Raw Data Table ---
    st.dataframe(df)


if __name__ == "__main__":
    main()
