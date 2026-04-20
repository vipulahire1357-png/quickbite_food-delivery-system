# 🍔 QuickBite — Food Delivery System
### DBMS College Project | Python (Flask) + SQLite

> A fully functional, database-driven food delivery web application built as a college-level DBMS project. Demonstrates proper database design, CRUD operations, relational joins, and real-world use-case implementation.

---

## 📌 Project Overview

**QuickBite** is a web-based food delivery management system that allows administrators to:
- Manage **customers** and their delivery addresses
- Add **restaurants** and their **menu items**
- **Place orders** with automatic total calculation
- **Assign delivery personnel** and track order status
- View **analytics and reports** with SQL JOINs and aggregate queries

---

## 🧱 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3.x + Flask |
| **Database** | SQLite (via `database.db`) |
| **Frontend** | HTML5 + Vanilla CSS |
| **Templating** | Jinja2 (Flask built-in) |
| **Queries** | Raw SQL (no ORM) |

---

## 🗄️ Database Design

### Entity-Relationship Overview

```
Customers ──< Orders >── Delivery_Person
                │
           Order_Items
                │
             Menu >── Restaurants
```

### Tables & Schema

#### `Customers`
| Column | Type | Constraint |
|--------|------|-----------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT |
| name | TEXT | NOT NULL |
| phone | TEXT | NOT NULL |
| address | TEXT | NOT NULL |

#### `Restaurants`
| Column | Type | Constraint |
|--------|------|-----------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT |
| name | TEXT | NOT NULL |
| location | TEXT | NOT NULL |

#### `Menu`
| Column | Type | Constraint |
|--------|------|-----------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT |
| restaurant_id | INTEGER | FK → Restaurants(id) |
| item_name | TEXT | NOT NULL |
| price | REAL | NOT NULL |

#### `Delivery_Person`
| Column | Type | Constraint |
|--------|------|-----------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT |
| name | TEXT | NOT NULL |
| phone | TEXT | NOT NULL |

#### `Orders`
| Column | Type | Constraint |
|--------|------|-----------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT |
| customer_id | INTEGER | FK → Customers(id) |
| delivery_person_id | INTEGER | FK → Delivery_Person(id) |
| total_amount | REAL | NOT NULL DEFAULT 0 |
| status | TEXT | NOT NULL DEFAULT 'Pending' |
| order_date | TEXT | NOT NULL |

#### `Order_Items`
| Column | Type | Constraint |
|--------|------|-----------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT |
| order_id | INTEGER | FK → Orders(id) |
| menu_id | INTEGER | FK → Menu(id) |
| quantity | INTEGER | NOT NULL DEFAULT 1 |

---

## 🔗 Relationships

| Relationship | Type |
|---|---|
| Customer → Orders | One-to-Many |
| Restaurant → Menu | One-to-Many |
| Order → Order_Items | One-to-Many |
| Order → Delivery_Person | Many-to-One |
| Menu Item → Order_Items | One-to-Many |

---

## 📦 Core Features

### 1. 👥 Customer Management
- Add new customers with name, phone, and address
- View all customers with live order count (via LEFT JOIN)

### 2. 🏪 Restaurant & Menu
- Add restaurants with name and location
- Add menu items linked to a specific restaurant
- View all restaurants with their complete menus

### 3. 🛒 Order System
- Select a customer and multiple menu items
- Live total price calculation (JavaScript + SQL)
- Each order stores items in a separate `Order_Items` table (normalized)
- Multi-item orders fully supported

### 4. 🛵 Delivery Tracking
- Assign a delivery person to any order
- Update order status:
  - ⏳ **Pending** — Order received, not yet picked up
  - 🛵 **Out for Delivery** — Rider is on the way
  - ✅ **Delivered** — Customer received the order
- Filter orders by status on the orders page

### 5. 📈 Reports & Analytics
- Orders count and revenue **by customer**
- Revenue **by restaurant**
- **Top 10 best-selling menu items**
- Dashboard with total orders, total revenue, status breakdown

---

## ⚙️ Flask Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Dashboard with stats |
| `/customers` | GET | List all customers |
| `/customers/add` | POST | Add new customer |
| `/restaurants` | GET | List restaurants & menus |
| `/restaurants/add` | POST | Add new restaurant |
| `/menu/add` | POST | Add menu item |
| `/place_order` | GET, POST | Place a new order |
| `/orders` | GET | List all orders (filterable) |
| `/orders/<id>` | GET | Order detail / bill |
| `/orders/<id>/update` | POST | Update status & delivery person |
| `/delivery` | GET | List delivery personnel |
| `/delivery/add` | POST | Add delivery person |
| `/reports` | GET | Analytics page |

---

## 📊 SQL Queries Implemented

### 1. Orders with Customer Name (JOIN)
```sql
SELECT o.id, c.name, o.total_amount, o.status
FROM Orders o
JOIN Customers c ON o.customer_id = c.id
ORDER BY o.id DESC;
```

### 2. Order Items with Details (Multi-JOIN)
```sql
SELECT oi.quantity, m.item_name, m.price,
       (oi.quantity * m.price) AS subtotal, r.name AS restaurant
FROM Order_Items oi
JOIN Menu m ON oi.menu_id = m.id
JOIN Restaurants r ON m.restaurant_id = r.id
WHERE oi.order_id = ?;
```

### 3. Revenue by Customer
```sql
SELECT c.name, COUNT(o.id) AS total_orders,
       COALESCE(SUM(o.total_amount), 0) AS revenue
FROM Customers c
LEFT JOIN Orders o ON c.id = o.customer_id
GROUP BY c.id ORDER BY revenue DESC;
```

### 4. Top Selling Items
```sql
SELECT m.item_name, r.name AS restaurant,
       SUM(oi.quantity) AS qty_sold,
       SUM(oi.quantity * m.price) AS revenue
FROM Order_Items oi
JOIN Menu m ON oi.menu_id = m.id
JOIN Restaurants r ON m.restaurant_id = r.id
GROUP BY m.id ORDER BY qty_sold DESC LIMIT 10;
```

---

## 📁 Project Structure

```
food_delivery/
│
├── app.py                  ← Main Flask application (routes + DB logic)
├── database.db             ← SQLite database (auto-created on first run)
├── requirements.txt        ← Python dependencies
├── README.md               ← This file
├── SETUP_AND_RUN.md        ← Step-by-step setup guide
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
    ├── order_detail.html   ← Individual order + bill
    ├── delivery.html       ← Delivery team management
    └── reports.html        ← Analytics & reports
```

---

## 🎯 Sample Data (Preloaded)

The database is automatically seeded with:

- **4 Customers** — Aditi Sharma, Rohan Mehta, Priya Nair, Vikram Singh
- **3 Restaurants** — Spice Garden, Biryani Palace, Dosa Delight
- **12 Menu Items** — across all 3 restaurants
- **3 Delivery Personnel** — Anil Kumar, Suresh Babu, Deepak Raj

---

## 🖥️ UI Pages

| Page | URL | Purpose |
|------|-----|---------|
| Dashboard | `/` | Overview stats + recent orders |
| Customers | `/customers` | Add & view all customers |
| Restaurants | `/restaurants` | Manage restaurants + menus |
| Place Order | `/place_order` | Multi-item order form |
| All Orders | `/orders` | Filter, view, update orders |
| Order Detail | `/orders/<id>` | Full bill & delivery info |
| Delivery | `/delivery` | Manage delivery team |
| Reports | `/reports` | SQL analytics |

---

## 👩‍💻 Author

**Aditi** | DBMS Project — 2026  
Built with Python (Flask) + SQLite
