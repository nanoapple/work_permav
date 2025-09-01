# Work PERMA+V Dashboard

A demo Streamlit app for visualizing **workplace wellbeing (PERMA+V framework)**.  
This project uses **Google Sheets** for data collection and **Streamlit + Plotly** for interactive visualization.

---

## ✨ Features

- **Google Sheets Integration**  
  Survey data is stored in Google Sheets and automatically loaded into the dashboard.

- **PERMA+V Radar Chart**  
  Six-dimensional wellbeing profile (Positive Emotion, Engagement, Relationships, Meaning, Accomplishment, Vitality) shown as an interactive hexagon chart.

- **Interactive Filters**  
  Slice and analyze wellbeing by demographic and work-related factors:  
  - Gender  
  - Age Group  
  - Department  
  - Tenure  
  - Marital Status  
  - Children  
  - Smoking & Exercise Habits  
  - Living Situation  

- **Detailed Analysis**  
  - Mean and distribution of scores  
  - Boxplots and histograms by group  
  - Highlight top and bottom scorers  

---

## 🛠 Tech Stack

- **Frontend & Dashboard**: [Streamlit](https://streamlit.io/)  
- **Visualization**: [Plotly](https://plotly.com/python/)  
- **Data Source**: Google Sheets (via `streamlit-gsheets`)  

---

## 🚀 How to Run Locally

1. Clone this repository:
   ```bash
   git clone https://github.com/nanoapple/work_permav.git
   cd work_permav
