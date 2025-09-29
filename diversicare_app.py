#!/usr/bin/env python3
"""
Diversicare Contracts Processing App
A Streamlit app for processing and analyzing Diversicare contract data
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import json
from typing import Dict, List, Optional, Tuple
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="Diversicare Contracts Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

class DiversicareDataProcessor:
    """Processes and analyzes Diversicare contract data"""
    
    def __init__(self):
        self.contracts_data = None
        self.pending_data = None
        self.processed_data = None
        self.load_data()
    
    def load_data(self):
        """Load all available data files"""
        try:
            # Load CSV files
            if os.path.exists("Diversicare_Contracts_Sorted_by_Dealer_Name.csv"):
                self.contracts_data = pd.read_csv("Diversicare_Contracts_Sorted_by_Dealer_Name.csv")
                st.success("✅ Loaded contracts data from CSV")
            
            # Load Excel file (AllPending)
            if os.path.exists("AllPending-09292025.xlsx"):
                try:
                    # Read the correct sheet with contract data (no header initially)
                    self.pending_data = pd.read_excel("AllPending-09292025.xlsx", 
                                                    sheet_name='RPT908 - Contract Transaction D', 
                                                    engine='openpyxl', 
                                                    header=None)
                    
                    # The header is in row 2 (0-indexed), data starts from row 3
                    if len(self.pending_data) > 3:
                        # Use row 2 as column names
                        self.pending_data.columns = self.pending_data.iloc[2]
                        # Drop the header rows and keep only data
                        self.pending_data = self.pending_data.iloc[3:].reset_index(drop=True)
                    
                    # Remove any completely empty rows
                    self.pending_data = self.pending_data.dropna(how='all')
                    st.success(f"✅ Loaded {len(self.pending_data)} pending contracts from Excel")
                except Exception as e:
                    st.warning(f"⚠️ Issue loading Excel file: {e}")
                    # Try alternative approach
                    try:
                        self.pending_data = pd.read_excel("AllPending-09292025.xlsx", 
                                                        sheet_name='RPT908 - Contract Transaction D',
                                                        engine='xlrd',
                                                        header=None)
                        if len(self.pending_data) > 3:
                            self.pending_data.columns = self.pending_data.iloc[2]
                            self.pending_data = self.pending_data.iloc[3:].reset_index(drop=True)
                        self.pending_data = self.pending_data.dropna(how='all')
                        st.success(f"✅ Loaded {len(self.pending_data)} pending contracts from Excel (alternative method)")
                    except Exception as e2:
                        st.error(f"❌ Failed to load Excel file: {e2}")
                        self.pending_data = None
            
            # Process and combine data
            self.process_data()
            
        except Exception as e:
            st.error(f"Error loading data: {e}")
    
    def process_data(self):
        """Process and combine all data sources"""
        # For now, let's focus on the Excel data since that's where the 1150+ contracts are
        if self.pending_data is not None:
            # Use Excel data as the primary dataset
            self.processed_data = self.pending_data.copy()
            
            # Clean and process the data
            self.clean_data()
            
            st.success(f"✅ Processed {len(self.processed_data)} pending contracts from Excel")
        elif self.contracts_data is not None:
            # Fallback to CSV data if Excel is not available
            self.processed_data = self.contracts_data.copy()
            
            # Clean and process the data
            self.clean_data()
            
            st.success(f"✅ Processed {len(self.processed_data)} contracts from CSV")
        else:
            st.warning("No data available to process")
    
    def clean_data(self):
        """Clean and standardize the data"""
        if self.processed_data is not None:
            # Remove any completely empty rows
            self.processed_data = self.processed_data.dropna(how='all')
            
            # Convert date columns
            date_columns = ['Effective Date', 'Date Cancelled']
            for col in date_columns:
                if col in self.processed_data.columns:
                    self.processed_data[col] = pd.to_datetime(self.processed_data[col], errors='coerce')
            
            # Convert numeric columns - handle mixed types
            numeric_columns = ['MSRP', 'Loan Amount', 'APR', 'Customer Cost', 'Dealer Cost', 'Odometer']
            for col in numeric_columns:
                if col in self.processed_data.columns:
                    # First convert to string, then to numeric to handle mixed types
                    self.processed_data[col] = pd.to_numeric(
                        self.processed_data[col].astype(str).str.replace(r'[^\d.-]', '', regex=True), 
                        errors='coerce'
                    )
            
            # Fill missing values with appropriate defaults
            self.processed_data = self.processed_data.fillna({
                'Loan Amount': 0,
                'MSRP': 0,
                'APR': 0,
                'Customer Cost': 0,
                'Dealer Cost': 0,
                'Odometer': 0
            })
            
            # Fill other missing values with empty string
            self.processed_data = self.processed_data.fillna('')
    
    def get_summary_stats(self):
        """Get summary statistics"""
        if self.processed_data is None:
            return {}
        
        # Calculate total loan amount from available amount columns
        total_loan_amount = 0
        amount_columns = ['Amount', 'Loan Amount', 'Contract Amount', 'Premium Amount']
        for col in amount_columns:
            if col in self.processed_data.columns:
                # Convert to numeric, handling any non-numeric values
                numeric_amounts = pd.to_numeric(self.processed_data[col], errors='coerce')
                total_loan_amount = numeric_amounts.sum()
                break
        
        # Calculate average loan amount
        average_loan_amount = total_loan_amount / len(self.processed_data) if len(self.processed_data) > 0 else 0
        
        # Get date range from available date columns
        date_columns = ['Contract Sale Date', 'Effective Date', 'Transaction Date', 'Billed Date']
        earliest_date = None
        latest_date = None
        
        for col in date_columns:
            if col in self.processed_data.columns:
                dates = pd.to_datetime(self.processed_data[col], errors='coerce')
                if not dates.isna().all():
                    if earliest_date is None or dates.min() < earliest_date:
                        earliest_date = dates.min()
                    if latest_date is None or dates.max() > latest_date:
                        latest_date = dates.max()
        
        stats = {
            'total_contracts': len(self.processed_data),
            'total_dealers': self.processed_data['Dealer Name'].nunique() if 'Dealer Name' in self.processed_data.columns else 0,
            'total_loan_amount': total_loan_amount,
            'average_loan_amount': average_loan_amount,
            'date_range': {
                'earliest': earliest_date,
                'latest': latest_date
            }
        }
        return stats
    
    def get_dealer_summary(self):
        """Get summary by dealer"""
        if self.processed_data is None or 'Dealer Name' not in self.processed_data.columns:
            return pd.DataFrame()
        
        # Find the appropriate columns for counting and amounts
        count_col = 'Contract Number' if 'Contract Number' in self.processed_data.columns else 'Waiver No'
        
        # Find amount column
        amount_col = None
        amount_columns = ['Amount', 'Loan Amount', 'Contract Amount', 'Premium Amount']
        for col in amount_columns:
            if col in self.processed_data.columns:
                amount_col = col
                break
        
        # Find date column
        date_col = None
        date_columns = ['Contract Sale Date', 'Effective Date', 'Transaction Date', 'Billed Date']
        for col in date_columns:
            if col in self.processed_data.columns:
                date_col = col
                break
        
        # Build aggregation dictionary
        agg_dict = {count_col: 'count'}
        if amount_col:
            agg_dict[amount_col] = ['sum', 'mean']
        if date_col:
            agg_dict[date_col] = ['min', 'max']
        
        dealer_summary = self.processed_data.groupby('Dealer Name').agg(agg_dict).round(2)
        
        # Flatten column names
        dealer_summary.columns = [' '.join(col).strip() for col in dealer_summary.columns.values]
        
        # Rename columns to standard names
        column_mapping = {
            f'{count_col} count': 'Contract Count',
            f'{amount_col} sum': 'Total Amount' if amount_col else 'Total Amount',
            f'{amount_col} mean': 'Avg Amount' if amount_col else 'Avg Amount',
            f'{date_col} min': 'First Contract' if date_col else 'First Contract',
            f'{date_col} max': 'Last Contract' if date_col else 'Last Contract'
        }
        
        dealer_summary = dealer_summary.rename(columns=column_mapping)
        
        return dealer_summary.sort_values('Contract Count', ascending=False)
    
    def get_monthly_trends(self):
        """Get monthly contract trends"""
        if self.processed_data is None or 'Effective Date' not in self.processed_data.columns:
            return pd.DataFrame()
        
        # Create monthly trends
        monthly_data = self.processed_data.copy()
        monthly_data['YearMonth'] = monthly_data['Effective Date'].dt.to_period('M')
        
        monthly_trends = monthly_data.groupby('YearMonth').agg({
            'Waiver No': 'count',
            'Loan Amount': 'sum'
        }).reset_index()
        
        monthly_trends.columns = ['Month', 'Contract Count', 'Total Loan Amount']
        return monthly_trends
    
    def generate_html_report(self):
        """Generate HTML report"""
        if self.processed_data is None:
            return "<html><body><h1>No data available</h1></body></html>"
        
        stats = self.get_summary_stats()
        dealer_summary = self.get_dealer_summary()
        monthly_trends = self.get_monthly_trends()
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Diversicare Contracts Report</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                    background-color: #f5f5f5;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background-color: white;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                .header {{
                    text-align: center;
                    color: #2c3e50;
                    border-bottom: 3px solid #3498db;
                    padding-bottom: 20px;
                    margin-bottom: 30px;
                }}
                .stats-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 20px;
                    margin-bottom: 30px;
                }}
                .stat-card {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 20px;
                    border-radius: 10px;
                    text-align: center;
                }}
                .stat-value {{
                    font-size: 2em;
                    font-weight: bold;
                    margin-bottom: 5px;
                }}
                .stat-label {{
                    font-size: 0.9em;
                    opacity: 0.9;
                }}
                .section {{
                    margin-bottom: 40px;
                }}
                .section h2 {{
                    color: #2c3e50;
                    border-left: 4px solid #3498db;
                    padding-left: 15px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 15px;
                }}
                th, td {{
                    padding: 12px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }}
                th {{
                    background-color: #3498db;
                    color: white;
                }}
                tr:nth-child(even) {{
                    background-color: #f2f2f2;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 40px;
                    padding-top: 20px;
                    border-top: 1px solid #ddd;
                    color: #666;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Diversicare Contracts Analysis Report</h1>
                    <p>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
                </div>
                
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-value">{stats['total_contracts']:,}</div>
                        <div class="stat-label">Total Contracts</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{stats['total_dealers']:,}</div>
                        <div class="stat-label">Total Dealers</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">${stats['total_loan_amount']:,.2f}</div>
                        <div class="stat-label">Total Loan Amount</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">${stats['average_loan_amount']:,.2f}</div>
                        <div class="stat-label">Average Loan Amount</div>
                    </div>
                </div>
                
                <div class="section">
                    <h2>Top Dealers by Contract Count</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Dealer Name</th>
                                <th>Contract Count</th>
                                <th>Total Loan Amount</th>
                                <th>Average Loan Amount</th>
                                <th>First Contract</th>
                                <th>Last Contract</th>
                            </tr>
                        </thead>
                        <tbody>
        """
        
        # Add dealer data
        for dealer, row in dealer_summary.head(20).iterrows():
            html_content += f"""
                            <tr>
                                <td>{dealer}</td>
                                <td>{row['Contract Count']}</td>
                                <td>${row['Total Loan Amount']:,.2f}</td>
                                <td>${row['Avg Loan Amount']:,.2f}</td>
                                <td>{row['First Contract'].strftime('%Y-%m-%d') if pd.notna(row['First Contract']) else 'N/A'}</td>
                                <td>{row['Last Contract'].strftime('%Y-%m-%d') if pd.notna(row['Last Contract']) else 'N/A'}</td>
                            </tr>
            """
        
        html_content += """
                        </tbody>
                    </table>
                </div>
                
                <div class="section">
                    <h2>Monthly Trends</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Month</th>
                                <th>Contract Count</th>
                                <th>Total Loan Amount</th>
                            </tr>
                        </thead>
                        <tbody>
        """
        
        # Add monthly trends data
        for _, row in monthly_trends.tail(12).iterrows():
            html_content += f"""
                            <tr>
                                <td>{row['Month']}</td>
                                <td>{row['Contract Count']}</td>
                                <td>${row['Total Loan Amount']:,.2f}</td>
                            </tr>
            """
        
        html_content += """
                        </tbody>
                    </table>
                </div>
                
                <div class="footer">
                    <p>Report generated by Diversicare Contracts Analysis System</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html_content

def main():
    st.title("📊 Diversicare Contracts Analysis")
    st.markdown("*Process and analyze Diversicare contract data*")
    
    # Initialize data processor
    if "data_processor" not in st.session_state:
        st.session_state.data_processor = DiversicareDataProcessor()
    
    processor = st.session_state.data_processor
    
    # Sidebar
    with st.sidebar:
        st.header("📋 Data Sources")
        
        if processor.contracts_data is not None:
            st.success(f"✅ Contracts CSV: {len(processor.contracts_data)} records")
        else:
            st.error("❌ Contracts CSV not found")
        
        if processor.pending_data is not None:
            st.success(f"✅ Pending Excel: {len(processor.pending_data)} records")
        else:
            st.error("❌ Pending Excel not found")
        
        if processor.processed_data is not None:
            st.success(f"✅ Combined Data: {len(processor.processed_data)} records")
        
        st.header("📊 Quick Actions")
        
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.session_state.data_processor = DiversicareDataProcessor()
            st.rerun()
        
        if st.button("📄 Generate HTML Report", use_container_width=True):
            st.session_state.generate_report = True
    
    # Main content
    if processor.processed_data is None:
        st.error("No data available. Please check that the data files are present.")
        return
    
    # Summary statistics
    st.header("📈 Summary Statistics")
    stats = processor.get_summary_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Contracts", f"{stats['total_contracts']:,}")
    
    with col2:
        st.metric("Total Dealers", f"{stats['total_dealers']:,}")
    
    with col3:
        st.metric("Total Loan Amount", f"${stats['total_loan_amount']:,.2f}")
    
    with col4:
        st.metric("Average Loan Amount", f"${stats['average_loan_amount']:,.2f}")
    
    # Data overview
    st.header("📋 Data Overview")
    
    tab1, tab2, tab3 = st.tabs(["Dealer Summary", "Monthly Trends", "Raw Data"])
    
    with tab1:
        st.subheader("Top Dealers by Contract Count")
        dealer_summary = processor.get_dealer_summary()
        if not dealer_summary.empty:
            st.dataframe(dealer_summary.head(20), use_container_width=True)
        else:
            st.info("No dealer data available")
    
    with tab2:
        st.subheader("Monthly Contract Trends")
        monthly_trends = processor.get_monthly_trends()
        if not monthly_trends.empty:
            st.dataframe(monthly_trends.tail(12), use_container_width=True)
            
            # Create a simple chart
            if len(monthly_trends) > 1:
                fig = px.line(monthly_trends, x='Month', y='Contract Count', 
                            title='Monthly Contract Count Trend')
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No monthly trend data available")
    
    with tab3:
        st.subheader("Raw Contract Data")
        st.dataframe(processor.processed_data.head(100), use_container_width=True)
    
    # Generate HTML report
    if st.session_state.get("generate_report", False):
        st.header("📄 HTML Report Generation")
        
        with st.spinner("Generating HTML report..."):
            html_content = processor.generate_html_report()
            
            # Save to file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"diversicare_report_{timestamp}.html"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            st.success(f"✅ HTML report generated: {filename}")
            
            # Provide download link
            with open(filename, 'rb') as f:
                st.download_button(
                    label="📥 Download HTML Report",
                    data=f.read(),
                    file_name=filename,
                    mime="text/html"
                )
            
            # Reset the flag
            st.session_state.generate_report = False

if __name__ == "__main__":
    main()
