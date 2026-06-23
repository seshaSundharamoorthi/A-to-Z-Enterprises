"""
A to Z Enterprises - Mobile Accessories & Repair Shop
Flask Backend — SQLite version (no MySQL setup needed!)
"""

import os
import sqlite3
from datetime import timedelta, datetime
from functools import wraps

from flask import (
    Flask, render_template, request, redirect, url_for,
    session, flash, g
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.secret_key = "atoz-enterprises-secret-2024"
app.permanent_session_lifetime = timedelta(hours=4)

DB_PATH = os.path.join(os.path.dirname(__file__), "atoz.db")

SHOP_INFO = {
    "name": "A to Z Enterprises",
    "tagline": "Mobile Accessories & Repair Specialists",
    "phone_1": "8838519294",
    "phone_2": "8248398049",
    "email": "seshasundharamoorthi2005@gmail.com",
    "address": "Muthayammal Engineering College Opposite, Kakaveri, Rasipuram, Namakkal",
    "hours": "Morning 8:00 AM – Night 10:00 PM",
}


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        val = row[idx]
        if col[0] == "created_at" and val and isinstance(val, str):
            try:
                val = datetime.fromisoformat(val)
            except:
                pass
        d[col[0]] = val
    return d


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = dict_factory
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    """Create tables and seed data if DB doesn't exist."""
    if os.path.exists(DB_PATH):
        return
    conn = get_db()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS admin_users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TEXT DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        slug TEXT UNIQUE NOT NULL,
        display_order INTEGER DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        description TEXT,
        price REAL NOT NULL,
        mrp REAL,
        image_url TEXT,
        in_stock INTEGER DEFAULT 1,
        is_featured INTEGER DEFAULT 0,
        created_at TEXT DEFAULT (datetime('now')),
        FOREIGN KEY (category_id) REFERENCES categories(id)
    );

    CREATE TABLE IF NOT EXISTS repair_services (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        service_name TEXT NOT NULL,
        description TEXT,
        price_range TEXT NOT NULL,
        estimated_time TEXT,
        icon_key TEXT,
        display_order INTEGER DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT NOT NULL,
        rating INTEGER NOT NULL,
        review_text TEXT NOT NULL,
        is_approved INTEGER DEFAULT 0,
        created_at TEXT DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS enquiries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        message TEXT,
        enquiry_type TEXT DEFAULT 'general',
        is_read INTEGER DEFAULT 0,
        created_at TEXT DEFAULT (datetime('now'))
    );

    INSERT INTO categories (name, slug, display_order) VALUES
        ('Mobile Cases & Covers', 'cases-covers', 1),
        ('Chargers & Adapters', 'chargers', 2),
        ('Earphones & Headsets', 'earphones', 3),
        ('Power Banks', 'power-banks', 4),
        ('Cables', 'cables', 5),
        ('Screen Guards & Tempered Glass', 'screen-guards', 6),
        ('Bluetooth Speakers', 'speakers', 7),
        ('Mobile Holders & Stands', 'holders', 8);

    INSERT INTO repair_services (service_name, description, price_range, estimated_time, icon_key, display_order) VALUES
        ('Screen / Display Repair', 'Cracked or dead display replacement for all major brands', 'Rs.800 - Rs.4500', '45 mins', 'screen', 1),
        ('Battery Replacement', 'Original quality battery replacement with 6 month warranty', 'Rs.500 - Rs.2000', '20 mins', 'battery', 2),
        ('Charging Port Repair', 'Fix loose or non-working charging port issues', 'Rs.400 - Rs.1200', '30 mins', 'charging', 3),
        ('Speaker / Mic Repair', 'Speaker, earpiece and microphone repair or replacement', 'Rs.350 - Rs.1000', '25 mins', 'speaker', 4),
        ('Camera Repair', 'Front and back camera module repair / replacement', 'Rs.600 - Rs.3000', '40 mins', 'camera', 5),
        ('Water Damage Service', 'Complete cleaning and component-level water damage repair', 'Rs.500 - Rs.3500', '24-48 hrs', 'water', 6);

    INSERT INTO products (category_id, name, description, price, mrp, in_stock, is_featured) VALUES
        (1, 'Shockproof Back Cover', 'Military grade drop protection, all popular models available', 199, 399, 1, 1),
        (1, 'Transparent TPU Case', 'Slim fit clear case with anti-yellowing coating', 149, 299, 1, 0),
        (1, 'Leather Flip Cover', 'Premium PU leather with card slots', 299, 599, 1, 0),
        (2, '20W Fast Charger', 'PD fast charging adapter, type-C output', 449, 899, 1, 1),
        (2, '33W Multi-Port Adapter', 'Dual port charger for phone and accessories together', 599, 1199, 1, 0),
        (3, 'Wired Earphones with Mic', 'Clear bass, in-line mic and remote', 199, 399, 1, 0),
        (3, 'Bluetooth Neckband', '20 hours battery, fast charging, deep bass', 699, 1499, 1, 1),
        (4, '10000mAh Power Bank', 'Dual output, fast charging support', 899, 1599, 1, 1),
        (5, 'Type-C Fast Charging Cable', '1 meter braided cable, 3A fast charging', 99, 199, 1, 0),
        (6, 'Tempered Glass 9H', 'Edge to edge protection, anti-fingerprint coating', 99, 249, 1, 0),
        (7, 'Mini Bluetooth Speaker', 'Portable speaker with deep bass, 8 hr playback', 599, 1199, 1, 0),
        (8, 'Car Mobile Holder', '360 degree rotating dashboard mount', 249, 499, 1, 0);

    INSERT INTO reviews (customer_name, rating, review_text, is_approved) VALUES
        ('Karthik R', 5, 'Screen repair was quick and affordable. Phone works like new!', 1),
        ('Priya S', 5, 'Bought a power bank here, good quality and genuine pricing.', 1),
        ('Manoj Kumar', 4, 'Battery replacement done same day. Good service.', 1);
    """)
    conn.commit()
    conn.close()
    print("✅ Database created with sample data!")


def login_required(view_func):
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if not session.get("admin_logged_in"):
            flash("Please login to continue.", "error")
            return redirect(url_for("admin_login"))
        return view_func(*args, **kwargs)
    return wrapped


# ========================================================================
# PUBLIC ROUTES
# ========================================================================

@app.route("/")
def home():
    conn = get_db()
    featured_products = conn.execute(
        "SELECT * FROM products WHERE is_featured=1 AND in_stock=1 ORDER BY id DESC LIMIT 8"
    ).fetchall()
    repair_services = conn.execute(
        "SELECT * FROM repair_services ORDER BY display_order"
    ).fetchall()
    reviews = conn.execute(
        "SELECT * FROM reviews WHERE is_approved=1 ORDER BY id DESC LIMIT 6"
    ).fetchall()
    conn.close()
    return render_template("index.html", shop=SHOP_INFO,
                           featured_products=featured_products,
                           repair_services=repair_services,
                           reviews=reviews)


@app.route("/products")
def products():
    selected_category = request.args.get("category", type=int)
    conn = get_db()
    categories = conn.execute("SELECT * FROM categories ORDER BY display_order").fetchall()
    if selected_category:
        product_list = conn.execute(
            "SELECT * FROM products WHERE category_id=? ORDER BY in_stock DESC, id DESC",
            (selected_category,)
        ).fetchall()
    else:
        product_list = conn.execute(
            "SELECT * FROM products ORDER BY in_stock DESC, id DESC"
        ).fetchall()
    conn.close()
    return render_template("products.html", shop=SHOP_INFO,
                           categories=categories, products=product_list,
                           selected_category=selected_category)


@app.route("/repairs")
def repairs():
    conn = get_db()
    repair_services = conn.execute("SELECT * FROM repair_services ORDER BY display_order").fetchall()
    conn.close()
    return render_template("repairs.html", shop=SHOP_INFO, repair_services=repair_services)


@app.route("/reviews")
def reviews_page():
    conn = get_db()
    reviews = conn.execute(
        "SELECT * FROM reviews WHERE is_approved=1 ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return render_template("reviews.html", shop=SHOP_INFO, reviews=reviews)


@app.route("/reviews/submit", methods=["POST"])
def submit_review():
    name = request.form.get("customer_name", "").strip()
    rating = request.form.get("rating", type=int)
    text = request.form.get("review_text", "").strip()
    if not name or not rating or not text:
        flash("Please fill all fields.", "error")
        return redirect(url_for("reviews_page"))
    conn = get_db()
    conn.execute(
        "INSERT INTO reviews (customer_name, rating, review_text, is_approved) VALUES (?,?,?,0)",
        (name, rating, text)
    )
    conn.commit()
    conn.close()
    flash("Thank you! Your review will appear after approval.", "success")
    return redirect(url_for("reviews_page"))


@app.route("/contact")
def contact():
    return render_template("contact.html", shop=SHOP_INFO)


@app.route("/contact/submit", methods=["POST"])
def submit_enquiry():
    name = request.form.get("name", "").strip()
    phone = request.form.get("phone", "").strip()
    message = request.form.get("message", "").strip()
    enquiry_type = request.form.get("enquiry_type", "general")
    if not name or not phone:
        flash("Name and phone are required.", "error")
        return redirect(url_for("contact"))
    conn = get_db()
    conn.execute(
        "INSERT INTO enquiries (name, phone, message, enquiry_type) VALUES (?,?,?,?)",
        (name, phone, message, enquiry_type)
    )
    conn.commit()
    conn.close()
    flash("Thanks! We will contact you shortly.", "success")
    return redirect(url_for("contact"))


# ========================================================================
# ADMIN ROUTES
# ========================================================================

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        conn = get_db()
        admin = conn.execute(
            "SELECT * FROM admin_users WHERE username=?", (username,)
        ).fetchone()
        conn.close()
        if admin and check_password_hash(admin["password_hash"], password):
            session.permanent = True
            session["admin_logged_in"] = True
            session["admin_username"] = admin["username"]
            flash(f"Welcome back, {admin['username']}!", "success")
            return redirect(url_for("admin_dashboard"))
        flash("Invalid username or password.", "error")
    return render_template("admin/login.html", shop=SHOP_INFO)


@app.route("/admin/logout")
def admin_logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for("admin_login"))


@app.route("/admin")
@login_required
def admin_dashboard():
    conn = get_db()
    product_count = conn.execute("SELECT COUNT(*) c FROM products").fetchone()["c"]
    repair_count = conn.execute("SELECT COUNT(*) c FROM repair_services").fetchone()["c"]
    pending_reviews = conn.execute("SELECT COUNT(*) c FROM reviews WHERE is_approved=0").fetchone()["c"]
    unread_enquiries = conn.execute("SELECT COUNT(*) c FROM enquiries WHERE is_read=0").fetchone()["c"]
    recent_enquiries = conn.execute("SELECT * FROM enquiries ORDER BY id DESC LIMIT 5").fetchall()
    conn.execute("UPDATE enquiries SET is_read=1")
    conn.commit()
    conn.close()
    return render_template("admin/dashboard.html", shop=SHOP_INFO,
                           product_count=product_count, repair_count=repair_count,
                           pending_reviews=pending_reviews, unread_enquiries=unread_enquiries,
                           recent_enquiries=recent_enquiries)


@app.route("/admin/products")
@login_required
def admin_products():
    conn = get_db()
    product_list = conn.execute("""
        SELECT p.*, c.name AS category_name FROM products p
        JOIN categories c ON p.category_id=c.id ORDER BY p.id DESC
    """).fetchall()
    categories = conn.execute("SELECT * FROM categories ORDER BY display_order").fetchall()
    conn.close()
    return render_template("admin/products.html", shop=SHOP_INFO,
                           products=product_list, categories=categories)


@app.route("/admin/products/add", methods=["POST"])
@login_required
def admin_add_product():
    name = request.form.get("name", "").strip()
    category_id = request.form.get("category_id", type=int)
    description = request.form.get("description", "").strip()
    price = request.form.get("price", type=float)
    mrp = request.form.get("mrp", type=float)
    image_url = None

    if "product_image" in request.files:
        image = request.files["product_image"]

        if image and image.filename:
            print("Image received:", image.filename)
            filename = secure_filename(image.filename)

            image_path = os.path.join(
                 app.config["UPLOAD_FOLDER"],
                 filename
            )

            image.save(image_path)

            image_url = f"uploads/{filename}"
    is_featured = 1 if request.form.get("is_featured") else 0
    if not name or not category_id or price is None:
        flash("Name, category and price are required.", "error")
        return redirect(url_for("admin_products"))
    conn = get_db()
    conn.execute(
        "INSERT INTO products (category_id, name, description, price, mrp, image_url, is_featured) VALUES (?,?,?,?,?,?,?)",
        (category_id, name, description, price, mrp, image_url, is_featured)
    )
    conn.commit()
    conn.close()
    flash(f"Product '{name}' added!", "success")
    return redirect(url_for("admin_products"))


@app.route("/admin/products/<int:product_id>/edit", methods=["POST"])
@login_required
def admin_edit_product(product_id):
    name = request.form.get("name", "").strip()
    category_id = request.form.get("category_id", type=int)
    description = request.form.get("description", "").strip()
    price = request.form.get("price", type=float)
    mrp = request.form.get("mrp", type=float)
    image_url = request.form.get("image_url", "").strip() or None
    in_stock = 1 if request.form.get("in_stock") else 0
    is_featured = 1 if request.form.get("is_featured") else 0
    conn = get_db()
    conn.execute(
        "UPDATE products SET category_id=?, name=?, description=?, price=?, mrp=?, image_url=?, in_stock=?, is_featured=? WHERE id=?",
        (category_id, name, description, price, mrp, image_url, in_stock, is_featured, product_id)
    )
    conn.commit()
    conn.close()
    flash("Product updated!", "success")
    return redirect(url_for("admin_products"))


@app.route("/admin/products/<int:product_id>/delete", methods=["POST"])
@login_required
def admin_delete_product(product_id):
    conn = get_db()
    conn.execute("DELETE FROM products WHERE id=?", (product_id,))
    conn.commit()
    conn.close()
    flash("Product deleted.", "success")
    return redirect(url_for("admin_products"))


@app.route("/admin/repairs")
@login_required
def admin_repairs():
    conn = get_db()
    repair_list = conn.execute("SELECT * FROM repair_services ORDER BY display_order").fetchall()
    conn.close()
    return render_template("admin/repairs.html", shop=SHOP_INFO, repairs=repair_list)


@app.route("/admin/repairs/add", methods=["POST"])
@login_required
def admin_add_repair():
    service_name = request.form.get("service_name", "").strip()
    description = request.form.get("description", "").strip()
    price_range = request.form.get("price_range", "").strip()
    estimated_time = request.form.get("estimated_time", "").strip()
    if not service_name or not price_range:
        flash("Service name and price range are required.", "error")
        return redirect(url_for("admin_repairs"))
    conn = get_db()
    conn.execute(
        "INSERT INTO repair_services (service_name, description, price_range, estimated_time) VALUES (?,?,?,?)",
        (service_name, description, price_range, estimated_time)
    )
    conn.commit()
    conn.close()
    flash(f"Service '{service_name}' added!", "success")
    return redirect(url_for("admin_repairs"))


@app.route("/admin/repairs/<int:repair_id>/delete", methods=["POST"])
@login_required
def admin_delete_repair(repair_id):
    conn = get_db()
    conn.execute("DELETE FROM repair_services WHERE id=?", (repair_id,))
    conn.commit()
    conn.close()
    flash("Service deleted.", "success")
    return redirect(url_for("admin_repairs"))


@app.route("/admin/reviews")
@login_required
def admin_reviews():
    conn = get_db()
    review_list = conn.execute("SELECT * FROM reviews ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("admin/reviews.html", shop=SHOP_INFO, reviews=review_list)


@app.route("/admin/reviews/<int:review_id>/approve", methods=["POST"])
@login_required
def admin_approve_review(review_id):
    conn = get_db()
    conn.execute("UPDATE reviews SET is_approved=1 WHERE id=?", (review_id,))
    conn.commit()
    conn.close()
    flash("Review approved!", "success")
    return redirect(url_for("admin_reviews"))


@app.route("/admin/reviews/<int:review_id>/delete", methods=["POST"])
@login_required
def admin_delete_review(review_id):
    conn = get_db()
    conn.execute("DELETE FROM reviews WHERE id=?", (review_id,))
    conn.commit()
    conn.close()
    flash("Review deleted.", "success")
    return redirect(url_for("admin_reviews"))


@app.route("/admin/enquiries")
@login_required
def admin_enquiries():
    conn = get_db()
    enquiry_list = conn.execute("SELECT * FROM enquiries ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("admin/enquiries.html", shop=SHOP_INFO, enquiries=enquiry_list)


@app.route("/admin/enquiries/<int:enquiry_id>/delete", methods=["POST"])
@login_required
def admin_delete_enquiry(enquiry_id):
    conn = get_db()
    conn.execute("DELETE FROM enquiries WHERE id=?", (enquiry_id,))
    conn.commit()
    conn.close()
    flash("Enquiry deleted.", "success")
    return redirect(url_for("admin_enquiries"))


# ========================================================================
# Create admin user
# ========================================================================

@app.cli.command("create-admin")
def create_admin():
    import getpass
    username = input("Enter admin username: ").strip()
    password = getpass.getpass("Enter admin password: ")
    confirm = getpass.getpass("Confirm password: ")
    if password != confirm:
        print("Passwords do not match!")
        return
    conn = get_db()
    existing = conn.execute("SELECT id FROM admin_users WHERE username=?", (username,)).fetchone()
    if existing:
        print(f"User '{username}' already exists!")
        conn.close()
        return
    conn.execute(
        "INSERT INTO admin_users (username, password_hash) VALUES (?,?)",
        (username, generate_password_hash(password))
    )
    conn.commit()
    conn.close()
    print(f"✅ Admin user '{username}' created successfully!")


if __name__ == "__main__":
    init_db()
    print("✅ A to Z Enterprises website starting...")
    print("🌐 Open browser: http://127.0.0.1:5000")
    print("🔧 Admin panel: http://127.0.0.1:5000/admin/login")
    app.run(debug=True, host="0.0.0.0", port=5000)
