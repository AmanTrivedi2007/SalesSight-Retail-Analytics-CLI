import os
from datetime import datetime

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

timestamp = datetime.now()

print("===== Welcome to Sales Data Analysis Program =====")
print("This program will help you analyze sales data and generate insights.")
print("please enter The asked infromation By the Program: ")

def data_loder(file_path):
    encs = [
        "UTF-8",
        "UTF-16",
        "UTF-32",
        "ASCII",
        "ISO-8859-1",
        "ISO-8859-15",
        "Windows-1252",
        "Big5",
        "GB2312",
        "Shift_JIS",
        "EUC-JP",
        "KOI8-R",
        "MacRoman",
        "IBM850",
        "ISO-2022-JP",
    ]

    if not os.path.exists(file_path):
        print("File not found PLease recheck your file path")
        return None

    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    # Helper: ensure Tax Amount exists to avoid KeyError downstream
    def ensure_tax_amount(df: pd.DataFrame) -> pd.DataFrame:
        if 'Tax Amount' in df.columns:
            return df
        # try aliases (case-insensitive)
        normalized = {c.strip().lower(): c for c in df.columns}
        for alias in ['Tax Amount', 'Tax', 'GST', 'VAT']:
            key = alias.strip().lower()
            if key in normalized:
                df['Tax Amount'] = df[normalized[key]]
                return df
        # approximate if possible: Tax ≈ Total - (Unit*Qty) - Shipping + Discount
        def col(name):
            return normalized.get(name.strip().lower())
        up = col('Unit Price')
        qty = col('Quantity Sold')
        ship = col('Shipping Charges')
        disc = col('Discount Applied')
        tot = col('Total Amount')
        if up and qty and ship and disc and tot:
            try:
                base = df[up].astype(float) * df[qty].astype(float)
                approx = df[tot].astype(float) - base - df[ship].astype(float) + df[disc].astype(float)
                df['Tax Amount'] = approx.clip(lower=0)
                return df
            except Exception:
                pass
        # fallback to zero column to avoid crashes
        df['Tax Amount'] = 0.0
        return df

    if ext in [".csv", ".txt"]:
        # Try encodings for CSV-like files
        for enc in encs:
            try:
                df = pd.read_csv(file_path, encoding=enc)

                # Core columns validation (case-insensitive)
                required = ['Total Amount', 'Net Revenue', 'Discount Applied', 'Category', 'Delivery Status', 'Payment Method']
                normalized = {c.strip().lower(): c for c in df.columns}
                missing_core = [col for col in required if col.strip().lower() not in normalized]

                # Ensure Tax Amount present
                df = ensure_tax_amount(df)

                if missing_core:
                    print(f"Error: Missing required columns: {', '.join(missing_core)}")
                    print("Available columns in your file:", ', '.join(df.columns))
                    return None

                print("File Load success - Columns validated")
                return df
            except UnicodeDecodeError:
                continue
            except Exception as e:
                print(f"Error reading file: {str(e)}")
                continue
        print("Unable to decode the file with common encodings. Please supply a UTF-8/compatible CSV.")
        return None

    elif ext in [".xlsx", ".xls"]:
        # Excel does not support encoding param
        try:
            df = pd.read_excel(file_path)

            # Core columns validation (case-insensitive)
            required = ['Total Amount', 'Net Revenue', 'Discount Applied', 'Category', 'Delivery Status', 'Payment Method']
            normalized = {c.strip().lower(): c for c in df.columns}
            missing_core = [col for col in required if col.strip().lower() not in normalized]

            # Ensure Tax Amount present
            df = ensure_tax_amount(df)

            if missing_core:
                print(f"Error: Missing required columns: {', '.join(missing_core)}")
                print("Available columns in your file:", ', '.join(df.columns))
                return None

            print("File Load success - Columns validated")
            return df
        except Exception as e:
            print("Failed to read Excel file. Please verify the file is a valid Excel document.")
            return None
    else:
        print("Unsupported file type. Please provide a CSV or Excel file.")
        return None

import pandas as pd

def handle_missing_values(df):
    """
    Handles missing values in a sales dataset by filling in appropriate columns
    with mean, mode, or default values. Leaves identifier and date columns untouched.
    """
    # Columns to fill with mean (numeric)
    mean_fill_cols = [
        "Quantity Sold",
        "Unit Price",
        "Total Amount",
        "Discount Applied",
        "Shipping Charges",
        "Net Revenue",
        "Stock Level",
        "Profit Margin"
    ]
    
    # Columns to fill with mode (categorical)
    mode_fill_cols = [
        "Currency",
        "Payment Method",
        "Fulfilled By",
        "Delivery Status",
        "Warehouse Location",
        "Shipping Partner",
        "Customer Region",
        "Sales Channel",
        "Category",
        "Brand"
    ]
    
    # Fill numeric columns with mean
    for col in mean_fill_cols:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].mean())
    
    # Fill categorical columns with mode
    for col in mode_fill_cols:
        if col in df.columns:
            mode_val = df[col].mode()
            if not mode_val.empty:
                df[col] = df[col].fillna(mode_val[0])
    
    # Optional: Fill missing product or customer names with "Unknown"
    if "Product Name" in df.columns:
        df["Product Name"] = df["Product Name"].fillna("Unknown")
    if "Customer Name" in df.columns:
        df["Customer Name"] = df["Customer Name"].fillna("Unknown")

    return df



def providing_info(df):
    print(df.info())

def providing_drscription(df):
    print(df.describe())

def report_maker(df):
    total_tax_paid = df['Tax Amount'].sum()
    total_amount_sold = df['Total Amount'].sum()
    net_revenue = df['Net Revenue'].sum()
    average_order_value = df['Total Amount'].mean()
    average_discount_applied = df['Discount Applied'].mean()
    total_discount_given = df['Discount Applied'].sum()

    max_sales = df.groupby('Category')['Total Amount'].sum()
    max_sales2 = df.groupby('Delivery Status')['Total Amount'].sum()
    payment_sum = df.groupby('Payment Method')['Total Amount'].sum()
    avergae_order_values_category = df.groupby('Category')['Total Amount'].mean()

    sales_report = f"""
============================================================
🧾 SALES PERFORMANCE SUMMARY REPORT
============================================================
📅 Report Generated On: {timestamp}
👤 Analyst: Aman
------------------------------------------------------------
🔹 FINANCIAL OVERVIEW
------------------------------------------------------------
• Total Tax Paid: ₹{total_tax_paid:,.2f}
• Total Amount Sold: ₹{total_amount_sold:,.2f}
• Net Revenue Generated: ₹{net_revenue:,.2f}
• Total Discount Given: ₹{total_discount_given:,.2f}
------------------------------------------------------------
📊 AVERAGE METRICS
------------------------------------------------------------
• Average Order Value: ₹{average_order_value:,.2f}
• Average Discount Applied per Order: ₹{average_discount_applied:,.2f}
------------------------------------------------------------
📦 SALES BY CATEGORY
------------------------------------------------------------
{max_sales.to_string()}
------------------------------------------------------------
🚚 SALES BY DELIVERY STATUS
------------------------------------------------------------
{max_sales2.to_string()}
------------------------------------------------------------
💳 SALES BY PAYMENT METHOD
------------------------------------------------------------
{payment_sum.to_string()}
------------------------------------------------------------
📈 AVERAGE ORDER VALUE BY CATEGORY
------------------------------------------------------------
{avergae_order_values_category.to_string()}
============================================================
📌 NOTES
============================================================
This report provides a consolidated view of sales performance across key dimensions including product category, delivery efficiency, and payment trends. It is designed to support strategic decisions in inventory planning, marketing optimization, and customer engagement.
End of Report
============================================================
"""
    with open('Sales_report.txt', 'a', encoding='utf-8') as file:
        file.write(sales_report)

# Put these two lines near the top of the file BEFORE importing pyplot:
# import matplotlib
# matplotlib.use('Agg')

def generate_sales_report(df):
    import matplotlib
    matplotlib.use('Agg')  # force non-GUI backend for saving
    import matplotlib.pyplot as plt
    import os

    # Create output directory (absolute path helps visibility)
    output_dir = os.path.abspath("sales_graphs")
    os.makedirs(output_dir, exist_ok=True)

    # Convert Order Date to datetime safely
    df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')

    def savefig_safe(path):
        plt.savefig(path, format='png', dpi=150, bbox_inches='tight')
        plt.close()
        if not os.path.exists(path) or os.path.getsize(path) == 0:
            print(f"Warning: failed to write figure: {path}")
        else:
            print(f"Saved: {path}")

    # -------------------- BAR CHART: Total Sales by Category --------------------
    category_sales = df.groupby('Category')['Total Amount'].sum().sort_values(ascending=False)
    plt.figure(figsize=(10, 6))
    category_sales.plot(kind='bar', color='skyblue')
    plt.title("Total Sales by Category")
    plt.xlabel("Category")
    plt.ylabel("Total Sales")
    plt.tight_layout()
    savefig_safe(os.path.join(output_dir, 'bar_sales_by_category.png'))

    # -------------------- PIE CHART: Payment Method Distribution --------------------
    payment_distribution = df['Payment Method'].value_counts()
    plt.figure(figsize=(8, 8))
    payment_distribution.plot(kind='pie', autopct='%1.1f%%', startangle=140)
    plt.title("Payment Method Distribution")
    plt.ylabel("")
    plt.tight_layout()
    savefig_safe(os.path.join(output_dir, 'pie_payment_methods.png'))

    # -------------------- LINE CHART: Net Revenue Over Time --------------------
    revenue_over_time = df.groupby(df['Order Date'].dt.to_period('M'))['Net Revenue'].sum()
    revenue_over_time.index = revenue_over_time.index.to_timestamp()
    plt.figure(figsize=(12, 6))
    revenue_over_time.plot(kind='line', marker='o', color='green')
    plt.title("Net Revenue Over Time")
    plt.xlabel("Month")
    plt.ylabel("Net Revenue")
    plt.grid(True)
    plt.tight_layout()
    savefig_safe(os.path.join(output_dir, 'line_net_revenue_over_time.png'))

    # -------------------- BAR CHART: Sales by Delivery Status --------------------
    delivery_status_sales = df.groupby('Delivery Status')['Total Amount'].sum().sort_values(ascending=False)
    plt.figure(figsize=(8, 5))
    delivery_status_sales.plot(kind='bar', color='orange')
    plt.title("Sales by Delivery Status")
    plt.xlabel("Delivery Status")
    plt.ylabel("Total Sales")
    plt.tight_layout()
    savefig_safe(os.path.join(output_dir, 'bar_sales_by_delivery_status.png'))

    # -------------------- BAR CHART: Sales by Region --------------------
    region_sales = df.groupby('Customer Region')['Total Amount'].sum().sort_values(ascending=False)
    plt.figure(figsize=(10, 6))
    region_sales.plot(kind='bar', color='purple')
    plt.title("Sales by Region")
    plt.xlabel("Region")
    plt.ylabel("Total Sales")
    plt.tight_layout()
    savefig_safe(os.path.join(output_dir, 'bar_sales_by_region.png'))

    # -------------------- BAR CHART: Top-Selling Products --------------------
    top_products = df.groupby('Product Name')['Quantity Sold'].sum().sort_values(ascending=False).head(10)
    plt.figure(figsize=(10, 6))
    top_products.plot(kind='bar', color='teal')
    plt.title("Top 10 Best-Selling Products")
    plt.xlabel("Product Name")
    plt.ylabel("Units Sold")
    plt.tight_layout()
    savefig_safe(os.path.join(output_dir, 'bar_top_selling_products.png'))


    # -------------------- Summary Statistics --------------------
    total_sales = df['Total Amount'].sum()
    net_revenue = df['Net Revenue'].sum()
    average_order_value = df['Total Amount'].mean()
    average_discount = df['Discount Applied'].mean()
    total_discount = df['Discount Applied'].sum()
    total_shipping_charges = df['Shipping Charges'].sum()

    print("📈 SALES DATA SUMMARY")
    print(f"Total Sales: ₹{total_sales:,.2f}")
    print(f"Net Revenue: ₹{net_revenue:,.2f}")
    print(f"Average Order Value: ₹{average_order_value:,.2f}")
    print(f"Average Discount Applied: ₹{average_discount:,.2f}")
    print(f"Total Discount Given: ₹{total_discount:,.2f}")
    print(f"Total Shipping Charges: ₹{total_shipping_charges:,.2f}")

sales_data_columns = [
    "Order ID",
    "Order Date",
    "Customer ID",
    "Customer Name",
    "Product ID / SKU",
    "Product Name",
    "Category",
    "Brand",
    "Quantity Sold",
    "Unit Price",
    "Total Amount",
    "Discount Applied",
    "Shipping Charges",
    "Net Revenue",
    "Currency",
    "Payment Method",
    "Fulfilled By",
    "Delivery Status",
    "Delivery Date",
    "Warehouse Location",
    "Shipping Partner",
    "Customer Region",
    "Stock Level",
    "Profit Margin",
    "Sales Channel",
]

df = None  # will hold loaded dataframe

while True:
    print("please enter the asked inforamtion: ")
    print("\n")

    print(sales_data_columns)
    print("\n")
    print("\n")
    print("please make sure that your datra is in the given fromate or atlest \n have the name of the filed in the way provided ")
    print("\n")
    print("\n")

    validation = input("would you like to procide enter yes to continue or enter no to stop :").lower().strip()

    if validation == 'yes':
        input1 = input("please  enter U to upload  your document: ").strip()

        if input1.lower() == 'u':
            path_input = input('please enter your file path which you would like to analyse: ').strip()
            df = data_loder(path_input)
            if df is not None:
                print("your data has been loaded succesfully ")
                print("\nColumns in your data:")
                print(df.columns.tolist())
            else:
                print("data load failed, please try again")
                continue
        else:
            print("please enter corect option")
            continue

        validation2 = input("would you like to proceed with the data yes/no : ").lower().strip()
        if validation2 == 'yes':  # run menu loop
            while True:
                print("please enter 1 to see the information about the table: ")
                print("please enter 2 to see the overview analysis of the data")
                print("please enter 3 to generate the analysis report and save it to the system")
                print("please enter q to exit the program ")
                menu_choice = input("please enter your option ").lower().strip()

                if menu_choice == '1':
                    print("you have opted to see the information of the table ")
                    providing_info(df)
                elif menu_choice == '2':
                    print("you have opted to see the description of the data ")
                    providing_drscription(df)
                elif menu_choice == '3':
                    print("report is ready!")
                    handle_missing_values(df)
                    print("Filled the missing values!!")
                    report_maker(df)
                    generate_sales_report(df)
                    print("report saved!")
                elif menu_choice == 'q':
                    print("Thank you for using the program ")
                    break
                else:
                    print("please select from the given options")
                    continue

        elif validation2 == 'no':
            print("Thank you for using the program")
            continue
        else:
            print("please enter correct option ")
            continue

    elif validation == 'no':
        print("thank you for using the program")
        break
    else:
        print("please enter the correct option")
        continue
