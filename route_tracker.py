
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from geopy.distance import geodesic
import time






def main():
#    st.title("🚛 Truck GPS Tracking")

# =====================================
# LOCATIONS
# =====================================

    LOCATIONS = {
        "Bidadi": (12.7975, 77.3842),
        "Tumakuru": (13.3409, 77.1010),
        "Mangalore": (12.9141, 74.8560)
    }

    ROUTE = [
        LOCATIONS["Bidadi"],
        LOCATIONS["Tumakuru"],
        LOCATIONS["Mangalore"]
    ]

    # =====================================
    # DISTANCE
    # =====================================

    distance_1 = geodesic(
        LOCATIONS["Bidadi"],
        LOCATIONS["Tumakuru"]
    ).km

    distance_2 = geodesic(
        LOCATIONS["Tumakuru"],
        LOCATIONS["Mangalore"]
    ).km

    TOTAL_DISTANCE = distance_1 + distance_2

    # =====================================
    # PAGE
    # =====================================

    st.title("🚛 Truck GPS Tracking")

    st.write(
        f"Total Route Distance: {TOTAL_DISTANCE:.1f} km"
    )

    # =====================================
    # SIMULATION
    # =====================================

    progress = st.slider(
        "Trip Progress (%)",
        0,
        100,
        25
    )

    # =====================================
    # CURRENT POSITION
    # =====================================

    if progress <= 50:

        ratio = progress / 50

        lat = (
            ROUTE[0][0]
            + ratio * (ROUTE[1][0] - ROUTE[0][0])
        )

        lon = (
            ROUTE[0][1]
            + ratio * (ROUTE[1][1] - ROUTE[0][1])
        )

        current_stage = "Bidadi → Tumakuru"

    else:

        ratio = (progress - 50) / 50

        lat = (
            ROUTE[1][0]
            + ratio * (ROUTE[2][0] - ROUTE[1][0])
        )

        lon = (
            ROUTE[1][1]
            + ratio * (ROUTE[2][1] - ROUTE[1][1])
        )

        current_stage = "Tumakuru → Mangalore"

    # =====================================
    # ETA
    # =====================================

    remaining_distance = (
        TOTAL_DISTANCE *
        (100 - progress) / 100
    )

    truck_speed = 50

    eta_hours = (
        remaining_distance /
        truck_speed
    )

    # =====================================
    # KPI
    # =====================================

    c1,c2,c3 = st.columns(3)

    with c1:
        st.metric(
            "Progress",
            f"{progress}%"
        )

    with c2:
        st.metric(
            "Distance Remaining",
            f"{remaining_distance:.1f} km"
        )

    with c3:
        st.metric(
            "ETA",
            f"{eta_hours:.1f} hrs"
        )

    st.info(
        f"Current Route: {current_stage}"
    )

    # =====================================
    # MAP
    # =====================================

    m = folium.Map(
        location=[12.9,76.5],
        zoom_start=7
    )

    # Factory markers

    folium.Marker(
        ROUTE[0],
        popup="Factory 1 - Bidadi",
        tooltip="Condenser Manufacturing"
    ).add_to(m)

    folium.Marker(
        ROUTE[1],
        popup="Factory 2 - Tumakuru",
        tooltip="Compressor Manufacturing"
    ).add_to(m)

    folium.Marker(
        ROUTE[2],
        popup="Factory 3 - Mangalore",
        tooltip="Cabinet Manufacturing"
    ).add_to(m)

    # Route line

    folium.PolyLine(
        ROUTE,
        weight=5
    ).add_to(m)

    # Truck

    folium.Marker(
        [lat, lon],
        popup="Truck Current Position",
        tooltip="Truck",
        icon=folium.Icon(icon="truck")
    ).add_to(m)

    st_folium(
        m,
        width=1200,
        height=600
    )

    # =====================================
    # SHIPMENT STATUS
    # =====================================

    st.subheader("Shipment Status")

    if progress < 20:

        st.warning(
            "Loading Condensers at Bidadi"
        )

    elif progress < 50:

        st.success(
            "Truck moving to Tumakuru"
        )

    elif progress < 60:

        st.warning(
            "Loading Compressors"
        )

    elif progress < 90:

        st.success(
            "Truck moving to Mangalore"
        )

    else:

        st.success(
            "Reached Mangalore Port"
        )
