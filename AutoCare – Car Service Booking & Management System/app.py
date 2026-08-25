from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

import mysql.connector

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)


app = Flask(__name__)

# Used for Flask sessions
app.secret_key = "autocare_secret_key_2026"


# =====================================================
# DATABASE CONNECTION
# =====================================================

def get_db_connection():

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="amitkumar@47",
        database="autocare_db"
    )

    return connection


# =====================================================
# HOME
# =====================================================

@app.route("/")
def home():

    return render_template("home.html")


# =====================================================
# SERVICES
# =====================================================

@app.route("/services")
def services():

    return render_template("services.html")


# =====================================================
# ABOUT
# =====================================================

@app.route("/about")
def about():

    return render_template("about.html")


# =====================================================
# CONTACT
# =====================================================

@app.route(
    "/contact",
    methods=["GET", "POST"]
)
def contact():

    if request.method == "POST":

        name = request.form["name"]

        email = request.form["email"]

        phone = request.form["phone"]

        message = request.form["message"]


        connection = get_db_connection()

        cursor = connection.cursor()


        query = """
            INSERT INTO contact_messages
            (
                name,
                email,
                phone,
                message
            )
            VALUES
            (%s, %s, %s, %s)
        """


        values = (
            name,
            email,
            phone,
            message
        )


        cursor.execute(query, values)

        connection.commit()


        cursor.close()

        connection.close()


        flash(
            "Your message has been sent successfully!",
            "success"
        )


        return redirect(
            url_for("contact")
        )


    return render_template(
        "contact.html"
    )


# =====================================================
# BOOK SERVICE
# =====================================================

@app.route(
    "/book-service",
    methods=["GET", "POST"]
)
def book_service():

    # Require login

    if "user_id" not in session:

        flash(
            "Please login to book a service.",
            "warning"
        )

        return redirect(
            url_for("login")
        )


    if request.method == "POST":

        name = request.form["name"]

        phone = request.form["phone"]

        email = request.form["email"]

        brand = request.form["brand"]

        model = request.form["model"]

        vehicle_number = request.form["vehicle_number"]

        service = request.form["service"]

        booking_date = request.form["date"]

        booking_time = request.form["time"]

        message = request.form["message"]


        connection = get_db_connection()

        cursor = connection.cursor()


        query = """

            INSERT INTO bookings

            (
                name,
                phone,
                email,
                brand,
                model,
                vehicle_number,
                service,
                booking_date,
                booking_time,
                message
            )

            VALUES

            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )

        """


        values = (

            name,

            phone,

            email,

            brand,

            model,

            vehicle_number,

            service,

            booking_date,

            booking_time,

            message

        )


        cursor.execute(
            query,
            values
        )


        connection.commit()


        cursor.close()

        connection.close()


        flash(
            "Service booked successfully!",
            "success"
        )


        return redirect(
            url_for("bookings")
        )


    return render_template(
        "book_service.html"
    )


# =====================================================
# BOOKINGS
# =====================================================

@app.route("/bookings")
def bookings():

    # Require login

    if "user_id" not in session:

        flash(
            "Please login to view your bookings.",
            "warning"
        )

        return redirect(
            url_for("login")
        )


    connection = get_db_connection()

    cursor = connection.cursor(
        dictionary=True
    )


    cursor.execute("""

        SELECT *

        FROM bookings

        ORDER BY created_at DESC

    """)


    bookings = cursor.fetchall()


    cursor.close()

    connection.close()


    return render_template(

        "bookings.html",

        bookings=bookings

    )


# =====================================================
# REGISTER
# =====================================================

@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if request.method == "POST":

        name = request.form["name"]

        email = request.form["email"]

        password = request.form["password"]

        confirm_password = request.form[
            "confirm_password"
        ]


        # Check passwords

        if password != confirm_password:

            flash(
                "Passwords do not match.",
                "error"
            )

            return redirect(
                url_for("register")
            )


        # Check password length

        if len(password) < 6:

            flash(
                "Password must contain at least 6 characters.",
                "error"
            )

            return redirect(
                url_for("register")
            )


        connection = get_db_connection()

        cursor = connection.cursor()


        # Check if email already exists

        cursor.execute(
            """
            SELECT id
            FROM users
            WHERE email = %s
            """,
            (email,)
        )


        existing_user = cursor.fetchone()


        if existing_user:

            cursor.close()

            connection.close()


            flash(
                "An account with this email already exists.",
                "error"
            )


            return redirect(
                url_for("login")
            )


        # Hash password

        hashed_password = generate_password_hash(
            password
        )


        # Insert user

        cursor.execute(

            """
            INSERT INTO users
            (
                name,
                email,
                password
            )
            VALUES
            (
                %s,
                %s,
                %s
            )
            """,

            (
                name,
                email,
                hashed_password
            )

        )


        connection.commit()


        cursor.close()

        connection.close()


        flash(
            "Account created successfully! Please login.",
            "success"
        )


        return redirect(
            url_for("login")
        )


    return render_template(
        "register.html"
    )


# =====================================================
# LOGIN
# =====================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        email = request.form["email"]

        password = request.form["password"]


        connection = get_db_connection()

        cursor = connection.cursor(
            dictionary=True
        )


        cursor.execute(

            """
            SELECT *
            FROM users
            WHERE email = %s
            """,

            (email,)

        )


        user = cursor.fetchone()


        cursor.close()

        connection.close()


        # User does not exist

        if not user:

            flash(
                "Invalid email or password.",
                "error"
            )

            return redirect(
                url_for("login")
            )


        # Check password

        if not check_password_hash(
            user["password"],
            password
        ):

            flash(
                "Invalid email or password.",
                "error"
            )

            return redirect(
                url_for("login")
            )


        # Create session

        session["user_id"] = user["id"]

        session["user_name"] = user["name"]

        session["user_email"] = user["email"]


        flash(
            "Welcome back, " + user["name"] + "!",
            "success"
        )


        return redirect(
            url_for("home")
        )


    return render_template(
        "login.html"
    )


# =====================================================
# LOGOUT
# =====================================================

@app.route("/logout")
def logout():

    session.clear()


    flash(
        "You have been logged out.",
        "success"
    )


    return redirect(
        url_for("home")
    )


# =====================================================
# ADMIN DASHBOARD
# =====================================================

@app.route("/admin")
def admin():

    connection = get_db_connection()

    cursor = connection.cursor(
        dictionary=True
    )


    # Get bookings

    cursor.execute("""

        SELECT *

        FROM bookings

        ORDER BY created_at DESC

    """)


    bookings = cursor.fetchall()


    # Get messages

    cursor.execute("""

        SELECT *

        FROM contact_messages

        ORDER BY created_at DESC

    """)


    messages = cursor.fetchall()


    # Get users

    cursor.execute("""

        SELECT *

        FROM users

        ORDER BY created_at DESC

    """)


    users = cursor.fetchall()


    cursor.close()

    connection.close()


    return render_template(

        "admin.html",

        bookings=bookings,

        messages=messages,

        users=users

    )


# =====================================================
# RUN APPLICATION
# =====================================================

if __name__ == "__main__":

    app.run(debug=True)