import os
import sqlite3
import hashlib
import bcrypt
import time
import threading
from datetime import datetime, timedelta
import secrets
import glob
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory, jsonify, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from PIL import Image
import io
import base64

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Ensure directories exist
os.makedirs('static/uploads', exist_ok=True)
os.makedirs('static/images', exist_ok=True)
os.makedirs('adminrandomhashorlongtexttopreventguess/logs', exist_ok=True)

# Global variables to track crash state
crash_occurred = False
crash_timestamp = None

class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return User(user[0], user[1])
    return None

def init_db():
    """Initialize the SQLite database"""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def encode_lsb_standard(image, message):
    """Standard LSB encoding (least significant bit)"""
    encoded = image.copy()
    message += chr(0)  # Null terminator
    message_bits = ''.join(format(ord(char), '08b') for char in message)
    
    pixels = list(encoded.getdata())
    for i, bit in enumerate(message_bits):
        if i >= len(pixels) * 3:  # RGB channels
            break
        pixel_idx = i // 3
        channel = i % 3
        pixel = list(pixels[pixel_idx])
        pixel[channel] = (pixel[channel] & 0xFE) | int(bit)
        pixels[pixel_idx] = tuple(pixel)
    
    encoded.putdata(pixels)
    return encoded

def decode_lsb_standard(image):
    """Standard LSB decoding"""
    pixels = list(image.getdata())
    message_bits = []
    
    for pixel in pixels:
        for channel in pixel[:3]:  # RGB channels
            message_bits.append(str(channel & 1))
    
    message = ''
    for i in range(0, len(message_bits), 8):
        byte = ''.join(message_bits[i:i+8])
        if len(byte) == 8:
            char = chr(int(byte, 2))
            if char == chr(0):  # Null terminator
                break
            message += char
    
    return message

def encode_lsb_alternative(image, message):
    """Alternative LSB encoding (4th least significant bit - only for crash images)"""
    encoded = image.copy()
    message += chr(0)  # Null terminator
    message_bits = ''.join(format(ord(char), '08b') for char in message)
    
    pixels = list(encoded.getdata())
    for i, bit in enumerate(message_bits):
        if i >= len(pixels) * 3:  # RGB channels
            break
        pixel_idx = i // 3
        channel = i % 3
        pixel = list(pixels[pixel_idx])
        # Use 4th least significant bit instead of 1st
        pixel[channel] = (pixel[channel] & 0xF7) | (int(bit) << 3)
        pixels[pixel_idx] = tuple(pixel)
    
    encoded.putdata(pixels)
    return encoded

def decode_lsb_alternative(image):
    """Alternative LSB decoding (4th least significant bit - only for crash images)"""
    pixels = list(image.getdata())
    message_bits = []
    
    for pixel in pixels:
        for channel in pixel[:3]:  # RGB channels
            message_bits.append(str((channel >> 3) & 1))
    
    message = ''
    for i in range(0, len(message_bits), 8):
        byte = ''.join(message_bits[i:i+8])
        if len(byte) == 8:
            char = chr(int(byte, 2))
            if char == chr(0):  # Null terminator
                break
            message += char
    
    return message

def is_polyglot_file(file_data):
    """Check if uploaded file has magic byte mismatch (polyglot)"""
    if len(file_data) < 10:
        return False
    
    # Check for common polyglot patterns
    # PNG magic bytes but different content structure
    if file_data[:8] == b'\x89PNG\r\n\x1a\n' and b'JFIF' in file_data[:100]:
        return True
    
    # JPEG magic bytes but PNG content
    if file_data[:2] == b'\xff\xd8' and b'PNG' in file_data[:100]:
        return True
    
    return False

def trigger_crash():
    """Simulate server crash and log it"""
    global crash_occurred, crash_timestamp
    crash_occurred = True
    crash_timestamp = datetime.now()
    
    # Unique timestamp + random suffix for uniqueness
    ts_str = crash_timestamp.strftime("%Y-%m-%d_%H-%M-%S")
    suffix = secrets.token_hex(3)
    log_filename = f"{ts_str}_{suffix}.log"
    log_path = os.path.join('adminrandomhashorlongtexttopreventguess', 'logs', log_filename)
    
    log_content = """[INFO] Server crash detected - polyglot file upload
[INFO] File saved to /adminrandomhashorlongtexttopreventguess/flag.txt
[TIMESTAMP] """ + crash_timestamp.strftime("%Y-%m-%d %H:%M:%S")
    
    with open(log_path, 'w') as f:
        f.write(log_content)
    
    # Schedule file deletion after 2 minutes
    def delete_log():
        time.sleep(120)
        if os.path.exists(log_path):
            os.remove(log_path)
    
    threading.Thread(target=delete_log, daemon=True).start()
    
    # Create flag file if it doesn't exist
    flag_path = 'adminrandomhashorlongtexttopreventguess/flag.txt'
    if not os.path.exists(flag_path):
        with open(flag_path, 'w') as f:
            f.write('🎉 Congratulations! You found the final flag: CTF{st3g4n0gr4phy_4nd_t1m1ng_m4st3r_2024}')
    
    # Create crash image immediately using demo.png as base
    crash_img_name = f"democrashed_{ts_str}_{suffix}.png"
    crash_img_path = os.path.join('static', 'uploads', crash_img_name)
    demo_img_path = 'static/images/demo.png'
    if os.path.exists(demo_img_path):
        demo_img = Image.open(demo_img_path).convert('RGB')
    else:
        demo_img = Image.new('RGB', (400, 300), color='lightblue')
    
    hidden_message = f"[!] Crash logged at: /adminrandomhashorlongtexttopreventguess/logs/{log_filename}"
    crash_img = encode_lsb_alternative(demo_img, hidden_message)
    crash_img.save(crash_img_path)
    
    # Schedule crash image deletion after 2 minutes
    def delete_crash_img():
        time.sleep(120)
        if os.path.exists(crash_img_path):
            os.remove(crash_img_path)
    
    threading.Thread(target=delete_crash_img, daemon=True).start()
    
    return log_filename

@app.route('/')
def index():
    """Homepage with demo image; after crash, only reveal hint via comment and text"""
    # Default to demo image always
    image_url = '/static/images/demo.png'
    crash_comment = ''
    found_text = ''

    # Check if coming from 500 error page
    referrer = request.headers.get('Referer', '')
    from_error_page = '/500' in referrer or request.args.get('from_crash') == 'true'

    # If we recently crashed and user came from crash flow, reveal hidden comment + text
    if crash_occurred and from_error_page:
        # Find the most recent democrashed image
        candidates = sorted(glob.glob('static/uploads/democrashed_*.png'), key=os.path.getmtime, reverse=True)
        if candidates:
            latest = candidates[0].replace('static', '')  # to web path
            crash_comment = f'<!-- crash_image_url: {latest} -->'
            found_text = 'congrats u found.'

    return render_template('index.html', image_url=image_url, crash_comment=crash_comment, found_text=found_text)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', 
                         (username, hashed_password))
            conn.commit()
            conn.close()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists!', 'error')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user[2]):
            user_obj = User(user[0], user[1])
            login_user(user_obj)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/encode', methods=['GET', 'POST'])
@login_required
def encode():
    if request.method == 'POST':
        if 'image' not in request.files or 'message' not in request.form:
            flash('Please provide both image and message!', 'error')
            return redirect(url_for('encode'))
        
        file = request.files['image']
        message = request.form['message']
        
        if file.filename == '':
            flash('No file selected!', 'error')
            return redirect(url_for('encode'))
        
        # Read file data to check for polyglot (OUTSIDE try/except to allow abort to work)
        file_data = file.read()
        file.seek(0)  # Reset file pointer
        
        # Check for polyglot file (triggers crash)
        if is_polyglot_file(file_data):
            trigger_crash()
            # Return 500 error to simulate server crash
            abort(500)
        
        try:
            # Process normal image
            image = Image.open(io.BytesIO(file_data))
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Encode message
            encoded_image = encode_lsb_standard(image, message)
            
            # Save encoded image
            filename = f"encoded_{int(time.time())}.png"
            filepath = os.path.join('static/uploads', filename)
            encoded_image.save(filepath)
            
            flash('Message encoded successfully!', 'success')
            return render_template('encode.html', result_image=f'/static/uploads/{filename}')
            
        except Exception as e:
            flash(f'Error processing image: {str(e)}', 'error')
    
    return render_template('encode.html')

@app.route('/decode', methods=['GET', 'POST'])
@login_required
def decode():
    if request.method == 'POST':
        if 'image' not in request.files:
            flash('Please provide an image!', 'error')
            return redirect(url_for('decode'))
        
        file = request.files['image']
        
        if file.filename == '':
            flash('No file selected!', 'error')
            return redirect(url_for('decode'))
        
        try:
            image = Image.open(file)
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Try standard decoding first
            message = decode_lsb_standard(image)
            
            if not message.strip():
                flash('No hidden message found or image not encoded.', 'warning')
            else:
                return render_template('decode.html', decoded_message=message)
                
        except Exception as e:
            flash(f'Error processing image: {str(e)}', 'error')
    
    return render_template('decode.html')

@app.route('/adminrandomhashorlongtexttopreventguess/logs/<filename>')
def admin_logs(filename):
    """Time-sensitive log files"""
    log_path = f'adminrandomhashorlongtexttopreventguess/logs/{filename}'
    
    if not os.path.exists(log_path):
        return "Too late. File deleted.", 404
    
    with open(log_path, 'r') as f:
        content = f.read()
    
    return f"<pre>{content}</pre>"

@app.route('/adminrandomhashorlongtexttopreventguess/flag.txt')
def admin_flag():
    """Final flag with host-based access control"""
    # Check Host header
    host = request.headers.get('Host', '')
    if '127.0.0.1' not in host and 'localhost' not in host:
        print(f"DEBUG: Host header: {host}")
        return redirect('https://www.youtube.com/watch?v=dQw4w9WgXcQ')  # Rickroll
    
    flag_path = 'adminrandomhashorlongtexttopreventguess/flag.txt'
    if os.path.exists(flag_path):
        with open(flag_path, 'r') as f:
            return f"<pre>{f.read()}</pre>"
    else:
        return "Flag not available yet. Trigger crash first.", 404

@app.route('/decode-alternative')
@login_required
def decode_alternative():
    """Hidden endpoint to decode crash image with alternative method"""
    try:
        # Find most recent democrashed image
        candidates = sorted(glob.glob('static/uploads/democrashed_*.png'), key=os.path.getmtime, reverse=True)
        if not candidates:
            return jsonify({'error': 'Crash not found. Try triggering crash again.'})
        crash_img_path = candidates[0]
        image = Image.open(crash_img_path)
        message = decode_lsb_alternative(image)
        return jsonify({'message': message})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.errorhandler(500)
def internal_server_error(error):
    """Handle 500 errors - simulate server crash"""
    return render_template('500.html'), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=2000)
