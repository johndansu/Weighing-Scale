// Ensure this file is named chart.js and placed under static/js in your Django project

// Line Graph: Weight Trend Over Time
const lineCtx = document.getElementById('line-chart').getContext('2d');
const lineChart = new Chart(lineCtx, {
    type: 'line',
    data: {
        labels: ['Second 1', 'Second 2', 'Second 3', 'Minute 1', 'Hour 1', 'Day 1', 'Year 1'],
        datasets: [{
            label: 'Weight Over Time',
            data: [12, 15, 10, 18, 25, 30, 50], // Sample data
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 2,
            fill: true,
            tension: 0.4 // Smooth the line
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Weight (kg)'
                }
            },
            x: {
                title: {
                    display: true,
                    text: 'Time'
                }
            }
        }
    }
});

// Bar Graph: Weight by Category
const barCtx = document.getElementById('bar-chart').getContext('2d');
const barChart = new Chart(barCtx, {
    type: 'bar',
    data: {
        labels: ['Category A', 'Category B', 'Category C'],
        datasets: [{
            label: 'Weights (kg)',
            data: [30, 50, 70], // Sample data
            backgroundColor: [
                'rgba(255, 99, 132, 0.6)',
                'rgba(54, 162, 235, 0.6)',
                'rgba(255, 206, 86, 0.6)',
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
            ],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Weight (kg)'
                }
            },
            x: {
                title: {
                    display: true,
                    text: 'Categories'
                }
            }
        }
    }
});

// Pie Chart: Weight Distribution
const pieCtx = document.getElementById('pie-chart').getContext('2d');
const pieChart = new Chart(pieCtx, {
    type: 'pie',
    data: {
        labels: ['Type A', 'Type B', 'Type C'],
        datasets: [{
            label: 'Weight Distribution (%)',
            data: [30, 50, 20], // Sample data
            backgroundColor: [
                'rgba(255, 99, 132, 0.6)',
                'rgba(54, 162, 235, 0.6)',
                'rgba(255, 206, 86, 0.6)',
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
            ],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: 'Weight Distribution by Type'
            }
        }
    }
});

// Area Graph: Cumulative Weight Over Time
const areaCtx = document.getElementById('area-chart').getContext('2d');
const areaChart = new Chart(areaCtx, {
    type: 'line',
    data: {
        labels: ['Second 1', 'Second 2', 'Second 3', 'Minute 1', 'Hour 1', 'Day 1', 'Year 1'],
        datasets: [{
            label: 'Cumulative Weight',
            data: [5, 10, 15, 25, 35, 50, 80], // Sample data
            backgroundColor: 'rgba(75, 192, 192, 0.5)',
            borderColor: 'rgba(75, 192, 192, 1)',
            fill: true,
            borderWidth: 2,
            tension: 0.4 // Smooth the line
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Cumulative Weight (kg)'
                }
            },
            x: {
                title: {
                    display: true,
                    text: 'Time'
                }
            }
        }
    }
});

// Scatter Plot: Weight vs. Time
const scatterCtx = document.getElementById('scatter-plot').getContext('2d');
const scatterChart = new Chart(scatterCtx, {
    type: 'scatter',
    data: {
        datasets: [{
            label: 'Weight vs. Time',
            data: [
                { x: 1, y: 12 },
                { x: 2, y: 15 },
                { x: 3, y: 10 },
                { x: 60, y: 25 },
                { x: 3600, y: 50 } // Sample data in seconds
            ],
            backgroundColor: 'rgba(255, 206, 86, 1)'
        }]
    },
    options: {
        responsive: true,
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Time (seconds)'
                }
            },
            y: {
                title: {
                    display: true,
                    text: 'Weight (kg)'
                }
            }
        }
    }
});

// Donut Chart: Material Composition by Weight
const donutCtx = document.getElementById('donut-chart').getContext('2d');
const donutChart = new Chart(donutCtx, {
    type: 'doughnut',
    data: {
        labels: ['Material A', 'Material B', 'Material C'],
        datasets: [{
            label: 'Material Composition',
            data: [40, 35, 25], // Sample data
            backgroundColor: [
                'rgba(255, 99, 132, 0.6)',
                'rgba(54, 162, 235, 0.6)',
                'rgba(255, 206, 86, 0.6)',
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
            ],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: 'Material Composition by Weight'
            }
        }
    }
});
