// Payment Manager
class PaymentManager {
    constructor() {
        this.paymentMethod = 'stripe'; // Can be 'stripe', 'paypal', or 'cash'
        this.setupPaymentModal();
    }

    setupPaymentModal() {
        // Payment modal will be created in HTML
    }

    async processPayment(orderData) {
        const method = this.paymentMethod;

        switch(method) {
            case 'stripe':
                return await this.processStripePayment(orderData);
            case 'paypal':
                return await this.processPayPalPayment(orderData);
            case 'cash':
                return await this.processCashPayment(orderData);
            default:
                throw new Error('Invalid payment method');
        }
    }

    async processStripePayment(orderData) {
        // In a real application, this would integrate with Stripe API
        // For now, we'll simulate the payment process

        return new Promise((resolve, reject) => {
            // Show payment modal
            this.showStripePaymentModal(orderData, (result) => {
                if (result.success) {
                    resolve({
                        success: true,
                        transactionId: this.generateTransactionId(),
                        method: 'stripe',
                        amount: orderData.total,
                        timestamp: new Date().toISOString()
                    });
                } else {
                    reject(new Error('Payment cancelled'));
                }
            });
        });
    }

    async processPayPalPayment(orderData) {
        // Simulate PayPal payment
        return new Promise((resolve, reject) => {
            this.showPayPalPaymentModal(orderData, (result) => {
                if (result.success) {
                    resolve({
                        success: true,
                        transactionId: this.generateTransactionId(),
                        method: 'paypal',
                        amount: orderData.total,
                        timestamp: new Date().toISOString()
                    });
                } else {
                    reject(new Error('Payment cancelled'));
                }
            });
        });
    }

    async processCashPayment(orderData) {
        // Cash on delivery
        return Promise.resolve({
            success: true,
            transactionId: this.generateTransactionId(),
            method: 'cash',
            amount: orderData.total,
            timestamp: new Date().toISOString(),
            note: 'Cash on Delivery'
        });
    }

    showStripePaymentModal(orderData, callback) {
        const modal = document.getElementById('paymentModal');
        const modalContent = document.getElementById('paymentModalContent');

        modalContent.innerHTML = `
            <h2>💳 Payment Details</h2>
            <p style="margin-bottom: 2rem; color: var(--text-secondary);">
                Total Amount: <strong style="color: var(--primary-color); font-size: 1.5rem;">$${orderData.total.toFixed(2)}</strong>
            </p>

            <form id="stripePaymentForm">
                <div class="form-group">
                    <label>Card Number</label>
                    <input type="text" id="cardNumber" placeholder="1234 5678 9012 3456" maxlength="19" required autocomplete="cc-number">
                </div>

                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                    <div class="form-group">
                        <label>Expiry Date</label>
                        <input type="text" id="expiryDate" placeholder="MM/YY" maxlength="5" required autocomplete="cc-exp">
                    </div>
                    <div class="form-group">
                        <label>CVV</label>
                        <input type="text" id="cvv" placeholder="123" maxlength="4" required autocomplete="cc-csc">
                    </div>
                </div>

                <div class="form-group">
                    <label>Cardholder Name</label>
                    <input type="text" id="cardholderName" placeholder="John Doe" required autocomplete="cc-name">
                </div>

                <div style="display: flex; gap: 1rem; margin-top: 2rem;">
                    <button type="submit" class="btn btn-primary" style="flex: 1;">
                        Pay $${orderData.total.toFixed(2)}
                    </button>
                    <button type="button" class="btn btn-secondary" onclick="paymentManager.cancelPayment()">
                        Cancel
                    </button>
                </div>
            </form>

            <div style="margin-top: 1.5rem; padding: 1rem; background: var(--bg-secondary); border-radius: var(--radius-md); font-size: 0.875rem;">
                <p style="color: var(--text-secondary); margin: 0;">
                    🔒 <strong>Secure Payment:</strong> This is a demo. In production, we use Stripe's secure payment processing.
                </p>
            </div>
        `;

        // Format card number input
        const cardNumberInput = document.getElementById('cardNumber');
        cardNumberInput.addEventListener('input', (e) => {
            let value = e.target.value.replace(/\s/g, '');
            let formattedValue = value.match(/.{1,4}/g)?.join(' ') || value;
            e.target.value = formattedValue;
        });

        // Format expiry date
        const expiryInput = document.getElementById('expiryDate');
        expiryInput.addEventListener('input', (e) => {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length >= 2) {
                value = value.slice(0, 2) + '/' + value.slice(2, 4);
            }
            e.target.value = value;
        });

        // Only allow numbers in CVV
        const cvvInput = document.getElementById('cvv');
        cvvInput.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/\D/g, '');
        });

        // Handle form submission
        document.getElementById('stripePaymentForm').addEventListener('submit', (e) => {
            e.preventDefault();

            // Validate card number (basic validation)
            const cardNumber = document.getElementById('cardNumber').value.replace(/\s/g, '');
            const expiryDate = document.getElementById('expiryDate').value;
            const cvv = document.getElementById('cvv').value;

            if (cardNumber.length < 13 || cardNumber.length > 19) {
                toastManager.error('Invalid card number');
                return;
            }

            if (!expiryDate.match(/^\d{2}\/\d{2}$/)) {
                toastManager.error('Invalid expiry date');
                return;
            }

            if (cvv.length < 3 || cvv.length > 4) {
                toastManager.error('Invalid CVV');
                return;
            }

            // Simulate payment processing
            const btn = e.target.querySelector('button[type="submit"]');
            btn.disabled = true;
            btn.textContent = 'Processing...';

            setTimeout(() => {
                modal.style.display = 'none';
                callback({ success: true });
            }, 2000);
        });

        modal.style.display = 'block';
    }

    showPayPalPaymentModal(orderData, callback) {
        const modal = document.getElementById('paymentModal');
        const modalContent = document.getElementById('paymentModalContent');

        modalContent.innerHTML = `
            <h2>💙 PayPal Payment</h2>
            <p style="margin-bottom: 2rem; color: var(--text-secondary);">
                Total Amount: <strong style="color: var(--primary-color); font-size: 1.5rem;">$${orderData.total.toFixed(2)}</strong>
            </p>

            <div style="text-align: center; padding: 2rem;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">💙</div>
                <p style="font-size: 1.125rem; margin-bottom: 2rem;">
                    You will be redirected to PayPal to complete your payment
                </p>

                <div style="display: flex; gap: 1rem; justify-content: center;">
                    <button class="btn btn-primary" onclick="paymentManager.simulatePayPalPayment(${orderData.total})">
                        Continue to PayPal
                    </button>
                    <button class="btn btn-secondary" onclick="paymentManager.cancelPayment()">
                        Cancel
                    </button>
                </div>
            </div>

            <div style="margin-top: 1.5rem; padding: 1rem; background: var(--bg-secondary); border-radius: var(--radius-md); font-size: 0.875rem;">
                <p style="color: var(--text-secondary); margin: 0;">
                    🔒 <strong>Secure Payment:</strong> This is a demo. In production, PayPal handles the payment securely.
                </p>
            </div>
        `;

        this.paypalCallback = callback;
        modal.style.display = 'block';
    }

    simulatePayPalPayment(total) {
        toastManager.info('Redirecting to PayPal...');

        setTimeout(() => {
            toastManager.success('PayPal payment successful!');
            document.getElementById('paymentModal').style.display = 'none';
            if (this.paypalCallback) {
                this.paypalCallback({ success: true });
            }
        }, 2000);
    }

    showPaymentMethodSelector(orderData, callback) {
        const modal = document.getElementById('paymentModal');
        const modalContent = document.getElementById('paymentModalContent');

        modalContent.innerHTML = `
            <h2>💰 Select Payment Method</h2>
            <p style="margin-bottom: 2rem; color: var(--text-secondary); text-align: center;">
                Total Amount: <strong style="color: var(--primary-color); font-size: 1.5rem;">$${orderData.total.toFixed(2)}</strong>
            </p>

            <div class="payment-methods">
                <div class="payment-method-card" onclick="paymentManager.selectPaymentMethod('stripe', ${JSON.stringify(orderData).replace(/"/g, '&quot;')})">
                    <div class="payment-icon">💳</div>
                    <h3>Credit/Debit Card</h3>
                    <p>Pay securely with your card via Stripe</p>
                </div>

                <div class="payment-method-card" onclick="paymentManager.selectPaymentMethod('paypal', ${JSON.stringify(orderData).replace(/"/g, '&quot;')})">
                    <div class="payment-icon">💙</div>
                    <h3>PayPal</h3>
                    <p>Fast and secure PayPal payment</p>
                </div>

                <div class="payment-method-card" onclick="paymentManager.selectPaymentMethod('cash', ${JSON.stringify(orderData).replace(/"/g, '&quot;')})">
                    <div class="payment-icon">💵</div>
                    <h3>Cash on Delivery</h3>
                    <p>Pay when you receive your order</p>
                </div>
            </div>

            <button class="btn btn-secondary btn-block" style="margin-top: 1.5rem;" onclick="paymentManager.cancelPayment()">
                Cancel
            </button>
        `;

        this.paymentCallback = callback;
        modal.style.display = 'block';
    }

    async selectPaymentMethod(method, orderData) {
        this.paymentMethod = method;

        try {
            const result = await this.processPayment(orderData);
            if (this.paymentCallback) {
                this.paymentCallback(result);
            }
        } catch (error) {
            console.error('Payment error:', error);
            toastManager.error(error.message || 'Payment failed');
            document.getElementById('paymentModal').style.display = 'none';
        }
    }

    cancelPayment() {
        document.getElementById('paymentModal').style.display = 'none';
        toastManager.info('Payment cancelled');
    }

    generateTransactionId() {
        return 'TXN' + Date.now() + Math.random().toString(36).substr(2, 9).toUpperCase();
    }
}

// Create global payment manager instance
const paymentManager = new PaymentManager();
window.paymentManager = paymentManager;
