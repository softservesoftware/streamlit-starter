import streamlit as st

st.set_page_config(layout="wide")

from utils.authentication import login_required, log_activity
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime


@st.cache_data
def load_data():
    df = pd.read_csv(f"{os.getcwd()}/static/big_mart_data_example.csv")
    # Enhanced location mapping
    friendly_name_map = {
        "OUT027": "California",
        "OUT013": "New York",
        "OUT049": "Texas",
        "OUT046": "Florida",
        "OUT035": "Oklahoma",
        "OUT045": "California",
        "OUT018": "Arizona",
        "OUT017": "Nevada",
        "OUT010": "Pennsylvania",
        "OUT019": "New Jersey",
    }
    df["Outlet_Identifier"] = df["Outlet_Identifier"].map(friendly_name_map)

    # Enhanced store type mapping
    store_type_map = {
        "Supermarket Type1": "Standard Supermarket",
        "Grocery Store": "Local Grocery",
        "Supermarket Type3": "Premium Supermarket",
        "Supermarket Type2": "Discount Supermarket",
    }
    df["Outlet_Type"] = df["Outlet_Type"].map(store_type_map)

    # Calculate additional metrics
    df["Profit_Margin"] = (
        (df["Item_Outlet_Sales"] - df["Item_MRP"]) / df["Item_Outlet_Sales"]
    ) * 100
    df["Revenue_per_Visibility"] = df["Item_Outlet_Sales"] / df["Item_Visibility"]

    return df


@log_activity
@login_required
def render():
    data = load_data()

    # Executive Summary Header
    st.title("🎯 Executive Sales Performance Dashboard")
    current_year = datetime.now().year
    st.markdown(
        f"""
    ### Real-time Sales Analytics & Performance Insights
    *Last updated: {datetime.now().strftime('%B %d, %Y')}*
    """
    )

    # Advanced Filters in Expandable Sidebar
    with st.sidebar.expander("📊 Advanced Filters", expanded=False):
        outlet_filter = st.multiselect(
            "Market Locations:",
            options=data["Outlet_Identifier"].unique(),
            default=data["Outlet_Identifier"].unique(),
        )
        store_type_filter = st.multiselect(
            "Store Format:",
            options=data["Outlet_Type"].unique(),
            default=data["Outlet_Type"].unique(),
        )
        item_type_filter = st.multiselect(
            "Product Categories:",
            options=data["Item_Type"].unique(),
            default=data["Item_Type"].unique(),
        )

    # Filter application
    filtered_data = data[
        (data["Outlet_Identifier"].isin(outlet_filter))
        & (data["Outlet_Type"].isin(store_type_filter))
        & (data["Item_Type"].isin(item_type_filter))
    ]

    # Key Performance Metrics
    col1, col2, col3, col4 = st.columns(4)
    total_sales = filtered_data["Item_Outlet_Sales"].sum()
    avg_profit_margin = filtered_data["Profit_Margin"].mean()
    top_performing_store = (
        filtered_data.groupby("Outlet_Identifier")["Item_Outlet_Sales"].sum().idxmax()
    )
    yoy_growth = 15.5  # Placeholder - would calculate from historical data

    col1.metric("Total Revenue", f"${total_sales:,.0f}", f"+{yoy_growth}% YoY")
    col2.metric("Avg Profit Margin", f"{avg_profit_margin:.1f}%", "+2.3%")
    col3.metric("Top Market", top_performing_store)
    col4.metric("Store Count", len(outlet_filter))

    # Main Dashboard Tabs
    tab1, tab2, tab3 = st.tabs(
        [
            "📈 Performance Analysis",
            "🎯 Market Insights",
            "💡 Optimization Opportunities",
        ]
    )

    with tab1:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Revenue by Market")
            market_performance = (
                filtered_data.groupby("Outlet_Identifier")["Item_Outlet_Sales"]
                .sum()
                .sort_values(ascending=True)
            )
            fig = go.Figure(
                go.Bar(
                    x=market_performance.values,
                    y=market_performance.index,
                    orientation="h",
                    text=market_performance.values.round(0),
                    texttemplate="$%{text:,.0f}",
                    textposition="outside",
                )
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Store Format Performance")
            format_performance = (
                filtered_data.groupby("Outlet_Type")
                .agg({"Item_Outlet_Sales": "sum", "Profit_Margin": "mean"})
                .round(2)
            )

            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(
                go.Bar(
                    x=format_performance.index,
                    y=format_performance["Item_Outlet_Sales"],
                    name="Revenue",
                ),
                secondary_y=False,
            )
            fig.add_trace(
                go.Scatter(
                    x=format_performance.index,
                    y=format_performance["Profit_Margin"],
                    name="Profit Margin",
                    mode="lines+markers",
                ),
                secondary_y=True,
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Product Category Performance")
            category_sales = (
                filtered_data.groupby("Item_Type")
                .agg({"Item_Outlet_Sales": "sum", "Item_Visibility": "mean"})
                .sort_values("Item_Outlet_Sales", ascending=False)
            )

            fig = px.scatter(
                category_sales,
                x="Item_Visibility",
                y="Item_Outlet_Sales",
                size="Item_Outlet_Sales",
                text=category_sales.index,
            )
            fig.update_traces(textposition="top center")
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Price Point Analysis")
            fig = px.box(
                filtered_data,
                x="Outlet_Type",
                y="Item_MRP",
                color="Outlet_Type",
                title="Price Distribution by Store Format",
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.subheader("Optimization Opportunities")

        # Low Performing Products
        low_performing = (
            filtered_data.groupby("Item_Type")
            .agg(
                {
                    "Item_Outlet_Sales": "sum",
                    "Profit_Margin": "mean",
                    "Item_Visibility": "mean",
                }
            )
            .sort_values("Profit_Margin")
        )

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Products Needing Attention")
            st.dataframe(
                low_performing.head().style.format(
                    {
                        "Item_Outlet_Sales": "${:,.0f}",
                        "Profit_Margin": "{:.1f}%",
                        "Item_Visibility": "{:.2%}",
                    }
                )
            )

        with col2:
            st.markdown("#### Visibility vs. Sales Performance")
            fig = px.scatter(
                filtered_data,
                x="Item_Visibility",
                y="Item_Outlet_Sales",
                color="Outlet_Type",
                trendline="ols",
                title="Impact of Product Visibility on Sales",
            )
            st.plotly_chart(fig, use_container_width=True)

    # Export Options
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Export Options")
    csv = filtered_data.to_csv(index=False)
    st.sidebar.download_button(
        label="📥 Download Full Report (CSV)",
        data=csv,
        file_name=f"sales_analytics_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
    )


render()
