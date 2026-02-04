// Main JavaScript file for Business Dashboard

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Set current year in footer
    document.querySelectorAll('.current-year').forEach(function(el) {
        el.textContent = new Date().getFullYear();
    });
    
    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
    
    // Add active class to current nav item
    var currentPath = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(function(link) {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
    
    // Format currency display
    formatCurrencyOnPage();
});

// Format all currency elements on page
function formatCurrencyOnPage() {
    document.querySelectorAll('.currency-amount').forEach(function(el) {
        var amount = parseFloat(el.textContent.replace(/[^0-9.-]+/g, ""));
        if (!isNaN(amount)) {
            el.textContent = formatCurrency(amount);
        }
    });
}

// Format currency with MWK prefix
function formatCurrency(amount) {
    if (typeof amount !== 'number') {
        amount = parseFloat(amount);
    }
    
    if (isNaN(amount)) {
        return 'MWK 0.00';
    }
    
    // Format with thousands separator and 2 decimal places
    return 'MWK ' + amount.toLocaleString('en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
}

// Format date to local string
function formatDate(dateString) {
    var date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Format date with time
function formatDateTime(dateString) {
    var date = new Date(dateString);
    return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Show loading spinner
function showLoading(element) {
    var originalContent = element.innerHTML;
    element.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...';
    element.disabled = true;
    return originalContent;
}

// Hide loading spinner
function hideLoading(element, originalContent) {
    element.innerHTML = originalContent;
    element.disabled = false;
}

// Show success message
function showSuccess(message, container = document.body) {
    var alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-success alert-dismissible fade show';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    container.prepend(alertDiv);
    
    setTimeout(function() {
        var bsAlert = new bootstrap.Alert(alertDiv);
        bsAlert.close();
    }, 5000);
}

// Show error message
function showError(message, container = document.body) {
    var alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-danger alert-dismissible fade show';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    container.prepend(alertDiv);
    
    setTimeout(function() {
        var bsAlert = new bootstrap.Alert(alertDiv);
        bsAlert.close();
    }, 5000);
}

// Show warning message
function showWarning(message, container = document.body) {
    var alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-warning alert-dismissible fade show';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    container.prepend(alertDiv);
    
    setTimeout(function() {
        var bsAlert = new bootstrap.Alert(alertDiv);
        bsAlert.close();
    }, 5000);
}

// Confirm dialog
function confirmDialog(message, onConfirm) {
    if (confirm(message)) {
        if (typeof onConfirm === 'function') {
            onConfirm();
        }
        return true;
    }
    return false;
}

// Copy text to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        showSuccess('Copied to clipboard!');
    }).catch(function(err) {
        console.error('Failed to copy: ', err);
        showError('Failed to copy to clipboard');
    });
}

// Download file
function downloadFile(filename, content, type = 'text/plain') {
    var element = document.createElement('a');
    element.setAttribute('href', 'data:' + type + ';charset=utf-8,' + encodeURIComponent(content));
    element.setAttribute('download', filename);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}

// Debounce function for search inputs
function debounce(func, wait) {
    var timeout;
    return function executedFunction() {
        var context = this;
        var args = arguments;
        var later = function() {
            timeout = null;
            func.apply(context, args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Truncate text with ellipsis
function truncateText(text, maxLength) {
    if (text.length <= maxLength) {
        return text;
    }
    return text.substring(0, maxLength) + '...';
}

// Calculate percentage
function calculatePercentage(part, total) {
    if (total === 0) return 0;
    return ((part / total) * 100).toFixed(2);
}

// Validate email
function validateEmail(email) {
    var re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Validate phone number (simple validation)
function validatePhone(phone) {
    var re = /^[\+]?[0-9]{10,15}$/;
    return re.test(phone.replace(/\s/g, ''));
}

// Format number with commas
function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// Calculate profit margin
function calculateProfitMargin(cost, price) {
    if (price === 0) return 0;
    return ((price - cost) / price * 100).toFixed(2);
}

// Toggle visibility of element
function toggleVisibility(elementId) {
    var element = document.getElementById(elementId);
    if (element) {
        element.classList.toggle('d-none');
    }
}

// Make AJAX request
function makeRequest(url, method = 'GET', data = null) {
    return fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: data ? JSON.stringify(data) : null
    })
    .then(function(response) {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .catch(function(error) {
        console.error('Request failed:', error);
        showError('Request failed: ' + error.message);
        throw error;
    });
}

// Export data to CSV
function exportToCSV(data, filename) {
    var csv = '';
    
    // Add headers
    var headers = Object.keys(data[0]);
    csv += headers.join(',') + '\n';
    
    // Add rows
    data.forEach(function(row) {
        var values = headers.map(function(header) {
            return '"' + (row[header] || '').toString().replace(/"/g, '""') + '"';
        });
        csv += values.join(',') + '\n';
    });
    
    downloadFile(filename + '.csv', csv, 'text/csv');
}

// Theme switcher (light/dark mode)
function toggleTheme() {
    var html = document.documentElement;
    var currentTheme = html.getAttribute('data-bs-theme');
    var newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    html.setAttribute('data-bs-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    
    showSuccess('Switched to ' + newTheme + ' theme');
}

// Check and apply saved theme
function applySavedTheme() {
    var savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        document.documentElement.setAttribute('data-bs-theme', savedTheme);
    }
}

// Initialize theme on page load
applySavedTheme();

// Ensure footer with developer details is always present and correct
(function() {
    const desiredFooterHTML = `
        <div class="container">
            <p class="mb-0">
                <small>
                    Business Dashboard &copy; ${new Date().getFullYear()} | 
                    Developed by Gomezgani Chirwa - MUBAS MIS Year 3 |
                    <a href="https://github.com/gomezgani/business-intelligence-dashboard" class="text-decoration-none">
                        <i class="bi bi-github"></i> View on GitHub
                    </a>
                </small>
            </p>
        </div>
    `;
    
    let footer = document.querySelector('footer');
    if (footer) {
        footer.className = 'bg-light text-center py-3 mt-5 border-top';
        footer.innerHTML = desiredFooterHTML;
    } else {
        footer = document.createElement('footer');
        footer.className = 'bg-light text-center py-3 mt-5 border-top';
        footer.innerHTML = desiredFooterHTML;
        document.body.appendChild(footer);
    }
})();