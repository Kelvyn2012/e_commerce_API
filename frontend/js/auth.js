// Authentication Manager
class AuthManager {
    constructor() {
        this.currentUser = null;
        this.token = localStorage.getItem('authToken');
        this.username = localStorage.getItem('username');
    }

    isAuthenticated() {
        return !!this.token;
    }

    async login(username, password) {
        try {
            const response = await api.login(username, password);
            this.token = response.token;
            this.username = username;

            localStorage.setItem('authToken', response.token);
            localStorage.setItem('username', username);

            this.updateUI();
            return true;
        } catch (error) {
            throw error;
        }
    }

    async register(username, email, password) {
        try {
            await api.register(username, email, password);
            // Auto login after registration
            return await this.login(username, password);
        } catch (error) {
            throw error;
        }
    }

    logout() {
        this.token = null;
        this.username = null;
        this.currentUser = null;

        localStorage.removeItem('authToken');
        localStorage.removeItem('username');

        this.updateUI();

        // Reload products to show public view
        if (window.productsManager) {
            window.productsManager.loadProducts();
        }
    }

    updateUI() {
        const loginBtn = document.getElementById('loginBtn');
        const registerBtn = document.getElementById('registerBtn');
        const userMenu = document.getElementById('userMenu');
        const usernameEl = document.getElementById('username');
        const fabAddProduct = document.getElementById('fabAddProduct');

        if (this.isAuthenticated()) {
            loginBtn.style.display = 'none';
            registerBtn.style.display = 'none';
            userMenu.style.display = 'flex';
            usernameEl.textContent = this.username;
            fabAddProduct.style.display = 'block';
        } else {
            loginBtn.style.display = 'block';
            registerBtn.style.display = 'block';
            userMenu.style.display = 'none';
            fabAddProduct.style.display = 'none';
        }
    }
}

// Create global auth manager instance
const authManager = new AuthManager();

// Login Modal Handler
document.getElementById('loginBtn').addEventListener('click', () => {
    document.getElementById('loginModal').style.display = 'block';
});

document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;
    const errorEl = document.getElementById('loginError');

    try {
        await authManager.login(username, password);
        document.getElementById('loginModal').style.display = 'none';
        document.getElementById('loginForm').reset();
        errorEl.textContent = '';

        // Show success message
        toastManager.success('Login successful!');
    } catch (error) {
        errorEl.textContent = error.message || 'Login failed. Please check your credentials.';
    }
});

// Register Modal Handler
document.getElementById('registerBtn').addEventListener('click', () => {
    document.getElementById('registerModal').style.display = 'block';
});

// Password Strength Checker
function checkPasswordStrength(password) {
    let strength = 0;
    const requirements = {
        length: password.length >= 8,
        uppercase: /[A-Z]/.test(password),
        lowercase: /[a-z]/.test(password),
        number: /[0-9]/.test(password),
        special: /[^A-Za-z0-9]/.test(password)
    };

    // Count met requirements
    Object.values(requirements).forEach(met => {
        if (met) strength++;
    });

    // Determine strength level
    let level = '';
    if (strength === 0) level = '';
    else if (strength <= 2) level = 'weak';
    else if (strength === 3) level = 'fair';
    else if (strength === 4) level = 'good';
    else level = 'strong';

    return { level, requirements, strength };
}

// Update password strength UI
function updatePasswordStrength(password) {
    const strengthBar = document.getElementById('passwordStrengthBar');
    const strengthText = document.getElementById('passwordStrengthText');
    const { level, requirements } = checkPasswordStrength(password);

    // Remove all classes
    strengthBar.className = 'password-strength-fill';
    strengthText.className = 'password-strength-text';

    // Add strength class
    if (level) {
        strengthBar.classList.add(level);
        strengthText.classList.add(level);
        strengthText.textContent = level.charAt(0).toUpperCase() + level.slice(1) + ' Password';
    } else {
        strengthText.textContent = '';
    }

    // Update requirements
    document.getElementById('passwordReq1').className = requirements.length ? 'req-item met' : 'req-item';
    document.getElementById('passwordReq2').className = requirements.uppercase ? 'req-item met' : 'req-item';
    document.getElementById('passwordReq3').className = requirements.lowercase ? 'req-item met' : 'req-item';
    document.getElementById('passwordReq4').className = requirements.number ? 'req-item met' : 'req-item';
    document.getElementById('passwordReq5').className = requirements.special ? 'req-item met' : 'req-item';

    // Update requirement text
    document.getElementById('passwordReq1').textContent = (requirements.length ? '✓' : '✗') + ' At least 8 characters';
    document.getElementById('passwordReq2').textContent = (requirements.uppercase ? '✓' : '✗') + ' Contains uppercase letter';
    document.getElementById('passwordReq3').textContent = (requirements.lowercase ? '✓' : '✗') + ' Contains lowercase letter';
    document.getElementById('passwordReq4').textContent = (requirements.number ? '✓' : '✗') + ' Contains number';
    document.getElementById('passwordReq5').textContent = (requirements.special ? '✓' : '✗') + ' Contains special character';
}

// Add password strength checker on input
document.getElementById('registerPassword').addEventListener('input', (e) => {
    updatePasswordStrength(e.target.value);
});

document.getElementById('registerForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('registerUsername').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    const errorEl = document.getElementById('registerError');

    // Check password strength
    const { level } = checkPasswordStrength(password);
    if (!level || level === 'weak') {
        errorEl.textContent = 'Please choose a stronger password';
        toastManager.warning('Password is too weak. Please meet all requirements.');
        return;
    }

    try {
        await authManager.register(username, email, password);
        document.getElementById('registerModal').style.display = 'none';
        document.getElementById('registerForm').reset();
        errorEl.textContent = '';

        // Reset password strength UI
        updatePasswordStrength('');

        // Show success message
        toastManager.success('Registration successful! You are now logged in.');
    } catch (error) {
        errorEl.textContent = error.message || 'Registration failed. Please try again.';
    }
});

// Logout Handler
document.getElementById('logoutBtn').addEventListener('click', () => {
    if (confirm('Are you sure you want to logout?')) {
        authManager.logout();
        toastManager.success('You have been logged out.');
    }
});

// Close modals when clicking the X
document.querySelectorAll('.close').forEach(closeBtn => {
    closeBtn.addEventListener('click', function() {
        this.closest('.modal').style.display = 'none';
    });
});

// Close modals when clicking outside
window.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal')) {
        e.target.style.display = 'none';
    }
});
