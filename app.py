import sqlite3
import csv
import pandas as pd
from flask import Flask, render_template, request, redirect
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


# Create the Founder Fit Evaluation database
con = sqlite3.connect("FounderFitEvaluation.db")
cur = con.cursor()

# Add tables to the database by importing a csv (CSV's were generated using AI)
# Replace the tables after each run
df_founders = pd.read_csv('Founders_Table.csv', encoding='latin1')
df_founders.to_sql('Founders_Table', con, if_exists='replace', index=False)

df_startups = pd.read_csv('Startups_Table.csv', encoding='latin1')
df_startups.to_sql('Startups_Table', con, if_exists='replace', index=False)

df_evaluations = pd.read_csv('Evaluations_Table.csv', encoding='latin1')
df_evaluations.to_sql('Evaluations_Table', con, if_exists='replace', index=False)


# Initialize the Flask app
app = Flask(__name__)

## -------------------------------------------------------------------------------------------------------------------
## Create Main Routes

# Route 1: Landing page
# This route is designated as the landing page route using @app.route("/"). In Flask, the @app.route() is used
# to map URLs to Python functions, and "/" represents the root URL, which is basically the landing/home page of a web application.
@app.route("/")
def index():
    # HTML files, which contain the structure and content of webpages,
    # are usually stored within a folder named 'templates' in Flask.
    # This separation helps Flask locate and render HTML templates when requested by routes.
    return render_template("landing.html")

# Route 2: Founders page
# Displays the list of founders
@app.route("/founders")
def show_founders():
    con = sqlite3.connect("FounderFitEvaluation.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM Founders_Table")
    founders = cur.fetchall()
    con.close()
    return render_template("founders.html", founders=founders)

# Route 3: Startups page
# Displays the list of startups
@app.route("/startups")
def show_startups():
    con = sqlite3.connect("FounderFitEvaluation.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM Startups_Table")
    startups = cur.fetchall()
    con.close()
    return render_template("startups.html", startups=startups)

# Route 4: Evaluations page
# Displays the list of evaluations
@app.route("/evaluations")
def show_evaluations():
    con = sqlite3.connect("FounderFitEvaluation.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM Evaluations_Table")
    evaluations = cur.fetchall()
    con.close()
    return render_template("evaluations.html", evaluations=evaluations)


## -------------------------------------------------------------------------------------------------------------------
## Add, Edit, Delete Routes


# Route 5: Add a new startup
# Allows users to add a new founder
@app.route("/add_startup", methods=["GET", "POST"])
def add_startup():
    con = sqlite3.connect("FounderFitEvaluation.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM Founders_Table")
    founders = cur.fetchall()

    if request.method == "POST":
        # Manually assign startup_id = current max + 1
        cur.execute("SELECT MAX(startup_id) FROM Startups_Table")
        max_id_row = cur.fetchone()
        new_id = (max_id_row[0] or 0) + 1

        name = request.form["name"]
        sector = request.form["sector"]
        team_size = request.form["team_size"]
        funding_ask = request.form["funding_ask"]
        founder_id = request.form["founder_id"]

        cur.execute("""
            INSERT INTO Startups_Table (startup_id, name, sector, team_size, funding_ask, founder_id) VALUES (?, ?, ?, ?, ?, ?)""",
            (new_id, name, sector, team_size, funding_ask, founder_id))
        
        con.commit()
        con.close()
        return redirect("/startups")

    return render_template("add_startup.html", founders=founders)

# Route 6: Edit a startup
# Allows users to edit an existing startup.
@app.route("/edit_startup/<int:startup_id>", methods=["GET", "POST"])
def edit_startup(startup_id):
    con = sqlite3.connect("FounderFitEvaluation.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    if request.method == "POST":
        name = request.form["name"]
        sector = request.form["sector"]
        team_size = request.form["team_size"]
        funding_ask = request.form["funding_ask"]
        founder_id = request.form["founder_id"]

        cur.execute("""
            UPDATE Startups_Table SET name=?, sector=?, team_size=?, funding_ask=?, founder_id=? WHERE startup_id=?""",
            (name, sector, team_size, funding_ask, founder_id, startup_id))
        con.commit()
        con.close()
        return redirect("/startups")

    cur.execute("SELECT * FROM Startups_Table WHERE startup_id=?", (startup_id,))
    startup = cur.fetchone()
    cur.execute("SELECT * FROM Founders_Table")
    founders = cur.fetchall()
    con.close()
    return render_template("edit_startup.html", startup=startup, founders=founders)

# Route 7: Delete a startup
# Allows users to delete a startup.
@app.route("/delete_startup/<int:startup_id>")
def delete_startup(startup_id):
    con = sqlite3.connect("FounderFitEvaluation.db")
    cur = con.cursor()
    cur.execute("DELETE FROM Startups_Table WHERE startup_id=?", (startup_id,))
    con.commit()
    con.close()
    return redirect("/startups")

# Route 8: Add a new evaluation
# Allow users to add a new evaluation.
@app.route("/add_evaluation", methods=["GET", "POST"])
def add_evaluation():
    con = sqlite3.connect("FounderFitEvaluation.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM Startups_Table")
    startups = cur.fetchall()

    if request.method == "POST":
        # Manually assign eval_id = current max + 1
        cur.execute("SELECT MAX(eval_id) FROM Evaluations_Table")
        max_id_row = cur.fetchone()
        new_id = (max_id_row[0] or 0) + 1

        startup_id = request.form["startup_id"]
        investor_id = request.form["investor_id"]
        fit_score = request.form["fit_score"]
        notes = request.form["notes"]

        cur.execute("""
            INSERT INTO Evaluations_Table (eval_id, startup_id, investor_id, fit_score, notes) VALUES (?, ?, ?, ?, ?)""",
            (new_id, startup_id, investor_id, fit_score, notes))
        
        con.commit()
        con.close()
        return redirect("/evaluations")

    return render_template("add_evaluation.html", startups=startups)

# Route 9: Edit an evaluation
# Allow users to edit an existing evaluation.
@app.route("/edit_evaluation/<int:eval_id>", methods=["GET", "POST"])
def edit_evaluation(eval_id):
    con = sqlite3.connect("FounderFitEvaluation.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    if request.method == "POST":
        startup_id = request.form["startup_id"]
        investor_id = request.form["investor_id"]
        fit_score = request.form["fit_score"]
        notes = request.form["notes"]

        cur.execute("""
            UPDATE Evaluations_Table SET startup_id=?, investor_id=?, fit_score=?, notes=? WHERE eval_id=?""",
            (startup_id, investor_id, fit_score, notes, eval_id))
        con.commit()
        con.close()
        return redirect("/evaluations")

    cur.execute("SELECT * FROM Evaluations_Table WHERE eval_id=?", (eval_id,))
    evaluation = cur.fetchone()
    cur.execute("SELECT * FROM Startups_Table")
    startups = cur.fetchall()
    con.close()
    return render_template("edit_evaluation.html", evaluation=evaluation, startups=startups)

# Route 10: Delete an evaluation
# Allow users to delete an evaluation.
@app.route("/delete_evaluation/<int:eval_id>")
def delete_evaluation(eval_id):
    con = sqlite3.connect("FounderFitEvaluation.db")
    cur = con.cursor()
    cur.execute("DELETE FROM Evaluations_Table WHERE eval_id=?", (eval_id,))
    con.commit()
    con.close()
    return redirect("/evaluations")

# Route 11: Add a new founder
# Allow users to add a new founder.
@app.route("/add_founder", methods=["GET", "POST"])
def add_founder():
    con = sqlite3.connect("FounderFitEvaluation.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    if request.method == "POST":
        # Manually assign founder_id = current max + 1
        cur.execute("SELECT MAX(founder_id) FROM Founders_Table")
        max_id_row = cur.fetchone()
        new_id = (max_id_row[0] or 0) + 1  # Handles empty table case

        name = request.form["name"]
        education = request.form["education"]
        experience_years = request.form["experience_years"]
        prev_startups = request.form["prev_startups"]
        domain_expertise = request.form["domain_expertise"]

        cur.execute("""
            INSERT INTO Founders_Table (founder_id, name, education, experience_years, prev_startups, domain_expertise) VALUES (?, ?, ?, ?, ?, ?)""",
            (new_id, name, education, experience_years, prev_startups, domain_expertise))
        
        con.commit()
        con.close()
        return redirect("/founders")

    return render_template("add_founder.html")

# Route 12: Edit a founder
# Allow users to edit an existing founder.
@app.route("/edit_founder/<int:founder_id>", methods=["GET", "POST"])
def edit_founder(founder_id):
    con = sqlite3.connect("FounderFitEvaluation.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    if request.method == "POST":
        name = request.form["name"]
        education = request.form["education"]
        experience_years = request.form["experience_years"]
        prev_startups = request.form["prev_startups"]
        domain_expertise = request.form["domain_expertise"]

        cur.execute("""
            UPDATE Founders_Table SET name=?, education=?, experience_years=?, prev_startups=?, domain_expertise=? WHERE founder_id=?""",
            (name, education, experience_years, prev_startups, domain_expertise, founder_id))
        con.commit()
        con.close()
        return redirect("/founders")

    cur.execute("SELECT * FROM Founders_Table WHERE founder_id=?", (founder_id,))
    founder = cur.fetchone()
    con.close()
    return render_template("edit_founder.html", founder=founder)

# Route 13: Delete a founder
# Allow users to delete a founder.
@app.route("/delete_founder/<int:founder_id>")
def delete_founder(founder_id):
    con = sqlite3.connect("FounderFitEvaluation.db")
    cur = con.cursor()
    cur.execute("DELETE FROM Founders_Table WHERE founder_id = ?", (founder_id,))
    con.commit()
    con.close()
    return redirect("/founders")


## -------------------------------------------------------------------------------------------------------------------
## Table Statistic Routes


# Route 14: Statistics for Founders
# Display statistics about founders.
@app.route("/stats_founders")
def stats_founders():
    con = sqlite3.connect("FounderFitEvaluation.db")
    df = pd.read_sql_query("SELECT * FROM Founders_Table", con)
    con.close()

    stats = {
        "Total Founders": len(df),
        "Avg Experience (Years)": round(df["experience_years"].mean(), 2),
        "Max Experience": int(df["experience_years"].max()),
        "Min Experience": int(df["experience_years"].min()),
        "Avg Prior Startups": round(df["prev_startups"].mean(), 2),
        "Unique Domains": df["domain_expertise"].nunique()
    }

    return render_template("stats_founders.html", stats=stats)

# Route 15: Statistics for Startups
# Display statistics about startups.
@app.route("/stats_startups")
def stats_startups():
    con = sqlite3.connect("FounderFitEvaluation.db")
    df = pd.read_sql_query("SELECT * FROM Startups_Table", con)
    con.close()

    stats = {
        "Total Startups": len(df),
        "Avg Team Size": round(df["team_size"].mean(), 2),
        "Max Team Size": int(df["team_size"].max()),
        "Min Team Size": int(df["team_size"].min()),
        "Avg Funding Ask ($)": round(df["funding_ask"].mean(), 2),
        "Max Funding Ask": round(df["funding_ask"].max(), 2),
        "Most Common Sector": df["sector"].mode().iloc[0] if not df["sector"].mode().empty else "N/A"
    }

    return render_template("stats_startups.html", stats=stats)

# Route 16: Statistics for Evaluations
# Display statistics about evaluations.
@app.route("/stats_evaluations")
def stats_evaluations():
    con = sqlite3.connect("FounderFitEvaluation.db")
    df = pd.read_sql_query("SELECT * FROM Evaluations_Table", con)
    con.close()

    stats = {
        "Total Evaluations": len(df),
        "Avg Fit Score": round(df["fit_score"].mean(), 2),
        "Min Fit Score": round(df["fit_score"].min(), 2),
        "Max Fit Score": round(df["fit_score"].max(), 2),
        "Median Fit Score": round(df["fit_score"].median(), 2),
        "Std Dev of Fit Score": round(df["fit_score"].std(), 2),
        "Unique Investors": df["investor_id"].nunique()
    }

    return render_template("stats_evaluations.html", stats=stats)


## -------------------------------------------------------------------------------------------------------------------
## Join Routes


# Route 17: Average Score by Founder
# Display the average score by founder using a JOIN in SQL.
@app.route("/avg_score_by_founder")
def avg_score_by_founder():
    con = sqlite3.connect("FounderFitEvaluation.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    cur.execute(
        """SELECT f.name AS founder_name, AVG(e.fit_score) AS avg_score FROM Evaluations_Table e JOIN Startups_Table s ON e.startup_id = s.startup_id
        JOIN Founders_Table f ON s.founder_id = f.founder_id GROUP BY f.name """)
    results = cur.fetchall()
    con.close()
    return render_template("avg_score_by_founder.html", results=results)

# Route 18: Key Information
# Display key information about evaluations using JOIN in SQL.
@app.route("/key_info")
def key_info():
    con = sqlite3.connect("FounderFitEvaluation.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    query = """
        SELECT f.name AS founder_name, s.name AS startup_name, e.fit_score, e.notes
        FROM Evaluations_Table e JOIN Startups_Table s ON e.startup_id = s.startup_id JOIN Founders_Table f ON s.founder_id = f.founder_id
    """

    cur.execute(query)
    results = cur.fetchall()
    con.close()

    return render_template("key_info.html", results=results)


## -------------------------------------------------------------------------------------------------------------------
## Visualizations

# Route 19: Visuals
# Display visualizations of the data.
@app.route("/visuals")
def visuals():
    os.makedirs("static", exist_ok=True)

    con = sqlite3.connect("FounderFitEvaluation.db")
    df = pd.read_sql_query("SELECT * FROM Startups_Table", con)
    con.close()

    # Bar plot: Total funding per sector
    funding_by_sector = df.groupby("sector")["funding_ask"].sum().sort_values(ascending=False)
    plt.figure(figsize=(8, 5))
    funding_by_sector.plot(kind="bar")
    plt.title("Total Funding by Sector")
    plt.ylabel("Funding ($)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("static/funding_by_sector.png")
    plt.close()

    # Histogram: Funding Ask Distribution
    plt.figure(figsize=(8, 5))
    df["funding_ask"].plot(kind="hist", bins=10, edgecolor="black")
    plt.title("Distribution of Funding Ask Amounts")
    plt.xlabel("Funding Ask ($)")
    plt.ylabel("Number of Startups")
    plt.tight_layout()
    plt.savefig("static/funding_distribution.png")
    plt.close()

    return render_template("visuals.html")


## -------------------------------------------------------------------------------------------------------------------
## Query Routes

# Route 20: Query Founders
# Allow users to query founders based on domain expertise.
@app.route("/query_founders", methods=["GET", "POST"])
def query_founders():
    results = []
    if request.method == "POST":
        domain = request.form["domain"]
        con = sqlite3.connect("FounderFitEvaluation.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM Founders_Table WHERE domain_expertise LIKE ?", ('%' + domain + '%',))
        results = cur.fetchall()
        con.close()

    return render_template("query_founders.html", results=results)

# Route 21: Query Startups
# Allow users to query startups based on sector.
@app.route("/query_startups", methods=["GET", "POST"])
def query_startups():
    results = []
    if request.method == "POST":
        sector = request.form["sector"]
        con = sqlite3.connect("FounderFitEvaluation.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM Startups_Table WHERE sector LIKE ?", ('%' + sector + '%',))
        results = cur.fetchall()
        con.close()
    return render_template("query_startups.html", results=results)

# Route 22: Query Evaluations
# Allow users to query evaluations based on score.
@app.route("/query_evaluations", methods=["GET", "POST"])
def query_evaluations():
    results = []
    if request.method == "POST":
        threshold = request.form["score"]
        con = sqlite3.connect("FounderFitEvaluation.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM Evaluations_Table WHERE fit_score >= ?", (threshold,))
        results = cur.fetchall()
        con.close()
    return render_template("query_evaluations.html", results=results)


app.run(debug=True)