# N.D.Chanditha  24IT0458 (1 - 113)
from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
import os
from werkzeug.utils import secure_filename
from database import get_db_connection
from travel_engine import generate_seasonal_itinerary

app = Flask(__name__)
app.secret_key = 'travelmate_secret_key'

# setup file uploader
UPLOAD_FOLDER = 'static/uploads'
 app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# if folder not create new one
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# check file pdf or not
def allowed_file(filename):
    
    if filename.lower().endswith('.pdf'):
        return True
    return False

# 1. Home Page
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/destinations')
def destinations_page():
    return render_template('destinations.html')

# 2. Tourist Register 
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        nationality = request.form['nationality']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # check email already have or not
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            cursor.close()
            conn.close()
            flash('Email already registered!', 'error')
            return redirect(url_for('register'))
        
        # input new user to database
        cursor.execute("INSERT INTO users (name, email, password, nationality) VALUES (%s, %s, %s, %s)",
                       (name, email, password, nationality))
        conn.commit()
        cursor.close()
        conn.close()
        
        flash('Registration Successful!', 'success')
        return redirect(url_for('login'))
            
    return render_template('register.html')

# 3. Login / Logout 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # check is admin or not
        cursor.execute("SELECT * FROM admins WHERE email = %s AND password = %s", (email, password))
        admin = cursor.fetchone()
        
        if admin:
            session['is_admin'] = True
            session['user_name'] = admin[1] # admin name
            cursor.close()
            conn.close()
            flash('Welcome Admin!', 'success')
            return redirect(url_for('admin_dashboard'))
            
        # check normal user or not
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user:
            session['user_id'] = user[0] 
            session['user_name'] = user[1] 
            session['is_admin'] = False
            flash('Login Successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid Email or Password', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out.', 'info')
    return redirect(url_for('home'))
# W.A.C.Heshan  24IT473 (114 - 184)
# 4. Trip Planner
@app.route('/plan', methods=['GET', 'POST'])
def plan_trip():
    itinerary = []
    if request.method == 'POST':
        arrival_date = request.form['arrival_date']
        days = request.form['days']
        itinerary = generate_seasonal_itinerary(arrival_date, days)
    return render_template('plan.html', itinerary=itinerary)

# 5. Driver Register
@app.route('/register_driver', methods=['GET', 'POST'])
def register_driver():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        vehicle_type = request.form['vehicle_type']
        rate_per_km = request.form['rate_per_km']
        
        file = request.files.get('document_pdf')
        
        if not file or file.filename == '':
            flash('Please upload PDF!', 'error')
            return redirect(url_for('register_driver'))
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            flash('Only PDF files are allowed!', 'error')
            return redirect(url_for('register_driver'))
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # check driver already registered or not
        cursor.execute("SELECT * FROM drivers WHERE email = %s", (email,))
        existing_driver = cursor.fetchone()
        
        if existing_driver:
            cursor.close()
            conn.close()
            flash('Email already registered!', 'error')
            return redirect(url_for('register_driver'))
        
        # input driver details
        cursor.execute(
            "INSERT INTO drivers (name, email, password, phone, vehicle_type, rate_per_km, document_pdf, is_verified) VALUES (%s, %s, %s, %s, %s, %s, %s, 0)",
            (name, email, password, phone, vehicle_type, rate_per_km, filename)
        )
        conn.commit()
        cursor.close()
        conn.close()
        
        return render_template('driver_success.html', driver_name=name)
            
    return render_template('register_driver.html')

# show drivers page
@app.route('/drivers')
def view_drivers():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, email, phone, vehicle_type, rate_per_km, is_verified FROM drivers")
    drivers_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('drivers.html', drivers=drivers_list)
# Y.Kavishagini  24IT0482 (185 - 219)
# 6. Admin Panel Dashboard
@app.route('/admin/dashboard')
def admin_dashboard():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, phone, vehicle_type, document_pdf, is_verified FROM drivers ORDER BY id DESC")
    all_drivers = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('admin_dashboard.html', drivers=all_drivers)

# Driver Approve 
@app.route('/admin/approve_driver/<int:driver_id>')
def approve_driver(driver_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE drivers SET is_verified = 1 WHERE id = %s", (driver_id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Driver verified!', 'success')
    return redirect(url_for('admin_dashboard'))

# Driver Reject 
@app.route('/admin/reject_driver/<int:driver_id>')
def reject_driver(driver_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE drivers SET is_verified = 0 WHERE id = %s", (driver_id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Driver unverified.', 'info')
    return redirect(url_for('admin_dashboard'))
# L.B.P.Mihiranga  24IT0490   (219 - 284)
# 7. Reviews Page
@app.route('/reviews')
def reviews():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM reviews ORDER BY date_posted DESC")
    all_reviews = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('reviews.html', reviews=all_reviews)

# add review page
@app.route('/add_review_page')
def add_review_page():
    if 'user_id' not in session:
        flash('Please login first!', 'warning')
        return redirect(url_for('login'))
    return render_template('add_review.html')

@app.route('/submit_review', methods=['POST'])
def submit_review():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    name = request.form.get('reviewer_name')
    rating = request.form.get('rating')
    comment = request.form.get('comment')
    user_id = session['user_id']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reviews (user_id, reviewer_name, rating, comment) VALUES (%s, %s, %s, %s)", 
                   (user_id, name, int(rating), comment))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Review added!', 'success')
    return redirect(url_for('reviews'))

# 8. Admin Profile Update
@app.route('/admin/update_profile', methods=['POST'])
def admin_update_profile():
    if not session.get('is_admin'):
        flash('Unauthorized!', 'danger')
        return redirect(url_for('login'))
        
    new_email = request.form['admin_email']
    new_password = request.form['admin_password']
    new_name = request.form['admin_name']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE admins SET email = %s, password = %s, name = %s WHERE id = 1", 
                   (new_email, new_password, new_name))
    conn.commit()
    cursor.close()
    conn.close()
    
    session['user_name'] = new_name
    flash('Profile Updated!', 'success')
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    app.run(debug=True)