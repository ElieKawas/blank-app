import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

st.set_page_config(page_title="Water Data Explorer", layout="wide")
st.title("Water Data Explorer")

# Intro Section

st.subheader(". About the Dataset")
st.write("""
Covers all Lebanese towns (2023)  
Permanent & Seasonal Springs  
Water Network Rating (Good / Acceptable / Bad)  
Gallons Purchased  

The charts below compare towns, show the mix of conditions, and highlight patterns and outliers.
""")

# Data Preparation (Explanation)

st.subheader(". Data Preparation")
st.write("""
- Loaded the raw CSV  
- Dropped extra metadata columns  
- Renamed long headers to short, clear labels  
- No rows were changed  

The cleaned file was saved as **dataset clean.csv** and is used for the visualizations below.
""")


# Load dataset

df = pd.read_csv("dataset clean.csv")
# Visualization 1: Correlation Heatmap

st.header("Correlation Heatmap")

numeric_cols = df.select_dtypes(include="number").columns.tolist()
st.write("**Click on the bubbles below to include/exclude variables:**")

# Horizontal checkboxes (bubble-style)
selected_cols = []
cols = st.columns(len(numeric_cols))  # one column per variable

for i, var in enumerate(numeric_cols):
    if cols[i].checkbox(var, value=True):
        selected_cols.append(var)

# Show the heatmap
if selected_cols:
    corr = df[selected_cols].corr()
    fig = ff.create_annotated_heatmap(
        z=corr.values,
        x=corr.columns.tolist(),
        y=corr.columns.tolist(),
        annotation_text=corr.round(2).values,
        colorscale="Viridis",
        showscale=True
    )
    st.plotly_chart(fig, use_container_width=True)
    

# Visualization 2: Grouped Bar

st.header("Permanent vs Seasonal Springs")

top_n = st.slider("Number of towns to compare:", 5, 20, 12)

sample_df = df.sample(top_n, random_state=7)[["Town", "Permanent Springs", "Seasonal Springs"]]
long_df = sample_df.melt(
    id_vars="Town",
    value_vars=["Permanent Springs", "Seasonal Springs"],
    var_name="Spring Type",
    value_name="Count"
)

fig_bar = px.bar(
    long_df,
    x="Town",
    y="Count",
    color="Spring Type",
    barmode="group",
    title=f"Permanent vs Seasonal Springs ({top_n} Towns)"
)
st.plotly_chart(fig_bar, use_container_width=True)
