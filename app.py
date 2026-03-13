from flask import Flask, render_template, request, redirect, url_for, flash, session 
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "elitestay-secret-key"
DB_NAME = "bookings.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            room_type TEXT NOT NULL,
            check_in TEXT NOT NULL,
            check_out TEXT NOT NULL,
            guests INTEGER NOT NULL,
            special_request TEXT
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/rooms")
def rooms():
    room_data = [
        {
            "name": "Standard Room",
            "price": "GHS 450 / night",
            "description": "Comfortable room for individuals and short stays.",
            "image": "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=900&q=80",
        },
        {
            "name": "Executive Room",
            "price": "GHS 750 / night",
            "description": "Spacious room for premium comfort and business travelers.",
            "image": "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=900&q=80",
        },
        {
            "name": "Conference Booking",
            "price": "Custom Quote",
            "description": "Suitable for events, seminars, and corporate meetings.",
            "image": "https://images.unsplash.com/photo-1517457373958-b7bdd4587205?auto=format&fit=crop&w=900&q=80",
        },
    ]
    return render_template("rooms.html", rooms=room_data)

@app.route("/booking", methods=["GET", "POST"])
def booking():
    if request.method == "POST":
        full_name = request.form["full_name"].strip()
        email = request.form["email"].strip()
        phone = request.form["phone"].strip()
        room_type = request.form["room_type"].strip()
        check_in = request.form["check_in"]
        check_out = request.form["check_out"]
        guests = request.form["guests"]
        special_request = request.form.get("special_request", "").strip()

        if check_out < check_in:
            flash("Check-out date cannot be earlier than check-in date.")
            return redirect(url_for("booking"))

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO bookings (
                full_name, email, phone, room_type,
                check_in, check_out, guests, special_request
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (full_name, email, phone, room_type, check_in, check_out, guests, special_request))
        conn.commit()
        conn.close()

        return render_template("success.html", name=full_name, room_type=room_type)

    return render_template("booking.html")

@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin123":
            session["admin_logged_in"] = True
            return redirect(url_for("admin"))
        else:
            flash("Invalid admin credentials.")

    return render_template("admin_login.html")

@app.route("/admin")
def admin():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT full_name, email, phone, room_type, check_in, check_out, guests, special_request
        FROM bookings
        ORDER BY id DESC
    """)
    bookings = cursor.fetchall()
    total_bookings = len(bookings)
    conn.close()
    return render_template("admin.html", bookings=bookings, total_bookings=total_bookings)

if __name__ == "__main__":
    init_db()
    port =
    int(os.environ.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port)