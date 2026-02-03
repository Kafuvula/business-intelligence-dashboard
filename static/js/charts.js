// Charts and data visualization utilities

// Global chart instances storage
window.chartInstances = {};

// Chart colors palette
const chartColors = {
    primary: '#4e73df',
    success: '#1cc88a',
    info: '#36b9cc',
    warning: '#f6c23e',
    danger: '#e74a3b',
    secondary: '#858796',
    dark: '#5a5c69',
    light: '#f8f9fc'
};

// Extended palette for multiple datasets
const extendedPalette = [
    '#4e73df', '#1cc88a', '#36b9cc', '#f6c23e', '#e74a3b',
    '#858796', '#6f42c1', '#20c9a6', '#fd7e14', '#e83e8c'
];

// Create bar chart
function createBarChart(canvasId, data, options = {}) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    
    const defaultOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'top',
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                ticks: {
                    callback: function(value) {
                        return numberWithCommas(value);
                    }
                }
            }
        }
    };
    
    const mergedOptions = mergeOptions(defaultOptions, options);
    
    const chart = new Chart(ctx, {
        type: 'bar',
        data: data,
        options: mergedOptions
    });
    
    window.chartInstances[canvasId] = chart;
    return chart;
}

// Create line chart
function createLineChart(canvasId, data, options = {}) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    
    const defaultOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'top',
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                ticks: {
                    callback: function(value) {
                        return numberWithCommas(value);
                    }
                }
            }
        },
        elements: {
            line: {
                tension: 0.1
            }
        }
    };
    
    const mergedOptions = mergeOptions(defaultOptions, options);
    
    const chart = new Chart(ctx, {
        type: 'line',
        data: data,
        options: mergedOptions
    });
    
    window.chartInstances[canvasId] = chart;
    return chart;
}

// Create pie/doughnut chart
function createPieChart(canvasId, data, options = {}) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    
    const defaultOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'right',
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        const label = context.label || '';
                        const value = context.raw || 0;
                        const total = context.dataset.data.reduce((a, b) => a + b, 0);
                        const percentage = Math.round((value / total) * 100);
                        return `${label}: ${numberWithCommas(value)} (${percentage}%)`;
                    }
                }
            }
        }
    };
    
    const mergedOptions = mergeOptions(defaultOptions, options);
    
    const chart = new Chart(ctx, {
        type: 'doughnut',
        data: data,
        options: mergedOptions
    });
    
    window.chartInstances[canvasId] = chart;
    return chart;
}

// Create sales trend chart
function createSalesTrendChart(canvasId, labels, datasets) {
    const data = {
        labels: labels,
        datasets: datasets.map((dataset, index) => ({
            label: dataset.label,
            data: dataset.data,
            borderColor: extendedPalette[index % extendedPalette.length],
            backgroundColor: hexToRGBA(extendedPalette[index % extendedPalette.length], 0.1),
            borderWidth: 2,
            fill: true,
            tension: 0.1
        }))
    };
    
    const options = {
        scales: {
            y: {
                beginAtZero: true,
                ticks: {
                    callback: function(value) {
                        return 'MWK ' + numberWithCommas(value);
                    }
                }
            }
        },
        plugins: {
            tooltip: {
                callbacks: {
                    label: function(context) {
                        return context.dataset.label + ': MWK ' + numberWithCommas(context.raw);
                    }
                }
            }
        }
    };
    
    return createLineChart(canvasId, data, options);
}

// Create product performance chart
function createProductPerformanceChart(canvasId, products, salesData) {
    const sortedData = products.map((product, index) => ({
        product: product,
        sales: salesData[index] || 0
    })).sort((a, b) => b.sales - a.sales).slice(0, 10); // Top 10 products
    
    const data = {
        labels: sortedData.map(item => item.product),
        datasets: [{
            label: 'Sales Revenue',
            data: sortedData.map(item => item.sales),
            backgroundColor: extendedPalette.slice(0, 10),
            borderColor: extendedPalette.slice(0, 10).map(color => darkenColor(color, 20)),
            borderWidth: 1
        }]
    };
    
    const options = {
        indexAxis: 'y', // Horizontal bar chart
        scales: {
            x: {
                beginAtZero: true,
                ticks: {
                    callback: function(value) {
                        return 'MWK ' + numberWithCommas(value);
                    }
                }
            }
        },
        plugins: {
            legend: {
                display: false
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        return 'Sales: MWK ' + numberWithCommas(context.raw);
                    }
                }
            }
        }
    };
    
    return createBarChart(canvasId, data, options);
}

// Create customer segmentation chart
function createCustomerSegmentationChart(canvasId, segments) {
    const data = {
        labels: segments.map(segment => segment.label),
        datasets: [{
            data: segments.map(segment => segment.value),
            backgroundColor: segments.map((_, index) => extendedPalette[index % extendedPalette.length]),
            borderColor: segments.map((_, index) => darkenColor(extendedPalette[index % extendedPalette.length], 20)),
            borderWidth: 2
        }]
    };
    
    const options = {
        plugins: {
            tooltip: {
                callbacks: {
                    label: function(context) {
                        const value = context.raw;
                        const total = context.dataset.data.reduce((a, b) => a + b, 0);
                        const percentage = ((value / total) * 100).toFixed(1);
                        return `${context.label}: ${value} customers (${percentage}%)`;
                    }
                }
            }
        }
    };
    
    return createPieChart(canvasId, data, options);
}

// Create monthly comparison chart
function createMonthlyComparisonChart(canvasId, currentMonthData, previousMonthData, labels) {
    const data = {
        labels: labels,
        datasets: [
            {
                label: 'Current Month',
                data: currentMonthData,
                backgroundColor: hexToRGBA(chartColors.primary, 0.7),
                borderColor: chartColors.primary,
                borderWidth: 2
            },
            {
                label: 'Previous Month',
                data: previousMonthData,
                backgroundColor: hexToRGBA(chartColors.secondary, 0.7),
                borderColor: chartColors.secondary,
                borderWidth: 2
            }
        ]
    };
    
    const options = {
        scales: {
            y: {
                beginAtZero: true,
                ticks: {
                    callback: function(value) {
                        return 'MWK ' + numberWithCommas(value);
                    }
                }
            }
        },
        plugins: {
            tooltip: {
                callbacks: {
                    label: function(context) {
                        return context.dataset.label + ': MWK ' + numberWithCommas(context.raw);
                    }
                }
            }
        }
    };
    
    return createBarChart(canvasId, data, options);
}

// Update chart data
function updateChartData(chartId, newData, newLabels = null) {
    const chart = window.chartInstances[chartId];
    if (!chart) {
        console.error(`Chart ${chartId} not found`);
        return;
    }
    
    chart.data.datasets.forEach((dataset, index) => {
        if (newData[index]) {
            dataset.data = newData[index];
        }
    });
    
    if (newLabels) {
        chart.data.labels = newLabels;
    }
    
    chart.update();
}

// Destroy chart
function destroyChart(chartId) {
    const chart = window.chartInstances[chartId];
    if (chart) {
        chart.destroy();
        delete window.chartInstances[chartId];
    }
}

// Export chart as image
function exportChartAsImage(chartId, filename = 'chart') {
    const chart = window.chartInstances[chartId];
    if (!chart) {
        showError('Chart not found');
        return;
    }
    
    const link = document.createElement('a');
    link.download = filename + '.png';
    link.href = chart.toBase64Image();
    link.click();
}

// Utility function to merge options
function mergeOptions(defaultOptions, customOptions) {
    return deepMerge(defaultOptions, customOptions);
}

// Deep merge objects
function deepMerge(target, source) {
    const output = Object.assign({}, target);
    
    if (isObject(target) && isObject(source)) {
        Object.keys(source).forEach(key => {
            if (isObject(source[key])) {
                if (!(key in target)) {
                    Object.assign(output, { [key]: source[key] });
                } else {
                    output[key] = deepMerge(target[key], source[key]);
                }
            } else {
                Object.assign(output, { [key]: source[key] });
            }
        });
    }
    
    return output;
}

// Check if value is an object
function isObject(item) {
    return (item && typeof item === 'object' && !Array.isArray(item));
}

// Convert hex to RGBA
function hexToRGBA(hex, alpha = 1) {
    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);
    
    return `rgba(${r}, ${g}, ${b}, ${alpha})`;
}

// Darken color
function darkenColor(hex, percent) {
    // Remove # if present
    hex = hex.replace(/^#/, '');
    
    // Parse r, g, b
    let r = parseInt(hex.substr(0, 2), 16);
    let g = parseInt(hex.substr(2, 2), 16);
    let b = parseInt(hex.substr(4, 2), 16);
    
    // Darken each component
    r = Math.max(0, Math.floor(r * (100 - percent) / 100));
    g = Math.max(0, Math.floor(g * (100 - percent) / 100));
    b = Math.max(0, Math.floor(b * (100 - percent) / 100));
    
    // Convert back to hex
    return `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`;
}

// Generate random data for demo charts
function generateDemoData(count = 7, min = 100, max = 1000) {
    return Array.from({ length: count }, () => 
        Math.floor(Math.random() * (max - min + 1)) + min
    );
}

// Initialize demo charts on page
function initDemoCharts() {
    // Only initialize if we're on a page that needs charts
    if (!document.querySelector('.chart-container')) {
        return;
    }
    
    // Check for specific chart containers and create demo charts
    if (document.getElementById('demoSalesChart')) {
        const labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'];
        const salesData = generateDemoData(7, 5000, 20000);
        createSalesTrendChart('demoSalesChart', labels, [{
            label: 'Monthly Sales',
            data: salesData
        }]);
    }
    
    if (document.getElementById('demoProductChart')) {
        const products = ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones', 'Webcam', 'Tablet'];
        const productSales = generateDemoData(7, 1000, 10000);
        createProductPerformanceChart('demoProductChart', products, productSales);
    }
    
    if (document.getElementById('demoCustomerChart')) {
        const segments = [
            { label: 'New Customers', value: 45 },
            { label: 'Regular Customers', value: 120 },
            { label: 'VIP Customers', value: 25 },
            { label: 'Inactive Customers', value: 60 }
        ];
        createCustomerSegmentationChart('demoCustomerChart', segments);
    }
}

// Initialize charts when DOM is loaded
document.addEventListener('DOMContentLoaded', initDemoCharts);