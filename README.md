SalesSight: Retail Analytics CLI 🚀
A fast, user-friendly CLI that transforms CSV sales data into actionable insights. Generate executive-ready summaries and clean PNG charts for categories, payment methods, delivery status, regions, and top products—with robust column validation, encoding fallback, and safe date parsing. 📊✨

Why this tool
   Focused on CSV pipelines—no spreadsheet engine needed, zero Excel assumptions. 🎯

   Reliable runs on “real” exports: mixed encodings, varied headers, sparse data. 🛡️

   Direct, PNG-first visualization without GUI dependencies. 🖼️

Features
 Data loading

   CSV ingestion with multi-encoding fallback (UTF-8 → UTF-16 → others) 📥

   Case-insensitive column validation with clear error messages 🧭

 Automatic Tax Amount resolution:

   Accepts aliases like Tax/GST/VAT

   Approximates when missing via: Tax ≈ Total − (Unit×Qty) − Shipping + Discount

   Falls back to 0 to prevent crashes 🧩

Reporting

   Financial summary: Total Tax Paid, Total Amount, Net Revenue, Discounts 🧾

   Breakdowns by Category, Payment Method, Delivery Status; AOV by Category 📚

Charts (PNG)

   Category sales, payment distribution, revenue over time, delivery status, region, top products 📈

   Saved to sales_graphs/ with non-GUI backend and explicit PNG saves 🖨️

CLI UX

   Guided prompts: upload path, preview columns, choose actions, safe exits 🧑‍✈️

Data requirements (CSV only)
  Required columns (case-insensitive match):

   Total Amount, Net Revenue, Discount Applied, Category, Delivery Status, Payment Method

Recommended for richer outputs:

   Order Date, Unit Price, Quantity Sold, Shipping Charges, Product Name, Customer Region

Notes:

   Header must be the first row; avoid pre-header titles/merged cells in CSV exports

   Dates should be ISO-like strings (YYYY-MM-DD); parser is tolerant and safe 🗓️

How it works
   Start the script, choose “U” to upload, and paste a full path to a CSV file.

   The loader validates columns and resolves Tax Amount (via alias/approx/zero).

Menu options:

   1: DataFrame info (schema, dtypes, non-null counts)

   2: Descriptive stats (numeric summaries)

   3: Generate report + PNG charts

Outputs:

   Sales_report.txt appended in the project root

PNG charts inside sales_graphs/ (e.g., bar_sales_by_category.png) 🗂️

Troubleshooting
   Charts not saving

   Ensure write permissions; the app forces a non-GUI backend and saves .png files to sales_graphs/ with confirmation prints 📌

   “Missing required columns”

   The loader prints what’s missing and what it found. Rename headers in the CSV to match the expected names (case-insensitive) ✅

Encoding errors on CSV

   The loader retries common encodings. Prefer UTF-8 CSV exports when possible 🔁

Date parsing issues

   Non-parseable dates become NaT; the time-series chart uses month aggregation and will skip entirely null periods gracefully 🧠

Project structure
   sales_anan.py — CLI app (load → validate → analyze → export)

   Sales_report.txt — cumulative text summary

   sales_graphs/ — exported PNG charts 📂

Design notes
   Philosophy: keep inputs simple (CSV), validate early, fail informatively, and always produce actionable outputs (report + PNGs) 🔎

   Readability over cleverness: clear prompts, explicit filenames, and deterministic flows 📐

Roadmap
   Configurable column mapping for custom schemas

Optional HTML/Markdown report export

   Lightweight aggregation presets (e.g., weekly, quarterly) 📅

Contributing
   Fork → feature branch → PR with a clear description and small sample CSV for testing

   Keep dataset samples anonymized and minimal

   Prefer changes that preserve the current CLI flow and error messaging 🤝

License
   Add a LICENSE file (MIT or Apache-2.0 recommended) and reference it here for clarity 🏷️

   This README follows proven documentation patterns—clear intent, setup-free usage, strong troubleshooting, and future-friendly structure—optimized specifically for CSV-driven sales analytics in a CLI workflow. ✅


