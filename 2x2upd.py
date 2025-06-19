import streamlit as st
import pandas as pd
import plotly.express as px

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="🚬 Smoking Dashboard", layout="wide")

# ── Sidebar Filters ────────────────────────────────────────────────────────────
st.sidebar.header("Filters")
df = pd.read_csv("smoking.csv")
years = sorted(df["Year"].astype(int).unique())
countries = sorted(df["Country"].unique())

# year range slider
yr_min, yr_max = st.sidebar.slider(
    "Period",
    min_value=years[0],
    max_value=years[-1],
    value=(years[0], years[-1])
)
# country multiselect
sel_countries = st.sidebar.multiselect(
    "Country",
    options=countries,
    default=countries
)

# filter data
df_f = df[
    (df["Year"] >= yr_min) &
    (df["Year"] <= yr_max) &
    (df["Country"].isin(sel_countries))
]

# ── Title & Metrics ────────────────────────────────────────────────────────────
st.title("🚬 Global Smoking Dashboard")
st.markdown("Explore global smoking prevalence in one view—no scrolling needed.")

col = "Data.Percentage.Total"
m1, m2, m3 = st.columns(3)
m1.metric("Records",      df_f.shape[0])
m2.metric("Countries",    df_f["Country"].nunique())
m3.metric("Avg Rate (%)", f"{df_f[col].mean():.1f}")

# ── 2×2 Grid of Charts ─────────────────────────────────────────────────────────
r1c1, r1c2 = st.columns(2)

with r1c1:
    # Map
    mdf = df_f.groupby("Country")[col].mean().reset_index()
    fig_map = px.choropleth(
        mdf,
        locations="Country",
        locationmode="country names",
        color=col,
        title="Avg. Rate by Country"
    )
    fig_map.update_layout(
        height=200,
        margin=dict(t=30, b=10, l=10, r=10),
        title_x=0.5
    )
    st.plotly_chart(fig_map, use_container_width=True)

with r1c2:
    # Gender comparison
    if {"Data.Percentage.Male","Data.Percentage.Female"} <= set(df.columns):
        gdf = df_f.melt(
            id_vars=["Country","Year"],
            value_vars=["Data.Percentage.Male","Data.Percentage.Female"],
            var_name="Gender",
            value_name="Rate"
        )
        gdf["Gender"] = gdf["Gender"].str.replace("Data.Percentage.","")
        fig_box = px.box(
            gdf,
            x="Gender",
            y="Rate",
            title="Rate by Gender"
        )
        fig_box.update_layout(
            height=200,
            margin=dict(t=30, b=10, l=10, r=10),
            title_x=0.5
        )
        st.plotly_chart(fig_box, use_container_width=True)

r2c1, r2c2 = st.columns(2)

with r2c1:
    # Trend over time
    tdf = df_f.groupby("Year")[col].mean().reset_index()
    fig_line = px.line(
        tdf,
        x="Year",
        y=col,
        markers=True,
        title="Avg. Rate Over Time"
    )
    fig_line.update_layout(
        height=200,
        margin=dict(t=30, b=10, l=10, r=10),
        title_x=0.5
    )
    st.plotly_chart(fig_line, use_container_width=True)

with r2c2:
    # Top-10 countries
    top10 = df_f.groupby("Country")[col].mean().nlargest(10).reset_index()
    fig_bar = px.bar(
        top10,
        x="Country",
        y=col,
        title="Top 10 Countries"
    )
    fig_bar.update_layout(
        height=200,
        margin=dict(t=30, b=10, l=10, r=10),
        title_x=0.5
    )
    st.plotly_chart(fig_bar, use_container_width=True)
