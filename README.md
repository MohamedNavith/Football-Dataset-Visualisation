# **⚽ Football Analytics Pro (2014-2020)**

**A high-performance data visualisation dashboard to explore, compare, and analyze football player statistics from the EPL, La Liga, and Bundesliga.**

Built with **Python** and **Streamlit**, this app transforms raw CSV data into an interactive "Insane UI" experience with dark mode, automated insights, and professional-grade visualizations.

---

### **🚀 Features**

* **📊 Multi-League Analysis:** Switch between EPL, La Liga, and Bundesliga seamlessly.
* **🔍 Smart Player Search:** Instant auto-complete search to find any player's stats across 6 years.
* **⚔️ Head-to-Head Comparison:** A "Tale of the Tape" style comparison with ability radars and green/white advantage highlighting.
* **🛡️ Team Deep Dives:** Select a team to see how goals were distributed among the squad.
* **📈 Cumulative Impact:** Visualize a player's total contribution vs. their team and league averages.
* **📝 Statistical Summary:** The app generates a text-based performance report for any selected player.
* **🎨 Premium UI:** Dark mode, glassmorphism-inspired design, and interactive Plotly charts.

---

### **🛠️ Installation & Setup**

**1. Prerequisites**
You need **Python** installed on your computer.

**2. Project Structure**
Ensure your folder looks like this to avoid data errors:

```text
Football-Project/
│
├── dashboard.py           # The main application code
├── requirements.txt       # List of dependencies
│
└── data/                  # Folder containing your CSV files
    ├── EPL_14_20_players_stat.csv
    ├── laliga_14_20_players_stat.csv
    └── Bundesliga_14_20_players_stat.csv

```

**3. Install Dependencies**
Open your terminal (Command Prompt or VS Code Terminal) in the project folder and run:

```bash
pip install streamlit pandas plotly

```

---

### **▶️ How to Run**

1. Navigate to your project directory in the terminal:
```bash
cd "path/to/Football-Project"

```


2. Run the Streamlit app:
```bash
streamlit run dashboard.py

```


3. A new tab will automatically open in your browser at `http://localhost:8501`.

---

### **🧠 Code Overview**

This project uses **Streamlit** for the frontend and **Pandas** for data processing, all contained in a single file (`dashboard.py`).

* **Robust Data Loader:** Automatically detects the location of your `data/` folder, cleans the CSVs, and standardizes column names.
* **Dynamic Filtering:** Filters data by League → Team → Position → Player.
* **Visualization Engine:** Uses **Plotly** for interactive Scatter plots, Radar charts, and Combo charts.
* **Insights Logic:** Calculates efficiency (`Goals - xG`) and percentile rankings on the fly to generate insights.

---

### **⚠️ Troubleshooting**

* **"FileNotFoundError":** Check that your folder is named exactly `data` and contains the 3 CSV files.
* **"ModuleNotFoundError":** Run `pip install streamlit pandas plotly` again.

---

**License:** Open Source. Data from Kaggle (2014-2020 Aggregated Stats).