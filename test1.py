
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

import route_tracker
import ship_tracker



st.set_page_config(
    page_title="Refrigerator Supply Chain Planner",
    layout="wide"
)

# ====================================
# SIDEBAR NAVIGATION
# ====================================
page = st.sidebar.selectbox(
    "Select Module",
    [
        "Load Planner",
        "Truck Tracking",
        "Ocean Freight"
    ]
)
# ====================================
# PAGE ROUTING
# ====================================
if page == "Truck Tracking":
    route_tracker.main()
    st.stop()
if page == "Ocean Freight":
    ship_tracker.main()
    st.stop()

# =====================================================
# CONTAINER SPECIFICATIONS
# =====================================================

CONTAINER_LENGTH = 589
CONTAINER_WIDTH = 235
CONTAINER_HEIGHT = 239

CONTAINER_VOLUME = (
    CONTAINER_LENGTH *
    CONTAINER_WIDTH *
    CONTAINER_HEIGHT
)

# =====================================================
# PARTS DATA
# =====================================================

parts = pd.DataFrame([

{
    "Part":"Condenser",
    "Factory":"Bidadi",
    "Length":120,
    "Width":80,
    "Height":90,
    "Weight":250,
    "Qty":10
},

{
    "Part":"Compressor",
    "Factory":"Tumakuru",
    "Length":100,
    "Width":70,
    "Height":60,
    "Weight":180,
    "Qty":15
},

{
    "Part":"Cabinet",
    "Factory":"Mangalore",
    "Length":150,
    "Width":120,
    "Height":180,
    "Weight":400,
    "Qty":8
}

])

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("Supply Chain Planner")
selected_parts = st.sidebar.multiselect(
   "Select Parts",
   parts["Part"].tolist(),
   default=parts["Part"].tolist()
)
filtered_parts = parts[
   parts["Part"].isin(selected_parts)
].copy()
st.sidebar.subheader("Production Quantity")
for idx in filtered_parts.index:
   filtered_parts.loc[idx, "Qty"] = st.sidebar.number_input(
       f"{filtered_parts.loc[idx,'Factory']} - {filtered_parts.loc[idx,'Part']}",
       min_value=0,
       max_value=100,
       value=int(filtered_parts.loc[idx,'Qty']),
       step=1
   )
# =====================================================
# HEADER
# =====================================================
st.title("🚛 Refrigerator Supply Chain Planner")
st.markdown("""
Factory Flow
Bidadi ➜ Tumakuru ➜ Mangalore ➜ New York
""")
# =====================================================
# PARTS TABLE
# =====================================================
st.subheader("Manufacturing Parts")
st.dataframe(filtered_parts)
# =====================================================
# LOAD CALCULATIONS
# =====================================================

filtered_parts["PartVolume"] = (
   filtered_parts["Length"] *
   filtered_parts["Width"] *
   filtered_parts["Height"] *
   filtered_parts["Qty"]
)
total_volume = filtered_parts["PartVolume"].sum()
total_weight = (
   filtered_parts["Weight"] *
   filtered_parts["Qty"]
).sum()
utilization = (
   total_volume /
   CONTAINER_VOLUME
) * 100

# =====================================================
# KPI SECTION
# =====================================================

col1,col2,col3 = st.columns(3)

with col1:
    st.metric(
        "Container Volume",
        f"{CONTAINER_VOLUME:,.0f}"
    )

with col2:
    st.metric(
        "Used Volume",
        f"{total_volume:,.0f}"
    )

with col3:
    st.metric(
        "Utilization %",
        f"{utilization:.2f}%"
    )

st.metric(
    "Total Shipment Weight (kg)",
    total_weight
)

remaining_volume = CONTAINER_VOLUME - total_volume
c1,c2 = st.columns(2)
with c1:
   st.metric(
       "Remaining Volume",
       f"{remaining_volume:,.0f}"
   )
with c2:
   st.metric(
       "Parts Selected",
       len(filtered_parts)
   )

# ==================================================
# BOX CREATION
# ==================================================

def add_cuboid(fig, x, y, z, dx, dy, dz, color, name):
   vertices = [
       [x, y, z],
       [x+dx, y, z],
       [x+dx, y+dy, z],
       [x, y+dy, z],
       [x, y, z+dz],
       [x+dx, y, z+dz],
       [x+dx, y+dy, z+dz],
       [x, y+dy, z+dz]
   ]
   x_v = [v[0] for v in vertices]
   y_v = [v[1] for v in vertices]
   z_v = [v[2] for v in vertices]
   fig.add_trace(
       go.Mesh3d(
           x=x_v,
           y=y_v,
           z=z_v,
           i=[0,0,0,1,1,2,4,4,5,5,6,7],
           j=[1,2,4,2,5,3,5,7,6,2,7,3],
           k=[2,4,1,5,6,0,6,6,2,1,3,0],
           opacity=0.9,
           color=color,
           name=name,
           flatshading=True
       )
   )

# =====================================================
# 3D CONTAINER LOADING
# =====================================================
st.subheader("3D Container Loading Simulation")
fig = go.Figure()
# -----------------------------------------------------
# DRAW CONTAINER
# -----------------------------------------------------
container_x = [0,589,589,0,0,589,589,0]
container_y = [0,0,235,235,0,0,235,235]
container_z = [0,0,0,0,239,239,239,239]
fig.add_trace(
   go.Mesh3d(
       x=container_x,
       y=container_y,
       z=container_z,
       opacity=0.08,
       color="lightblue",
       name="20ft Container"
   )
)
# -----------------------------------------------------
# FUNCTION TO DRAW BOX
# -----------------------------------------------------
def draw_box(fig, x, y, z,
            length,
            width,
            height,
            color,
            name):
   vertices_x = [
       x, x+length, x+length, x,
       x, x+length, x+length, x
   ]
   vertices_y = [
       y, y, y+width, y+width,
       y, y, y+width, y+width
   ]
   vertices_z = [
       z, z, z, z,
       z+height,
       z+height,
       z+height,
       z+height
   ]
   fig.add_trace(
       go.Mesh3d(
           x=vertices_x,
           y=vertices_y,
           z=vertices_z,
           opacity=0.8,
           color=color,
           name=name
       )
   )
# -----------------------------------------------------
# COLOR MAP
# -----------------------------------------------------
colors = {
   "Condenser":"red",
   "Compressor":"green",
   "Cabinet":"orange"
}
# -----------------------------------------------------
# PACKING LOGIC
# -----------------------------------------------------
current_x = 0
current_y = 0
current_z = 0
row_height = 0
overflow_parts = 0
for _, row in filtered_parts.iterrows():
   qty = int(row["Qty"])
   length = row["Length"]
   width = row["Width"]
   height = row["Height"]
   for i in range(qty):
       # Move next row
       if current_x + length > CONTAINER_LENGTH:
           current_x = 0
           current_y += row_height
           row_height = 0
       # Move next layer
       if current_y + width > CONTAINER_WIDTH:
           current_y = 0
           current_x = 0
           current_z += height
           row_height = 0
       # Container full
       if current_z + height > CONTAINER_HEIGHT:
           overflow_parts += 1
           continue
       add_cuboid(
       #draw_box(
           fig,
           current_x,
           current_y,
           current_z,
           length,
           width,
           height,
           colors.get(row["Part"], "blue"),
           row["Part"]
       )
       current_x += length
       row_height = max(
           row_height,
           width
       )
# -----------------------------------------------------
# LAYOUT
# -----------------------------------------------------
fig.update_layout(
   height=800,
   scene=dict(
       xaxis_title="Length (cm)",
       yaxis_title="Width (cm)",
       zaxis_title="Height (cm)",
       aspectmode="data",
       camera=dict(
           eye=dict(
               x=2.5,
               y=2.2,
               z=1.8
           )
       )
   )
)
st.plotly_chart(
   fig,
   #use_container_width=True
   width="stretch"
)
# -----------------------------------------------------
# OVERFLOW
# -----------------------------------------------------
if overflow_parts > 0:
   st.error(
       f"{overflow_parts} parts could not fit into the container."
   )
else:
   st.success(
       "All selected parts fit into the container."
   )

# =====================================================
# LOAD SUMMARY
# =====================================================

st.subheader("Load Summary")
summary = pd.DataFrame({
    "Factory": filtered_parts["Factory"],
    "Part": filtered_parts["Part"],
    "Quantity": filtered_parts["Qty"]
})
st.dataframe(summary)
# =====================================================
# SHIPMENT FLOW
# =====================================================
st.subheader("Shipment Route")
st.markdown("""
✅ Bidadi → Load Condensers
✅ Tumakuru → Load Compressors
✅ Mangalore → Load Cabinets
✅ Mangalore Port → Container Stuffing
✅ New York Port → Final Assembly
""")
# =====================================================
# UTILIZATION BAR
# =====================================================
st.subheader("Container Utilization")
st.progress(
    min(int(utilization),100)
)
st.success(
    f"Current Utilization : {utilization:.2f}%"
)


