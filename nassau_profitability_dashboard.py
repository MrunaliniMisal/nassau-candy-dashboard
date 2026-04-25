import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(page_title="Nassau Candy Profitability & Logistics", layout="wide")

st.title("Nassau Candy: Product Line Profitability & Margin Performance Analysis")
st.markdown("""
This dashboard provides actionable insights into product margins and logistics performance 
to reduce delays and enhance nationwide delivery reliability.
""")

# --- LOAD DATA ---
@st.cache_data
def load_data():
    df = pd.read_csv("Nassau Candy Distributor.csv")

    df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True)
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], dayfirst=True)

    df["Shipping Delay"] = (df["Ship Date"] - df["Order Date"]).dt.days

    df = df[df["Sales"] > 0]
    df = df[df["Cost"] >= 0]
    df["Units"] = df["Units"].fillna(1)

    df["Gross Margin %"] = (df["Gross Profit"] / df["Sales"]) * 100
    df["Profit per Unit"] = df["Gross Profit"] / df["Units"]

    total_sales = df["Sales"].sum()
    total_profit = df["Gross Profit"].sum()

    df["Revenue Contribution"] = df["Sales"] / total_sales
    df["Profit Contribution"] = df["Gross Profit"] / total_profit

    # Factory Mapping
    factory_mapping = {
        "Wonka Bar - Nutty Crunch Surprise": "Lot's O' Nuts",
        "Wonka Bar - Fudge Mallows": "Lot's O' Nuts",
        "Wonka Bar -Scrumdiddlyumptious": "Lot's O' Nuts",
        "Wonka Bar - Milk Chocolate": "Wicked Choccy's",
        "Wonka Bar - Triple Dazzle Caramel": "Wicked Choccy's",
        "Laffy Taffy": "Sugar Shack", "SweeTARTS": "Sugar Shack",
        "Nerds": "Sugar Shack", "Fun Dip": "Sugar Shack",
        "Fizzy Lifting Drinks": "Sugar Shack",
        "Everlasting Gobstopper": "Secret Factory",
        "Hair Toffee": "The Other Factory",
        "Lickable Wallpaper": "Secret Factory",
        "Wonka Gum": "Secret Factory",
        "Kazookles": "The Other Factory"
    }

    df["Factory"] = df["Product Name"].map(factory_mapping)

    factory_coords = {
        "Lot's O' Nuts": [32.881893, -111.768036],
        "Wicked Choccy's": [32.076176, -81.088371],
        "Sugar Shack": [48.11914, -96.18115],
        "Secret Factory": [41.446333, -90.565487],
        "The Other Factory": [35.1175, -89.971107]
    }

    df["Factory_Lat"] = df["Factory"].apply(lambda x: factory_coords.get(x, [None, None])[0])
    df["Factory_Lon"] = df["Factory"].apply(lambda x: factory_coords.get(x, [None, None])[1])

    return df

df = load_data()

# --- SIDEBAR ---
st.sidebar.header("Filters")

date_range = st.sidebar.date_input(
    "Date Range",
    [df["Order Date"].min(), df["Order Date"].max()]
)

division = st.sidebar.multiselect("Division", df["Division"].unique(), default=df["Division"].unique())
region = st.sidebar.multiselect("Region", df["Region"].unique(), default=df["Region"].unique())
ship_mode = st.sidebar.multiselect("Ship Mode", df["Ship Mode"].unique(), default=df["Ship Mode"].unique())

margin_threshold = st.sidebar.slider("Minimum Margin %", -50, 100, 0)
search_query = st.sidebar.text_input("Search Product")

# --- FILTERING ---
filtered_df = df[
    (df["Order Date"] >= pd.to_datetime(date_range[0])) &
    (df["Order Date"] <= pd.to_datetime(date_range[1])) &
    (df["Division"].isin(division)) &
    (df["Region"].isin(region)) &
    (df["Ship Mode"].isin(ship_mode)) &
    (df["Gross Margin %"] >= margin_threshold)
]

if search_query:
    filtered_df = filtered_df[
        filtered_df["Product Name"].str.contains(search_query, case=False)
    ]

# --- KPIs ---
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"${filtered_df['Sales'].sum():,.0f}")
col2.metric("Total Profit", f"${filtered_df['Gross Profit'].sum():,.0f}")
col3.metric("Avg Margin %", f"{filtered_df['Gross Margin %'].mean():.2f}%")
col4.metric("Avg Ship Delay", f"{filtered_df['Shipping Delay'].mean():.1f} Days")

# --- TABS ---
tabs = st.tabs([
    "Product Profitability",
    "Division Performance",
    "Cost Diagnostics",
    "Profit Concentration",
    "Logistics"
])

# 1️⃣ PRODUCT
with tabs[0]:
    st.subheader("Top Products by Profit")

    product_stats = filtered_df.groupby("Product Name").agg({
        "Gross Profit": "sum",
        "Gross Margin %": "mean"
    }).reset_index()

    fig1 = px.bar(
        product_stats.sort_values("Gross Profit", ascending=False).head(10),
        x="Gross Profit", y="Product Name",
        orientation="h", color="Gross Profit",
        color_continuous_scale="Blues"
    )
    fig1.update_layout(xaxis_title="Total Profit ($)", yaxis_title="Product")
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Top Products by Margin")

    fig1b = px.bar(
        product_stats.sort_values("Gross Margin %", ascending=False).head(10),
        x="Gross Margin %", y="Product Name",
        orientation="h", color="Gross Margin %",
        color_continuous_scale="Blues"
    )
    fig1b.update_layout(xaxis_title="Margin (%)", yaxis_title="Product")
    st.plotly_chart(fig1b, use_container_width=True)

    st.markdown("""
    **Insight:**
    - A small number of products dominate profit contribution.
    - High margin products are not always the highest revenue generators.
    """)

# 2️⃣ DIVISION
with tabs[1]:
    st.subheader("Revenue vs Profit by Division")

    div_stats = filtered_df.groupby("Division").agg({
        "Sales": "sum",
        "Gross Profit": "sum"
    }).reset_index()

    fig2 = px.bar(div_stats, x="Division", y=["Sales", "Gross Profit"], barmode="group")
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Margin Distribution")

    fig_box = px.box(filtered_df, x="Division", y="Gross Margin %")
    st.plotly_chart(fig_box, use_container_width=True)

    # Margin Volatility
    st.subheader("Margin Volatility Over Time")

    vol_df = filtered_df.groupby(filtered_df["Order Date"].dt.to_period("M"))["Gross Margin %"].std().reset_index()
    vol_df["Order Date"] = vol_df["Order Date"].astype(str)

    fig_vol = px.line(vol_df, x="Order Date", y="Gross Margin %")
    st.plotly_chart(fig_vol, use_container_width=True)

    st.markdown("""
    **Insight:**
    - Some divisions generate high revenue but low profit.
    - Margin volatility indicates instability in pricing or cost structure.
    """)

# 3️⃣ COST
with tabs[2]:
    st.subheader("Cost vs Sales (Pricing Efficiency Analysis)")

    fig3 = px.scatter(filtered_df, x="Cost", y="Sales",
                      color="Gross Margin %",
                      color_continuous_scale="Blues",
                      hover_data=["Product Name"])
    st.plotly_chart(fig3, use_container_width=True)

    filtered_df = filtered_df.copy()
    filtered_df["Risk"] = "Normal"

    filtered_df.loc[filtered_df["Gross Margin %"] < 10, "Risk"] = "Low Margin"
    filtered_df.loc[filtered_df["Cost"] > filtered_df["Sales"] * 0.8, "Risk"] = "High Cost"
    filtered_df.loc[filtered_df["Shipping Delay"] > 5, "Risk"] = "Logistics Delay"

    st.markdown("### Products Requiring Review (High Cost / Low Margin)")

    risk_df = filtered_df[filtered_df["Risk"] != "Normal"][
        ["Product Name", "Cost", "Sales", "Gross Margin %", "Factory"]
    ].sort_values(by="Gross Margin %")

    st.dataframe(risk_df, use_container_width=True, hide_index=True)

    st.markdown("""
    **Insight:**
    - High cost and low margin products indicate pricing inefficiencies.
    """)

# 4️⃣ PARETO
with tabs[3]:
    st.subheader("Pareto Analysis")

    pareto = filtered_df.groupby("Product Name")["Gross Profit"].sum() \
        .sort_values(ascending=False).reset_index()

    pareto["Cumulative %"] = pareto["Gross Profit"].cumsum() / pareto["Gross Profit"].sum() * 100
    pareto["Rank"] = range(1, len(pareto) + 1)

    fig4 = px.line(
        pareto,
        x="Rank",
        y="Cumulative %",
        hover_data={
            "Product Name": True,
            "Gross Profit": ":,.0f",
            "Cumulative %": ":.2f"
        }
    )

    fig4.add_hline(y=80, line_dash="dash", line_color="red")
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown(f"""
    **Insight:**
    - {len(pareto[pareto['Cumulative %'] <= 80])} products contribute to 80% of total profit.
    """)

# 5️⃣ LOGISTICS
with tabs[4]:
    st.subheader("Avg Delay by Region")

    delay = filtered_df.groupby("Region")["Shipping Delay"].mean().reset_index()

    fig5 = px.bar(delay, x="Region", y="Shipping Delay",
                  color="Shipping Delay", color_continuous_scale="Blues")
    st.plotly_chart(fig5, use_container_width=True)

    st.subheader("Delay vs Margin")

    fig6 = px.scatter(filtered_df, x="Shipping Delay",
                      y="Gross Margin %",
                      color="Ship Mode")
    st.plotly_chart(fig6, use_container_width=True)

    st.subheader("Factory Locations")

    map_data = filtered_df.groupby("Factory").agg({
        "Factory_Lat": "first",
        "Factory_Lon": "first",
        "Sales": "sum",
        "Shipping Delay": "mean"
    }).reset_index()

    fig_map = px.scatter_geo(
        map_data,
        lat="Factory_Lat",
        lon="Factory_Lon",
        size="Sales",
        color="Shipping Delay",
        color_continuous_scale="Blues",
        scope="usa"
    )
    st.plotly_chart(fig_map, use_container_width=True)

    st.markdown("""
    **Insight:**
    - Regions with higher delays may impact profitability.
    - Logistics efficiency directly influences margin performance.
    """)

     # --- SECTION 6: FOOTER ---
st.markdown("""
    <style>
    .footer {
        position: relative;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #1E1E1E;
        color: #7F8C8D;
        text-align: center;
        padding: 20px;
        font-family: sans-serif;
        border-top: 1px solid #333;
        margin-top: 50px;
    }
    .footer-highlight { color: #D96A13; font-weight: bold; }
    </style>
    <div class="footer">
        <p>Nassau Candy | <span class="footer-highlight">Profitability & Route Efficiency Dashboard</span></p>
        <p style="font-size: 0.8em;">© Mrunalini Misal | www.linkedin.com/in/mrunalini-misal-263735192 </p>
    </div>
    """, unsafe_allow_html=True)