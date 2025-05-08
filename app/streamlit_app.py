import pandas as pd
import streamlit as st
import plotly.express as px
from db_utils import load_all_sales

def main():
    st.set_page_config(
        page_title="Car Sales Dashboard",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.title("🚗 Car Sales Dashboard")

    # 1) Load & prepare data
    df_all = load_all_sales()
    df_all["date"]  = pd.to_datetime(df_all["date"])
    df_all["year"]  = df_all["date"].dt.year
    df_all["month"] = df_all["date"].dt.month_name().str.slice(0,3)

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

    # 3) KPIs
    total_sales   = len(df)
    total_revenue = df["Sale Price"].sum()
    avg_price     = df["Sale Price"].mean()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📅 Records", f"{total_sales:,}")
    c2.metric("💰 Total Revenue", f"${total_revenue:,.0f}")
    c3.metric("🔖 Avg. Price", f"${avg_price:,.0f}")
    c4.metric("🗓 Years Shown", ", ".join(str(y) for y in selected_years))

    st.markdown("---")

    # 4) Monthly Transactions
    monthly_df = (
        df.groupby("month")
          .size()
          .reindex(["Jan","Feb","Mar","Apr","May","Jun",
                    "Jul","Aug","Sep","Oct","Nov","Dec"])
          .reset_index(name="transactions")
    )
    min_t, max_t = monthly_df["transactions"].min(), monthly_df["transactions"].max()

    fig1 = px.line(
        monthly_df, x="month", y="transactions",
        title="Monthly Transactions",
        range_y=[min_t * 0.95, max_t * 1.05]
    )
    st.plotly_chart(fig1, use_container_width=True)

    # 5) Revenue by Make
    by_make_df = (
    df.groupby("make")["Sale Price"]
      .sum()
      .reset_index(name="revenue")
      .sort_values("revenue", ascending=False)
)

    # take only the first five rows (Chevrolet, Toyota, Nissan, Honda, Ford)
    top5 = by_make_df.head(5)

    fig2 = px.bar(
        top5,
        x="make",
        y="revenue",
        title="Revenue by Make"
    )
    # keep the labels for those five only
    fig2.update_xaxes(tickmode="array", tickvals=top5["make"], ticktext=top5["make"])

    st.plotly_chart(fig2, use_container_width=True)

    # 6) Raw data expander
    with st.expander("🔽 Show raw data"):
        st.dataframe(df, use_container_width=True, hide_index=True)

if __name__ == "__main__":
    main()
