import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Kitchen PNL", layout="wide")
st.title("📊 Kitchen Level PNL")

# Load & prep data
@st.cache_data
def load_data():
    df = pd.read_excel("data/kitchen_data.xlsx", engine="openpyxl")
    df.columns = df.columns.str.strip().str.upper().str.replace(" ", "_")
    df["MONTH"] = pd.to_datetime(df["MONTH"], format="%b-%Y", errors="coerce")
    df["MONTH_LABEL"] = df["MONTH"].dt.strftime("%b %Y")

    # In case columns are missing
    if "GM%" not in df.columns:
        df["GM%"] = (df["GROSS_MARGIN"] / df["NET_REVENUE"].replace(0, np.nan) * 100).round(2)
    if "EBITDA" not in df.columns:
        df.rename(columns={"KITCHEN_EBITDA": "EBITDA"}, inplace=True)
    if "CM" not in df.columns:
        df["CM"] = df.get("CONTRIBUTION_MARGIN", df["EBITDA"])
    if "CM%" not in df.columns:
        df["CM%"] = (df["CM"] / df["NET_REVENUE"].replace(0, np.nan) * 100).round(2)

    return df

df = load_data()

#Sidebar filters

st.sidebar.header("Filters")

sel_store = st.sidebar.selectbox("Store", ["All"] + sorted(df["STORE"].dropna().unique().tolist()))
sel_month = st.sidebar.multiselect("Month", sorted(df["MONTH_LABEL"].dropna().unique().tolist(), reverse=True))
sel_zone  = st.sidebar.selectbox("Zone", ["All"] + sorted(df["ZONE_MAPPING"].dropna().unique().tolist()))

sel_rev_cohort   = st.sidebar.selectbox("Revenue Cohort",  ["All"] + sorted(df["REVENUE_COHORT"].dropna().unique().tolist()))
sel_cm_cohort    = st.sidebar.selectbox("CM Cohort",       ["All"] + sorted(df["CM_COHORT"].dropna().unique().tolist()))
sel_ebitda_cat   = st.sidebar.selectbox("EBITDA Category", ["All"] + sorted(df["EBITDA_CATEGORY"].dropna().unique().tolist()))
sel_ebitda_cohort = st.sidebar.selectbox("EBITDA Cohort",  ["All"] + sorted(df["EBITDA_COHORT"].dropna().unique().tolist()))

ebitda_min, ebitda_max = int(df["EBITDA"].min()), int(df["EBITDA"].max())
sel_ebitda = st.sidebar.slider("EBITDA Range (₹)", ebitda_min, ebitda_max, (ebitda_min, ebitda_max))

rev_min, rev_max = int(df["NET_REVENUE"].min()), int(df["NET_REVENUE"].max())
sel_rev = st.sidebar.slider("Net Revenue Range (₹)", rev_min, rev_max, (rev_min, rev_max))

cm_min, cm_max = int(df["CM"].min()), int(df["CM"].max())
sel_cm = st.sidebar.slider("CM Range (₹)", cm_min, cm_max, (cm_min, cm_max))

# Filter Logic
f = df.copy()
if sel_store != "All":        f = f[f["STORE"] == sel_store]
if sel_month:                 f = f[f["MONTH_LABEL"].isin(sel_month)]
if sel_zone != "All":         f = f[f["ZONE_MAPPING"] == sel_zone]
if sel_rev_cohort != "All":   f = f[f["REVENUE_COHORT"] == sel_rev_cohort]
if sel_cm_cohort != "All":    f = f[f["CM_COHORT"] == sel_cm_cohort]
if sel_ebitda_cat != "All":   f = f[f["EBITDA_CATEGORY"] == sel_ebitda_cat]
if sel_ebitda_cohort != "All":f = f[f["EBITDA_COHORT"] == sel_ebitda_cohort]
f = f[(f["EBITDA"] >= sel_ebitda[0]) & (f["EBITDA"] <= sel_ebitda[1])]
f = f[(f["NET_REVENUE"] >= sel_rev[0]) & (f["NET_REVENUE"] <= sel_rev[1])]
f = f[(f["CM"] >= sel_cm[0]) & (f["CM"] <= sel_cm[1])]

# Summary of data on top
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Net Revenue",  f"₹{f['NET_REVENUE'].sum():,.0f}")
c2.metric("Avg GM%",      f"{f['GM%'].mean():.1f}%")
c3.metric("Avg CM%",      f"{f['CM%'].mean():.1f}%")
c4.metric("Total EBITDA", f"₹{f['EBITDA'].sum():,.0f}")
c5.metric("Stores",       f['STORE'].nunique())

st.divider()

# Pivot table
st.subheader("Kitchen Snapshot")

if f.empty:
    st.warning("No data for selected filters.")
else:
    month_order = (f[["MONTH","MONTH_LABEL"]].drop_duplicates()
                    .sort_values("MONTH", ascending=False)["MONTH_LABEL"].tolist())

    pivot = f.pivot_table(
        index="STORE",
        columns="MONTH_LABEL",
        values=["NET_REVENUE", "GM%", "CM%", "CM", "EBITDA"],
        aggfunc="sum"
    ).reindex(month_order, axis=1, level=1)

    st.dataframe(pivot.style.format("{:,.0f}", na_rep="-"), use_container_width=True, height=450)
