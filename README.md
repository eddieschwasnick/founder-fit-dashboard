# Founder Fit Dashboard

This project builds an interactive dashboard using Flask and SQLite to evaluate founder-investor fit, track startup metrics, and visualize investment insights. Designed as an academic data application, it enables dynamic querying, multi-table joins, and real-time statistical summaries to support decision-making in early-stage venture capital contexts.

---

### Key Features

- **Founder-Investor Fit Visualization:** View joined data across founders, startups, and evaluations to understand investment alignment and performance
- **Multi-table SQL JOINs:** Routes like `/key_info` and `/avg_score_by_founder` integrate insights from three relational tables
- **Live Search & Query:** Dynamically filter data by sector, score, or evaluation notes with routes like `/query_startups` and `/query_founders`
- **Statistical Dashboards:** Routes like `/stats_evaluations` and `/avg_score_by_founder` summarize numeric metrics and scores
- **Visualizations:** Bar and histogram plots display trends in funding amounts and sector activity
- **Modular Flask App:** Clean routing architecture using HTML templates and static plots

---

### Sample Visualizations

Located under `/static/` and rendered via the `/visuals` route:

- **Funding Histogram:** Distribution of startup funding ask amounts  
- **Sector Bar Chart:** Total funding requested by sector

---

### Tech Stack

- **Python 3.10+**
- **Flask** for routing and dynamic content
- **SQLite** as the lightweight database engine
- **matplotlib** for charting
- **HTML + Jinja templates** for page rendering

---

### Project Structure

founder-fit-dashboard/
├── app.py
├── FounderFitEvaluation.db
├── templates/
│ ├── index.html
│ ├── founders.html
│ └── ...
├── static/
│ ├── visuals_plot1.png
│ └── style.css
├── E-R Diagram.pdf # optional
├── Relational Schema.pdf # optional
├── README.md

yaml
Copy
Edit

---

### 🚀 How to Run

1. Clone the repository
2. Ensure `FounderFitEvaluation.db` is in the root folder
3. Run the app:
```bash
python app.py
