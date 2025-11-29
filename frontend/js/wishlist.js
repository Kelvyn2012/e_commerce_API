// Wishlist Manager
class WishlistManager {
    constructor() {
        this.wishlist = this.loadWishlistFromStorage();
        this.updateWishlistCount();
    }

    loadWishlistFromStorage() {
        const wishlist = localStorage.getItem('wishlist');
        return wishlist ? JSON.parse(wishlist) : [];
    }

    saveWishlistToStorage() {
        localStorage.setItem('wishlist', JSON.stringify(this.wishlist));
    }

    isInWishlist(productId) {
        return this.wishlist.some(item => item.id === productId);
    }

    toggleWishlist(product) {
        const index = this.wishlist.findIndex(item => item.id === product.id);

        if (index > -1) {
            // Remove from wishlist
            this.wishlist.splice(index, 1);
            this.saveWishlistToStorage();
            this.updateWishlistCount();

            if (window.toastManager) {
                toastManager.show(`${product.name} removed from wishlist`, 'info');
            }
            return false;
        } else {
            // Add to wishlist
            this.wishlist.push({
                id: product.id,
                name: product.name,
                price: product.price,
                image_url: product.image_url || '',
                category: product.category
            });
            this.saveWishlistToStorage();
            this.updateWishlistCount();

            if (window.toastManager) {
                toastManager.success(`${product.name} added to wishlist!`);
            }
            return true;
        }
    }

    updateWishlistCount() {
        const count = this.wishlist.length;
        const badge = document.getElementById('wishlistCount');
        if (badge) {
            badge.textContent = count;
            badge.style.display = count > 0 ? 'inline-block' : 'none';
        }
    }

    showWishlist() {
        this.renderWishlist();
        document.getElementById('wishlistModal').style.display = 'block';
    }

    renderWishlist() {
        const wishlistItemsContainer = document.getElementById('wishlistItems');

        if (this.wishlist.length === 0) {
            wishlistItemsContainer.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">💝</div>
                    <p>Your wishlist is empty</p>
                    <p style="font-size: 1rem; margin-top: 0.5rem; color: var(--text-tertiary);">
                        Click the heart icon on products to add them here
                    </p>
                </div>
            `;
            return;
        }

        wishlistItemsContainer.innerHTML = `
            <div class="products-grid">
                ${this.wishlist.map(item => `
                    <div class="product-card" onclick="productsManager.showProductDetail(${item.id})">
                        <div class="product-image">
                            ${item.image_url ?
                                `<img src="${item.image_url}" alt="${item.name}" onerror="this.style.display='none'; this.parentElement.innerHTML='🛍️';">` :
                                '🛍️'
                            }
                        </div>
                        <div class="product-info">
                            <div class="product-category">${item.category?.name || 'Uncategorized'}</div>
                            <h3 class="product-name">${item.name}</h3>
                            <div class="product-price">$${parseFloat(item.price).toFixed(2)}</div>
                            <div class="product-actions" style="margin-top: 1rem;">
                                <button class="btn btn-sm btn-danger" onclick="event.stopPropagation(); wishlistManager.removeFromWishlist(${item.id})">
                                    Remove
                                </button>
                                <button class="btn btn-sm btn-primary" onclick="event.stopPropagation(); wishlistManager.moveToCart(${item.id})">
                                    Add to Cart
                                </button>
                            </div>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    }

    removeFromWishlist(productId) {
        const item = this.wishlist.find(item => item.id === productId);
        if (item) {
            this.wishlist = this.wishlist.filter(item => item.id !== productId);
            this.saveWishlistToStorage();
            this.updateWishlistCount();
            this.renderWishlist();

            if (window.toastManager) {
                toastManager.info(`${item.name} removed from wishlist`);
            }

            // Update heart icons on product cards
            const heartBtn = document.querySelector(`[data-product-id="${productId}"] .wishlist-btn`);
            if (heartBtn) {
                heartBtn.classList.remove('active');
            }
        }
    }

    async moveToCart(productId) {
        try {
            const product = await api.getProduct(productId);

            if (product.stock_quantity > 0) {
                cartManager.addToCart(productId, product.name, product.price);
                this.removeFromWishlist(productId);

                if (window.toastManager) {
                    toastManager.success(`${product.name} moved to cart!`);
                }
            } else {
                if (window.toastManager) {
                    toastManager.warning(`${product.name} is out of stock`);
                }
            }
        } catch (error) {
            console.error('Error moving to cart:', error);
            if (window.toastManager) {
                toastManager.error('Error adding to cart');
            }
        }
    }

    clearWishlist() {
        if (confirm('Are you sure you want to clear your wishlist?')) {
            this.wishlist = [];
            this.saveWishlistToStorage();
            this.updateWishlistCount();
            this.renderWishlist();

            if (window.toastManager) {
                toastManager.info('Wishlist cleared');
            }
        }
    }
}

// Create global wishlist manager instance
const wishlistManager = new WishlistManager();
window.wishlistManager = wishlistManager;

// Event Listener for Wishlist Button
document.getElementById('wishlistBtn').addEventListener('click', () => {
    wishlistManager.showWishlist();
});
