from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)
app.secret_key = 'your-secret-key'
UPLOAD_FOLDER = 'static/sounds'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ✅ Create DB
def init_db():
    with sqlite3.connect('inventory.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL
                     )''')
        c.execute('''CREATE TABLE IF NOT EXISTS inventory (
                        product_id TEXT PRIMARY KEY,
                        product_name TEXT,
                        quantity INTEGER,
                        arrival_date TEXT,
                        source TEXT,
                        box_id TEXT,
                        unit_price REAL
                    )''')
        conn.commit()

init_db()

# ✅ Login required decorator
def login_required(func):
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user' not in session:
            flash('Please login to continue.', 'warning')
            return redirect('/login')
        return func(*args, **kwargs)
    return wrapper

# ✅ Home Page – Add Product
@app.route('/')
@login_required
def home():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
@login_required
def add():
    data = request.form
    with sqlite3.connect('inventory.db') as conn:
        c = conn.cursor()
        try:
            c.execute('''INSERT INTO inventory (product_id, product_name, quantity, arrival_date, source, box_id, unit_price)
                         VALUES (?, ?, ?, ?, ?, ?, ?)''',
                      (data['product_id'], data['product_name'], data['quantity'], data['arrival_date'],
                       data['source'], data['box_id'], data['unit_price']))
            conn.commit()
            flash('✅ Product added!', 'success')
        except sqlite3.IntegrityError:
            flash('⚠️ Product with this ID already exists!', 'danger')
    return redirect('/')

# ✅ Inventory View
@app.route('/inventory')
@login_required
def inventory():
    with sqlite3.connect('inventory.db') as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM inventory")
        products = c.fetchall()
    return render_template('inventory.html', products=products)

# ✅ Edit Product
@app.route('/edit/<product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    with sqlite3.connect('inventory.db') as conn:
        c = conn.cursor()
        if request.method == 'POST':
            data = request.form
            c.execute('''UPDATE inventory SET product_name=?, quantity=?, arrival_date=?, source=?, box_id=?, unit_price=?
                         WHERE product_id=?''',
                      (data['product_name'], data['quantity'], data['arrival_date'], data['source'],
                       data['box_id'], data['unit_price'], product_id))
            conn.commit()
            flash('✅ Product updated!', 'success')
            return redirect('/inventory')
        else:
            c.execute("SELECT * FROM inventory WHERE product_id=?", (product_id,))
            product = c.fetchone()
            return render_template('edit.html', product=product)

# ✅ Delete Product
@app.route('/delete/<product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    with sqlite3.connect('inventory.db') as conn:
        c = conn.cursor()
        c.execute("DELETE FROM inventory WHERE product_id=?", (product_id,))
        conn.commit()
        flash('🗑️ Product deleted!', 'success')
    return redirect('/inventory')

# ✅ Summary Dashboard with Filters + Charts
@app.route('/summary')
@login_required
def summary():
    vendor = request.args.get('vendor', '').strip().lower()
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')

    with sqlite3.connect('inventory.db') as conn:
        c = conn.cursor()
        query = "SELECT product_name, quantity, unit_price, arrival_date, source FROM inventory"
        c.execute(query)
        rows = c.fetchall()

    filtered = []
    for r in rows:
        r_vendor = r[4].lower()
        r_date = r[3]
        if (not vendor or vendor in r_vendor) and \
           (not start_date or r_date >= start_date) and \
           (not end_date or r_date <= end_date):
            filtered.append(r)

    summary = defaultdict(lambda: [0, 0.0])  # product_name: [total_qty, total_value]
    for name, qty, price, *_ in filtered:
        summary[name][0] += qty
        summary[name][1] += qty * price

    summary_data = [(k, v[0], v[1]) for k, v in summary.items()]
    summary_data.sort(key=lambda x: x[0])

    chart_labels = [x[0] for x in summary_data]
    chart_quantities = [x[1] for x in summary_data]
    chart_values = [x[2] for x in summary_data]

    return render_template("summary.html",
                           summary_data=summary_data,
                           chart_labels=chart_labels,
                           chart_quantities=chart_quantities,
                           chart_values=chart_values)

# ✅ Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = request.form['username']
        pw = generate_password_hash(request.form['password'])
        with sqlite3.connect('inventory.db') as conn:
            c = conn.cursor()
            try:
                c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user, pw))
                conn.commit()
                flash('✅ Registration successful! Please login.', 'success')
                return redirect('/login')
            except sqlite3.IntegrityError:
                flash('⚠️ Username already exists.', 'danger')
    return render_template('register.html')

# ✅ Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pw = request.form['password']
        with sqlite3.connect('inventory.db') as conn:
            c = conn.cursor()
            c.execute("SELECT password FROM users WHERE username=?", (user,))
            result = c.fetchone()
            if result and check_password_hash(result[0], pw):
                session['user'] = user
                flash(f'👋 Welcome back, {user}!', 'success')
                return redirect('/')
            else:
                flash('❌ Invalid credentials.', 'danger')
    return render_template('login.html')

# ✅ Logout
@app.route('/logout')
@login_required
def logout():
    session.pop('user', None)
    flash('👋 Logged out successfully.', 'info')
    return redirect('/login')

# ✅ Run App
if __name__ == '__main__':
    app.run(debug=True)





