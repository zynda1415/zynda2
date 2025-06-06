import streamlit as st
import data
import pandas as pd
from fpdf import FPDF
import tempfile
import os
from datetime import datetime, date
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import base64

class ProfessionalPDF(FPDF):
    def __init__(self, company_name="Your Company", company_address="", company_phone="", company_email=""):
        super().__init__()
        self.company_name = company_name
        self.company_address = company_address
        self.company_phone = company_phone
        self.company_email = company_email
        
    def header(self):
        # Company header
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, self.company_name, 0, 1, 'C')
        
        if self.company_address:
            self.set_font('Arial', '', 10)
            self.cell(0, 5, self.company_address, 0, 1, 'C')
        
        contact_info = []
        if self.company_phone:
            contact_info.append(f"Phone: {self.company_phone}")
        if self.company_email:
            contact_info.append(f"Email: {self.company_email}")
        
        if contact_info:
            self.cell(0, 5, " | ".join(contact_info), 0, 1, 'C')
        
        self.ln(5)
        
        # Line separator
        self.set_draw_color(128, 128, 128)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_draw_color(128, 128, 128)
        self.line(10, self.get_y()-5, 200, self.get_y()-5)
        self.cell(0, 10, f'Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} - Page {self.page_no()}', 0, 0, 'C')

    def add_title(self, title, subtitle=""):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, title, 0, 1, 'L')
        
        if subtitle:
            self.set_font('Arial', '', 10)
            self.set_text_color(100, 100, 100)
            self.cell(0, 5, subtitle, 0, 1, 'L')
            self.set_text_color(0, 0, 0)
        
        self.ln(5)

    def add_summary_stats(self, stats_dict):
        """Add a professional summary statistics section"""
        self.set_font('Arial', 'B', 12)
        self.cell(0, 8, 'Summary Statistics', 0, 1, 'L')
        self.ln(2)
        
        # Calculate positions for 2-column layout
        col_width = (self.w - 20) / 2
        y_start = self.get_y()
        
        stats_items = list(stats_dict.items())
        for i, (label, value) in enumerate(stats_items):
            if i % 2 == 0:  # Left column
                self.set_xy(10, y_start + (i // 2) * 8)
            else:  # Right column
                self.set_xy(10 + col_width, y_start + (i // 2) * 8)
            
            self.set_font('Arial', '', 10)
            self.cell(col_width - 5, 6, f"{label}:", 0, 0, 'L')
            self.set_font('Arial', 'B', 10)
            self.cell(0, 6, str(value), 0, 0, 'R')
        
        # Move cursor to next line after stats
        self.set_y(y_start + ((len(stats_items) + 1) // 2) * 8 + 5)

    def add_professional_table(self, df, title="Data Table"):
        """Add a professional-looking table with alternating row colors"""
        self.add_title(title)
        
        if df.empty:
            self.set_font('Arial', 'I', 10)
            self.cell(0, 10, 'No data available', 0, 1, 'C')
            return
        
        # Calculate column widths
        available_width = self.w - 20
        col_count = len(df.columns)
        col_width = available_width / col_count
        
        # Table headers
        self.set_font('Arial', 'B', 9)
        self.set_fill_color(70, 130, 180)  # Steel blue
        self.set_text_color(255, 255, 255)
        
        for col in df.columns:
            self.cell(col_width, 8, str(col), 1, 0, 'C', True)
        self.ln()
        
        # Table data with alternating colors
        self.set_font('Arial', '', 8)
        self.set_text_color(0, 0, 0)
        
        for i, (_, row) in enumerate(df.iterrows()):
            # Alternating row colors
            if i % 2 == 0:
                self.set_fill_color(245, 245, 245)  # Light gray
            else:
                self.set_fill_color(255, 255, 255)  # White
            
            for item in row:
                # Format numbers nicely
                if isinstance(item, (int, float)):
                    if isinstance(item, float) and item.is_integer():
                        text = str(int(item))
                    elif isinstance(item, float):
                        text = f"{item:,.2f}"
                    else:
                        text = f"{item:,}"
                else:
                    text = str(item)
                
                self.cell(col_width, 6, text, 1, 0, 'C', True)
            self.ln()

def export_pdf_module():
    st.header("📄 Professional PDF Export System")
    
    # Company Information Section
    with st.expander("🏢 Company Information (Optional)", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            company_name = st.text_input("Company Name", value="Your Inventory Company")
            company_address = st.text_input("Address", value="123 Business Street, City, State")
        with col2:
            company_phone = st.text_input("Phone", value="+1 (555) 123-4567")
            company_email = st.text_input("Email", value="info@yourcompany.com")
    
    # Report Configuration
    st.subheader("📊 Report Configuration")
    
    report_options = [
        " Inventory Report",
        " Sales Summary",
        " Financial Analysis",
        " Executive Summary",
        " Low Stock Alert",
        " Customer Analysis",
        " Category Performance"
    ]
    
    report_type = st.selectbox("Select Report Type", report_options)
    
    # Date Range for relevant reports
    if "Sales" in report_type or "Financial" in report_type or "Executive" in report_type:
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", value=date.today().replace(day=1))
        with col2:
            end_date = st.date_input("End Date", value=date.today())
    
    # Advanced Options
    with st.expander("⚙️ Advanced Options", expanded=False):
        include_charts = st.checkbox("Include Charts", value=True)
        include_summary = st.checkbox("Include Summary Statistics", value=True)
        page_orientation = st.selectbox("Page Orientation", ["Portrait", "Landscape"])
        
    if st.button("🚀 Generate Professional PDF", type="primary"):
        with st.spinner("Generating professional PDF report..."):
            try:
                if report_type == "📦 Inventory Report":
                    pdf_bytes = generate_inventory_report(
                        company_name, company_address, company_phone, company_email,
                        include_charts, include_summary
                    )
                    filename = f"inventory_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                
                elif report_type == "💰 Sales Summary":
                    pdf_bytes = generate_sales_summary_report(
                        company_name, company_address, company_phone, company_email,
                        start_date, end_date, include_charts, include_summary
                    )
                    filename = f"sales_summary_{start_date}_{end_date}.pdf"
                
                elif report_type == "📈 Financial Analysis":
                    pdf_bytes = generate_financial_analysis(
                        company_name, company_address, company_phone, company_email,
                        start_date, end_date, include_charts
                    )
                    filename = f"financial_analysis_{start_date}_{end_date}.pdf"
                
                elif report_type == "🎯 Executive Summary":
                    pdf_bytes = generate_executive_summary(
                        company_name, company_address, company_phone, company_email,
                        start_date, end_date
                    )
                    filename = f"executive_summary_{start_date}_{end_date}.pdf"
                
                elif report_type == "📋 Low Stock Alert":
                    pdf_bytes = generate_low_stock_report(
                        company_name, company_address, company_phone, company_email
                    )
                    filename = f"low_stock_alert_{datetime.now().strftime('%Y%m%d')}.pdf"
                
                elif report_type == "👥 Customer Analysis":
                    pdf_bytes = generate_customer_analysis(
                        company_name, company_address, company_phone, company_email,
                        start_date, end_date
                    )
                    filename = f"customer_analysis_{start_date}_{end_date}.pdf"
                
                elif report_type == "📊 Category Performance":
                    pdf_bytes = generate_category_performance(
                        company_name, company_address, company_phone, company_email,
                        start_date, end_date
                    )
                    filename = f"category_performance_{start_date}_{end_date}.pdf"
                
                st.success("✅ Professional PDF Generated Successfully!")
                st.download_button(
                    label="📥 Download PDF Report",
                    data=pdf_bytes,
                    file_name=filename,
                    mime="application/pdf"
                )
                
            except Exception as e:
                st.error(f"❌ Error generating PDF: {str(e)}")

def generate_inventory_report(company_name, company_address, company_phone, company_email, include_charts, include_summary):
    """Generate comprehensive inventory report"""
    pdf = ProfessionalPDF(company_name, company_address, company_phone, company_email)
    pdf.add_page()
    
    # Load data
    inventory_df = data.load_inventory()
    
    # Report title
    pdf.add_title("Inventory Management Report", f"Generated on {datetime.now().strftime('%B %d, %Y')}")
    
    # Summary statistics
    if include_summary:
        total_items = len(inventory_df)
        total_quantity = inventory_df["Quantity"].sum()
        total_value = (inventory_df["Quantity"] * inventory_df["Sale Price"]).sum()
        avg_price = inventory_df["Sale Price"].mean()
        
        stats = {
            "Total Items": f"{total_items:,}",
            "Total Quantity": f"{int(total_quantity):,}",
            "Total Value": f"${total_value:,.2f}",
            "Average Price": f"${avg_price:.2f}",
            "Categories": len(inventory_df['Category'].unique()),
            "Suppliers": len(inventory_df['Supplier'].unique())
        }
        pdf.add_summary_stats(stats)
    
    # Low stock items
    low_stock = inventory_df[inventory_df['Quantity'] < 10]  # Assume 10 is low stock threshold
    if not low_stock.empty:
        pdf.add_professional_table(low_stock[['Item Name', 'Category', 'Quantity', 'Sale Price']], 
                                 "⚠️ Low Stock Items (Quantity < 10)")
    
    # Full inventory table
    pdf.add_professional_table(inventory_df, "Complete Inventory Listing")
    
    return pdf_to_bytes(pdf)

def generate_sales_summary_report(company_name, company_address, company_phone, company_email, start_date, end_date, include_charts, include_summary):
    """Generate comprehensive sales summary report"""
    pdf = ProfessionalPDF(company_name, company_address, company_phone, company_email)
    pdf.add_page()
    
    # Load and filter sales data
    sales_df = data.load_sales()
    sales_df['Date'] = pd.to_datetime(sales_df['Date'])
    sales_df = sales_df[(sales_df['Date'] >= pd.to_datetime(start_date)) & 
                       (sales_df['Date'] <= pd.to_datetime(end_date))]
    
    # Convert numeric columns
    sales_df['Total Price'] = pd.to_numeric(sales_df['Total Price'], errors='coerce')
    sales_df['Quantity Sold'] = pd.to_numeric(sales_df['Quantity Sold'], errors='coerce')
    
    # Report title
    pdf.add_title("Sales Summary Report", 
                 f"Period: {start_date.strftime('%B %d, %Y')} - {end_date.strftime('%B %d, %Y')}")
    
    # Summary statistics
    if include_summary and not sales_df.empty:
        total_revenue = sales_df['Total Price'].sum()
        total_quantity = sales_df['Quantity Sold'].sum()
        avg_order_value = total_revenue / len(sales_df) if len(sales_df) > 0 else 0
        unique_customers = sales_df['Name'].nunique()
        
        stats = {
            "Total Revenue": f"${total_revenue:,.2f}",
            "Total Units Sold": f"{int(total_quantity):,}",
            "Number of Orders": f"{len(sales_df):,}",
            "Unique Customers": f"{unique_customers:,}",
            "Average Order Value": f"${avg_order_value:.2f}",
            "Period Days": f"{(end_date - start_date).days + 1}"
        }
        pdf.add_summary_stats(stats)
    
    # Top selling items
    if not sales_df.empty:
        top_items = sales_df.groupby('Item').agg({
            'Quantity Sold': 'sum',
            'Total Price': 'sum'
        }).round(2).sort_values('Total Price', ascending=False).head(10)
        
        pdf.add_professional_table(top_items.reset_index(), "🏆 Top 10 Selling Items")
        
        # Customer analysis
        customer_summary = sales_df.groupby('Name').agg({
            'Total Price': ['sum', 'count'],
            'Quantity Sold': 'sum'
        }).round(2)
        customer_summary.columns = ['Total Spent', 'Orders Count', 'Items Bought']
        customer_summary = customer_summary.sort_values('Total Spent', ascending=False).head(10)
        
        pdf.add_professional_table(customer_summary.reset_index(), "💎 Top 10 Customers")
    
    return pdf_to_bytes(pdf)

def generate_financial_analysis(company_name, company_address, company_phone, company_email, start_date, end_date, include_charts):
    """Generate financial analysis report"""
    pdf = ProfessionalPDF(company_name, company_address, company_phone, company_email)
    pdf.add_page()
    
    # Load data
    sales_df = data.load_sales()
    inventory_df = data.load_inventory()
    
    # Filter sales by date
    sales_df['Date'] = pd.to_datetime(sales_df['Date'])
    sales_df = sales_df[(sales_df['Date'] >= pd.to_datetime(start_date)) & 
                       (sales_df['Date'] <= pd.to_datetime(end_date))]
    
    sales_df['Total Price'] = pd.to_numeric(sales_df['Total Price'], errors='coerce')
    sales_df['Quantity Sold'] = pd.to_numeric(sales_df['Quantity Sold'], errors='coerce')
    
    pdf.add_title("Financial Analysis Report", 
                 f"Period: {start_date.strftime('%B %d, %Y')} - {end_date.strftime('%B %d, %Y')}")
    
    # Financial metrics
    if not sales_df.empty:
        total_revenue = sales_df['Total Price'].sum()
        
        # Calculate cost (assuming cost is purchase price from inventory)
        sales_with_cost = sales_df.merge(inventory_df[['Item Name', 'Purchase Price']], 
                                       left_on='Item', right_on='Item Name', how='left')
        sales_with_cost['Cost'] = sales_with_cost['Quantity Sold'] * sales_with_cost['Purchase Price']
        total_cost = sales_with_cost['Cost'].sum()
        gross_profit = total_revenue - total_cost
        gross_margin = (gross_profit / total_revenue * 100) if total_revenue > 0 else 0
        
        financial_stats = {
            "Total Revenue": f"${total_revenue:,.2f}",
            "Total Cost": f"${total_cost:,.2f}",
            "Gross Profit": f"${gross_profit:,.2f}",
            "Gross Margin": f"{gross_margin:.1f}%",
            "Inventory Value": f"${(inventory_df['Quantity'] * inventory_df['Sale Price']).sum():,.2f}",
            "Avg Daily Revenue": f"${total_revenue / ((end_date - start_date).days + 1):,.2f}"
        }
        pdf.add_summary_stats(financial_stats)
        
        # Profitability by item
        profit_analysis = sales_with_cost.groupby('Item').agg({
            'Total Price': 'sum',
            'Cost': 'sum',
            'Quantity Sold': 'sum'
        }).round(2)
        profit_analysis['Profit'] = profit_analysis['Total Price'] - profit_analysis['Cost']
        profit_analysis['Margin %'] = (profit_analysis['Profit'] / profit_analysis['Total Price'] * 100).round(1)
        profit_analysis = profit_analysis.sort_values('Profit', ascending=False).head(10)
        
        pdf.add_professional_table(profit_analysis.reset_index(), "💰 Most Profitable Items")
    
    return pdf_to_bytes(pdf)

def generate_executive_summary(company_name, company_address, company_phone, company_email, start_date, end_date):
    """Generate executive summary report"""
    pdf = ProfessionalPDF(company_name, company_address, company_phone, company_email)
    pdf.add_page()
    
    pdf.add_title("Executive Summary Report", 
                 f"Period: {start_date.strftime('%B %d, %Y')} - {end_date.strftime('%B %d, %Y')}")
    
    # Load all data
    sales_df = data.load_sales()
    inventory_df = data.load_inventory()
    clients_df = data.load_clients()
    
    # Filter sales by date
    sales_df['Date'] = pd.to_datetime(sales_df['Date'])
    period_sales = sales_df[(sales_df['Date'] >= pd.to_datetime(start_date)) & 
                           (sales_df['Date'] <= pd.to_datetime(end_date))]
    
    period_sales['Total Price'] = pd.to_numeric(period_sales['Total Price'], errors='coerce')
    
    # Key metrics
    total_revenue = period_sales['Total Price'].sum()
    total_inventory_value = (inventory_df['Quantity'] * inventory_df['Sale Price']).sum()
    total_customers = len(clients_df)
    active_customers = period_sales['Name'].nunique()
    
    executive_stats = {
        "Period Revenue": f"${total_revenue:,.2f}",
        "Inventory Value": f"${total_inventory_value:,.2f}",
        "Total Customers": f"{total_customers:,}",
        "Active Customers": f"{active_customers:,}",
        "Customer Activity": f"{(active_customers/total_customers*100):.1f}%" if total_customers > 0 else "0%",
        "Avg Revenue/Day": f"${total_revenue / ((end_date - start_date).days + 1):,.2f}"
    }
    
    pdf.add_summary_stats(executive_stats)
    
    # Key insights section
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 8, 'Key Business Insights', 0, 1, 'L')
    pdf.set_font('Arial', '', 10)
    
    insights = [
        f"• Revenue for the period: ${total_revenue:,.2f}",
        f"• Current inventory worth: ${total_inventory_value:,.2f}",
        f"• {active_customers} out of {total_customers} customers made purchases",
        f"• Average daily revenue: ${total_revenue / ((end_date - start_date).days + 1):,.2f}",
        f"• Total product categories: {inventory_df['Category'].nunique()}",
        f"• Items needing restock: {len(inventory_df[inventory_df['Quantity'] < 10])}"
    ]
    
    for insight in insights:
        pdf.cell(0, 6, insight, 0, 1, 'L')
    
    return pdf_to_bytes(pdf)

def generate_low_stock_report(company_name, company_address, company_phone, company_email):
    """Generate low stock alert report"""
    pdf = ProfessionalPDF(company_name, company_address, company_phone, company_email)
    pdf.add_page()
    
    inventory_df = data.load_inventory()
    
    pdf.add_title("⚠️ Low Stock Alert Report", f"Generated on {datetime.now().strftime('%B %d, %Y')}")
    
    # Define stock levels
    critical_stock = inventory_df[inventory_df['Quantity'] <= 5]
    low_stock = inventory_df[(inventory_df['Quantity'] > 5) & (inventory_df['Quantity'] <= 15)]
    
    # Summary
    stock_stats = {
        "Critical Stock (≤5)": len(critical_stock),
        "Low Stock (6-15)": len(low_stock),
        "Normal Stock (>15)": len(inventory_df[inventory_df['Quantity'] > 15]),
        "Total Items": len(inventory_df),
        "Items Need Attention": len(critical_stock) + len(low_stock),
        "Stock Health": f"{((len(inventory_df) - len(critical_stock) - len(low_stock))/len(inventory_df)*100):.1f}%"
    }
    
    pdf.add_summary_stats(stock_stats)
    
    if not critical_stock.empty:
        pdf.add_professional_table(critical_stock[['Item Name', 'Category', 'Quantity', 'Supplier']], 
                                 "🚨 Critical Stock Items (≤5 units)")
    
    if not low_stock.empty:
        pdf.add_professional_table(low_stock[['Item Name', 'Category', 'Quantity', 'Supplier']], 
                                 "⚠️ Low Stock Items (6-15 units)")
    
    return pdf_to_bytes(pdf)

def generate_customer_analysis(company_name, company_address, company_phone, company_email, start_date, end_date):
    """Generate customer analysis report"""
    pdf = ProfessionalPDF(company_name, company_address, company_phone, company_email)
    pdf.add_page()
    
    sales_df = data.load_sales()
    clients_df = data.load_clients()
    
    # Filter sales by date
    sales_df['Date'] = pd.to_datetime(sales_df['Date'])
    period_sales = sales_df[(sales_df['Date'] >= pd.to_datetime(start_date)) & 
                           (sales_df['Date'] <= pd.to_datetime(end_date))]
    
    period_sales['Total Price'] = pd.to_numeric(period_sales['Total Price'], errors='coerce')
    
    pdf.add_title("👥 Customer Analysis Report", 
                 f"Period: {start_date.strftime('%B %d, %Y')} - {end_date.strftime('%B %d, %Y')}")
    
    # Customer metrics
    if not period_sales.empty:
        customer_stats = period_sales.groupby('Name').agg({
            'Total Price': ['sum', 'mean', 'count'],
            'Quantity Sold': 'sum'
        }).round(2)
        
        customer_stats.columns = ['Total Spent', 'Avg Order Value', 'Order Count', 'Items Purchased']
        customer_stats = customer_stats.sort_values('Total Spent', ascending=False)
        
        # Summary stats
        summary_stats = {
            "Active Customers": len(customer_stats),
            "Total Customers": len(clients_df),
            "Activity Rate": f"{(len(customer_stats)/len(clients_df)*100):.1f}%" if len(clients_df) > 0 else "0%",
            "Avg Spend/Customer": f"${customer_stats['Total Spent'].mean():.2f}",
            "Top Customer Spend": f"${customer_stats['Total Spent'].max():.2f}",
            "Repeat Customer Rate": f"{(len(customer_stats[customer_stats['Order Count'] > 1])/len(customer_stats)*100):.1f}%"
        }
        
        pdf.add_summary_stats(summary_stats)
        
        # Top customers table
        pdf.add_professional_table(customer_stats.head(15).reset_index(), "🏆 Top 15 Customers")
    
    return pdf_to_bytes(pdf)

def generate_category_performance(company_name, company_address, company_phone, company_email, start_date, end_date):
    """Generate category performance report"""
    pdf = ProfessionalPDF(company_name, company_address, company_phone, company_email)
    pdf.add_page()
    
    sales_df = data.load_sales()
    inventory_df = data.load_inventory()
    
    # Filter and merge data
    sales_df['Date'] = pd.to_datetime(sales_df['Date'])
    period_sales = sales_df[(sales_df['Date'] >= pd.to_datetime(start_date)) & 
                           (sales_df['Date'] <= pd.to_datetime(end_date))]
    
    period_sales['Total Price'] = pd.to_numeric(period_sales['Total Price'], errors='coerce')
    period_sales['Quantity Sold'] = pd.to_numeric(period_sales['Quantity Sold'], errors='coerce')
    
    # Merge with inventory to get categories
    sales_with_category = period_sales.merge(inventory_df[['Item Name', 'Category']], 
                                           left_on='Item', right_on='Item Name', how='left')
    
    pdf.add_title("📊 Category Performance Report", 
                 f"Period: {start_date.strftime('%B %d, %Y')} - {end_date.strftime('%B %d, %Y')}")
    
    if not sales_with_category.empty:
        # Category performance
        category_performance = sales_with_category.groupby('Category').agg({
            'Total Price': 'sum',
            'Quantity Sold': 'sum',
            'Item': 'count'
        }).round(2)
        category_performance.columns = ['Revenue', 'Units Sold', 'Orders']
        category_performance['Avg Order Value'] = (category_performance['Revenue'] / category_performance['Orders']).round(2)
        category_performance = category_performance.sort_values('Revenue', ascending=False)
        
        # Category inventory status
        inventory_by_category = inventory_df.groupby('Category').agg({
            'Quantity': 'sum',
            'Item Name': 'count'
        })
        inventory_by_category.columns = ['Stock Quantity', 'Product Count']
        
        # Combine data
        combined_analysis = category_performance.merge(inventory_by_category, left_index=True, right_index=True, how='outer').fillna(0)
        
        pdf.add_professional_table(combined_analysis.reset_index(), "📈 Category Performance Analysis")
    
    return pdf_to_bytes(pdf)

def pdf_to_bytes(pdf):
    """Convert PDF object to bytes using temporary file"""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        temp_filename = tmp_file.name
    
    try:
        pdf.output(temp_filename)
        with open(temp_filename, 'rb') as f:
            pdf_bytes = f.read()
        return pdf_bytes
    finally:
        if os.path.exists(temp_filename):
            os.unlink(temp_filename)
