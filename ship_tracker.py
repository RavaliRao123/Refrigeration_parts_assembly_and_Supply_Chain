import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.distance import geodesic



def main():
#    st.title("🚢 Ocean Freight Tracking")

# ==================================================
# PORTS
# ==================================================
    MANGALORE = (12.9141, 74.8560)
    DUBAI = (25.2048, 55.2708)
    SUEZ = (30.0444, 31.2357)
    NEW_YORK = (40.7128, -74.0060)
    ROUTE = [
        MANGALORE,
        DUBAI,
        SUEZ,
        NEW_YORK
    ]

    # ==================================================
    # DISTANCE CALCULATION
    # ==================================================
    total_distance = 0
    for i in range(len(ROUTE)-1):
        total_distance += geodesic(
            ROUTE[i],
            ROUTE[i+1]
        ).km
    # ==================================================
    # PAGE
    # ==================================================

    st.title("🚢 Ocean Freight Tracking")

    st.write(
        f"Total Ocean Route Distance : {total_distance:,.0f} km"
    )

    # ==================================================
    # SHIP PROGRESS
    # ==================================================

    progress = st.slider(
        "Voyage Progress %",
        0,
        100,
        20
    )

    # ==================================================
    # SHIP LOCATION
    # ==================================================

    if progress <= 33:

        ratio = progress / 33

        lat = ROUTE[0][0] + ratio * (
            ROUTE[1][0] - ROUTE[0][0]
        )

        lon = ROUTE[0][1] + ratio * (
            ROUTE[1][1] - ROUTE[0][1]
        )

        stage = "Mangalore ➜ Dubai"

    elif progress <= 66:

        ratio = (progress - 33) / 33

        lat = ROUTE[1][0] + ratio * (
            ROUTE[2][0] - ROUTE[1][0]
        )

        lon = ROUTE[1][1] + ratio * (
            ROUTE[2][1] - ROUTE[1][1]
        )

        stage = "Dubai ➜ Suez"

    else:

        ratio = (progress - 66) / 34

        lat = ROUTE[2][0] + ratio * (
            ROUTE[3][0] - ROUTE[2][0]
        )

        lon = ROUTE[2][1] + ratio * (
            ROUTE[3][1] - ROUTE[2][1]
        )

        stage = "Suez ➜ New York"

    # ==================================================
    # ETA
    # ==================================================

    remaining_distance = (
        total_distance *
        (100 - progress) / 100
    )

    ship_speed = 35

    eta_hours = remaining_distance / ship_speed

    eta_days = eta_hours / 24

    # ==================================================
    # KPIs
    # ==================================================

    c1,c2,c3,c4 = st.columns(4)

    with c1:
        st.metric(
            "Voyage Progress",
            f"{progress}%"
        )

    with c2:
        st.metric(
            "Distance Remaining",
            f"{remaining_distance:,.0f} km"
        )

    with c3:
        st.metric(
            "ETA Hours",
            f"{eta_hours:.1f}"
        )

    with c4:
        st.metric(
            "ETA Days",
            f"{eta_days:.1f}"
        )

    st.info(
        f"Current Voyage Stage : {stage}"
    )

    # ==================================================
    # MAP
    # ==================================================

    m = folium.Map(
        location=[25,20],
        zoom_start=3
    )

    # Route

    folium.PolyLine(
        ROUTE,
        weight=4,
        color="blue"
    ).add_to(m)

    # Ports

    folium.Marker(
        MANGALORE,
        popup="Mangalore Port"
    ).add_to(m)

    folium.Marker(
        DUBAI,
        popup="Dubai Port"
    ).add_to(m)

    folium.Marker(
        SUEZ,
        popup="Suez Canal"
    ).add_to(m)

    folium.Marker(
        NEW_YORK,
        popup="New York Port"
    ).add_to(m)

    # Ship

    folium.Marker(
        [lat,lon],
        popup="Cargo Ship",
        tooltip="Current Vessel Position",
        icon=folium.Icon(
            icon="ship",
            prefix="fa"
        )
    ).add_to(m)

    st_folium(
        m,
        width=1300,
        height=650
    )

    # ==================================================
    # CONTAINER STATUS
    # ==================================================

    st.subheader("Container Status")

    if progress < 10:

        st.warning(
            "Container loaded at Mangalore Port"
        )

    elif progress < 33:

        st.success(
            "Sailing toward Dubai"
        )

    elif progress < 66:

        st.success(
            "Crossing Suez Canal"
        )

    elif progress < 95:

        st.success(
            "Crossing Atlantic Ocean"
        )

    else:

        st.success(
            "Arriving at New York Port"
        )

    # ==================================================
    # SHIPMENT TIMELINE
    # ==================================================

    st.subheader("Shipment Events")

    events = [
        "Container Stuffing - Mangalore",
        "Port Departure",
        "Dubai Transit",
        "Suez Canal Crossing",
        "Atlantic Crossing",
        "New York Arrival",
        "Final Assembly Delivery"
    ]

    for e in events:
        st.write("✅", e)
