// Main Application Initialization
document.addEventListener('DOMContentLoaded', async () => {
    console.log('E-Commerce App Initialized');

    // Update UI based on authentication status
    authManager.updateUI();

    // Load categories first
    await productsManager.loadCategories();

    // Load products
    await productsManager.loadProducts();

    // Update cart count on load
    cartManager.updateCartCount();

    console.log('App ready!');
});

// Categories Button Handler
document.getElementById('categoriesBtn').addEventListener('click', () => {
    const categoryFilter = document.getElementById('categoryFilter');
    categoryFilter.focus();
    categoryFilter.scrollIntoView({ behavior: 'smooth', block: 'center' });
});

// Utility: Format currency
function formatCurrency(amount) {
    return `$${parseFloat(amount).toFixed(2)}`;
}

// Utility: Debounce function for search
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Add debounced search
const debouncedSearch = debounce(() => {
    productsManager.applyFilters();
}, 500);

document.getElementById('searchInput').addEventListener('input', debouncedSearch);

// Auto-apply filters when category or sort changes
document.getElementById('categoryFilter').addEventListener('change', () => {
    productsManager.applyFilters();
});

document.getElementById('sortBy').addEventListener('change', () => {
    productsManager.applyFilters();
});

// Handle keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // ESC to close modals
    if (e.key === 'Escape') {
        document.querySelectorAll('.modal').forEach(modal => {
            modal.style.display = 'none';
        });
    }

    // Ctrl/Cmd + K to focus search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        document.getElementById('searchInput').focus();
    }
});

// Error handling for images
document.addEventListener('error', (e) => {
    if (e.target.tagName === 'IMG') {
        e.target.style.display = 'none';
        e.target.parentElement.innerHTML = '🛍️';
    }
}, true);

// Service Worker Registration (for future PWA support)
if ('serviceWorker' in navigator) {
    // Uncomment when you add a service worker
    // navigator.serviceWorker.register('/sw.js');
}

console.log('%c Welcome to ShopHub! ', 'background: #6366f1; color: white; font-size: 20px; padding: 10px;');
console.log('%c Build your e-commerce experience ', 'color: #6366f1; font-size: 14px;');
