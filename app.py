import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Workplace PERMA+V Dashboard", layout="wide")
st.title("📊 Workplace Wellbeing Dashboard (PERMA+V)")

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
st.sidebar.header("⚙️ Data Filters")

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
# 3. Sidebar Filters
# ---------------------------
gender_filter = st.sidebar.multiselect("Gender", df["Gender"].unique(), default=df["Gender"].unique())
age_filter = st.sidebar.multiselect("Age Group", df["AgeGroup"].unique(), default=df["AgeGroup"].unique())
dept_filter = st.sidebar.multiselect("Department", df["Department"].unique(), default=df["Department"].unique())
tenure_filter = st.sidebar.multiselect("Tenure", df["Tenure"].unique(), default=df["Tenure"].unique())

filtered_df = df[
    (df["Gender"].isin(gender_filter)) &
    (df["AgeGroup"].isin(age_filter)) &
    (df["Department"].isin(dept_filter)) &
    (df["Tenure"].isin(tenure_filter))
]

st.sidebar.write(f"✅ {len(filtered_df)} employees selected")

# ---------------------------
# 4. Radar Chart (PERMA+V)
# ---------------------------
st.subheader("🌟 PERMA+V Radar Chart")

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
    polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
    showlegend=True,
    height=600
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# 5. Distribution by Dimension
# ---------------------------
st.subheader("📈 Distribution by Dimension")

box_fig = go.Figure()
for dim in dims:
    box_fig.add_trace(go.Box(y=filtered_df[dim], name=dim, boxmean="sd"))

box_fig.update_layout(height=500)
st.plotly_chart(box_fig, use_container_width=True)

# ---------------------------
# 6. Summary Statistics
# ---------------------------
st.subheader("📊 Summary Statistics")

summary = filtered_df[dims].agg(["mean", "std", "min", "max"]).T
st.dataframe(summary.style.format("{:.2f}"))
