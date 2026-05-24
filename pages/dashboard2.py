import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Variance PNL", layout="wide")
st.title("📉 Variance Level PNL")

# Load & prep data
@st.cache_data
def load_data():
    df = pd.read_excel("data/kitchen_data.xlsx", engine="openpyxl")
    df.columns = df.columns.str.strip().str.upper().str.replace(" ", "_")
    df["MONTH"] = pd.to_datetime(df["MONTH"], format="%b-%Y", errors="coerce")
    df["MONTH_LABEL"] = df["MONTH"].dt.strftime("%b %Y")
    if "EBITDA" not in df.columns:
        df.rename(columns={"KITCHEN_EBITDA": "EBITDA"}, inplace=True)

    df["VARIANCE%"] = (df["VARIANCE"] / df["NET_REVENUE"].replace(0, np.nan) * 100).round(2)

    df["VARIANCE_CATEGORY"] = pd.cut(
        df["VARIANCE%"],
        bins=[-np.inf, 2, 3, 5, np.inf],
        labels=["(a) Var < 2%", "(b) Var 2% to 3%", "(c) Var 3% to 5%", "(d) Var > 5%"]
    )

    df["REVENUE_RANGE"] = pd.cut(
        df["NET_REVENUE"],
        bins=[-np.inf, 1500000, 2500000, 3500000, 4500000, np.inf],
        labels=["(a) Below INR 15 lacs", "(b) INR 15 to 25 lacs", "(c) INR 25 to 35 lacs",
                "(d) INR 35 to 45 lacs", "(e) Above INR 45 lacs"]
    )
    return df

df = load_data()

st.subheader("🔽 Variance Category Filter")
all_cats = ["(a) Var < 2%", "(b) Var 2% to 3%", "(c) Var 3% to 5%", "(d) Var > 5%"]
sel_cats = st.multiselect("Select Variance Category", all_cats, default=all_cats)
f = df[df["VARIANCE_CATEGORY"].isin(sel_cats)].copy()

st.info(f" **{f['STORE'].nunique()} stores** match the selected variance filter.")
st.divider()

month_order = (f[["MONTH","MONTH_LABEL"]].drop_duplicates()
                .sort_values("MONTH", ascending=False)["MONTH_LABEL"].tolist())

# SUMMARY TABLE 1: Average Variance % by Revenue Category × Month

st.subheader("Summary Table 1 — Average Variance % by Revenue Category")
st.caption("Average variance % of kitchens under each revenue category, by month")

pivot1 = f.pivot_table(
    index="REVENUE_COHORT",
    columns="MONTH_LABEL",
    values="VARIANCE%",
    aggfunc="mean"
).reindex(month_order, axis=1)

pivot1.loc["Total Average"] = f.groupby("MONTH_LABEL")["VARIANCE%"].mean().reindex(month_order)

st.dataframe(
    pivot1.style.format("{:.2f}%", na_rep="-"),
    use_container_width=True
)

st.divider()

# TABLE 2: Store Count by Revenue Range

st.subheader("Summary Table 2 — Store Count by Revenue Range")
st.caption("Count of kitchen stores:")

pivot2 = f.pivot_table(
    index="REVENUE_RANGE",
    columns="MONTH_LABEL",
    values="STORE",
    aggfunc="count",
    fill_value=0
).reindex(month_order, axis=1)

rev_range_order = [
    "(a) Below INR 15 lacs",
    "(b) INR 15 to 25 lacs",
    "(c) INR 25 to 35 lacs",
    "(d) INR 35 to 45 lacs",
    "(e) Above INR 45 lacs"
]
pivot2 = pivot2.reindex([r for r in rev_range_order if r in pivot2.index])

pivot2.loc["Grand Total"] = pivot2.sum()

st.dataframe(
    pivot2.style.format("{:.0f}"),
    use_container_width=True
)

