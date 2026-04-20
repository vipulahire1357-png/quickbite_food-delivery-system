from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "food_delivery_secret_2026"

DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")


# ─────────────────────────────────────────────
#  DB HELPERS
# ─────────────────────────────────────────────

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create tables and insert sample data if the DB is fresh."""
    conn = get_db()
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS Customers (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            name    TEXT    NOT NULL,
            phone   TEXT    NOT NULL,
            address TEXT    NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Restaurants (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            name     TEXT NOT NULL,
            location TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Menu (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            restaurant_id INTEGER NOT NULL,
            item_name     TEXT    NOT NULL,
            price         REAL    NOT NULL,
            FOREIGN KEY (restaurant_id) REFERENCES Restaurants(id)
        );

        CREATE TABLE IF NOT EXISTS Delivery_Person (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            name  TEXT NOT NULL,
            phone TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Orders (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id      INTEGER NOT NULL,
            delivery_person_id INTEGER,
            total_amount     REAL    NOT NULL DEFAULT 0,
            status           TEXT    NOT NULL DEFAULT 'Pending',
            order_date       TEXT    NOT NULL,
            FOREIGN KEY (customer_id)       REFERENCES Customers(id),
            FOREIGN KEY (delivery_person_id) REFERENCES Delivery_Person(id)
        );

        CREATE TABLE IF NOT EXISTS Order_Items (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            menu_id  INTEGER NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 1,
            FOREIGN KEY (order_id) REFERENCES Orders(id),
            FOREIGN KEY (menu_id)  REFERENCES Menu(id)
        );
    """)

    # Seed sample data only when tables are empty
    if c.execute("SELECT COUNT(*) FROM Customers").fetchone()[0] == 0:
        c.executescript("""
            INSERT INTO Customers (name, phone, address) VALUES
                ('Aditi Sharma',  '9876543210', '12, MG Road, Bangalore'),
                ('Rohan Mehta',   '9123456780', '45, Linking Rd, Mumbai'),
                ('Priya Nair',    '9988776655', '7, Anna Salai, Chennai'),
                ('Vikram Singh',  '9001122334', '33, Sector 17, Chandigarh');

            INSERT INTO Restaurants (name, location) VALUES
                ('Spice Garden',   'Koramangala, Bangalore'),
                ('Biryani Palace', 'Bandra, Mumbai'),
                ('Dosa Delight',   'T-Nagar, Chennai');

            INSERT INTO Menu (restaurant_id, item_name, price) VALUES
                (1, 'Paneer Butter Masala',  220.00),
                (1, 'Garlic Naan',            40.00),
                (1, 'Veg Fried Rice',        180.00),
                (1, 'Mango Lassi',            80.00),
                (2, 'Chicken Biryani',       280.00),
                (2, 'Mutton Biryani',        350.00),
                (2, 'Raita',                  50.00),
                (2, 'Gulab Jamun',            60.00),
                (3, 'Masala Dosa',           120.00),
                (3, 'Idli Sambar (3 pcs)',    90.00),
                (3, 'Filter Coffee',          40.00),
                (3, 'Vada (2 pcs)',           60.00);

            INSERT INTO Delivery_Person (name, phone) VALUES
                ('Anil Kumar',  '8800112233'),
                ('Suresh Babu', '7711223344'),
                ('Deepak Raj',  '9922334455');
        """)

    conn.commit()
    conn.close()


# ─────────────────────────────────────────────
#  HOME / DASHBOARD
# ─────────────────────────────────────────────

@app.route("/")
def index():
    conn = get_db()
    stats = {}
    stats["total_orders"]      = conn.execute("SELECT COUNT(*) FROM Orders").fetchone()[0]
    stats["total_revenue"]     = conn.execute("SELECT COALESCE(SUM(total_amount),0) FROM Orders").fetchone()[0]
    stats["total_customers"]   = conn.execute("SELECT COUNT(*) FROM Customers").fetchone()[0]
    stats["total_restaurants"] = conn.execute("SELECT COUNT(*) FROM Restaurants").fetchone()[0]
    stats["pending"]    = conn.execute("SELECT COUNT(*) FROM Orders WHERE status='Pending'").fetchone()[0]
    stats["out"]        = conn.execute("SELECT COUNT(*) FROM Orders WHERE status='Out for Delivery'").fetchone()[0]
    stats["delivered"]  = conn.execute("SELECT COUNT(*) FROM Orders WHERE status='Delivered'").fetchone()[0]

    recent_orders = conn.execute("""
        SELECT o.id, c.name AS customer, o.total_amount, o.status, o.order_date
        FROM Orders o
        JOIN Customers c ON o.customer_id = c.id
        ORDER BY o.id DESC LIMIT 5
    """).fetchall()

    conn.close()
    return render_template("index.html", stats=stats, recent_orders=recent_orders)


# ─────────────────────────────────────────────
#  CUSTOMERS
# ─────────────────────────────────────────────

@app.route("/customers")
def customers():
    conn = get_db()
    all_customers = conn.execute(
        "SELECT c.*, COUNT(o.id) AS order_count FROM Customers c "
        "LEFT JOIN Orders o ON c.id = o.customer_id GROUP BY c.id ORDER BY c.id"
    ).fetchall()
    conn.close()
    return render_template("customers.html", customers=all_customers)


@app.route("/customers/add", methods=["POST"])
def add_customer():
    name    = request.form.get("name", "").strip()
    phone   = request.form.get("phone", "").strip()
    address = request.form.get("address", "").strip()

    if not name or not phone or not address:
        flash("All fields are required.", "error")
        return redirect(url_for("customers"))

    conn = get_db()
    conn.execute("INSERT INTO Customers (name, phone, address) VALUES (?,?,?)",
                 (name, phone, address))
    conn.commit()
    conn.close()
    flash(f"Customer '{name}' added successfully!", "success")
    return redirect(url_for("customers"))


# ─────────────────────────────────────────────
#  RESTAURANTS & MENU
# ─────────────────────────────────────────────

@app.route("/restaurants")
def restaurants():
    conn = get_db()
    all_restaurants = conn.execute("SELECT * FROM Restaurants ORDER BY id").fetchall()
    menu_items = conn.execute(
        "SELECT m.*, r.name AS restaurant_name FROM Menu m "
        "JOIN Restaurants r ON m.restaurant_id = r.id ORDER BY m.restaurant_id, m.item_name"
    ).fetchall()
    conn.close()
    return render_template("restaurants.html",
                           restaurants=all_restaurants, menu_items=menu_items)


@app.route("/restaurants/add", methods=["POST"])
def add_restaurant():
    name     = request.form.get("name", "").strip()
    location = request.form.get("location", "").strip()
    if not name or not location:
        flash("Restaurant name and location are required.", "error")
        return redirect(url_for("restaurants"))

    conn = get_db()
    conn.execute("INSERT INTO Restaurants (name, location) VALUES (?,?)", (name, location))
    conn.commit()
    conn.close()
    flash(f"Restaurant '{name}' added!", "success")
    return redirect(url_for("restaurants"))


@app.route("/menu/add", methods=["POST"])
def add_menu_item():
    restaurant_id = request.form.get("restaurant_id", "").strip()
    item_name     = request.form.get("item_name", "").strip()
    price         = request.form.get("price", "").strip()

    if not restaurant_id or not item_name or not price:
        flash("All menu fields are required.", "error")
        return redirect(url_for("restaurants"))

    try:
        price = float(price)
        if price <= 0:
            raise ValueError
    except ValueError:
        flash("Price must be a positive number.", "error")
        return redirect(url_for("restaurants"))

    conn = get_db()
    conn.execute("INSERT INTO Menu (restaurant_id, item_name, price) VALUES (?,?,?)",
                 (restaurant_id, item_name, price))
    conn.commit()
    conn.close()
    flash(f"Menu item '{item_name}' added!", "success")
    return redirect(url_for("restaurants"))


# ─────────────────────────────────────────────
#  ORDERS
# ─────────────────────────────────────────────

@app.route("/orders")
def orders():
    conn = get_db()
    status_filter = request.args.get("status", "")

    query = """
        SELECT o.id, c.name AS customer, o.total_amount, o.status,
               o.order_date, COALESCE(dp.name, 'Not Assigned') AS delivery_person
        FROM Orders o
        JOIN Customers c ON o.customer_id = c.id
        LEFT JOIN Delivery_Person dp ON o.delivery_person_id = dp.id
    """
    if status_filter:
        all_orders = conn.execute(query + " WHERE o.status=? ORDER BY o.id DESC",
                                  (status_filter,)).fetchall()
    else:
        all_orders = conn.execute(query + " ORDER BY o.id DESC").fetchall()

    delivery_persons = conn.execute("SELECT * FROM Delivery_Person").fetchall()
    conn.close()
    return render_template("orders.html", orders=all_orders,
                           delivery_persons=delivery_persons,
                           status_filter=status_filter)


@app.route("/orders/<int:order_id>")
def order_detail(order_id):
    conn = get_db()
    order = conn.execute("""
        SELECT o.*, c.name AS customer_name, c.phone AS customer_phone,
               c.address AS customer_address,
               COALESCE(dp.name,'Not Assigned') AS delivery_name,
               COALESCE(dp.phone,'—') AS delivery_phone
        FROM Orders o
        JOIN Customers c ON o.customer_id = c.id
        LEFT JOIN Delivery_Person dp ON o.delivery_person_id = dp.id
        WHERE o.id = ?
    """, (order_id,)).fetchone()

    if not order:
        flash("Order not found.", "error")
        return redirect(url_for("orders"))

    items = conn.execute("""
        SELECT oi.quantity, m.item_name, m.price,
               (oi.quantity * m.price) AS subtotal,
               r.name AS restaurant
        FROM Order_Items oi
        JOIN Menu m ON oi.menu_id = m.id
        JOIN Restaurants r ON m.restaurant_id = r.id
        WHERE oi.order_id = ?
    """, (order_id,)).fetchall()

    conn.close()
    return render_template("order_detail.html", order=order, items=items)


@app.route("/place_order", methods=["GET", "POST"])
def place_order():
    conn = get_db()

    if request.method == "POST":
        customer_id = request.form.get("customer_id")
        menu_ids    = request.form.getlist("menu_id")
        quantities  = request.form.getlist("quantity")

        if not customer_id or not menu_ids:
            flash("Please select a customer and at least one item.", "error")
            return redirect(url_for("place_order"))

        # Calculate total
        total = 0.0
        for mid, qty in zip(menu_ids, quantities):
            try:
                q = int(qty)
                if q <= 0:
                    continue
            except ValueError:
                continue
            price = conn.execute("SELECT price FROM Menu WHERE id=?", (mid,)).fetchone()
            if price:
                total += price["price"] * q

        if total == 0:
            flash("Order total is zero — check item quantities.", "error")
            return redirect(url_for("place_order"))

        order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cur = conn.execute(
            "INSERT INTO Orders (customer_id, total_amount, status, order_date) VALUES (?,?,?,?)",
            (customer_id, total, "Pending", order_date)
        )
        order_id = cur.lastrowid

        for mid, qty in zip(menu_ids, quantities):
            try:
                q = int(qty)
                if q <= 0:
                    continue
            except ValueError:
                continue
            conn.execute(
                "INSERT INTO Order_Items (order_id, menu_id, quantity) VALUES (?,?,?)",
                (order_id, mid, q)
            )

        conn.commit()
        conn.close()
        flash(f"Order #{order_id} placed successfully! Total: ₹{total:.2f}", "success")
        return redirect(url_for("orders"))

    customers   = conn.execute("SELECT * FROM Customers ORDER BY name").fetchall()
    restaurants = conn.execute("SELECT * FROM Restaurants ORDER BY name").fetchall()
    menu_items  = conn.execute(
        "SELECT m.*, r.name AS restaurant_name FROM Menu m "
        "JOIN Restaurants r ON m.restaurant_id = r.id ORDER BY r.name, m.item_name"
    ).fetchall()
    conn.close()
    return render_template("place_order.html",
                           customers=customers,
                           restaurants=restaurants,
                           menu_items=menu_items)


# ─────────────────────────────────────────────
#  DELIVERY
# ─────────────────────────────────────────────

@app.route("/orders/<int:order_id>/update", methods=["POST"])
def update_order(order_id):
    status            = request.form.get("status")
    delivery_person_id = request.form.get("delivery_person_id") or None

    allowed_statuses = ["Pending", "Out for Delivery", "Delivered"]
    if status not in allowed_statuses:
        flash("Invalid status.", "error")
        return redirect(url_for("orders"))

    conn = get_db()
    conn.execute(
        "UPDATE Orders SET status=?, delivery_person_id=? WHERE id=?",
        (status, delivery_person_id, order_id)
    )
    conn.commit()
    conn.close()
    flash(f"Order #{order_id} updated to '{status}'.", "success")
    return redirect(url_for("orders"))


# ─────────────────────────────────────────────
#  REPORTS
# ─────────────────────────────────────────────

@app.route("/reports")
def reports():
    conn = get_db()

    orders_by_customer = conn.execute("""
        SELECT c.name, COUNT(o.id) AS total_orders, COALESCE(SUM(o.total_amount),0) AS revenue
        FROM Customers c
        LEFT JOIN Orders o ON c.id = o.customer_id
        GROUP BY c.id ORDER BY revenue DESC
    """).fetchall()

    orders_by_restaurant = conn.execute("""
        SELECT r.name, COUNT(DISTINCT o.id) AS total_orders,
               COALESCE(SUM(oi.quantity * m.price), 0) AS revenue
        FROM Restaurants r
        JOIN Menu m ON m.restaurant_id = r.id
        LEFT JOIN Order_Items oi ON oi.menu_id = m.id
        LEFT JOIN Orders o ON oi.order_id = o.id
        GROUP BY r.id ORDER BY revenue DESC
    """).fetchall()

    top_items = conn.execute("""
        SELECT m.item_name, r.name AS restaurant,
               SUM(oi.quantity) AS qty_sold,
               SUM(oi.quantity * m.price) AS revenue
        FROM Order_Items oi
        JOIN Menu m ON oi.menu_id = m.id
        JOIN Restaurants r ON m.restaurant_id = r.id
        GROUP BY m.id ORDER BY qty_sold DESC LIMIT 10
    """).fetchall()

    conn.close()
    return render_template("reports.html",
                           orders_by_customer=orders_by_customer,
                           orders_by_restaurant=orders_by_restaurant,
                           top_items=top_items)


# ─────────────────────────────────────────────
#  DELIVERY PERSONS
# ─────────────────────────────────────────────

@app.route("/delivery")
def delivery():
    conn = get_db()
    persons = conn.execute("""
        SELECT dp.*, COUNT(o.id) AS deliveries
        FROM Delivery_Person dp
        LEFT JOIN Orders o ON dp.id = o.delivery_person_id
        GROUP BY dp.id ORDER BY dp.id
    """).fetchall()
    conn.close()
    return render_template("delivery.html", persons=persons)


@app.route("/delivery/add", methods=["POST"])
def add_delivery_person():
    name  = request.form.get("name", "").strip()
    phone = request.form.get("phone", "").strip()
    if not name or not phone:
        flash("Name and phone are required.", "error")
        return redirect(url_for("delivery"))

    conn = get_db()
    conn.execute("INSERT INTO Delivery_Person (name, phone) VALUES (?,?)", (name, phone))
    conn.commit()
    conn.close()
    flash(f"Delivery person '{name}' added!", "success")
    return redirect(url_for("delivery"))


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)
