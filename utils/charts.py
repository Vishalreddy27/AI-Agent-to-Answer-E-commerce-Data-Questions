import pandas as pd
import plotly.express as px
import streamlit as st
import os

# File paths
ADS_CSV = "data/Product-Level Ad Sales and Metrics (mapped).csv"
SALES_CSV = "data/Product-Level Total Sales and Metrics (mapped).csv"
ELIGIBILITY_CSV = "data/Product-Level Eligibility Table (mapped).csv"

def load_data():
    ads_df = pd.read_csv(ADS_CSV)
    sales_df = pd.read_csv(SALES_CSV)
    eligibility_df = pd.read_csv(ELIGIBILITY_CSV)
    
    # Convert date columns to datetime
    ads_df['date'] = pd.to_datetime(ads_df['date'], errors='coerce')
    sales_df['date'] = pd.to_datetime(sales_df['date'], errors='coerce')
    eligibility_df['eligibility_datetime_utc'] = pd.to_datetime(eligibility_df['eligibility_datetime_utc'], errors='coerce')

    return ads_df, sales_df, eligibility_df

def show_charts():
    ads_df, sales_df, eligibility_df = load_data()

    st.subheader("📊 Advertisement Spend vs Sales")
    merged = pd.merge(ads_df, sales_df, on=["date", "item_id"], how="inner")
    fig1 = px.scatter(
        merged,
        x="ad_spend",
        y="total_sales",
        size="clicks",
        color="item_id",
        title="Ad Spend vs Total Sales with Click Volume"
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("📈 Total Sales Over Time")
    sales_by_date = sales_df.groupby("date")["total_sales"].sum().reset_index()
    fig2 = px.line(
        sales_by_date,
        x="date",
        y="total_sales",
        title="Total Sales Over Time"
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("📌 Click-Through Rate (CTR) by Item")
    ads_df["CTR"] = (ads_df["clicks"] / ads_df["impressions"]).fillna(0)
    fig3 = px.bar(
        ads_df.sort_values("CTR", ascending=False).head(10),
        x="item_id",
        y="CTR",
        title="Top 10 Items by CTR"
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("✅ Eligibility Status Distribution")
    fig4 = px.pie(
        eligibility_df,
        names="eligibility",
        title="Eligibility Status of Products"
    )
    st.plotly_chart(fig4, use_container_width=True)
