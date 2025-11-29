// Products Manager
class ProductsManager {
    constructor() {
        this.products = [];
        this.categories = [];
        this.filters = {
            search: '',
            category: '',
            minPrice: '',
            maxPrice: '',
            ordering: '-created_at',
        };
        this.editingProductId = null;
    }

    async loadProducts() {
        const loading = document.getElementById('loading');
        const productsGrid = document.getElementById('productsGrid');
        const emptyState = document.getElementById('emptyState');

        try {
            loading.style.display = 'block';
            productsGrid.innerHTML = '';
            emptyState.style.display = 'none';

            // Build query parameters
            const params = {
                ordering: this.filters.ordering,
            };

            if (this.filters.search) {
                params.search = this.filters.search;
            }
            if (this.filters.category) {
                params.category = this.filters.category;
            }
            if (this.filters.minPrice) {
                params.price_min = this.filters.minPrice;
            }
            if (this.filters.maxPrice) {
                params.price_max = this.filters.maxPrice;
            }

            this.products = await api.getProducts(params);
            this.renderProducts();
        } catch (error) {
            console.error('Error loading products:', error);
            emptyState.style.display = 'block';
            emptyState.innerHTML = '<p>Error loading products. Please try again.</p>';
        } finally {
            loading.style.display = 'none';
        }
    }

    renderProducts() {
        const productsGrid = document.getElementById('productsGrid');
        const emptyState = document.getElementById('emptyState');

        if (this.products.length === 0) {
            emptyState.style.display = 'block';
            return;
        }

        productsGrid.innerHTML = this.products.map(product => {
            const isInWishlist = window.wishlistManager ? wishlistManager.isInWishlist(product.id) : false;
            return `
            <div class="product-card" data-product-id="${product.id}" onclick="productsManager.showProductDetail(${product.id})">
                <button class="wishlist-btn ${isInWishlist ? 'active' : ''}" onclick="event.stopPropagation(); productsManager.toggleWishlist(${product.id})">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                        <path d="M12,21.35L10.55,20.03C5.4,15.36 2,12.27 2,8.5C2,5.41 4.42,3 7.5,3C9.24,3 10.91,3.81 12,5.08C13.09,3.81 14.76,3 16.5,3C19.58,3 22,5.41 22,8.5C22,12.27 18.6,15.36 13.45,20.03L12,21.35Z"/>
                    </svg>
                </button>
                <div class="product-image">
                    ${product.image_url ?
                        `<img src="${product.image_url}" alt="${product.name}" onerror="this.style.display='none'; this.parentElement.innerHTML='🛍️';">` :
                        '🛍️'
                    }
                </div>
                <div class="product-info">
                    <div class="product-category">${product.category?.name || 'Uncategorized'}</div>
                    <h3 class="product-name">${product.name}</h3>
                    <p class="product-description">${product.description || 'No description available'}</p>
                    <div class="product-footer">
                        <div>
                            <div class="product-price">$${parseFloat(product.price).toFixed(2)}</div>
                            <span class="stock-badge ${product.stock_quantity > 0 ? 'in-stock' : 'out-of-stock'}">
                                ${product.stock_quantity > 0 ? `In Stock (${product.stock_quantity})` : 'Out of Stock'}
                            </span>
                        </div>
                    </div>
                </div>
                <div class="quick-view-badge">Click to view details</div>
            </div>
        `}).join('');
    }

    async showProductDetail(productId) {
        try {
            const product = await api.getProduct(productId);
            const modal = document.getElementById('productModal');
            const detailContainer = document.getElementById('productDetail');

            // Check if current user owns this product
            const isOwner = authManager.isAuthenticated() &&
                           authManager.username === product.owner?.username;

            detailContainer.innerHTML = `
                <div class="product-detail">
                    <div class="product-detail-image">
                        ${product.image_url ?
                            `<img src="${product.image_url}" alt="${product.name}" onerror="this.style.display='none'; this.parentElement.innerHTML='🛍️';">` :
                            '🛍️'
                        }
                    </div>
                    <div class="product-detail-info">
                        <div class="product-category">${product.category?.name || 'Uncategorized'}</div>
                        <h2>${product.name}</h2>
                        <p>${product.description || 'No description available'}</p>
                        <div class="product-price" style="margin-bottom: 1rem;">$${parseFloat(product.price).toFixed(2)}</div>
                        <span class="stock-badge ${product.stock_quantity > 0 ? 'in-stock' : 'out-of-stock'}">
                            ${product.stock_quantity > 0 ? `In Stock: ${product.stock_quantity} units` : 'Out of Stock'}
                        </span>
                        <div class="product-actions" style="margin-top: 2rem;">
                            ${product.stock_quantity > 0 ?
                                `<button class="btn btn-primary" onclick="cartManager.addToCart(${product.id}, '${product.name}', ${product.price})">Add to Cart</button>` :
                                `<button class="btn btn-secondary" disabled>Out of Stock</button>`
                            }
                            ${isOwner ? `
                                <button class="btn btn-secondary" onclick="productsManager.editProduct(${product.id})">Edit</button>
                                <button class="btn btn-danger" onclick="productsManager.deleteProduct(${product.id})">Delete</button>
                            ` : ''}
                        </div>
                    </div>
                </div>
            `;

            modal.style.display = 'block';
        } catch (error) {
            console.error('Error loading product detail:', error);
            alert('Error loading product details');
        }
    }

    async loadCategories() {
        try {
            this.categories = await api.getCategories();
            this.renderCategoryFilters();
            this.renderCategoryOptions();
        } catch (error) {
            console.error('Error loading categories:', error);
        }
    }

    renderCategoryFilters() {
        const categoryFilter = document.getElementById('categoryFilter');
        categoryFilter.innerHTML = '<option value="">All Categories</option>' +
            this.categories.map(cat => `<option value="${cat.slug}">${cat.name}</option>`).join('');
    }

    renderCategoryOptions() {
        const productCategory = document.getElementById('productCategory');
        productCategory.innerHTML = '<option value="">Select Category</option>' +
            this.categories.map(cat => `<option value="${cat.id}">${cat.name}</option>`).join('');
    }

    applyFilters() {
        this.filters.search = document.getElementById('searchInput').value;
        this.filters.category = document.getElementById('categoryFilter').value;
        this.filters.minPrice = document.getElementById('minPrice').value;
        this.filters.maxPrice = document.getElementById('maxPrice').value;
        this.filters.ordering = document.getElementById('sortBy').value;

        this.loadProducts();
    }

    openAddProductModal() {
        if (!authManager.isAuthenticated()) {
            alert('Please login to add products');
            return;
        }

        this.editingProductId = null;
        document.getElementById('productFormTitle').textContent = 'Add Product';
        document.getElementById('productForm').reset();
        document.getElementById('addProductModal').style.display = 'block';
    }

    async editProduct(productId) {
        try {
            this.editingProductId = productId;
            const product = await api.getProduct(productId);

            document.getElementById('productFormTitle').textContent = 'Edit Product';
            document.getElementById('productName').value = product.name;
            document.getElementById('productDescription').value = product.description || '';
            document.getElementById('productPrice').value = product.price;
            document.getElementById('productCategory').value = product.category?.id || '';
            document.getElementById('productStock').value = product.stock_quantity;
            document.getElementById('productImage').value = product.image_url || '';

            document.getElementById('productModal').style.display = 'none';
            document.getElementById('addProductModal').style.display = 'block';
        } catch (error) {
            console.error('Error loading product for edit:', error);
            alert('Error loading product');
        }
    }

    async saveProduct(formData) {
        try {
            if (this.editingProductId) {
                await api.updateProduct(this.editingProductId, formData);
                alert('Product updated successfully!');
            } else {
                await api.createProduct(formData);
                alert('Product created successfully!');
            }

            document.getElementById('addProductModal').style.display = 'none';
            document.getElementById('productForm').reset();
            this.loadProducts();
        } catch (error) {
            throw error;
        }
    }

    async deleteProduct(productId) {
        if (!confirm('Are you sure you want to delete this product?')) {
            return;
        }

        try {
            await api.deleteProduct(productId);
            if (window.toastManager) {
                toastManager.success('Product deleted successfully!');
            }
            document.getElementById('productModal').style.display = 'none';
            this.loadProducts();
        } catch (error) {
            console.error('Error deleting product:', error);
            if (window.toastManager) {
                toastManager.error('Error deleting product');
            }
        }
    }

    async toggleWishlist(productId) {
        try {
            const product = await api.getProduct(productId);
            if (window.wishlistManager) {
                const added = wishlistManager.toggleWishlist(product);

                // Update the heart button
                const heartBtn = document.querySelector(`[data-product-id="${productId}"] .wishlist-btn`);
                if (heartBtn) {
                    if (added) {
                        heartBtn.classList.add('active');
                    } else {
                        heartBtn.classList.remove('active');
                    }
                }
            }
        } catch (error) {
            console.error('Error toggling wishlist:', error);
            if (window.toastManager) {
                toastManager.error('Error updating wishlist');
            }
        }
    }
}

// Create global products manager instance
const productsManager = new ProductsManager();
window.productsManager = productsManager;

// Event Listeners
document.getElementById('applyFilters').addEventListener('click', () => {
    productsManager.applyFilters();
});

document.getElementById('searchInput').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        productsManager.applyFilters();
    }
});

document.getElementById('fabAddProduct').addEventListener('click', () => {
    productsManager.openAddProductModal();
});

document.getElementById('productForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const errorEl = document.getElementById('productFormError');

    const formData = {
        name: document.getElementById('productName').value,
        description: document.getElementById('productDescription').value,
        price: parseFloat(document.getElementById('productPrice').value),
        category_id: parseInt(document.getElementById('productCategory').value),
        stock_quantity: parseInt(document.getElementById('productStock').value),
        image_url: document.getElementById('productImage').value || '',
    };

    try {
        await productsManager.saveProduct(formData);
        errorEl.textContent = '';
    } catch (error) {
        errorEl.textContent = error.message || 'Error saving product';
    }
});

document.getElementById('myProductsBtn').addEventListener('click', () => {
    // Filter to show only user's products
    productsManager.filters.search = '';
    productsManager.filters.category = '';
    productsManager.filters.minPrice = '';
    productsManager.filters.maxPrice = '';
    document.getElementById('searchInput').value = `owner:${authManager.username}`;
    productsManager.applyFilters();
});
