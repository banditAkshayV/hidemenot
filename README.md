# 🔐 hidemenot - Advanced Steganography Challenge

A sophisticated web application that combines steganography with multiple security challenges and vulnerabilities. This platform demonstrates LSB (Least Significant Bit) steganography techniques while hiding a complex multi-stage capture-the-flag challenge.

## 🎯 Challenge Overview

**hidemenot** appears to be a simple steganography web app but contains hidden layers of security challenges, timing-based vulnerabilities, and clever exploitation techniques that players must discover and exploit to reach the final flag.

## 🏗️ Architecture & Features

### Core Functionality
- **User Authentication**: Secure registration and login system with bcrypt password hashing
- **LSB Steganography**: Hide and extract secret messages in images using least significant bit encoding
- **Modern UI**: Beautiful, responsive interface with Bootstrap 5 and custom CSS
- **File Upload**: Secure image upload with validation and processing

### Hidden Challenge Components
- **Polyglot File Detection**: Server crash mechanism triggered by magic byte mismatches
- **Alternative LSB Encoding**: Crash images use different encoding methods (4th LSB bit)
- **Time-Sensitive Resources**: Log files that auto-delete after 5 minutes
- **Host-Based Access Control**: Final flag protected by HTTP Host header validation
- **Hidden Admin Directories**: Concealed paths not accessible through normal navigation

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package installer)

### Installation
1. **Clone or download the project**
   ```bash
   cd findmenot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   - Open your browser and navigate to `http://localhost:5000`
   - The application will create necessary directories and database automatically

## 🎮 Player Walkthrough

### Stage 1: Basic Exploration
1. **Register and Login**
   - Create a new account or login with existing credentials
   - Explore the encode and decode functionality

2. **Test Steganography**
   - Upload an image and hide a message using the Encode page
   - Extract messages from encoded images using the Decode page
   - Notice the demo image on the homepage

### Stage 2: Trigger Server Crash
3. **Create a Polyglot File**
   - Create a file with PNG magic bytes (`\x89PNG\r\n\x1a\n`) but containing JPEG markers
   - Or create a JPEG file (`\xff\xd8`) with PNG content markers
   - Upload this polyglot file through the Encode page

4. **Observe the Crash**
   - Server detects the magic byte mismatch and simulates a crash
   - You're redirected to the homepage
   - **Key observation**: The demo image changes to a crash image

### Stage 3: Source Code Analysis
5. **Inspect Homepage Source**
   - View the page source of the homepage after the crash
   - Look for the hidden HTML comment:
     ```html
     <!-- crash_image_url: /static/uploads/crash123.png -->
     ```

### Stage 4: Alternative Decoding
6. **Download and Analyze Crash Image**
   - Download the crash image from `/static/uploads/crash123.png`
   - Try the standard decoder - it won't work
   - The crash image uses **4th least significant bit** encoding instead of 1st

7. **Extract the Hidden Path**
   - Use alternative decoding methods to extract the message:
     ```
     [!] Crash logged at: /adminrandomhashorlongtexttopreventguess/logs/YYYY-MM-DD.log
     ```

### Stage 5: Time-Sensitive Log Access
8. **Access the Log File Quickly**
   - Navigate to the log file path immediately (within 5 minutes of crash)
   - Example: `/adminrandomhashorlongtexttopreventguess/logs/2024-01-15.log`
   - If too late, you'll see: "Too late. File deleted."

9. **Read Log Content**
   ```
   [INFO] Server crash detected - polyglot file upload
   [INFO] Dynamic flag file: /adminrandomhashorlongtexttopreventguess/logs/flag_2025-08-30_10-52-18_c736f7.txt
   [SECURITY] Access limited to internal host 127.0.0.1
   ```

### Stage 6: Host Header Bypass
10. **Extract Dynamic Flag Path**
    - The log file contains the path to the dynamic flag file
    - Example: `/adminrandomhashorlongtexttopreventguess/logs/flag_2025-08-30_10-52-18_c736f7.txt`

11. **Attempt Direct Access**
    - Try accessing the dynamic flag path
    - You'll be redirected to a Rickroll video

12. **Bypass with Host Header**
    - Use curl or modify the Host header to `127.0.0.1`:
      ```bash
      curl -H "Host: 127.0.0.1" http://localhost:5000/adminrandomhashorlongtexttopreventguess/logs/flag_2025-08-30_10-52-18_c736f7.txt
      ```
    - Or use browser developer tools to modify the request

13. **Capture the Final Flag**
    - Successfully bypassing the host check reveals the dynamic flag:
      ```
      🎉 Congratulations! You found the final flag: CTF{st3g4n0gr4phy_4nd_t1m1ng_m4st3r_20250830_105218_bafc881b}
      ```

## 🛠️ Technical Implementation

### Steganography Methods
- **Standard LSB**: Modifies the least significant bit of RGB channels
- **Alternative LSB**: Uses 4th least significant bit for crash images
- **Multi-channel Support**: Can encode across different color channels

### Security Features
- **Bcrypt Password Hashing**: Secure password storage
- **File Type Validation**: Prevents non-image uploads
- **Size Limits**: 10MB maximum file size
- **Session Management**: Flask-Login for user sessions

### Challenge Mechanisms
- **Polyglot Detection**: Analyzes magic bytes vs content structure
- **Thread-based File Deletion**: Automatic log cleanup after 5 minutes
- **HTTP Header Validation**: Host-based access control
- **Dynamic Path Generation**: Date-based log file names

## 🔧 Development & Customization

### File Structure
```
findmenot/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── database.db           # SQLite database (auto-created)
├── templates/
│   ├── base.html         # Base template with styling
│   ├── index.html        # Homepage
│   ├── register.html     # User registration
│   ├── login.html        # User login
│   ├── encode.html       # Message encoding page
│   └── decode.html       # Message decoding page
├── static/
│   ├── images/          # Demo images
│   └── uploads/         # User uploaded files
└── adminrandomhashorlongtexttopreventguess/
    └── logs/            # Time-sensitive log files and dynamic flag files
```

### Key Functions
- `encode_lsb_standard()`: Standard LSB encoding
- `encode_lsb_alternative()`: Alternative encoding for crash images
- `is_polyglot_file()`: Detects magic byte mismatches
- `trigger_crash()`: Handles crash simulation and logging

### Customization Options
- Modify encoding methods in the LSB functions
- Change time limits for log file deletion
- Customize the final flag message
- Adjust polyglot detection patterns

## 🎨 UI Features

### Modern Design Elements
- **Gradient Backgrounds**: Beautiful color transitions
- **Glassmorphism Effects**: Translucent cards with backdrop blur
- **Smooth Animations**: Hover effects and transitions
- **Responsive Layout**: Works on desktop and mobile devices
- **Interactive Elements**: Drag-and-drop file upload, progress indicators

### User Experience
- **File Preview**: Image preview before processing
- **Progress Feedback**: Loading states during operations
- **Error Handling**: Clear error messages and validation
- **Accessibility**: ARIA labels and keyboard navigation support

## 🔒 Security Considerations

### Vulnerabilities (By Design)
1. **Magic Byte Mismatch**: Polyglot file uploads trigger server crashes
2. **Information Disclosure**: Hidden HTML comments reveal sensitive paths
3. **Time-based Attacks**: Race condition with log file deletion
4. **Host Header Injection**: Bypassable access controls

### Defensive Measures
- Input validation for file types and sizes
- Secure password hashing
- Session management
- Error handling without information leakage

## 🧪 Testing & Debugging

### Creating Test Polyglots
```python
# Create a PNG file with JPEG markers
with open('polyglot.png', 'wb') as f:
    f.write(b'\x89PNG\r\n\x1a\n')  # PNG magic bytes
    f.write(b'JFIF')               # JPEG marker
    f.write(b'\x00' * 100)         # Padding
```

### Debug Mode
The application runs with `debug=True` by default. For production:
```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

### Log Monitoring
Watch for crash events and log file creation:
```bash
ls -la adminrandomhashorlongtexttopreventguess/logs/
```

## 📝 Challenge Notes

### Timing Considerations
- Log files are deleted exactly 5 minutes after crash
- Players must act quickly once they discover the log path
- Consider timezone differences in date formatting

### Hints for Players
- Source code inspection is crucial
- Different images may use different encoding methods
- HTTP headers can be modified and manipulated
- Timing is everything in some stages

## 🏆 Achievement Levels

1. **Novice**: Successfully encode and decode messages
2. **Investigator**: Trigger server crash with polyglot files
3. **Code Detective**: Find hidden comments in source code
4. **Cryptanalyst**: Decode crash image with alternative methods
5. **Speed Runner**: Access log files within time limit
6. **Master Hacker**: Bypass host-based access controls for final flag

## 🤝 Contributing

This challenge platform can be extended with:
- Additional steganography methods
- More complex polyglot detection
- Advanced timing-based challenges
- Alternative access control bypasses
- Enhanced UI features

## 📄 License

This project is for educational and training purposes. Use responsibly and only in authorized environments.

---

**Happy Hacking!** 🎯

*Remember: The goal is to learn about web security, steganography, and creative problem-solving. Every vulnerability here is intentional and designed for educational purposes.*
