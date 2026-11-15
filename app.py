
import os
import secrets
import hmac
import psycopg

from psycopg.rows import dict_row
from datetime import datetime
from functools import wraps

from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, abort, session
)
from werkzeug.security import check_password_hash


app = Flask(__name__)

app.secret_key = os.environ.get("FLASK_SECRET_KEY") or secrets.token_hex(32)

ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "")
ADMIN_PASSWORD_HASH = os.environ.get("ADMIN_PASSWORD_HASH", "")

DATABASE_URL = os.environ.get("DATABASE_URL", "")


def db():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not configured.")

    return psycopg.connect(
        DATABASE_URL,
        row_factory=dict_row,
        connect_timeout=15
    )


GAMES = {
    "roblox": {
        "name": "Roblox",
        "subtitle": "បញ្ចូល Robux",
        "field_label": "ឈ្មោះអ្នកប្រើ Roblox",
        "field_name": "account",
        "packages": [
            (50, 0.50), (100, 1.00), (200, 2.00),
            (400, 4.00), (800, 7.50), (1000, 9.98)
        ],
    },
    "free-fire": {
        "name": "Free Fire",
        "subtitle": "បញ្ចូល Diamonds",
        "field_label": "Player ID",
        "field_name": "player_id",
        "packages": [
            (100, 1.00), (310, 3.00),
            (520, 5.00), (1060, 10.00)
        ],
    },
    "mobile-legends": {
        "name": "Mobile Legends",
        "subtitle": "បញ្ចូល Diamonds",
        "field_label": "User ID",
        "field_name": "user_id",
        "extra_field_label": "Zone ID",
        "extra_field_name": "zone_id",
        "packages": [
            (86, 1.00), (172, 2.00),
            (257, 3.00), (706, 8.00)
        ],
    },
    "efootball-2026": {
        "name": "eFootball 2026",
        "subtitle": "បញ្ចូល Coins",
        "field_label": "ព័ត៌មានគណនី / Player ID",
        "field_name": "account",
        "packages": [
            (100, 1.00), (300, 3.00),
            (500, 5.00), (1000, 10.00)
        ],
    },
}


def init_db():
    with db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id BIGSERIAL PRIMARY KEY,
                game_slug TEXT NOT NULL,
                game_name TEXT NOT NULL,
                package_amount INTEGER NOT NULL,
                price DOUBLE PRECISION NOT NULL,
                account_info TEXT NOT NULL,
                extra_info TEXT,
                status TEXT NOT NULL DEFAULT 'រង់ចាំការតភ្ជាប់ការទូទាត់',
                created_at TEXT NOT NULL
            )
        """)


def admin_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if not session.get("is_admin"):
            return redirect(url_for("admin_login"))
        return view(*args, **kwargs)
    return wrapped_view


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
            package_index = int(
                request.form.get("package_index", "-1")
            )
            amount, price = game["packages"][package_index]
        except (ValueError, IndexError):
            flash("សូមជ្រើសរើសកញ្ចប់ឱ្យបានត្រឹមត្រូវ។", "error")
            return redirect(url_for("game_page", slug=slug))

        account_info = request.form.get(
            game["field_name"], ""
        ).strip()

        extra_info = request.form.get(
            game.get("extra_field_name", ""), ""
        ).strip()

        if not account_info:
            flash("សូមបញ្ចូលព័ត៌មានគណនីរបស់អ្នក។", "error")
            return redirect(url_for("game_page", slug=slug))

        if game.get("extra_field_name") and not extra_info:
            flash("សូមបញ្ចូលព័ត៌មានគណនីបន្ថែម។", "error")
            return redirect(url_for("game_page", slug=slug))

        with db() as conn:
            row = conn.execute("""
                INSERT INTO orders (
                    game_slug,
                    game_name,
                    package_amount,
                    price,
                    account_info,
                    extra_info,
                    status,
                    created_at
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (
                slug,
                game["name"],
                amount,
                price,
                account_info,
                extra_info,
                "មិនទាន់បានបង់ប្រាក់ — របៀបសាកល្បង",
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )).fetchone()

            order_id = row["id"]

        return redirect(url_for("checkout", order_id=order_id))

    return render_template(
        "game.html",
        game=game,
        slug=slug
    )


@app.route("/checkout/<int:order_id>")
def checkout(order_id):
    with db() as conn:
        order = conn.execute(
            "SELECT * FROM orders WHERE id = %s",
            (order_id,)
        ).fetchone()

    if not order:
        abort(404)

    return render_template("checkout.html", order=order)


@app.route("/orders")
@admin_required
def orders():
    with db() as conn:
        rows = conn.execute(
            "SELECT * FROM orders ORDER BY id DESC LIMIT 100"
        ).fetchall()

    return render_template("orders.html", orders=rows)


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if session.get("is_admin"):
        return redirect(url_for("admin"))

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if not ADMIN_USERNAME or not ADMIN_PASSWORD_HASH:
            flash(
                "Admin Login មិនទាន់បានកំណត់ទេ។ សូមកំណត់ Environment Variables ជាមុន។",
                "error"
            )
            return render_template("admin_login.html")

        username_ok = hmac.compare_digest(
            username, ADMIN_USERNAME
        )

        try:
            password_ok = check_password_hash(
                ADMIN_PASSWORD_HASH, password
            )
        except (ValueError, TypeError):
            password_ok = False

        if username_ok and password_ok:
            session.clear()
            session["is_admin"] = True
            flash("ចូល Admin បានជោគជ័យ។", "success")
            return redirect(url_for("admin"))

        flash(
            "ឈ្មោះអ្នកប្រើ ឬពាក្យសម្ងាត់មិនត្រឹមត្រូវទេ។",
            "error"
        )

    return render_template("admin_login.html")


@app.route("/admin/logout", methods=["POST"])
@admin_required
def admin_logout():
    session.clear()
    flash("អ្នកបានចាកចេញពី Admin ហើយ។", "success")
    return redirect(url_for("admin_login"))


@app.route("/admin")
@admin_required
def admin():
    with db() as conn:
        rows = conn.execute(
            "SELECT * FROM orders ORDER BY id DESC LIMIT 100"
        ).fetchall()

    return render_template("admin.html", orders=rows)


@app.route("/health")
def health():
    try:
        with db() as conn:
            conn.execute("SELECT 1")

        return {
            "service": "SARAH STORE website",
            "database": "connected",
            "status": "ok"
        }

    except Exception:
        app.logger.exception("Database health check failed")
        return {
            "service": "SARAH STORE website",
            "database": "unavailable",
            "status": "error"
        }, 503


init_db()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
