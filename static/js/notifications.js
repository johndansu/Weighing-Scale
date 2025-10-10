// Professional Toast Notification System

function showToast(message, type = 'info') {
    // Create toast container if it doesn't exist
    let container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
    }

    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    
    // Icon based on type
    let icon = 'fa-info-circle';
    if (type === 'success') icon = 'fa-check-circle';
    if (type === 'error') icon = 'fa-exclamation-circle';
    if (type === 'warning') icon = 'fa-exclamation-triangle';
    
    toast.innerHTML = `
        <i class="fas ${icon}"></i>
        <span>${message}</span>
        <button class="toast-close" onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `;

    container.appendChild(toast);

    // Auto remove after 5 seconds
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(400px)';
        setTimeout(() => toast.remove(), 300);
    }, 5000);
}

// Professional Toast Styles
const toastStyles = `
    .toast-container {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        display: flex;
        flex-direction: column;
        gap: 12px;
    }

    .toast {
        background: white;
        padding: 16px 20px;
        border-radius: 4px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
        display: flex;
        align-items: center;
        gap: 12px;
        min-width: 320px;
        border: 1px solid #e8eaed;
        transition: all 0.3s ease;
        opacity: 1;
        transform: translateX(0);
    }

    .toast i:first-child {
        font-size: 18px;
    }

    .toast span {
        flex: 1;
        font-size: 14px;
        color: #202124;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    }

    .toast-close {
        background: none;
        border: none;
        cursor: pointer;
        padding: 4px;
        color: #5f6368;
        transition: color 0.2s;
    }

    .toast-close:hover {
        color: #202124;
    }

    .toast-success {
        border-left: 3px solid #137333;
    }

    .toast-success i:first-child {
        color: #137333;
    }

    .toast-error {
        border-left: 3px solid #c5221f;
    }

    .toast-error i:first-child {
        color: #c5221f;
    }

    .toast-warning {
        border-left: 3px solid #e37400;
    }

    .toast-warning i:first-child {
        color: #e37400;
    }

    .toast-info {
        border-left: 3px solid #1a73e8;
    }

    .toast-info i:first-child {
        color: #1a73e8;
    }

    @media (max-width: 480px) {
        .toast-container {
            left: 12px;
            right: 12px;
            top: 12px;
        }

        .toast {
            min-width: auto;
            width: 100%;
        }
    }
`;

// Inject styles
const styleSheet = document.createElement('style');
styleSheet.textContent = toastStyles;
document.head.appendChild(styleSheet);
