// Main application controller for QuMail

class QuMailApp {
    constructor() {
        this.currentUser = null;
        this.initialize();
    }

    async initialize() {
        try {
            // Check authentication
            await this.checkAuthentication();

            // Load user info
            await this.loadUserInfo();

            // Initialize logout functionality
            this.initializeLogout();

            // Initialize responsive behavior
            this.initializeResponsive();

            console.log('QuMail application initialized successfully');
        } catch (error) {
            console.error('Failed to initialize QuMail:', error);
            // Redirect to login if initialization fails
            window.location.href = '/login';
        }
    }

    async checkAuthentication() {
        try {
            const response = await Utils.apiRequest('/api/auth/check');
            if (!response.authenticated) {
                throw new Error('Not authenticated');
            }
            this.currentUser = response.user;
        } catch (error) {
            // Redirect to login page
            window.location.href = '/login';
            throw error;
        }
    }

    async loadUserInfo() {
        if (!this.currentUser) return;

        // Update user info in sidebar
        const userName = document.getElementById('userName');
        const userEmail = document.getElementById('userEmail');
        const userAvatar = document.getElementById('userAvatar');

        if (userName) userName.textContent = this.currentUser.full_name;
        if (userEmail) userEmail.textContent = this.currentUser.email;
        if (userAvatar) {
            userAvatar.textContent = Utils.generateAvatar(this.currentUser.full_name);
        }
    }

    initializeLogout() {
        const logoutBtn = document.getElementById('logoutBtn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', async () => {
                try {
                    await Utils.apiRequest('/api/auth/logout', 'POST');
                    Utils.showToast('Logged out successfully', 'success');
                    setTimeout(() => {
                        window.location.href = '/login';
                    }, 1000);
                } catch (error) {
                    Utils.showToast('Logout failed', 'error');
                }
            });
        }
    }

    initializeResponsive() {
        // Handle mobile sidebar toggle (if implemented)
        const sidebarToggle = document.getElementById('sidebarToggle');
        const sidebar = document.querySelector('.sidebar');

        if (sidebarToggle && sidebar) {
            sidebarToggle.addEventListener('click', () => {
                sidebar.classList.toggle('active');
            });

            // Close sidebar when clicking outside on mobile
            document.addEventListener('click', (e) => {
                if (window.innerWidth <= 768 &&
                    !sidebar.contains(e.target) &&
                    !sidebarToggle.contains(e.target)) {
                    sidebar.classList.remove('active');
                }
            });
        }

        // Handle window resize
        window.addEventListener('resize', () => {
            if (window.innerWidth > 768 && sidebar) {
                sidebar.classList.remove('active');
            }
        });
    }

    // Utility methods for other components
    getCurrentUser() {
        return this.currentUser;
    }

    async refreshUserData() {
        await this.checkAuthentication();
        await this.loadUserInfo();
    }
}

// Global app instance
let quMailApp;

// Initialize application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    quMailApp = new QuMailApp();
});

// Global error handler for unhandled promise rejections
window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);

    // Show user-friendly error for network issues
    if (event.reason?.message?.includes('fetch')) {
        Utils.showToast('Network connection error', 'error');
    }
});

// Global error handler for JavaScript errors
window.addEventListener('error', (event) => {
    console.error('JavaScript error:', event.error);

    // Don't show toast for every JS error, just log them
    // Utils.showToast('An unexpected error occurred', 'error');
});