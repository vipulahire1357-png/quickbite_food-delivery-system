# 🚀 SETUP & RUN GUIDE — QuickBite Food Delivery System

> **Platform:** Windows 10/11 (PowerShell or Command Prompt)  
> **Stack:** Python 3.x · Flask · SQLite · Jinja2

---

## ✅ Prerequisites

Before you start, make sure the following are installed on your machine:

| Tool | Minimum Version | Download |
|------|----------------|----------|
| Python | 3.10+ | https://python.org/downloads |
| pip | 23+ | Included with Python |
| Git | Any | https://git-scm.com *(optional)* |

> **Verify Python is installed:**
> ```powershell
> python --version
> ```
> You should see something like `Python 3.11.x`. If not, install Python 3.10+ and make sure **"Add Python to PATH"** is checked during installation.

---

## 📥 Step 1 — Clone or Download the Project

### Option A — Clone via Git
```powershell
git clone https://github.com/vipulahire1357-png/onlystudents.git
cd onlystudents
```

### Option B — Download ZIP
1. Go to the GitHub repository page
2. Click **Code → Download ZIP**
3. Extract the ZIP to your preferred folder
4. Open PowerShell and `cd` into the extracted folder

---

## 🐍 Step 2 — Create a Virtual Environment

A virtual environment keeps project dependencies isolated from your system Python.

```powershell
python -m venv venv
```

> This creates a `venv/` folder inside the project directory.

---

## ▶️ Step 3 — Activate the Virtual Environment

```powershell
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Windows Command Prompt
venv\Scripts\activate.bat
```

You'll know it's active when your terminal prompt shows `(venv)` at the beginning.

> **Troubleshoot (PowerShell execution policy error):**
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```
> Then re-run the activation command.

---

## 📦 Step 4 — Install Dependencies

```powershell
pip install -r requirements.txt
```

This installs:

| Package | Purpose |
|---------|---------|
| `flask>=2.3.0` | Web framework + routing + Jinja2 templating |

> SQLite is **built into Python** — no extra installation needed.

---

## 🗄️ Step 5 — Database Setup (Automatic)

The database is **created and seeded automatically** the first time you run the app.

On startup, `app.py` calls `init_db()` which:
1. Creates all 6 tables (`Customers`, `Restaurants`, `Menu`, `Delivery_Person`, `Orders`, `Order_Items`)
2. Seeds sample data if the database is empty:
   - **4 customers** — Aditi Sharma, Rohan Mehta, Priya Nair, Vikram Singh
   - **3 restaurants** — Spice Garden, Biryani Palace, Dosa Delight
   - **12 menu items** — across all restaurants
   - **3 delivery personnel** — Anil Kumar, Suresh Babu, Deepak Raj

> The database file `database.db` is created in the **root project directory**.

---

## 🏃 Step 6 — Run the Application

```powershell
python app.py
```

**Expected output:**
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

---

## 🌐 Step 7 — Open in Browser

Open your web browser and navigate to:

```
http://127.0.0.1:5000
```

or equivalently:

```
http://localhost:5000
```

---

## 📋 Available Pages

| Page | URL | What You Can Do |
|------|-----|-----------------|
| 🏠 Dashboard | `http://localhost:5000/` | View stats, recent orders |
| 👥 Customers | `http://localhost:5000/customers` | Add & view customers |
| 🏪 Restaurants | `http://localhost:5000/restaurants` | Manage restaurants & menus |
| 🛒 Place Order | `http://localhost:5000/place_order` | Create a new food order |
| 📦 All Orders | `http://localhost:5000/orders` | Filter & view all orders |
| 🛵 Delivery | `http://localhost:5000/delivery` | Manage delivery team |
| 📊 Reports | `http://localhost:5000/reports` | View analytics & SQL reports |

---

## 🔄 Stopping the Server

Press **`Ctrl + C`** in the terminal to stop the Flask development server.

---

## 🧹 Reset the Database

To start fresh with a clean database:

```powershell
# Make sure the server is stopped first (Ctrl+C)
del database.db

# Then run the app again — it will auto-recreate and reseed
python app.py
```

---

## 🗂️ Project Structure

```
quickbite_food-delivery-system/
│
├── app.py                  ← Main Flask app (routes + DB logic)
├── database.db             ← SQLite database (auto-created on first run)
├── requirements.txt        ← Python dependencies
├── README.md               ← Project documentation
├── SETUP_AND_RUN.md        ← This file
│
├── static/
│   └── style.css           ← CSS design system (dark mode)
│
└── templates/
    ├── base.html           ← Base layout with sidebar navigation
    ├── index.html          ← Dashboard
    ├── customers.html      ← Customer management
    ├── restaurants.html    ← Restaurant & menu management
    ├── place_order.html    ← Order placement form
    ├── orders.html         ← Order listing with filters
    ├── order_detail.html   ← Individual order bill
    ├── delivery.html       ← Delivery team management
    └── reports.html        ← Analytics & reports
```

---

## ❓ Common Issues & Fixes

### ❌ `ModuleNotFoundError: No module named 'flask'`
**Cause:** Virtual environment is not activated or Flask is not installed.  
**Fix:**
```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

### ❌ `python` is not recognized
**Cause:** Python is not in your system PATH.  
**Fix:** Reinstall Python and check ✅ **"Add Python to PATH"** during setup, OR use `py` instead of `python`:
```powershell
py app.py
```

---

### ❌ Port 5000 is already in use
**Fix:** Change the port inside `app.py` (last line):
```python
app.run(debug=True, port=5001)   # Change 5000 → 5001
```
Then visit `http://localhost:5001`.

---

### ❌ PowerShell Execution Policy Error
**Cause:** Windows blocks unsigned scripts by default.  
**Fix:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 🎓 DBMS Concepts Demonstrated

This project showcases the following database concepts:

| Concept | Where Used |
|---------|-----------|
| **Normalization (3NF)** | Separate tables for Menu, Orders, Order_Items |
| **Foreign Keys** | Orders → Customers, Menu → Restaurants, etc. |
| **INNER JOIN** | Orders with customer names |
| **LEFT JOIN** | Customers with optional order history |
| **Multi-table JOIN** | Order items with menu and restaurant details |
| **GROUP BY + Aggregate** | Revenue per customer/restaurant |
| **COALESCE** | Handling NULL delivery persons |
| **Subquery / Parameterized** | Safe SQL with `?` placeholders |

---

## 👩‍💻 Author

**Aditi** | DBMS Project — 2026  
Tech Stack: Python (Flask) + SQLite + Jinja2 + Vanilla CSS
