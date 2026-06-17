import streamlit as st
import requests
import folium
from streamlit_folium import st_folium

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="FutureCity Lab",
    page_icon="🚦",
    layout="wide"
)

# ================= CUSTOM THEME =================
st.markdown("""
<style>

/* Main Background */
.stApp {
    background-color: #0e1117;
}

/* Headings */
h1, h2, h3, h4 {
    color: #00ffd5 !important;
}

/* All text */
p, span {
    color: white !important;
}

/* Labels */
label {
    color: white !important;
    font-weight: bold !important;
}

/* Selected dropdown box */
.stSelectbox div[data-baseweb="select"] > div {
    background-color: white !important;
    color: black !important;
    border-radius: 10px;
    font-weight: bold;
}

/* Dropdown menu */
div[role="listbox"] {
    background-color: white !important;
}

/* Dropdown options */
div[role="option"] {
    background-color: white !important;
    color: black !important;
}

/* Hover effect */
div[role="option"]:hover {
    background-color: #e6e6e6 !important;
    color: black !important;
}

/* Dashboard cards */
div[data-testid="metric-container"] {
    background-color: #1a1f2b !important;
    border: 1px solid #2e3440;
    border-radius: 12px;
    padding: 15px;
}

/* Dashboard text */
div[data-testid="metric-container"] * {
    color: white !important;
}

/* Buttons */
.stButton > button {
    background-color: #00ffd5 !important;
    color: black !important;
    font-weight: bold;
    border-radius: 10px;
    width: 100%;
}

/* Route text */
strong {
    color: #00ffd5 !important;
}

</style>
""", unsafe_allow_html=True)

# ================= TITLE =================
st.title("🚦 FutureCity Lab")
st.subheader("🌍 Urban Digital Twin Simulation Platform")

st.markdown("""
<div style="
background-color:#1a1f2b;
padding:15px;
border-radius:10px;
border-left:5px solid #00ffd5;
margin-bottom:15px;">
<b>FutureCity Lab</b> uses Digital Twin technology to simulate smart city scenarios and identify the most efficient road routes under different urban conditions.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ================= INPUTS =================
locations = [
    "Triplicane",
    "Mylapore",
    "T Nagar"
]

col1, col2, col3 = st.columns(3)

with col1:
    from_loc = st.selectbox(
        "🚩 From",
        locations
    )

with col2:
    to_loc = st.selectbox(
        "🎯 To",
        locations
    )

with col3:
    scenario = st.selectbox(
        "⚙️ Scenario",
        [
            "none",
            "road_closure",
            "metro_added",
            "bus_lane"
        ]
    )

run = st.button("🚀 Run Simulation")

# ================= API CALL =================
if run:

    try:

        with st.spinner("Running simulation..."):

            response = requests.get(
                "http://127.0.0.1:8000/simulate",
                params={
                    "from_loc": from_loc,
                    "to_loc": to_loc,
                    "scenario": scenario
                },
                timeout=120
            )

            st.session_state.data = response.json()

    except Exception as e:

        st.error("Backend connection failed")
        st.exception(e)

# ================= RESULTS =================
if "data" in st.session_state:

    data = st.session_state.data

    route = data.get("route", [])
    distance = data.get("distance", 0)
    message = data.get("message", "")
    error = data.get("error")

    # ================= DASHBOARD =================
    st.markdown("## 📊 Simulation Dashboard")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "📏 Distance",
        f"{distance/1000:.2f} km"
    )

    c2.metric(
        "⚙️ Scenario",
        scenario.replace("_", " ").title()
    )

    c3.metric(
        "🧭 Route Points",
        len(route)
    )

    st.markdown("---")

    # ================= IMPACT =================
    st.markdown("## 🧠 Impact Analysis")

    if error:

        st.error(error)

    else:

        st.success(message)

        if scenario == "road_closure":

            st.warning(
                "Road closure increases congestion and travel time."
            )

        elif scenario == "metro_added":

            st.success(
                "Metro connectivity improves mobility and reduces traffic."
            )

        elif scenario == "bus_lane":

            st.info(
                "Dedicated bus lanes improve public transport efficiency."
            )

        else:

            st.info(
                "Normal city conditions simulated."
            )

    # ================= ROUTE =================
    st.markdown("## 🧭 Route")

    st.write(
        f"**{from_loc} ➜ {to_loc}**"
    )

    # ================= MAP =================
    st.markdown("## 🗺️ Live Route Map")

    if route and len(route) > 1:

        m = folium.Map(
            location=route[0],
            zoom_start=13,
            tiles="OpenStreetMap"
        )

        folium.PolyLine(
            locations=route,
            color="blue",
            weight=6,
            opacity=0.9
        ).add_to(m)

        folium.Marker(
            route[0],
            tooltip="Start"
        ).add_to(m)

        folium.Marker(
            route[-1],
            tooltip="Destination"
        ).add_to(m)

        st_folium(
            m,
            width=1100,
            height=600
        )

    else:

        st.warning("No route available.")


















































