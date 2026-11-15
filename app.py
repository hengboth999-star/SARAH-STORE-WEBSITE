import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, abort

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "sarah_store.db")

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "change-this-before-deployment")

GAMES = {
    "roblox": {
        "name": "Roblox",
        "subtitle": "បញ្ចូល Robux",
        "field_label": "ឈ្មោះអ្នកប្រើ Roblox",
        "field_name": "account",
        "packages": [(50, 0.50), (100, 1.00), (200, 2.00), (400, 4.00), (800, 7.50), (1000, 9.98)],
    },
    "free-fire": {
        "name": "Free Fire",
        "subtitle": "បញ្ចូល Diamonds",
        "field_label": "Player ID",
        "field_name": "player_id",
        "packages": [(100, 1.00), (310, 3.00), (520, 5.00), (1060, 10.00)],
    },
    "mobile-legends": {
        "name": "Mobile Legends",
        "subtitle": "បញ្ចូល Diamonds",
        "field_label": "User ID",
        "field_name": "user_id",
        "extra_field_label": "Zone ID",
        "extra_field_name": "zone_id",
        "packages": [(86, 1.00), (172, 2.00), (257, 3.00), (706, 8.00)],
    },
    "efootball-2026": {
        "name": "eFootball 2026",
        "subtitle": "បញ្ចូល Coins",
        "field_label": "ព័ត៌មានគណនី / Player ID",
        "field_name": "account",
        "packages": [(100, 1.00), (300, 3.00), (500, 5.00), (1000, 10.00)],
    },
}

def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_slug TEXT NOT NULL,
                game_name TEXT NOT NULL,
                package_amount INTEGER NOT NULL,
                price REAL NOT NULL,
                account_info TEXT NOT NULL,
                extra_info TEXT,
                status TEXT NOT NULL DEFAULT 'រង់ចាំការតភ្ជាប់ការទូទាត់',
                created_at TEXT NOT NULL
            )
        """)

@app.route("/")
def home():
    return render_template("index.html", games=GAMES)

@app.route("/game/<slug>", methods=["GET", "POST"])
def game_page(slug):
    game = GAMES.get(slug)
    if not game:
        abort(404)

    if request.method == "POST":
        try:
            package_index = int(request.form.get("package_index", "-1"))
            amount, price = game["packages"][package_index]
        except (ValueError, IndexError):
            flash("សូមជ្រើសរើសកញ្ចប់ឱ្យបានត្រឹមត្រូវ។", "error")
            return redirect(url_for("game_page", slug=slug))

        account_info = request.form.get(game["field_name"], "").strip()
        extra_info = request.form.get(game.get("extra_field_name", ""), "").strip()
        if not account_info:
            flash("សូមបញ្ចូលព័ត៌មានគណនីរបស់អ្នក។", "error")
            return redirect(url_for("game_page", slug=slug))

        with db() as conn:
            cur = conn.execute("""
                INSERT INTO orders (game_slug, game_name, package_amount, price, account_info, extra_info, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (slug, game["name"], amount, price, account_info, extra_info,
                  "មិនទាន់បានបង់ប្រាក់ — របៀបសាកល្បង", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            order_id = cur.lastrowid
        return redirect(url_for("checkout", order_id=order_id))

    return render_template("game.html", game=game, slug=slug)

@app.route("/checkout/<int:order_id>")
def checkout(order_id):
    with db() as conn:
        order = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
    if not order:
        abort(404)
    return render_template("checkout.html", order=order)

@app.route("/orders")
def orders():
    with db() as conn:
        rows = conn.execute("SELECT * FROM orders ORDER BY id DESC LIMIT 100").fetchall()
    return render_template("orders.html", orders=rows)

@app.route("/admin")
def admin():
    # Starter dashboard only. Add proper login before public deployment.
    with db() as conn:
        rows = conn.execute("SELECT * FROM orders ORDER BY id DESC LIMIT 100").fetchall()
    return render_template("admin.html", orders=rows)

@app.route("/health")
def health():
    return {"service": "SARAH STORE website starter", "status": "ok"}

init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)