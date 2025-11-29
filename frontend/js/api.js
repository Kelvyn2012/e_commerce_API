// API Configuration
const API_BASE_URL = 'http://localhost:8000/api';

// API Client
class APIClient {
    constructor(baseURL) {
        this.baseURL = baseURL;
    }

    getAuthHeaders() {
        const token = localStorage.getItem('authToken');
        return token ? { 'Authorization': `Token ${token}` } : {};
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...this.getAuthHeaders(),
                ...options.headers,
            },
            ...options,
        };

        try {
            const response = await fetch(url, config);

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || error.error || 'An error occurred');
            }

            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // Auth endpoints
    async login(username, password) {
        return this.request('/auth/login/', {
            method: 'POST',
            body: JSON.stringify({ username, password }),
        });
    }

    async register(username, email, password) {
        return this.request('/auth/register/', {
            method: 'POST',
            body: JSON.stringify({ username, email, password }),
        });
    }

    // Products endpoints
    async getProducts(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        const endpoint = queryString ? `/products/?${queryString}` : '/products/';
        return this.request(endpoint);
    }

    async getProduct(id) {
        return this.request(`/products/${id}/`);
    }

    async createProduct(productData) {
        return this.request('/products/', {
            method: 'POST',
            body: JSON.stringify(productData),
        });
    }

    async updateProduct(id, productData) {
        return this.request(`/products/${id}/`, {
            method: 'PUT',
            body: JSON.stringify(productData),
        });
    }

    async deleteProduct(id) {
        return this.request(`/products/${id}/`, {
            method: 'DELETE',
        });
    }

    // Categories endpoints
    async getCategories() {
        return this.request('/categories/');
    }

    async getCategory(id) {
        return this.request(`/categories/${id}/`);
    }

    async createCategory(categoryData) {
        return this.request('/categories/', {
            method: 'POST',
            body: JSON.stringify(categoryData),
        });
    }

    // Users endpoints
    async getCurrentUser() {
        const token = localStorage.getItem('authToken');
        if (!token) return null;

        try {
            // Get user info from token by fetching users endpoint
            return await this.request('/users/');
        } catch (error) {
            console.error('Error fetching current user:', error);
            return null;
        }
    }
}

// Create a global API instance
const api = new APIClient(API_BASE_URL);
