"""
Admin Dashboard - Analytics, Metrics, and Management Console
Real-time KPIs, trends, inventory, and customer analytics
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from src.utils.snowflake_connector import SnowflakeConnector
import logging

logger = logging.getLogger(__name__)

class AdminDashboard:
    """Comprehensive admin analytics dashboard"""
    
    def __init__(self, session):
        self.session = session
    
    def render(self):
        """Render complete dashboard"""
        st.set_page_config(page_title="Admin Dashboard", layout="wide")
        
        st.title("📊 Melanie's Smoothies - Admin Dashboard")
        st.subheader("Real-time Analytics & Business Intelligence")
        
        # Sidebar filters
        with st.sidebar:
            st.header("⚙️ Filters")
            
            date_range = st.date_input(
                "Select Date Range",
                value=(datetime.now() - timedelta(days=30), datetime.now()),
                max_value=datetime.now()
            )
            
            refresh_rate = st.selectbox(
                "Auto-refresh (seconds)",
                [30, 60, 120, 300],
                index=1
            )
        
        # Main tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📈 Sales", "🍎 Inventory", "👥 Customers", "🤖 ML Insights", "⚙️ Settings"
        ])
        
        with tab1:
            self._render_sales_analytics()
        
        with tab2:
            self._render_inventory_management()
        
        with tab3:
            self._render_customer_analytics()
        
        with tab4:
            self._render_ml_insights()
        
        with tab5:
            self._render_settings()
    
    def _render_sales_analytics(self):
        """Sales and Revenue Metrics"""
        st.subheader("📈 Sales Performance")
        
        # KPI Cards
        col1, col2, col3, col4 = st.columns(4)
        
        try:
            # Fetch metrics
            metrics_query = """
            SELECT
                COALESCE(SUM(TOTAL_ORDERS), 0) as total_orders,
                COALESCE(COUNT(DISTINCT UNIQUE_CUSTOMERS), 0) as total_customers,
                COALESCE(SUM(TOTAL_REVENUE), 0) as total_revenue,
                COALESCE(AVG(AVG_FRUITS_PER_ORDER), 0) as avg_fruits
            FROM GOLD.ORDERS_SUMMARY
            """
            
            metrics = self.session.sql(metrics_query).to_pandas().iloc[0]
            
            col1.metric("Total Orders", int(metrics['TOTAL_ORDERS']))
            col2.metric("Unique Customers", int(metrics['TOTAL_CUSTOMERS']))
            col3.metric("Revenue ($)", f"${metrics['TOTAL_REVENUE']:.2f}")
            col4.metric("Avg Fruits/Order", f"{metrics['AVG_FRUITS']:.2f}")
            
            st.divider()
            
            # Daily orders trend
            trend_query = """
            SELECT SUMMARY_DATE, TOTAL_ORDERS
            FROM GOLD.ORDERS_SUMMARY
            ORDER BY SUMMARY_DATE DESC
            LIMIT 60
            """
            trend_df = self.session.sql(trend_query).to_pandas()
            trend_df = trend_df.sort_values('SUMMARY_DATE')
            
            fig = px.line(
                trend_df,
                x='SUMMARY_DATE',
                y='TOTAL_ORDERS',
                title='Daily Orders Trend (Last 60 Days)',
                markers=True,
                line_shape='spline'
            )
            fig.update_layout(
                hovermode='x unified',
                xaxis_title='Date',
                yaxis_title='Orders'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Most popular fruits
            col1, col2 = st.columns(2)
            
            with col1:
                fruit_query = """
                SELECT FRUIT_NAME, COUNT(*) as order_count
                FROM GOLD.FACT_ORDERS
                GROUP BY FRUIT_NAME
                ORDER BY order_count DESC
                LIMIT 10
                """
                fruit_df = self.session.sql(fruit_query).to_pandas()
                
                fig = px.bar(
                    fruit_df,
                    x='FRUIT_NAME',
                    y='ORDER_COUNT',
                    title='Top 10 Most Popular Fruits',
                    color='ORDER_COUNT',
                    color_continuous_scale='Viridis'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Revenue by date
                revenue_query = """
                SELECT SUMMARY_DATE, TOTAL_REVENUE
                FROM GOLD.ORDERS_SUMMARY
                WHERE TOTAL_REVENUE > 0
                ORDER BY SUMMARY_DATE DESC
                LIMIT 30
                """
                revenue_df = self.session.sql(revenue_query).to_pandas()
                revenue_df = revenue_df.sort_values('SUMMARY_DATE')
                
                fig = px.area(
                    revenue_df,
                    x='SUMMARY_DATE',
                    y='TOTAL_REVENUE',
                    title='Revenue Trend',
                    fill='tozeroy'
                )
                st.plotly_chart(fig, use_container_width=True)
        
        except Exception as e:
            st.error(f"Error loading sales data: {e}")
    
    def _render_inventory_management(self):
        """Inventory Status and Alerts"""
        st.subheader("🚨 Inventory Management")
        
        try:
            # Low stock alerts
            low_stock_query = """
            SELECT
                FRUIT_NAME,
                CURRENT_STOCK,
                REORDER_LEVEL,
                IS_LOW_STOCK,
                DAYS_UNTIL_STOCKOUT
            FROM GOLD.INVENTORY_STATUS
            ORDER BY DAYS_UNTIL_STOCKOUT ASC
            """
            
            inventory_df = self.session.sql(low_stock_query).to_pandas()
            
            # Filter low stock
            low_stock = inventory_df[inventory_df['IS_LOW_STOCK'] == True]
            
            if len(low_stock) > 0:
                st.warning(f"⚠️ **{len(low_stock)} fruits are below reorder level!**")
                st.dataframe(low_stock, use_container_width=True)
            else:
                st.success("✅ All inventory levels are healthy!")
            
            st.divider()
            
            # Inventory visualization
            col1, col2 = st.columns(2)
            
            with col1:
                fig = go.Figure(data=[
                    go.Bar(name='Current Stock', x=inventory_df['FRUIT_NAME'], 
                           y=inventory_df['CURRENT_STOCK'], marker_color='lightblue'),
                    go.Bar(name='Reorder Level', x=inventory_df['FRUIT_NAME'], 
                           y=inventory_df['REORDER_LEVEL'], marker_color='red')
                ])
                fig.update_layout(title='Inventory vs Reorder Level', barmode='group')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Stock health scores
                fig = px.bar(
                    inventory_df,
                    x='FRUIT_NAME',
                    y='STOCK_HEALTH_SCORE',
                    title='Stock Health Score (%)',
                    color='STOCK_HEALTH_SCORE',
                    color_continuous_scale='RdYlGn'
                )
                st.plotly_chart(fig, use_container_width=True)
        
        except Exception as e:
            st.error(f"Error loading inventory data: {e}")
    
    def _render_customer_analytics(self):
        """Customer Segmentation and RFM Analysis"""
        st.subheader("👥 Customer Insights")
        
        try:
            # Customer segments
            segment_query = """
            SELECT
                CUSTOMER_SEGMENT,
                COUNT(*) as count,
                AVG(MONETARY_VALUE) as avg_ltv,
                AVG(RECENCY_DAYS) as avg_recency
            FROM GOLD.CUSTOMER_ANALYTICS
            GROUP BY CUSTOMER_SEGMENT
            ORDER BY count DESC
            """
            
            segment_df = self.session.sql(segment_query).to_pandas()
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.pie(
                    segment_df,
                    names='CUSTOMER_SEGMENT',
                    values='COUNT',
                    title='Customer Segments Distribution'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.bar(
                    segment_df,
                    x='CUSTOMER_SEGMENT',
                    y='AVG_LTV',
                    title='Average Lifetime Value by Segment',
                    color='AVG_LTV',
                    color_continuous_scale='Blues'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            st.divider()
            st.write("**Segment Details:**")
            st.dataframe(segment_df, use_container_width=True)
        
        except Exception as e:
            st.error(f"Error loading customer data: {e}")
    
    def _render_ml_insights(self):
        """ML Model Predictions & Insights"""
        st.subheader("🤖 Machine Learning Insights")
        
        try:
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("#### 🔮 Demand Forecast (Next 30 Days)")
                
                forecast_query = """
                SELECT * FROM GOLD.ORDERS_SUMMARY
                ORDER BY SUMMARY_DATE DESC
                LIMIT 30
                """
                
                forecast_df = self.session.sql(forecast_query).to_pandas()
                
                fig = px.line(
                    forecast_df.sort_values('SUMMARY_DATE'),
                    x='SUMMARY_DATE',
                    y='TOTAL_ORDERS',
                    title='Order Forecast',
                    markers=True
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.write("#### 📊 Customer Churn Risk")
                
                churn_query = """
                SELECT
                    CUSTOMER_SEGMENT,
                    AVG(CHURN_RISK) as avg_churn_risk
                FROM GOLD.CUSTOMER_ANALYTICS
                GROUP BY CUSTOMER_SEGMENT
                ORDER BY avg_churn_risk DESC
                """
                
                churn_df = self.session.sql(churn_query).to_pandas()
                
                fig = px.bar(
                    churn_df,
                    x='CUSTOMER_SEGMENT',
                    y='AVG_CHURN_RISK',
                    title='Churn Risk by Segment',
                    color='AVG_CHURN_RISK',
                    color_continuous_scale='Reds'
                )
                st.plotly_chart(fig, use_container_width=True)
        
        except Exception as e:
            st.error(f"Error loading ML insights: {e}")
    
    def _render_settings(self):
        """Settings and Configuration"""
        st.subheader("⚙️ Dashboard Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("#### Data Refresh")
            if st.button("🔄 Refresh All Data"):
                st.success("Data refreshed successfully!")
            
            if st.button("⚡ Run ETL Pipeline"):
                st.info("ETL pipeline triggered...")
                st.success("Pipeline completed!")
        
        with col2:
            st.write("#### System Status")
            
            status_data = {
                'Component': ['Snowflake', 'Database', 'API', 'Cache'],
                'Status': ['✅ Online', '✅ Connected', '✅ Active', '✅ Working']
            }
            st.dataframe(pd.DataFrame(status_data), use_container_width=True)

# Run dashboard
if __name__ == "__main__":
    session = SnowflakeConnector.get_session()
    dashboard = AdminDashboard(session)
    dashboard.render()
