# Cloud Kitchen PNL Dashboard

A comprehensive Streamlit-based analytics dashboard for analyzing Profit & Loss (PNL) and food waste variance across cloud kitchen stores.

## 📋 Overview

This project provides two interactive dashboards:

1. **Kitchen Level PNL Dashboard** — Store-level financial analysis with multi-dimensional filters
2. **Variance Level PNL Dashboard** — Food waste variance analysis across revenue categories and ranges

## 🎯 Features

### Dashboard 1: Kitchen Level PNL
- Filter by Store, Zone, Month, Revenue Cohort, CM Cohort, EBITDA Category
- Range-based filters for EBITDA, Contribution Margin, and Net Revenue
- Kitchen snapshot pivot table showing Net Revenue, GM%, CM%, EBITDA by month
- Top performing stores analysis
- EBITDA trends over time
- Key metrics cards (Total Revenue, Average GM%, Average CM%, EBITDA, Store Count)

### Dashboard 2: Variance Level PNL
- **Summary Table 1:** Average Variance % by Revenue Category across months
- **Summary Table 2:** Store Count by Revenue Range across months
- Variance category filter (Var < 2%, Var 2-3%, Var 3-5%, Var > 5%)
- Grand total calculations for quick insights

## 🛠️ Tech Stack

- **Python:** 3.11.x
- **Streamlit:** 1.35.0 — Web app framework
- **Pandas:** 2.2.2 — Data manipulation
- **Plotly:** 5.22.0 — Interactive visualizations
- **NumPy:** 1.26.4 — Numerical computations
- **OpenPyXL:** 3.1.2 — Excel file handling

## 📦 Installation

### Prerequisites
- Python 3.11 or higher
- Git

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/cloud-kitchen-dashboard.git
cd cloud-kitchen-dashboard
```

### Step 2: Create Virtual Environment
```bash
python3.11 -m venv venv

# Activate on Mac/Linux:
source venv/bin/activate

# Activate on Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Add Data File
Place your kitchen data Excel file at: data/kitchen_data.xlsx

Required columns:
- MONTH, CITY, STORE, STATUS, ZONE MAPPING
- ORDER COUNT, CART SALES, DISCOUNT, NET REVENUE
- IDEAL FOOD COST, GROSS MARGIN, KITCHEN EBITDA, VARIANCE
- REVENUE COHORT, CM COHORT, EBITDA CATEGORY, EBITDA COHORT

### Step 5: Run the Application
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 📁 Project Structure

cloud-kitchen-dashboard/
├── app.py                          # Home page / Landing page
├── pages/
│   ├── 1_Kitchen_PNL.py           # Kitchen Level PNL Dashboard
│   └── 2_Variance_PNL.py          # Variance Level PNL Dashboard
├── data/
│   └── kitchen_data.xlsx          # Input data file (add your data here)
├── analysis/
│   └── EDA.ipynb                  # Exploratory Data Analysis notebook
├── requirements.txt               # Python dependencies
└── README.md                      # This file

## 🚀 Usage

### Home Page (`app.py`)
- Welcome page with overview of dashboards
- Navigation menu in sidebar

### Kitchen PNL Dashboard (`pages/1_Kitchen_PNL.py`)
1. Use sidebar filters to narrow down data
2. View KPI cards for quick metrics
3. Check Kitchen Snapshot pivot table for detailed store performance
4. Explore charts for trends and distributions
5. Download filtered data as CSV

**Available Filters:**
- Store (single select)
- Month (multi-select)
- Zone (single select)
- Revenue Cohort (single select)
- CM Cohort (single select)
- EBITDA Category (single select)
- EBITDA Cohort (single select)
- EBITDA Range (slider)
- CM Range (slider)
- Net Revenue Range (slider)

### Variance PNL Dashboard (`pages/2_Variance_PNL.py`)
1. Select Variance Categories at the top
2. View Summary Table 1: Average variance % by revenue category and month
3. View Summary Table 2: Store count by revenue range and month
4. Download filtered data as CSV

**Summary Tables:**
- **Table 1:** Shows average waste percentage (variance %) for each revenue category
- **Table 2:** Shows count of stores in each revenue range bucket

## 🔄 Performance Optimization

Both dashboards use Streamlit's `@st.cache_data` decorator for data caching:
- Data is cached for optimal performance
- Automatic refresh on file changes
- Ideal for real-time data updates

## 📊 Data Preparation

### Derived Columns (Auto-calculated)
The app automatically derives missing columns:
- **GM%** = (Gross Margin / Net Revenue) × 100
- **CM%** = (Contribution Margin / Net Revenue) × 100
- **EBITDA%** = (EBITDA / Net Revenue) × 100
- **VARIANCE%** = (Variance / Net Revenue) × 100

### Variance Categories (Fixed Buckets)
- (a) Var < 2%
- (b) Var 2% to 3%
- (c) Var 3% to 5%
- (d) Var > 5%

### Revenue Ranges (Range-based)
- (a) Below INR 15 lacs
- (b) INR 15 to 25 lacs
- (c) INR 25 to 35 lacs
- (d) INR 35 to 45 lacs
- (e) Above INR 45 lacs

## 📈 Analysis Notebook

The `analysis/EDA.ipynb` notebook includes:
- Data exploration and summary statistics
- Missing value analysis
- Revenue distribution
- EBITDA category breakdown
- Monthly trends
- City-level performance
- Variance analysis
- Correlation heatmap
- Store lifecycle analysis

Run it with:
```bash
jupyter notebook analysis/EDA.ipynb
```

## 🐛 Troubleshooting

### Issue: "FileNotFoundError: data/kitchen_data.xlsx"
**Solution:** Ensure your Excel file is placed in the `data/` folder with exact name `kitchen_data.xlsx`

### Issue: "AttributeError: 'Styler' object has no attribute 'applymap'"
**Solution:** This is a pandas 2.1+ compatibility issue. Already fixed in this version.

### Issue: App runs slowly
**Solution:** Data is cached automatically. Clear cache with:
```bash
streamlit cache clear
```

## 📝 Notes

- The dashboard auto-standardizes column names (strips spaces, converts to uppercase)
- All monetary values are in INR (₹)
- Month labels are formatted as "MMM YYYY" (e.g., "Mar 2025")
- Filters are independent — changes in one don't affect others
- Each page loads data independently for modularity


## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit changes (`git commit -m 'Add your feature'`)
4. Push to branch (`git push origin feature/your-feature`)
5. Open a Pull Request


## 🎯 Future Enhancements

- [ ] Add predictive analytics for EBITDA forecasting
- [ ] Implement real-time data refresh from database
- [ ] Add more detailed cost breakdowns
- [ ] Export dashboards as PDF reports
- [ ] Add user authentication
- [ ] Implement data quality checks
- [ ] Add anomaly detection for unusual variance patterns

---

**Last Updated:** 2026
**Python Version:** 3.11.x
**Streamlit Version:** 1.35.0
