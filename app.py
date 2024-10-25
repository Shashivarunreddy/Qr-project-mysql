from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import qrcode
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database connection setup
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="health"
    )

# Home page redirects to sign-in
@app.route('/')
def home():
    return redirect(url_for('login'))

# Sign-up page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Validate and insert new user into the database
        if len(password) >= 8:  # simple validation for password length
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
            connection.commit()
            cursor.close()
            connection.close()
            return redirect(url_for('login'))
        else:
            return 'Password must be at least 8 characters long'

    return render_template('signup.html')

# Sign-in page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Validate user credentials
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user:
            session['user_id'] = user['id']
            session['email'] = user['email']

            # Check if user has already entered their details
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM patients WHERE user_id = %s", (user['id'],))
            patient = cursor.fetchone()
            cursor.close()
            connection.close()

            if patient:
                return redirect(url_for('profile'))
            else:
                return redirect(url_for('details_form'))
        else:
            return 'Invalid credentials'

    return render_template('login.html')

# Form for new users to enter details
@app.route('/details_form', methods=['GET', 'POST'])
def details_form():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        blood_group = request.form['blood_group']
        health_condition = request.form['health_condition']

        # Insert patient details
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO patients (user_id, name, age, gender, blood_group, health_condition) VALUES (%s, %s, %s, %s, %s, %s)",
            (session['user_id'], name, age, gender, blood_group, health_condition)
        )
        connection.commit()
        cursor.close()
        connection.close()

        # Generate QR code
        patient_url = f'http://{request.host}/patient/{session["user_id"]}'
        qr_img = qrcode.make(patient_url)
        qr_img_path = os.path.join(os.getcwd(), f'static/qr_{session["user_id"]}.png')
        qr_img.save(qr_img_path)

        return redirect(url_for('profile'))

    return render_template('details_form.html')

# Display user's details and QR code
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    # Fetch patient details
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM patients WHERE user_id = %s", (session['user_id'],))
    patient = cursor.fetchone()
    cursor.close()
    connection.close()

    if request.method == 'POST':
        # Update patient details
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        blood_group = request.form['blood_group']
        health_condition = request.form['health_condition']

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE patients SET name=%s, age=%s, gender=%s, blood_group=%s, health_condition=%s WHERE user_id=%s",
            (name, age, gender, blood_group, health_condition, session['user_id'])
        )
        connection.commit()
        cursor.close()
        connection.close()

    qr_img_path = f'/static/qr_{session["user_id"]}.png'

    return render_template('profile.html', patient=patient, qr_img_path=qr_img_path)

if __name__ == '__main__':
    app.run(debug=True, host='192.168.29.141', port=5000)
