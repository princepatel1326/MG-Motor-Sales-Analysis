 
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="MG Motor | Sales Intelligence",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "Data" / "cleaned_data.csv"
ASSETS = BASE_DIR / "Assets"
CARS = ASSETS / "cars"

RED = "#e31837"
MONTHS = {
    1: "January", 2: "February", 3: "March",
    4: "April", 5: "May", 6: "June",
    7: "July", 8: "August", 9: "September",
    10: "October", 11: "November", 12: "December"
}

# ==========================================
# 2. LOAD DATA
# ==========================================

@st.cache_data
def load_data():
    data = pd.read_csv(DATA_PATH)

    numeric_columns = [
        "units_sold",
        "estimated_revenue_inr_crore",
        "avg_ex_showroom_price_inr_lakh",
        "month_number"
    ]

    for col in numeric_columns:
        data[col] = pd.to_numeric(data[col], errors="coerce")

    data = data.dropna(subset=numeric_columns)
    data["month_number"] = data["month_number"].astype(int)

    return data


try:
    df = load_data()
except FileNotFoundError:
    st.error("Dataset not found. Check Data/cleaned_data.csv")
    st.stop()
except Exception as error:
    st.error(f"Unable to load dataset: {error}")
    st.stop()

required = [
    "model", "fuel_type", "units_sold",
    "estimated_revenue_inr_crore",
    "avg_ex_showroom_price_inr_lakh",
    "month_number"
]

missing = [col for col in required if col not in df.columns]

if missing:
    st.error(f"Missing columns: {missing}")
    st.stop()

# ==========================================
# 3. PREMIUM DESIGN
# ==========================================

st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top right, #25202a, #080a0e 45%);
    color: white;
}

.block-container {
    max-width: 1550px;
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

[data-testid="stSidebar"] {
    background: #090c11;
    border-right: 1px solid #34303a;
}

h1, h2, h3, p, label {
    color: #f5f5f5;
}

.hero {
    background: linear-gradient(100deg, #090b10 15%, #241018 65%, #090b10);
    border: 1px solid #64202d;
    border-radius: 18px;
    padding: 25px;
    margin-bottom: 22px;
}

.hero-title {
    font-size: 38px;
    font-weight: 900;
    letter-spacing: 2px;
}

.hero-subtitle {
    color: #c4c4c4;
    font-size: 15px;
    letter-spacing: 2px;
}

.section-title {
    font-size: 21px;
    font-weight: 800;
    margin-top: 22px;
    margin-bottom: 12px;
    border-left: 4px solid #e31837;
    padding-left: 12px;
}

.kpi-card {
    background: linear-gradient(145deg, #20232b, #101217);
    border: 1px solid #44313a;
    border-bottom: 3px solid #e31837;
    border-radius: 13px;
    padding: 18px;
    min-height: 120px;
    box-shadow: 0 8px 25px #0008;
}

.kpi-label {
    color: #aeb5c0;
    font-size: 12px;
    letter-spacing: 1px;
}

.kpi-value {
    color: white;
    font-size: 25px;
    font-weight: 850;
    margin-top: 12px;
}

.car-card {
    background: linear-gradient(145deg, #20242d, #101319);
    border: 1px solid #414650;
    border-radius: 13px;
    padding: 10px;
    text-align: center;
    min-height: 190px;
}

.car-name {
    color: white;
    font-size: 15px;
    font-weight: 800;
    margin-top: 8px;
}

.car-sales {
    color: #ff526b;
    font-size: 19px;
    font-weight: 900;
}

.insight-card {
    background: #171c25;
    border: 1px solid #3d333a;
    border-left: 4px solid #e31837;
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 10px;
}

div[data-testid="stMetric"] {
    background: #171c25;
    border: 1px solid #3d333a;
    border-radius: 10px;
    padding: 12px;
}

.stDownloadButton button {
    background: #e31837;
    color: white;
    border: none;
    border-radius: 8px;
}

hr {
    border-color: #34303a;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 4. CHART DESIGN
# ==========================================

def style_chart(fig, height=350):
    fig.update_layout(
        template="plotly_dark",
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white", family="Arial"),
        margin=dict(l=15, r=15, t=55, b=25),
        title_font_size=17
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.08)")
    return fig


# ==========================================
# 5. SIDEBAR
# ==========================================

with st.sidebar:
    if (ASSETS / "mg_logo.png").exists():
        st.image(str(ASSETS / "mg_logo.png"), width=130)
    else:
        st.markdown("# ◈ MG MOTOR")

    st.markdown("### DRIVE THE FUTURE")
    st.caption("SALES INTELLIGENCE")

    st.markdown("---")
    st.markdown("### ⚙️ Dashboard Filters")

    models = sorted(df["model"].dropna().unique())
    fuels = sorted(df["fuel_type"].dropna().unique())
    months = sorted(df["month_number"].unique())

    selected_models = st.multiselect(
        "Car Models", models, default=models
    )

    selected_fuels = st.multiselect(
        "Fuel Types", fuels, default=fuels
    )

    selected_months = st.multiselect(
        "Months",
        months,
        default=months,
        format_func=lambda x: MONTHS.get(x, str(x))
    )

    st.markdown("---")
    st.caption("MG MOTOR INDIA | 2025")

filtered_df = df[
    df["model"].isin(selected_models)
    & df["fuel_type"].isin(selected_fuels)
    & df["month_number"].isin(selected_months)
].copy()

if filtered_df.empty:
    st.warning("No records found. Please change your filters.")
    st.stop()

# ==========================================
# 6. HERO HEADER
# ==========================================

hero_image = ASSETS / "mg_hero.jpg"

if hero_image.exists():
    st.image(str(hero_image), use_container_width=True)

st.markdown("""
<div class="hero">
    <div class="hero-title">
        MG MOTOR <span style="color:#e31837;">INDIA</span>
    </div>
    <div style="font-size:25px;font-weight:700;">
        Sales Intelligence Dashboard
    </div>
    <div class="hero-subtitle">
        SMARTER INSIGHTS. STRONGER DRIVE.
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 7. KPI CARDS
# ==========================================

total_sales = filtered_df["units_sold"].sum()
total_revenue = filtered_df["estimated_revenue_inr_crore"].sum()
total_models = filtered_df["model"].nunique()
average_price = filtered_df["avg_ex_showroom_price_inr_lakh"].mean()

st.markdown(
    '<div class="section-title">BUSINESS OVERVIEW</div>',
    unsafe_allow_html=True
)

kpis = st.columns(4)

kpi_data = [
    ("🚘", "TOTAL CARS SOLD", f"{total_sales:,.0f}"),
    ("₹", "ESTIMATED REVENUE", f"₹{total_revenue:,.2f} Cr"),
    ("🚗", "CAR MODELS", str(total_models)),
    ("🏷️", "AVERAGE PRICE", f"₹{average_price:.2f} Lakh")
]

for col, (icon, label, value) in zip(kpis, kpi_data):
    col.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">{icon} &nbsp; {label}</div>
        <div class="kpi-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 8. MODEL SALES AND FUEL DISTRIBUTION
# ==========================================

model_sales = (
    filtered_df.groupby("model", as_index=False)["units_sold"]
    .sum().sort_values("units_sold", ascending=False)
)

fuel_sales = (
    filtered_df.groupby("fuel_type", as_index=False)["units_sold"]
    .sum()
)

st.markdown(
    '<div class="section-title">SALES PERFORMANCE</div>',
    unsafe_allow_html=True
)

left, right = st.columns([1.4, 1])

with left:
    fig = px.bar(
        model_sales.sort_values("units_sold"),
        x="units_sold",
        y="model",
        orientation="h",
        text="units_sold",
        color="units_sold",
        color_continuous_scale=["#571421", "#e31837"],
        title="Sales by Car Model"
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(coloraxis_showscale=False)
    st.plotly_chart(style_chart(fig), use_container_width=True)

with right:
    fig = px.pie(
        fuel_sales,
        names="fuel_type",
        values="units_sold",
        hole=0.62,
        title="Sales by Fuel Type",
        color_discrete_sequence=[
            "#e31837", "#63758d", "#15a887", "#ed9b35"
        ]
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(style_chart(fig), use_container_width=True)

# ==========================================
# 9. TOP THREE MODELS
# ==========================================

st.markdown(
    '<div class="section-title">🏆 TOP 3 BEST-SELLING MODELS</div>',
    unsafe_allow_html=True
)

top_three = model_sales.head(3)
top_cols = st.columns(3)

for col, (_, item) in zip(top_cols, top_three.iterrows()):
    model = item["model"]
    filename = model.lower().replace(" ", "_") + ".jpg"
    image_path = CARS / filename

    with col:
        if image_path.exists():
            st.image(str(image_path), use_container_width=True)
        else:
            st.markdown("## 🚘")

        st.markdown(f"**{model}**")
        st.markdown(f"<h3 style='color:#e31837'>{item['units_sold']:,.0f}</h3>",
                    unsafe_allow_html=True)
        st.caption("Units sold")

# ==========================================
# 10. MONTHLY SALES TREND
# ==========================================

st.markdown(
    '<div class="section-title">📈 MONTHLY SALES TREND</div>',
    unsafe_allow_html=True
)

monthly = (
    filtered_df.groupby("month_number", as_index=False)["units_sold"]
    .sum().sort_values("month_number")
)

monthly["month_name"] = monthly["month_number"].map(MONTHS)

fig = px.area(
    monthly,
    x="month_name",
    y="units_sold",
    markers=True,
    title="Monthly Vehicle Sales",
    color_discrete_sequence=[RED]
)
fig.update_traces(
    line=dict(width=3),
    fillcolor="rgba(227,24,55,0.22)"
)
st.plotly_chart(style_chart(fig, 390), use_container_width=True)

# ==========================================
# 11. MODEL PHOTO GALLERY
# ==========================================

st.markdown(
    '<div class="section-title">🚗 MG CAR MODELS PERFORMANCE</div>',
    unsafe_allow_html=True
)

gallery_cols = st.columns(3)

for index, (_, item) in enumerate(model_sales.iterrows()):
    model = item["model"]
    filename = model.lower().replace(" ", "_") + ".jpg"
    image_path = CARS / filename
    col = gallery_cols[index % 3]

    with col:
        with st.container(border=True):
            if image_path.exists():
                st.image(str(image_path), use_container_width=True)
            else:
                st.markdown("### 🚘")

            st.markdown(f"**{model}**")
            st.markdown(
                f"<span style='color:#ff526b;font-size:22px;font-weight:900'>"
                f"{item['units_sold']:,.0f}</span>",
                unsafe_allow_html=True
            )
            st.caption("Units Sold")

# ==========================================
# 12. REVENUE BY MODEL
# ==========================================

st.markdown(
    '<div class="section-title">💰 REVENUE INTELLIGENCE</div>',
    unsafe_allow_html=True
)

revenue = (
    filtered_df.groupby("model", as_index=False)
    ["estimated_revenue_inr_crore"].sum()
    .sort_values("estimated_revenue_inr_crore", ascending=False)
)

fig = px.bar(
    revenue,
    x="model",
    y="estimated_revenue_inr_crore",
    text_auto=".2f",
    title="Estimated Revenue by Model",
    color="estimated_revenue_inr_crore",
    color_continuous_scale=["#571421", "#e31837"]
)
fig.update_layout(coloraxis_showscale=False)
st.plotly_chart(style_chart(fig, 380), use_container_width=True)

# ==========================================
# 13. BUSINESS INSIGHTS
# ==========================================

st.markdown(
    '<div class="section-title">💡 BUSINESS INSIGHTS</div>',
    unsafe_allow_html=True
)

top_model = model_sales.iloc[0]["model"]
top_units = model_sales.iloc[0]["units_sold"]
top_fuel = fuel_sales.sort_values(
    "units_sold", ascending=False
).iloc[0]["fuel_type"]
top_revenue = revenue.iloc[0]["model"]

top_month = monthly.loc[monthly["units_sold"].idxmax()]

a, b = st.columns(2)

with a:
    st.markdown(f"""
    <div class="insight-card">
        🏆 <b>Best-Selling Model</b><br>
        {top_model} leads with {top_units:,.0f} units sold.
    </div>
    <div class="insight-card">
        ⚡ <b>Leading Fuel Type</b><br>
        {top_fuel} has the highest sales in the selected data.
    </div>
    """, unsafe_allow_html=True)

with b:
    st.markdown(f"""
    <div class="insight-card">
        📅 <b>Highest Sales Month</b><br>
        {top_month["month_name"]} recorded {top_month["units_sold"]:,.0f} units.
    </div>
    <div class="insight-card">
        💰 <b>Revenue Leader</b><br>
        {top_revenue} has the highest estimated revenue.
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 14. DOWNLOAD AND DATA TABLE
# ==========================================

st.markdown(
    '<div class="section-title">📥 EXPORT REPORT</div>',
    unsafe_allow_html=True
)

st.download_button(
    "⬇️ Download Sales Report",
    filtered_df.to_csv(index=False).encode("utf-8"),
    file_name="MG_Sales_Analysis_Report.csv",
    mime="text/csv"
)

with st.expander("📋 View Detailed Sales Data"):
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)

# ==========================================
# 15. FOOTER
# ==========================================

st.markdown("---")

st.markdown("""
<div style="text-align:center;padding:18px;">
    <h3 style="color:#e31837;">MG MOTOR INDIA</h3>
    <p style="color:#aeb5c0;">SALES INTELLIGENCE DASHBOARD | 2025</p>
    <p style="color:#778493;font-size:12px;">
        Built with Python | Streamlit | Pandas | Plotly
    </p>
    <p style="color:#778493;font-size:11px;">
        Synthetic practice dataset. Not official MG Motor sales data.
    </p>
</div>
""", unsafe_allow_html=True)
