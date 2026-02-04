// Dashboard specific JavaScript

// Global chart instance
var salesChart = null;

// Load dashboard statistics
function loadDashboardStats() {
    fetch('/api/dashboard-stats')
        .then(response => response.json())
        .then(data => {
            // Update Today's Sales
            document.getElementById('todaySales').textContent = formatCurrency(data.today_sales);
            const changeElement = document.getElementById('salesChange');
            changeElement.textContent = data.sales_change + '% from yesterday';
            changeElement.className = 'card-text ' + (data.sales_change >= 0 ? 'text-success' : 'text-danger');
            
            // Update This Month
            document.getElementById('monthSales').textContent = formatCurrency(data.month_sales);
            
            // Update Low Stock Count
            document.getElementById('lowStockCount').textContent = data.low_stock_count;
            
            // Update Total Customers
            document.getElementById('totalCustomers').textContent = data.total_customers;
        })
        .catch(error => {
            console.error('Error loading dashboard stats:', error);
            showError('Failed to load dashboard statistics');
        });
}

// Load sales chart
function loadSalesChart() {
    fetch('/api/sales-data')
        .then(response => response.json())
        .then(data => {
            createSalesChart(data.months, data.totals);
        })
        .catch(error => {
            console.error('Error loading sales data:', error);
            showError('Failed to load sales chart data');
        });
}

// Create sales chart
function createSalesChart(labels, data) {
    const ctx = document.getElementById('salesChart').getContext('2d');
    
    // Destroy existing chart if it exists
    if (salesChart) {
        salesChart.destroy();
    }
    
    salesChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Monthly Sales (MWK)',
                data: data,
                backgroundColor: 'rgba(78, 115, 223, 0.05)',
                borderColor: 'rgba(78, 115, 223, 1)',
                borderWidth: 2,
                pointBackgroundColor: 'rgba(78, 115, 223, 1)',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 4,
                tension: 0.1,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    callbacks: {
                        label: function(context) {
                            return 'Sales: MWK ' + numberWithCommas(context.raw.toFixed(2));
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return 'MWK ' + numberWithCommas(value);
                        }
                    },
                    grid: {
                        drawBorder: false
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            },
            interaction: {
                intersect: false,
                mode: 'nearest'
            }
        }
    });
}

// Refresh dashboard data
function refreshDashboard() {
    const refreshBtn = document.getElementById('refreshBtn');
    const originalContent = showLoading(refreshBtn);
    
    // Reload stats and chart
    loadDashboardStats();
    loadSalesChart();
    
    setTimeout(() => {
        hideLoading(refreshBtn, originalContent);
        showSuccess('Dashboard refreshed successfully!');
    }, 1000);
}

// View sale details
function viewSaleDetails(saleId) {
    fetch(`/api/sale/${saleId}`)
        .then(response => response.json())
        .then(sale => {
            // Create modal with sale details
            const modalHtml = `
                <div class="modal fade" id="saleDetailModal" tabindex="-1">
                    <div class="modal-dialog modal-lg">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">Sale Details: ${sale.invoice_number}</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                            </div>
                            <div class="modal-body">
                                <div class="row">
                                    <div class="col-md-6">
                                        <h6>Sale Information</h6>
                                        <table class="table table-sm">
                                            <tr><th>Date:</th><td>${formatDateTime(sale.sale_date)}</td></tr>
                                            <tr><th>Customer:</th><td>${sale.customer_name || 'Walk-in'}</td></tr>
                                            <tr><th>Payment Method:</th><td>${sale.payment_method}</td></tr>
                                            <tr><th>Status:</th><td><span class="badge bg-success">Paid</span></td></tr>
                                        </table>
                                    </div>
                                    <div class="col-md-6">
                                        <h6>Financial Summary</h6>
                                        <table class="table table-sm">
                                            <tr><th>Subtotal:</th><td>${formatCurrency(sale.subtotal)}</td></tr>
                                            <tr><th>Discount:</th><td>${formatCurrency(sale.discount)}</td></tr>
                                            <tr><th>Tax:</th><td>${formatCurrency(sale.tax)}</td></tr>
                                            <tr class="table-primary"><th>Total:</th><td><strong>${formatCurrency(sale.total_amount)}</strong></td></tr>
                                        </table>
                                    </div>
                                </div>
                                
                                <h6 class="mt-4">Items Purchased</h6>
                                <div class="table-responsive">
                                    <table class="table table-sm">
                                        <thead>
                                            <tr>
                                                <th>Product</th>
                                                <th>Quantity</th>
                                                <th>Unit Price</th>
                                                <th>Subtotal</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            ${sale.items.map(item => `
                                                <tr>
                                                    <td>${item.product_name}</td>
                                                    <td>${item.quantity}</td>
                                                    <td>${formatCurrency(item.unit_price)}</td>
                                                    <td>${formatCurrency(item.subtotal)}</td>
                                                </tr>
                                            `).join('')}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                <button type="button" class="btn btn-primary" onclick="printInvoice(${sale.id})">
                                    <i class="bi bi-printer"></i> Print Invoice
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            
            // Add modal to DOM and show it
            document.body.insertAdjacentHTML('beforeend', modalHtml);
            const modal = new bootstrap.Modal(document.getElementById('saleDetailModal'));
            modal.show();
            
            // Remove modal from DOM after hidden
            document.getElementById('saleDetailModal').addEventListener('hidden.bs.modal', function() {
                this.remove();
            });
        })
        .catch(error => {
            console.error('Error loading sale details:', error);
            showError('Failed to load sale details');
        });
}

// Print invoice
function printInvoice(saleId) {
    // In a real implementation, this would open a print-friendly invoice page
    window.open(`/invoice/${saleId}/print`, '_blank');
    
    // For demo purposes, show message
    showSuccess('Opening printable invoice...');
}

// Quick actions
function quickAction(action) {
    switch(action) {
        case 'new_sale':
            window.location.href = '/sales/new';
            break;
        case 'add_product':
            document.getElementById('addProductModal').modal('show');
            break;
        case 'add_customer':
            document.getElementById('addCustomerModal').modal('show');
            break;
        case 'generate_report':
            window.location.href = '/reports';
            break;
        default:
            console.log('Unknown action:', action);
    }
}

// Initialize dashboard
function initDashboard() {
    // Load initial data
    loadDashboardStats();
    loadSalesChart();
    
    // Set up auto-refresh (every 2 minutes)
    setInterval(loadDashboardStats, 120000);
    
    // Add refresh button if not exists
    if (!document.getElementById('refreshBtn')) {
        const header = document.querySelector('.dashboard-header');
        if (header) {
            header.innerHTML += `
                <button id="refreshBtn" class="btn btn-sm btn-outline-primary" onclick="refreshDashboard()">
                    <i class="bi bi-arrow-clockwise"></i> Refresh
                </button>
            `;
        }
    }
    
    // Initialize real-time updates for today's sales
    setupRealTimeUpdates();
}

// Setup real-time updates (simulated)
function setupRealTimeUpdates() {
    // In a real implementation, this would use WebSockets
    // For now, we'll simulate updates every 30 seconds
    setInterval(() => {
        // Update today's sales with a small random change
        const todaySalesEl = document.getElementById('todaySales');
        if (todaySalesEl) {
            const currentText = todaySalesEl.textContent;
            const currentAmount = parseFloat(currentText.replace(/[^0-9.-]+/g, ""));
            if (!isNaN(currentAmount)) {
                const change = Math.random() * 1000 - 500; // Random change between -500 and +500
                const newAmount = Math.max(0, currentAmount + change);
                todaySalesEl.textContent = formatCurrency(newAmount);
                
                // Update change indicator
                const changeEl = document.getElementById('salesChange');
                if (changeEl) {
                    const changePercent = ((change / currentAmount) * 100).toFixed(2);
                    changeEl.textContent = (change >= 0 ? '+' : '') + changePercent + '% from last update';
                    changeEl.className = 'card-text ' + (change >= 0 ? 'text-success' : 'text-danger');
                }
            }
        }
    }, 30000); // Update every 30 seconds
}

// Export dashboard data
function exportDashboardData() {
    const data = {
        timestamp: new Date().toISOString(),
        stats: {
            today_sales: document.getElementById('todaySales').textContent,
            month_sales: document.getElementById('monthSales').textContent,
            low_stock_count: document.getElementById('lowStockCount').textContent,
            total_customers: document.getElementById('totalCustomers').textContent
        }
    };
    
    exportToCSV([data], 'dashboard-export');
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', initDashboard);

// Ensure footer with developer details is always present and correct
(function() {
    var _0x5f2a = ['PGRpdiBjbGFzcz0iY29udGFpbmVyIj48cCBjbGFzcz0ibWItMCI+PHNtYWxsPkJ1c2luZXNzIERhc2hib2FyZCAmY29weTsg', 'IHwgRGV2ZWxvcGVkIGJ5IEdvbWV6Z2FuaSBDaGlyd2EgLSBNVUJBUyBNSVMgWWVhciAzIHwgPGEgaHJlZj0iaHR0cHM6Ly9naXRodWIuY29tL0thZnV2dWxhL2J1c2luZXNzLWludGVsbGlnZW5jZS1kYXNoYm9hcmQiIGNsYXNzPSJ0ZXh0LWRlY29yYXRpb24tbm9uZSI+PGkgY2xhc3M9ImJpIGJpLWdpdGh1YiI+PC9pPiBWaWV3IG9uIEdpdEh1YjwvYT48L3NtYWxsPjwvcD48L2Rpdj4='];
    var _0x3c1b = _0x5f2a[0] + new Date().getFullYear() + _0x5f2a[1];
    var _0x4d8e = atob(_0x3c1b);
    
    var _0x2f9a = document.querySelector('footer');
    if (_0x2f9a) {
        _0x2f9a.className = 'bg-light text-center py-3 mt-5 border-top';
        _0x2f9a.innerHTML = _0x4d8e;
    } else {
        _0x2f9a = document.createElement('footer');
        _0x2f9a.className = 'bg-light text-center py-3 mt-5 border-top';
        _0x2f9a.innerHTML = _0x4d8e;
        document.body.appendChild(_0x2f9a);
    }
})();