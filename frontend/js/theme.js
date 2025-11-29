// Theme Manager for Dark Mode
class ThemeManager {
    constructor() {
        this.theme = localStorage.getItem('theme') || 'light';
        this.init();
    }

    init() {
        // Apply saved theme
        this.applyTheme(this.theme);

        // Setup toggle button
        const themeToggle = document.getElementById('themeToggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', () => this.toggleTheme());
        }

        // Update icon
        this.updateIcon();
    }

    toggleTheme() {
        this.theme = this.theme === 'light' ? 'dark' : 'light';
        this.applyTheme(this.theme);
        this.updateIcon();
        localStorage.setItem('theme', this.theme);

        // Show toast notification
        if (window.toastManager) {
            toastManager.show(
                `${this.theme === 'dark' ? '🌙' : '☀️'} ${this.theme === 'dark' ? 'Dark' : 'Light'} mode activated`,
                'info'
            );
        }
    }

    applyTheme(theme) {
        if (theme === 'dark') {
            document.documentElement.setAttribute('data-theme', 'dark');
        } else {
            document.documentElement.removeAttribute('data-theme');
        }
    }

    updateIcon() {
        const icon = document.getElementById('themeIcon');
        if (!icon) return;

        if (this.theme === 'dark') {
            // Sun icon for light mode
            icon.innerHTML = '<path d="M12,17c-2.76,0-5-2.24-5-5s2.24-5,5-5,5,2.24,5,5-2.24,5-5,5Zm0-8c-1.65,0-3,1.35-3,3s1.35,3,3,3,3-1.35,3-3-1.35-3-3-3Zm0-4c-.55,0-1-.45-1-1V2c0-.55.45-1,1-1s1,.45,1,1v2c0,.55-.45,1-1,1Zm0,18c-.55,0-1-.45-1-1v-2c0-.55.45-1,1-1s1,.45,1,1v2c0,.55-.45,1-1,1ZM5.99,7.99c-.39-.39-.39-1.02,0-1.41l1.41-1.42c.39-.38,1.03-.39,1.42,0,.39.39.39,1.02,0,1.41l-1.41,1.42c-.39.38-1.03.39-1.42,0Zm12.01,12.01c-.39-.39-.39-1.02,0-1.41l1.41-1.42c.39-.38,1.03-.39,1.42,0,.39.39.39,1.02,0,1.41l-1.41,1.42c-.39.38-1.03.39-1.42,0ZM23,11h-2c-.55,0-1,.45-1,1s.45,1,1,1h2c.55,0,1-.45,1-1s-.45-1-1-1ZM5,12c0-.55-.45-1-1-1H2c-.55,0-1,.45-1,1s.45,1,1,1h2c.55,0,1-.45,1-1Zm13.01,7.99c.39-.39,1.02-.39,1.41,0l1.42,1.41c.38.39.39,1.03,0,1.42-.39.39-1.02.39-1.41,0l-1.42-1.41c-.38-.39-.39-1.03,0-1.42ZM5.99,5.99c.39-.39,1.02-.39,1.41,0l1.42,1.41c.38.39.39,1.03,0,1.42-.39.39-1.02.39-1.41,0l-1.42-1.41c-.38-.39-.39-1.03,0-1.42Z"/>';
        } else {
            // Moon icon for dark mode
            icon.innerHTML = '<path d="M21.64,13a1,1,0,0,0-1.05-.14,8.05,8.05,0,0,1-3.37.73A8.15,8.15,0,0,1,9.08,5.49a8.59,8.59,0,0,1,.25-2A1,1,0,0,0,8,2.36,10.14,10.14,0,1,0,22,14.05,1,1,0,0,0,21.64,13Z"/>';
        }
    }

    getCurrentTheme() {
        return this.theme;
    }
}

// Create global theme manager instance
const themeManager = new ThemeManager();
window.themeManager = themeManager;
