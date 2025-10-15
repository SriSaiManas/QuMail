// Quantum service management for QuMail

class QuantumManager {
    constructor() {
        this.connectionStatus = false;
        this.initializeStatusCheck();
    }

    async initializeStatusCheck() {
        // Check quantum service status every 30 seconds
        await this.checkQuantumStatus();
        setInterval(() => this.checkQuantumStatus(), 30000);
    }

    async checkQuantumStatus() {
        try {
            const response = await Utils.apiRequest('/api/quantum/status');
            this.connectionStatus = response.connected;
            this.updateConnectionIndicator(response);
        } catch (error) {
            this.connectionStatus = false;
            this.updateConnectionIndicator({ connected: false, status: 'error' });
        }
    }

    updateConnectionIndicator(status) {
        const statusDot = document.getElementById('statusDot');
        const statusText = document.getElementById('statusText');

        if (!statusDot || !statusText) return;

        if (status.connected) {
            statusDot.className = 'status-dot connected';
            statusText.textContent = 'Quantum services online';
        } else {
            statusDot.className = 'status-dot error';
            statusText.textContent = 'Quantum service offline';
        }
    }

    async requestQuantumKey(recipientEmail, keyLength = 256) {
        try {
            const response = await Utils.apiRequest('/api/quantum/keys/request', 'POST', {
                recipient_email: recipientEmail,
                key_length: keyLength
            });

            if (response.success) {
                Utils.showToast('Quantum key obtained successfully', 'success');
                return response.key;
            }
        } catch (error) {
            Utils.showToast('Failed to obtain quantum key', 'error');
            throw error;
        }
    }

    async getUserKeys() {
        try {
            const response = await Utils.apiRequest('/api/quantum/keys');
            return response.keys || [];
        } catch (error) {
            console.error('Failed to get user keys:', error);
            return [];
        }
    }

    getSecurityLevelDescription(level) {
        const descriptions = {
            1: {
                name: 'Quantum Secure (One-Time Pad)',
                description: 'Perfect security using quantum keys. Each key is used once and provides unconditional security.',
                requirements: 'Requires quantum key of same length as message'
            },
            2: {
                name: 'Quantum-aided AES',
                description: 'AES encryption using quantum keys as seed. Combines quantum randomness with proven cryptography.',
                requirements: 'Requires quantum key of at least 32 bytes'
            },
            3: {
                name: 'Post-Quantum Cryptography',
                description: 'Advanced encryption resistant to quantum computer attacks.',
                requirements: 'No quantum infrastructure needed'
            },
            4: {
                name: 'Standard Encryption',
                description: 'Traditional encryption methods. Suitable for non-sensitive content.',
                requirements: 'No special requirements'
            }
        };
        return descriptions[level] || descriptions[4];
    }

    isQuantumSecurityAvailable() {
        return this.connectionStatus;
    }
}

// Initialize quantum manager
document.addEventListener('DOMContentLoaded', () => {
    window.quantumManager = new QuantumManager();
});