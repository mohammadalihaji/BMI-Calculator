# Oasis Infobyte — Task 2: Body Mass Index (BMI) Calculator Suite

A complete Body Mass Index (BMI) tracking suite featuring **3 deployment options**:
1. 🌐 **Web Application (`python app.py`)** — Full-stack browser application connected to SQLite with live trend graphs.
2. 🖥️ **Desktop GUI (`python bmi_gui.py`)** — Classic Tkinter desktop window.
3. 💻 **Command-Line Interface (`python bmi_cli.py`)** — Terminal tool with strict input validation.

---

## 🚀 Features Checklist

### ✅ Beginner Tier (Command-Line Tool)
- [x] Prompt user for weight (kg) and height (m) via command line.
- [x] Calculate BMI using the standard formula: $\text{BMI} = \frac{\text{weight}}{\text{height}^2}$.
- [x] Classify results into WHO standard categories:
  - **Underweight**: $< 18.5$
  - **Normal weight**: $18.5 - 24.9$
  - **Overweight**: $25.0 - 29.9$
  - **Obese**: $\ge 30.0$
- [x] Display BMI rounded to 2 decimal places with the descriptive category.
- [x] Robust input validation: rejects negative values, zero, and non-numeric inputs with helpful guidance.

### ✅ Advanced Tier (Desktop GUI & Web Application)
- [x] **Full GUI Window**: Built using Python `app.py` (Web browser GUI) and `bmi_gui.py` (Desktop GUI).
- [x] **Input Fields & Labels**: Structured inputs for weight (kg) and height (m or cm) with instant calculation.
- [x] **Colour-Coded Feedback**: Real-time badge indicators:
  - 🔵 **Underweight**: Soft blue
  - 🟢 **Normal**: Healthy green
  - 🟠 **Overweight**: Warning orange
  - 🔴 **Obese**: Alert red
- [x] **Multi-User Support**: Add and switch profiles (persists history per user).
- [x] **Historical Records Storage**: Persistent local **SQLite3** database (`bmi_history.db`).
- [x] **Graph View (Trend Analytics)**: Line charts plotting BMI trends over time with shaded WHO benchmark zones.
- [x] **Error Handling**: Graceful warnings for empty fields, non-numeric values, or database errors.

---

## 📁 Project Structure

```text
BMI Calulator/
│
├── app.py              # Primary Web Server: Serves browser app & connects to SQLite
├── index.html          # Web UI: Interactive frontend with live trend charts
├── bmi_gui.py          # Desktop GUI: Tkinter interface
├── bmi_cli.py          # Beginner CLI: Terminal version with input validation
├── database.py         # Data Access: SQLite persistence layer
├── charts.py           # Matplotlib visualization module
├── bmi_history.db      # SQLite database storing multi-user records
└── README.md           # Documentation
```

---

## 💻 How to Run

### 🌐 Option 1: Run in Browser (Recommended)
Simply run:
```bash
python app.py
```
*(Or `.\venv\Scripts\python.exe app.py`)*

This starts the server at `http://127.0.0.1:5000` and automatically opens your web browser!

---

### 🖥️ Option 2: Run Desktop GUI (Tkinter)
```bash
python bmi_gui.py
```

---

### 💻 Option 3: Run Command-Line Version (CLI)
```bash
python bmi_cli.py
```
