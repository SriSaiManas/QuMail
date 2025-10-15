// Authentication handling for QuMail

class AuthManager {
    constructor() {
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // Tab switching
        const tabButtons = document.querySelectorAll('.tab-btn');
        tabButtons.forEach(btn => {
            btn.addEventListener('click', (e) => this.switchTab(e.target.dataset.tab));
        });

        // Form submissions
        const loginForm = document.getElementById('loginForm');
        const registerForm = document.getElementById('registerForm');

        if (loginForm) {
            loginForm.addEventListener('submit', (e) => this.handleLogin(e));
        }

        if (registerForm) {
            registerForm.addEventListener('submit', (e) => this.handleRegister(e));
        }

        // Password confirmation validation
        const confirmPassword = document.getElementById('confirmPassword');
        if (confirmPassword) {
            confirmPassword.addEventListener('input', this.validatePasswordMatch);
        }

        // Check if user is already authenticated
        this.checkAuthStatus();
    }

    switchTab(tabName) {
        // Update tab buttons
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.tab === tabName);
        });

        // Update tab content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.toggle('active', content.id === tabName);
        });
    }

    async handleLogin(event) {
        event.preventDefault();
        const loginBtn = document.getElementById('loginBtn');
        const originalText = loginBtn.innerHTML;

        try {
            // Show loading state
            loginBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Signing in...';
            loginBtn    overflow: hidden;
}

.email-header {
    padding: 25px 30px;
    border-bottom: 1px solid var(--border-color);
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: var(--glass-bg);
    backdrop-filter: blur(10px);
}

.email-header h1 {
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--text-primary);
}

.email-actions {
    display: flex;
    gap: 10px;
}

.btn-refresh {
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    color: var(--text-secondary);
    padding: 10px 12px;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.btn-refresh:hover {
    background: rgba(255, 255, 255, 0.1);
    color: var(--text-primary);
}

/* Email List */
.email-list {
    flex: 1;
    overflow-y: auto;
    padding: 0;
}

.email-item {
    display: flex;
    align-items: center;
    padding: 20px 30px;
    border-bottom: 1px solid var(--border-color);
    cursor: pointer;
    transition: all 0.3s ease;
    position: relative;
}

.email-item:hover {
    background: var(--glass-bg);
}

.email-item.unread {
    background: rgba(79, 195, 247, 0.05);
}

.email-item.unread::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 4px;
    background: var(--accent-blue);
}

.email-sender {
    width: 200px;
    font-weight: 600;
    color: var(--text-primary);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.email-content {
    flex: 1;
    margin: 0 20px;
    overflow: hidden;
}

.email-subject {
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 4px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.email-preview {
    color: var(--text-secondary);
    font-size: 0.9rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.email-meta {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 8px;
    min-width: 120px;
}

.email-date {
    color: var(--text-muted);
    font-size: 0.85rem;
}

.security-badge {
    padding: 4px 8px;
    border-radius: 12px;
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
}

.security-badge.level-1 {
    background: rgba(79, 195, 247, 0.2);
    color: var(--accent-blue);
    border: 1px solid rgba(79, 195, 247, 0.3);
}

.security-badge.level-2 {
    background: rgba(76, 175, 80, 0.2);
    color: var(--success);
    border: 1px solid rgba(76, 175, 80, 0.3);
}

.security-badge.level-3 {
    background: rgba(255, 193, 7, 0.2);
    color: var(--warning);
    border: 1px solid rgba(255, 193, 7, 0.3);
}

.security-badge.level-4 {
    background: rgba(158, 158, 158, 0.2);
    color: var(--text-muted);
    border: 1px solid rgba(158, 158, 158, 0.3);
}

/* Compose Modal Specific Styles */
.compose-form {
    padding: 30px;
}

.form-row {
    margin-bottom: 25px;
}

.email-input-container {
    position: relative;
}

.email-validation {
    position: absolute;
    right: 12px;
    top: 50%;
    transform: translateY(-50%);
    display: none;
}

.email-validation.show {
    display: block;
}

.validation-text {
    font-size: 0.8rem;
    padding: 4px 8px;
    border-radius: 4px;
    font-weight: 600;
}

.validation-text.found {
    color: var(--success);
}

.validation-text.not-found {
    color: var(--warning);
}

/* Security Level Options */
.security-levels {
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-top: 10px;
}

.security-option {
    position: relative;
}

.security-option input[type="radio"] {
    position: absolute;
    opacity: 0;
    width: 0;
    height: 0;
}

.security-option label {
    display: block;
    padding: 15px 20px;
    background: var(--glass-bg);
    border: 2px solid var(--glass-border);
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.security-option input[type="radio"]:checked + label {
    border-color: var(--accent-blue);
    background: rgba(79, 195, 247, 0.1);
}

.level-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 8px;
}

.level-name {
    font-weight: 600;
    color: var(--text-primary);
}

.level-badge {
    padding: 4px 8px;
    border-radius: 12px;
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
}

.level-badge.high {
    background: rgba(79, 195, 247, 0.2);
    color: var(--accent-blue);
}

.level-badge.medium {
    background: rgba(255, 193, 7, 0.2);
    color: var(--warning);
}

.level-badge.low {
    background: rgba(158, 158, 158, 0.2);
    color: var(--text-muted);
}

.security-option p {
    margin: 0;
    font-size: 0.9rem;
    color: var(--text-secondary);
}

/* File Upload Area */
.file-upload-area {
    border: 2px dashed var(--glass-border);
    border-radius: 10px;
    padding: 20px;
    text-align: center;
    transition: all 0.3s ease;
    cursor: pointer;
}

.file-upload-area:hover {
    border-color: var(--accent-blue);
    background: rgba(79, 195, 247, 0.05);
}

.upload-prompt {
    color: var(--text-secondary);
}

.upload-prompt i {
    font-size: 2rem;
    margin-bottom: 10px;
    color: var(--accent-blue);
}

.attached-files {
    margin-top: 15px;
    text-align: left;
}

.attached-file {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 15px;
    background: var(--glass-bg);
    border-radius: 8px;
    margin-bottom: 8px;
}

.file-info {
    display: flex;
    align-items: center;
    gap: 10px;
}

.file-icon {
    color: var(--accent-blue);
}

.file-name {
    font-weight: 600;
    color: var(--text-primary);
}

.file-size {
    color: var(--text-muted);
    font-size: 0.8rem;
}

.remove-file {
    background: none;
    border: none;
    color: var(--danger);
    cursor: pointer;
    padding: 5px;
    border-radius: 4px;
    transition: all 0.3s ease;
}

.remove-file:hover {
    background: rgba(244, 67, 54, 0.1);
}

/* Email View Modal */
.email-view {
    width: 800px;
    max-width: 90vw;
}

.email-view .modal-header .email-info h2 {
    margin-bottom: 10px;
    color: var(--text-primary);
}

.email-meta {
    display: flex;
    gap: 20px;
    flex-wrap: wrap;
}

.email-meta span {
    font-size: 0.9rem;
    color: var(--text-secondary);
}

.email-content {
    padding: 30px;
}

.encrypted-state {
    text-align: center;
    padding: 40px 20px;
}

.encrypted-message {
    margin-bottom: 30px;
}

.encrypted-message i {
    font-size: 3rem;
    color: var(--accent-blue);
    margin-bottom: 20px;
}

.encrypted-message h3 {
    margin-bottom: 10px;
    color: var(--text-primary);
}

.encrypted-preview {
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: 8px;
    padding: 20px;
    margin: 20px 0;
    font-family: 'Courier New', monospace;
    font-size: 0.9rem;
    color: var(--text-muted);
    word-break: break-all;
    max-height: 150px;
    overflow-y: auto;
}

.btn-decrypt {
    background: linear-gradient(45deg, var(--success), #388e3c);
    color: white;
    border: none;
    padding: 15px 30px;
    border-radius: 10px;
    font-weight: 600;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 0 auto;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
}

.btn-decrypt:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
}

.decrypted-state .email-body {
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: 10px;
    padding: 25px;
    line-height: 1.6;
    color: var(--text-primary);
    white-space: pre-wrap;
}

.email-attachments {
    margin-top: 30px;
    padding-top: 20px;
    border-top: 1px solid var(--border-color);
}

.email-attachments h4 {
    margin-bottom: 15px;
    color: var(--text-primary);
}

.attachment-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.attachment-item {
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 15px;
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: 8px;
    transition: all 0.3s ease;
}

.attachment-item:hover {
    background: rgba(255, 255, 255, 0.1);
}

.attachment-icon {
    font-size: 1.5rem;
    color: var(--accent-blue);
}

.attachment-details {
    flex: 1;
}

.attachment-name {
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 4px;
}

.attachment-meta {
    font-size: 0.8rem;
    color: var(--text-muted);
}

.download-btn {
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    color: var(--text-primary);
    padding: 8px 12px;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.download-btn:hover {
    background: rgba(255, 255, 255, 0.1);
}

/* Modal Actions */
.modal-actions {
    display: flex;
    justify-content: flex-end;
    gap: 15px;
    padding-top: 20px;
    border-top: 1px solid var(--border-color);
}

/* Responsive Design */
@media (max-width: 1024px) {
    .sidebar {
        width: 250px;
    }

    .email-item {
        padding: 15px 20px;
    }

    .email-sender {
        width: 150px;
    }
}

@media (max-width: 768px) {
    .app-container {
        flex-direction: column;
    }

    .sidebar {
        width: 100%;
        height: auto;
        position: fixed;
        bottom: 0;
        left: 0;
        z-index: 1000;
        border-right: none;
        border-top: 1px solid var(--border-color);
        transform: translateY(100%);
        transition: transform 0.3s ease;
    }

    .sidebar.active {
        transform: translateY(0);
    }

    .main-panel {
        padding-bottom: 60px;
    }

    .email-item {
        flex-direction: column;
        align-items: flex-start;
        gap: 10px;
    }

    .email-sender {
        width: 100%;
    }

    .email-meta {
        flex-direction: row;
        align-items: center;
        width: 100%;
        justify-content: space-between;
    }

    .compose-form {
        padding: 20px;
    }

    .security-levels {
        gap: 8px;
    }

    .security-option label {
        padding: 12px 15px;
    }

    .email-view {
        width: 95vw;
        margin: 10px;
    }

    .email-content {
        padding: 20px;
    }
}

@media (max-width: 480px) {
    .email-header {
        padding: 20px;
    }

    .email-header h1 {
        font-size: 1.5rem;
    }

    .email-item {
        padding: 12px 15px;
    }

    .modal-actions {
        flex-direction: column;
        gap: 10px;
    }

    .modal-actions button {
        width: 100%;
    }
}