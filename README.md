# 🚀 Vision - Personal Productivity Intelligence System

> A data-driven productivity analytics platform that transforms behavioral data into actionable insights, performance trends, and productivity intelligence.

---

## 🎯 Project Overview

Vision is an end-to-end Python project that analyzes productivity behavior using data analytics, KPI scoring, trend analysis, and visualization techniques.

The system collects productivity-related metrics, stores them in a relational database, calculates a Productivity Score, identifies behavioral patterns, and generates automated insights to support data-driven self-improvement.

---

## ✨ Features

✅ Synthetic Productivity Data Generation

✅ SQLite Database Integration

✅ Productivity KPI Scoring (0–100)

✅ Weekly Trend Analysis

✅ Historical Productivity Tracking

✅ Rule-Based Insight Generation

✅ Productivity Visualizations

✅ Correlation Analysis of Productivity Factors

---

## 🏗️ Architecture

```text
Data Generation
      ↓
CSV Dataset
      ↓
SQLite Database
      ↓
Analytics Engine
      ↓
Productivity Scoring
      ↓
Trend Analysis
      ↓
Insight Generation
      ↓
Visualization Layer
      ↓
ML Forecasting
```

---

## 📂 Project Structure

```text
Vision/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── database/
│   └── focusiq.db
│
├── src/
│   ├── data_generator.py
│   ├── db_manager.py
│   ├── analysis.py
│   ├── metrics.py
│   ├── scoring.py
│   ├── productivity_history.py
│   ├── trend_analysis.py
│   ├── rules_engine.py
│   └── visualizer.py
│
└── visuals/
```

---

## 📊 Productivity Metrics

The system currently tracks:

| Metric                | Description               |
| --------------------- | ------------------------- |
| 📱 Phone Hours        | Daily screen time         |
| 😴 Sleep Quality      | Sleep quality score (1–5) |
| 😊 Mood               | Daily mood score (1–5)    |
| 🎯 Deep Work Hours    | Focused work duration     |
| ⏳ Distraction Minutes | Time lost to distractions |
| 📌 Primary Task       | Main activity performed   |

---

## 🧠 Analytics Capabilities

### Productivity Scoring Engine

Generates a composite productivity score based on:

* Deep Work Hours
* Phone Usage
* Sleep Quality
* Mood

### Trend Analysis Engine

Tracks productivity changes over time and compares recent performance against historical patterns.

### Rule-Based Intelligence Engine

Automatically generates productivity insights and identifies behavioral risks.

### Correlation Analysis

Measures relationships between productivity factors to uncover hidden patterns.

---

## 🛠️ Tech Stack

| Category        | Technologies        |
| --------------- | ------------------- |
| Programming     | Python              |
| Data Processing | Pandas, NumPy       |
| Database        | SQLite              |
| Visualization   | Matplotlib, Seaborn |
| File Handling   | Pathlib             |
| Date Processing | datetime            |

---


## 💡 Skills Demonstrated

* Data Analysis
* Data Engineering
* Database Management
* KPI Design
* Trend Analysis
* Data Visualization
* Python Development
* Business Intelligence
* Rule-Based Analytics
---

## 👨‍💻 Author

**Abhishek Kushwaha**

Data Science • Machine Learning • Artificial Intelligence

*"Turning productivity data into actionable intelligence."*
