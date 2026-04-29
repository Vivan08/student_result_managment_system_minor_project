from flask import Flask, render_template, request, redirect, session
import mysql.connector   # ✅ ADD THIS

app = Flask(__name__)
app.secret_key = "secret123"

# ✅ ADD THIS FUNCTION HERE
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="py_@pytho",
        database="result_system"
    )

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("minor.html")




# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )

        user = cursor.fetchone()

        if user:
            session["user"] = username
            return redirect("/result")
        else:
            return "Invalid Login ❌"

    return render_template("login.html")

@app.route("/staff-login", methods=["GET", "POST"])
def staff_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s AND role='staff'",
            (username, password)
        )

        staff = cursor.fetchone()

        if staff:
            session["staff"] = username
            return redirect("/marks")
        else:
            return "Invalid Staff Login ❌"

    return render_template("staff.html")


# ---------------- RESULT ----------------
@app.route("/result", methods=["GET","POST"])
def result():
    if "user" not in session:
        return redirect("/login")

    data = None

    if request.method == "POST":
        username = session["user"]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT subjects.subject_name, results.marks
        FROM results
        JOIN students ON results.student_id = students.student_id
        JOIN subjects ON results.subject_id = subjects.subject_id
        WHERE students.name = %s
        """, (username,))

        data = cursor.fetchall()

    return render_template("result.html", data=data)


# ---------------- MARKS ----------------
@app.route("/marks")
def marks():
    selected_course = request.args.get("course")
    selected_subject = request.args.get("subject")

    conn = get_db_connection()
    cursor = conn.cursor(buffered=True)

    query = """
        SELECT results.id, students.name, students.course, subjects.subject_name, results.marks
        FROM results
        JOIN students ON results.student_id = students.student_id
        JOIN subjects ON results.subject_id = subjects.subject_id
        WHERE 1=1
    """

    params = []

    # 🔹 COURSE FILTER
    if selected_course:
        query += " AND students.course = %s"
        params.append(selected_course)

    # 🔹 SUBJECT FILTER
    if selected_subject:
        query += " AND subjects.subject_name = %s"
        params.append(selected_subject)

    cursor.execute(query, tuple(params))
    data = cursor.fetchall()

    # ADD THIS BEFORE RETURN
    cursor.execute("SELECT DISTINCT course FROM students")
    courses = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT subject_name FROM subjects")
    subjects = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT student_id, name FROM students")
    students = cursor.fetchall()

    return render_template(
        "marks.html",
        data=data,
        courses=courses,
        subjects=subjects,
        students=students
    )



# ---------------- SUBJECTS ----------------
@app.route("/subjects")
def subjects():
    return render_template("subjects.html")


# ---------------- REPORT ----------------
@app.route("/report")
def report():
    return render_template("report_card.html")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/add-marks", methods=["POST"])
def add_marks():
    student_name = request.form["student_name"]
    course = request.form["course"]
    subject_name = request.form["subject_name"]
    marks = request.form["marks"]

    conn = get_db_connection()
    cursor = conn.cursor(buffered=True)   # 🔥 FIX

    # STUDENT
    cursor.execute("SELECT student_id FROM students WHERE name=%s", (student_name,))
    student = cursor.fetchone()

    if not student:
        cursor.execute(
            "INSERT INTO students (name, course) VALUES (%s, %s)",
            (student_name, course)
        )
        conn.commit()
        student_id = cursor.lastrowid
    else:
        student_id = student[0]

        cursor.execute(
            "UPDATE students SET course=%s WHERE student_id=%s",
            (course, student_id)
        )
        conn.commit()

    # SUBJECT
    cursor.execute("SELECT subject_id FROM subjects WHERE subject_name=%s", (subject_name,))
    subject = cursor.fetchone()

    if not subject:
        cursor.execute(
            "INSERT INTO subjects (subject_name) VALUES (%s)",
            (subject_name,)
        )
        conn.commit()
        subject_id = cursor.lastrowid
    else:
        subject_id = subject[0]

    # INSERT MARKS
    cursor.execute(
        "INSERT INTO results (student_id, subject_id, marks) VALUES (%s, %s, %s)",
        (student_id, subject_id, marks)
    )

    conn.commit()

    return redirect("/marks")

@app.route("/update-marks", methods=["POST"])
def update_marks():
    id = request.form["id"]
    marks = request.form["marks"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE results SET marks=%s WHERE id=%s",
        (marks, id)
    )

    conn.commit()

    return redirect("/marks")

@app.route("/delete-marks", methods=["POST"])
def delete_marks():
    id = request.form["id"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM results WHERE id=%s", (id,))
    conn.commit()

    return redirect("/marks")


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)

