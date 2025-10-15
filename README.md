# 🔐 QuMail - Quantum Secure Email Client

A modern email client application integrating **Quantum Key Distribution (QKD)** with existing email protocols to enhance security while maintaining compatibility with standard email servers.

---

## 📋 Overview

QuMail is designed to integrate quantum-secure encryption into everyday email communication. Built following **ETSI GS QKD 014** standards, it provides a multi-level security system where users can choose their desired encryption strength.

### Key Features
- ✅ **Multi-level quantum encryption** (4 security levels)
- ✅ **User authentication** with signup/login
- ✅ **Encrypted email storage** (emails stored in encrypted form)
- ✅ **Quantum key management** with metadata tracking
- ✅ **Light/Dark mode** professional UI
- ✅ **Real-time service status** monitoring
- ✅ **One-Time Pad support** (keys consumed after use)

---

## 🛠 Technology Stack

**Backend:**
- Python 3.8+ with Flask
- SQLAlchemy (ORM)
- Flask-JWT-Extended (Authentication)
- BCrypt (Password Hashing)
- Cryptography libraries

**Frontend:**
- HTML5/CSS3 with modern design
- Vanilla JavaScript (ES6+)
- CSS Variables for theming
- Glassmorphism UI effects

**Database:**
- SQLite (Development)
- PostgreSQL (Production-ready)

---

## 📦 Installation

### 1. Prerequisites
- Python 3.8+
- PyCharm (recommended) or any Python IDE
- pip and venv

### 2. Setup Virtual Environment

Open PyCharm terminal and run:

```bash
# Create virtual environment (PyCharm usually does this automatically)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install flask flask-cors flask-socketio flask-sqlalchemy
pip install flask-jwt-extended bcrypt python-dotenv
pip install cryptography pycryptodome
pip install pytest pytest-flask black flake8
```

Save dependencies:
```bash
pip freeze > requirements.txt
```

### 4. Create Environment Variables

Create a `.env` file in the project root:

```env
FLASK_APP=backend/app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here
DATABASE_URL=sqlite:///qumail.db
QKD_ENDPOINT=http://localhost:8080
QKD_API_KEY=qkd_api_key_12345
```

### 5. Initialize Database

```bash
python backend/init_db.py
```

### 6. Run Application

```bash
python run.py
```

Visit: `http://localhost:5000`

---

## 📁 Project Structure

```
QuMail/
├── backend/
│   ├── app.py                    # Main Flask application
│   ├── config.py                 # Configuration settings
│   ├── models/
│   │   ├── user.py              # User database model
│   │   ├── email.py             # Email database model
│   │   └── quantum_key.py       # Quantum key model
│   ├── routes/
│   │   ├── auth.py              # Login/Signup endpoints
│   │   ├── email_routes.py      # Email CRUD operations
│   │   └── quantum_routes.py    # QKD key management
│   ├── services/
│   │   ├── auth_service.py      # Authentication logic
│   │   ├── email_service.py     # Email encryption/decryption
│   │   ├── quantum_service.py   # QKD simulation
│   │   └── encryption_service.py # Encryption algorithms
│   └── utils/
│       └── helpers.py           # Utility functions
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   │   ├── style.css        # Main design system
│   │   │   ├── login.css        # Login page styles
│   │   │   └── components.css   # Reusable components
│   │   ├── js/
│   │   │   ├── app.js           # Main app logic
│   │   │   ├── auth.js          # Authentication
│   │   │   ├── email.js         # Email functionality
│   │   │   ├── quantum.js       # Quantum operations
│   │   │   └── utils.js         # Utilities & theme manager
│   │   └── images/
│   │       └── favicon.svg      # App icon
│   └── templates/
│       ├── base.html            # Base template
│       ├── login.html           # Login/Signup page
│       └── index.html           # Main application
├── tests/
│   ├── test_auth.py
│   ├── test_email.py
│   └── test_quantum.py
├── .env                          # Environment variables
├── .gitignore
├── requirements.txt
├── run.py                        # Application entry point
└── README.md
```

---

## 🔐 Security Levels

QuMail offers 4 levels of encryption security:

### Level 1: Quantum Secure (One-Time Pad)
- **Encryption**: XOR cipher with quantum-generated key
- **Security**: Information-theoretically secure
- **Key Usage**: Single-use only (consumed after decryption)
- **Use Case**: Maximum security communications

### Level 2: Quantum-aided AES
- **Encryption**: AES-256 with quantum key seeding
- **Security**: Enhanced entropy from QKD
- **Key Usage**: Reusable
- **Use Case**: Strong security with efficiency

### Level 3: Post-Quantum Cryptography
- **Encryption**: PQC algorithms (Kyber/Dilithium)
- **Security**: Quantum-attack resistant
- **Key Usage**: Reusable
- **Use Case**: Future-proof encryption

### Level 4: Standard Encryption
- **Encryption**: RSA-2048 + AES-256
- **Security**: Classical cryptography
- **Key Usage**: Reusable
- **Use Case**: Compatibility mode

---

## 🎯 Workflow

### User Registration/Login
1. User opens login page
2. Can **signup** with email/password or **login**
3. Backend validates credentials using BCrypt
4. JWT token issued for authenticated sessions
5. User redirected to main application

### Sending Encrypted Email
1. User clicks **"Compose"** button
2. Enters recipient email (must be registered user)
3. System checks if recipient exists in database
4. User selects **security level** (1-4)
5. User writes subject, message, and attaches files
6. On **"Send"**, system:
   - Generates/retrieves quantum key from Key Manager
   - Encrypts email content based on security level
   - Stores **encrypted email** in database
   - Links email to key ID for decryption
   - Sends notification to recipient

### Receiving and Decrypting Email
1. User navigates to **Inbox**
2. Emails displayed in **encrypted form** (preview shows encrypted data)
3. User clicks on email to view
4. System shows:
   - Sender information
   - Encrypted content preview
   - **"Decrypt"** button
5. On clicking **"Decrypt"**:
   - System fetches quantum key using key_id
   - Validates key hasn't expired
   - Decrypts email content
   - Displays decrypted message
   - **For Level 1 (OTP)**: Marks key as "used" (cannot reuse)
   - Shows error if key not found/expired

### Quantum Key Management
1. **Key Generation**:
   - When email is composed, system requests key from KM
   - KM generates quantum key using BB84 protocol simulation
   - Key stored with metadata: sender, recipient, timestamp, expiry

2. **Key Distribution**:
   - Keys stored in database with unique key_id
   - Metadata tracks: sender_id, recipient_id, security_level
   - System ensures only correct recipient can retrieve key

3. **Key Retrieval**:
   - When decrypting, system queries key by key_id
   - Validates recipient matches current user
   - Checks if key is still valid (not expired, not used for OTP)

4. **Key Expiry**:
   - Keys have 24-hour expiry by default
   - Expired keys cannot decrypt emails
   - System shows error message for expired keys

---

## 🎨 UI Features

### Theme System
- **Light/Dark Mode Toggle** (top-right corner)
- Smooth transitions between themes
- Theme preference saved in localStorage
- Professional azure blue color scheme

### Service Status Indicators
- **Real-time monitoring** of 3 services:
  - Key Manager (KM) status
  - Email Service status
  - Quantum Channel status
- **Glowing status dots**:
  - Green: Connected
  - Red: Error/Disconnected
  - Orange: Warning
- Located at top-left of login page

### Professional Design
- **Animated atom logo** (rotating electrons)
- **Glassmorphism effects** on cards
- **Quantum particle background** animations
- **Toast notifications** for feedback
- **Loading overlays** with quantum animations
- **Responsive design** for mobile/tablet/desktop

---

## 🔧 Development Workflow

### Adding New Features

1. **Backend (API)**:
   - Create route in `backend/routes/`
   - Implement logic in `backend/services/`
   - Add database model if needed in `backend/models/`
   - Write tests in `tests/`

2. **Frontend**:
   - Update HTML in `frontend/templates/`
   - Add styles in `frontend/static/css/`
   - Implement JS logic in `frontend/static/js/`
   - Test UI in both light/dark modes

3. **Testing**:
   ```bash
   pytest                    # Run all tests
   pytest -v                 # Verbose output
   pytest tests/test_auth.py # Specific test
   ```

4. **Code Formatting**:
   ```bash
   black backend/            # Format Python code
   flake8 backend/          # Check code style
   ```

---

## 🗄️ Database Schema

### Users Table
- `id`: Primary key
- `email`: Unique email address
- `password_hash`: BCrypt hashed password
- `name`: User full name
- `created_at`: Registration timestamp
- `is_active`: Account status

### Emails Table
- `id`: Primary key
- `sender_id`: Foreign key to Users
- `recipient_id`: Foreign key to Users
- `subject`: Email subject (can be encrypted)
- `encrypted_content`: Encrypted email body
- `security_level`: 1-4 (encryption level used)
- `key_id`: Foreign key to quantum_keys
- `timestamp`: When email was sent
- `is_read`: Read status

### Quantum Keys Table
- `id`: Primary key
- `key_id`: Unique identifier (e.g., QK_20250101_001)
- `sender_id`: Foreign key to Users
- `recipient_id`: Foreign key to Users
- `key_material`: Encrypted quantum key data
- `security_level`: Associated security level
- `protocol`: QKD protocol used (e.g., BB84)
- `generated_at`: Creation timestamp
- `expires_at`: Expiry timestamp
- `used`: Boolean (true for consumed OTP keys)
- `used_at`: When key was consumed

---

## 🚀 Running the Application

### Development Mode
```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Run Flask development server
python run.py

# Or use Flask CLI
flask run
```

### Production Mode
```bash
# Set production environment
export FLASK_ENV=production

# Use Gunicorn (recommended)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

---

## 🧪 Testing

Run the test suite:
```bash
# All tests
pytest

# With coverage report
pytest --cov=backend --cov-report=html

# Specific test file
pytest tests/test_email.py
```

---

## 📝 Notes

### Important Considerations

1. **Encrypted Storage**: 
   - Emails are stored in encrypted form in the database
   - Only users with valid quantum keys can decrypt
   - Preview in inbox shows encrypted data (not plaintext)

2. **One-Time Pad (Level 1)**:
   - Keys are consumed after single use
   - Cannot decrypt same email twice
   - Most secure but requires more keys

3. **Key Management**:
   - Keys expire after 24 hours by default
   - Expired keys cannot decrypt emails
   - System generates keys on-demand when sending emails

4. **User Registration**:
   - Must have an account to send/receive emails
   - Only registered users can be recipients
   - System validates email addresses in real-time

5. **Service Status**:
   - Simulated service monitoring (KM, Email, Quantum)
   - Random failures shown to demonstrate error handling
   - In production, connect to actual service health checks

---

## 🔮 Future Enhancements

- Real QKD hardware integration
- Email search and filtering
- Attachment encryption support
- Group email encryption
- Mobile applications
- Quantum-secure chat
- Video/audio calling with QKD

---

## 📄 License

Open source and free to use

---

## 👥 Contributors

Developed as part of a quantum communication security research project.

**Contact**: srisaimanas06@gmail.com

---

**Made with ❤️ and ⚛️**
