import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(page_title="Workplace PERMA+V Dashboard", layout="wide")
st.title("Workplace Wellbeing Dashboard (PERMA+V)")

# Add small description of PERMA+V
st.markdown("""
<small>
The **PERMA+V framework** is a holistic model of wellbeing developed by Martin Seligman in positive psychology.  
It identifies six core elements that contribute to human flourishing:
<table style="table-layout: fixed; width: 60%; border-collapse: collapse; text-align: center;">
  <tr>
    <th style="width:10%;"><b>P: Positive Emotions</b></th>
    <th style="width:10%;"><b>E: Engagement</b></th>
    <th style="width:10%;"><b>R: Relationships</b></th>
    <th style="width:10%;"><b>M: Meaning</b></th>
    <th style="width:10%;"><b>A: Accomplishment</b></th>
    <th style="width:10%;"><b>V: Vitality</b></th>
  </tr>
  <tr>
    <td>Joy, gratitude, optimism</td>
    <td>Flow, absorption</td>
    <td>Support, connection</td>
    <td>Purpose, values</td>
    <td>Mastery, achievement</td>
    <td>Energy, health</td>
  </tr>
</table>
</small>
""", unsafe_allow_html=True)

# ---------------------------
# 1. Load Data from Google Sheets (CSV Export)
# ---------------------------
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1ethwOtyt9_KpSkvF7zAaMUW99W1PoKp6onsIMWQ_IhU/export?format=csv"

@st.cache_data
def load_data():
    df = pd.read_csv(SPREADSHEET_URL)
    # Ensure numeric columns for Q1–Q13
    for q in [f"Q{i}" for i in range(1, 14)]:
        if q in df.columns:
            df[q] = pd.to_numeric(df[q], errors="coerce")
    return df

df = load_data()

# ---------------------------
# 2. Define PERMA+V mapping
# ---------------------------
perma_mapping = {
    "P": ["Q1", "Q2"],            # Positive Emotion
    "E": ["Q3", "Q4"],            # Engagement
    "R": ["Q5", "Q6"],            # Relationships
    "M": ["Q7", "Q8"],            # Meaning
    "A": ["Q9", "Q10"],           # Accomplishment
    "V": ["Q11", "Q12", "Q13"],   # Vitality
}

def compute_perma_scores(df):
    results = {}
    for dim, cols in perma_mapping.items():
        results[dim] = df[cols].mean(axis=1)
    return pd.DataFrame(results)

perma_scores = compute_perma_scores(df)
df = pd.concat([df, perma_scores], axis=1)

# ---------------------------
# 3. Sidebar Filters (single-select dropdowns)
# ---------------------------
with st.sidebar.expander("Data Filters", expanded=True):

    gender_filter = st.selectbox(
        "Gender", 
        options=["Choose options"] + list(df["Gender"].unique())
    )
    
    # Fix order for AgeGroup
    age_order = ["22-29", "30-39", "40-49", "50-60"]
    age_filter = st.selectbox(
        "Age Group", 
        options=["Choose options"] + age_order
    )
    
    dept_filter = st.selectbox(
        "Department", 
        options=["Choose options"] + sorted(df["Department"].unique())
    )

    # Fix order for Tenure
    tenure_order = ["0-1 year", "2-5 years", "6-10 years", "10+ years"]
    tenure_filter = st.selectbox(
        "Tenure", 
        options=["Choose options"] + tenure_order
    )

# ---------------------------
# Apply filters (skip "Choose options")
# ---------------------------
filtered_df = df.copy()
if gender_filter != "Choose options":
    filtered_df = filtered_df[filtered_df["Gender"] == gender_filter]
if age_filter != "Choose options":
    filtered_df = filtered_df[filtered_df["AgeGroup"] == age_filter]
if dept_filter != "Choose options":
    filtered_df = filtered_df[filtered_df["Department"] == dept_filter]
if tenure_filter != "Choose options":
    filtered_df = filtered_df[filtered_df["Tenure"] == tenure_filter]

st.sidebar.write(f"✅ {len(filtered_df)} employees selected")


# ---------------------------
# 4. Radar Chart (PERMA+V)
# ---------------------------
dims = list(perma_mapping.keys())
avg_scores = [filtered_df[d].mean() for d in dims]

fig = go.Figure()

# Overlay all individuals
for i, row in filtered_df.iterrows():
    fig.add_trace(go.Scatterpolar(
        r=row[dims].values,
        theta=dims,
        fill="toself",
        line=dict(color="rgba(100,100,200,0.2)"),
        name=row["ID"],
        opacity=0.1,
        showlegend=False
    ))

# Add average trend line
fig.add_trace(go.Scatterpolar(
    r=avg_scores,
    theta=dims,
    fill="toself",
    name="Average",
    line=dict(color="royalblue", width=3)
))

fig.update_layout(
    polar=dict(
        radialaxis=dict(visible=True, range=[0, 5], tickfont=dict(size=12)),
        angularaxis=dict(tickfont=dict(size=16))  # Bigger PERMA+V letters
    ),
    showlegend=True,
    height=600,
    margin=dict(t=40, b=20)  # Title spacing adjustment
)

# ---------------------------
# 5. Distribution by Dimension
# ---------------------------
box_fig = go.Figure()

for dim in dims:
    box_fig.add_trace(
        go.Box(
            y=filtered_df[dim],
            name=dim,
            boxmean="sd",
            marker=dict(opacity=0.6)
        )
    )

box_fig.update_layout(
    height=500,
    title="Distribution by Dimension",
    yaxis=dict(
        title="Score",
        range=[0, 5]
    )
)

# ---------------------------
# Layout: two columns
# ---------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("PERMA+V Radar Chart")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Distribution by Dimension")
    st.plotly_chart(box_fig, use_container_width=True)

# ---------------------------
# 6. Summary Statistics
# ---------------------------
st.subheader("Summary Statistics")
summary = filtered_df[dims].agg(["mean", "std", "min", "max"]).T
st.dataframe(summary.style.format("{:.2f}"))
