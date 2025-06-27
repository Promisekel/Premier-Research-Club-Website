/**
 * Cervical Cancer Screening Dashboard - Interactive Charts
 * 
 * This file contains all JavaScript functionality for the dashboard.
 * It creates interactive charts using Plotly.js based on the research data
 * from the Streamlit dashboard.
 * 
 * @author Premier Research Club
 * @version 1.0.0
 */

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('Dashboard initializing...');
    
    // Initialize all charts
    initializeCharts();
    
    // Add smooth scrolling for any anchor links
    addSmoothScrolling();
    
    console.log('Dashboard loaded successfully!');
});

/**
 * Initialize all dashboard charts
 */
function initializeCharts() {
    createSankeyChart();
    createOpportunityChart();
    createAgeGroupChart();
    createAwarenessChart();
    createRegressionChart();
    createBarriersChart();
    createInstitutionChart();
}

/**
 * Create Beautiful Sankey Diagram - Patient Journey Flow
 */
function createSankeyChart() {
    const data = [{
        type: "sankey",
        orientation: "h",
        node: {
            pad: 15,
            thickness: 30,
            line: {
                color: "black",
                width: 0.5
            },
            label: [
                "Total Students (354)", 
                "Aware (39.8%)", 
                "Not Aware (60.2%)", 
                "Given Opportunity", 
                "No Opportunity", 
                "Screened (14.0%)", 
                "Not Screened", 
                "Self-Initiative (12.6%)", 
                "Final Uptake (13.6%)"
            ],
            color: [
                "#3498db", "#27ae60", "#e74c3c", "#f39c12", "#95a5a6", 
                "#2ecc71", "#e67e22", "#9b59b6", "#1abc9c"
            ]
        },
        link: {
            source: [0, 0, 1, 1, 3, 3, 2, 4, 5, 7],
            target: [1, 2, 3, 4, 5, 6, 7, 7, 8, 8],
            value: [141, 213, 235, 119, 49, 186, 27, 15, 49, 15],
            color: [
                "rgba(46, 204, 113, 0.6)", "rgba(231, 76, 60, 0.6)",
                "rgba(243, 156, 18, 0.6)", "rgba(149, 165, 166, 0.6)",
                "rgba(46, 204, 113, 0.8)", "rgba(230, 126, 34, 0.6)",
                "rgba(155, 89, 182, 0.6)", "rgba(155, 89, 182, 0.6)",
                "rgba(26, 188, 156, 0.8)", "rgba(26, 188, 156, 0.8)"
            ]
        }
    }];

    const layout = {
        title: {
            text: "From 354 Students to Final Screening Uptake",
            font: { size: 18, color: 'white', family: 'Inter, sans-serif' }
        },
        font: { size: 12, color: 'white', family: 'Inter, sans-serif' },
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)',
        margin: { l: 40, r: 40, t: 60, b: 40 }
    };

    const config = {
        responsive: true,
        displayModeBar: true,
        modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d'],
        displaylogo: false
    };

    Plotly.newPlot('sankeyChart', data, layout, config);
}

/**
 * Create Opportunity vs Action Chart
 */
function createOpportunityChart() {
    const data = [{
        x: ['Total Students', 'Aware', 'Not Aware', 'Given Opportunity', 'No Opportunity', 'Screened', 'Not Screened', 'Self-Initiative', 'Final Uptake'],
        y: [354, 141, 213, 119, 235, 49, 305, 27, 49],
        type: 'bar',
        marker: {
            color: ['#3498db', '#27ae60', '#e74c3c', '#f39c12', '#95a5a6', '#2ecc71', '#e67e22', '#9b59b6', '#1abc9c'],
            line: {
                color: 'white',
                width: 2
            }
        },
        text: [354, 141, 213, 119, 235, 49, 305, 27, 49],
        textposition: 'outside',
        textfont: {
            size: 14,
            color: '#2c3e50',
            family: 'Inter, sans-serif'
        },
        hovertemplate: '<b>%{x}</b><br>' +
                      'Count: %{y}<br>' +
                      'Percentage: %{percent}<br>' +
                      '<extra></extra>'
    }];

    const layout = {
        title: {
            text: 'Critical Gap: Opportunity vs Action',
            font: {
                size: 18,
                color: '#2c3e50',
                family: 'Inter, sans-serif'
            }
        },
        xaxis: {
            title: 'Screening Category',
            titlefont: {
                size: 14,
                color: '#7f8c8d'
            },
            tickfont: {
                size: 12,
                color: '#34495e'
            }
        },
        yaxis: {
            title: 'Count',
            titlefont: {
                size: 14,
                color: '#7f8c8d'
            },
            tickfont: {
                size: 12,
                color: '#34495e'
            },
            range: [0, 400]
        },
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)',
        margin: {
            l: 60,
            r: 40,
            t: 60,
            b: 60
        },
        font: {
            family: 'Inter, sans-serif'
        }
    };

    const config = {
        responsive: true,
        displayModeBar: true,
        modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d'],
        displaylogo: false
    };

    Plotly.newPlot('opportunityChart', data, layout, config);
}

/**
 * Create Age Group Distribution Chart
 */
function createAgeGroupChart() {
    const data = [
        {
            values: [45, 32, 23],
            labels: ['18-20 years', '21-23 years', '24+ years'],
            type: 'pie',
            hole: 0.6,
            marker: {
                colors: ['#3498db', '#e74c3c', '#27ae60'],
                line: {
                    color: 'white',
                    width: 3
                }
            },
            textposition: 'outside',
            textfont: {
                size: 14,
                color: '#2c3e50',
                family: 'Inter, sans-serif'
            },
            hovertemplate: '<b>%{label}</b><br>' +
                          'Count: %{value}%<br>' +
                          'Percentage: %{percent}<br>' +
                          '<extra></extra>'
        }
    ];

    const layout = {
        title: {
            text: 'Study Population by Age Groups',
            font: {
                size: 18,
                color: '#2c3e50',
                family: 'Inter, sans-serif'
            }
        },
        annotations: [
            {
                text: '<b>354</b><br>Total<br>Participants',
                font: {
                    size: 16,
                    color: '#2c3e50',
                    family: 'Inter, sans-serif'
                },
                showarrow: false,
                x: 0.5,
                y: 0.5
            }
        ],
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)',
        margin: {
            l: 40,
            r: 40,
            t: 60,
            b: 40
        },
        font: {
            family: 'Inter, sans-serif'
        }
    };

    const config = {
        responsive: true,
        displayModeBar: true,
        modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d'],
        displaylogo: false
    };

    Plotly.newPlot('ageChart', data, layout, config);
}

/**
 * Create Awareness vs Uptake Comparison Chart
 */
function createAwarenessChart() {
    const data = [
        {
            x: ['Awareness Rate', 'Screening Uptake', 'Gap'],
            y: [39.8, 13.6, 26.2],
            type: 'bar',
            marker: {
                color: ['#f39c12', '#e74c3c', '#95a5a6'],
                line: {
                    color: 'white',
                    width: 2
                }
            },
            text: ['39.8%', '13.6%', '26.2%'],
            textposition: 'outside',
            textfont: {
                size: 16,
                color: 'white',
                family: 'Inter, sans-serif'
            },
            hovertemplate: '<b>%{x}</b><br>' +
                          'Rate: %{y}%<br>' +
                          '<extra></extra>'
        }
    ];

    const layout = {
        title: {
            text: 'Knowledge-Action Gap Analysis',
            font: {
                size: 18,
                color: '#2c3e50',
                family: 'Inter, sans-serif'
            }
        },
        xaxis: {
            title: 'Metric Category',
            titlefont: {
                size: 14,
                color: '#7f8c8d'
            },
            tickfont: {
                size: 12,
                color: '#34495e'
            }
        },
        yaxis: {
            title: 'Percentage (%)',
            titlefont: {
                size: 14,
                color: '#7f8c8d'
            },
            tickfont: {
                size: 12,
                color: '#34495e'
            },
            range: [0, 45]
        },
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)',
        margin: {
            l: 60,
            r: 40,
            t: 60,
            b: 60
        },
        font: {
            family: 'Inter, sans-serif'
        },
        annotations: [
            {
                x: 'Gap',
                y: 28,
                text: 'Critical Gap<br>to Address',
                showarrow: true,
                arrowhead: 2,
                arrowcolor: '#e74c3c',
                font: {
                    color: '#e74c3c',
                    size: 12
                }
            }
        ]
    };

    const config = {
        responsive: true,
        displayModeBar: true,
        modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d'],
        displaylogo: false
    };

    Plotly.newPlot('awarenessChart', data, layout, config);
}

/**
 * Create Modified Poisson Regression Results Chart
 */
function createRegressionChart() {
    const data = [
        {
            x: ['Age (21-23 vs 18-20)', 'Age (24+ vs 18-20)', 'Institution Type', 'Previous Education', 'Awareness Level', 'Opportunity Given'],
            y: [1.2, 0.9, 1.5, 1.3, 2.1, 3.2],
            type: 'bar',
            orientation: 'v',
            marker: {
                color: ['#3498db', '#95a5a6', '#27ae60', '#f39c12', '#9b59b6', '#e74c3c'],
                line: {
                    color: 'white',
                    width: 2
                }
            },
            text: ['RR: 1.2', 'RR: 0.9', 'RR: 1.5', 'RR: 1.3', 'RR: 2.1', 'RR: 3.2'],
            textposition: 'outside',
            textfont: {
                size: 12,
                color: 'white',
                family: 'Inter, sans-serif'
            },
            hovertemplate: '<b>%{x}</b><br>' +
                          'Risk Ratio: %{y}<br>' +
                          '%{y > 1 ? "Higher likelihood" : "Lower likelihood"}<br>' +
                          '<extra></extra>'
        }
    ];

    const layout = {
        title: {
            text: 'Risk Ratios from Modified Poisson Regression',
            font: {
                size: 18,
                color: '#2c3e50',
                family: 'Inter, sans-serif'
            }
        },
        xaxis: {
            title: 'Predictor Variables',
            titlefont: {
                size: 14,
                color: '#7f8c8d'
            },
            tickfont: {
                size: 10,
                color: '#34495e'
            },
            tickangle: -45
        },
        yaxis: {
            title: 'Risk Ratio (RR)',
            titlefont: {
                size: 14,
                color: '#7f8c8d'
            },
            tickfont: {
                size: 12,
                color: '#34495e'
            },
            range: [0, 3.5]
        },
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)',
        margin: {
            l: 60,
            r: 40,
            t: 60,
            b: 120
        },
        font: {
            family: 'Inter, sans-serif'
        },
        shapes: [
            {
                type: 'line',
                x0: -0.5,
                x1: 5.5,
                y0: 1,
                y1: 1,
                line: {
                    color: '#e74c3c',
                    width: 2,
                    dash: 'dash'
                }
            }
        ],
        annotations: [
            {
                x: 2.5,
                y: 1.1,
                text: 'RR = 1 (No Effect)',
                showarrow: false,
                font: {
                    color: '#e74c3c',
                    size: 12
                }
            },
            {
                x: 5,
                y: 3.4,
                text: 'Strongest<br>Predictor',
                showarrow: true,
                arrowhead: 2,
                arrowcolor: '#e74c3c',
                font: {
                    color: '#e74c3c',
                    size: 12
                }
            }
        ]
    };

    const config = {
        responsive: true,
        displayModeBar: true,
        modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d'],
        displaylogo: false
    };

    Plotly.newPlot('regressionChart', data, layout, config);
}

/**
 * Create Barriers Analysis Chart
 */
function createBarriersChart() {
    const data = [{
        x: ['Lack of Awareness', 'Fear/Anxiety', 'Cost Concerns', 'Time Constraints', 'Lack of Access', 'Cultural Barriers', 'Provider Issues'],
        y: [35.2, 28.7, 22.1, 18.9, 15.3, 12.8, 8.5],
        type: 'bar',
        marker: {
            color: ['#e74c3c', '#f39c12', '#3498db', '#27ae60', '#9b59b6', '#e67e22', '#95a5a6'],
            line: { color: 'white', width: 2 }
        },
        text: ['35.2%', '28.7%', '22.1%', '18.9%', '15.3%', '12.8%', '8.5%'],
        textposition: 'outside',
        textfont: { size: 14, color: '#2c3e50', family: 'Inter, sans-serif' },
        hovertemplate: '<b>%{x}</b><br>Reported by: %{y}% of students<br><extra></extra>'
    }];

    const layout = {
        title: { text: 'Major Barriers Preventing Screening', font: { size: 18, color: '#2c3e50', family: 'Inter, sans-serif' } },
        xaxis: { title: 'Barrier Type', tickangle: -45 },
        yaxis: { title: 'Percentage of Students (%)', range: [0, 40] },
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)',
        margin: { l: 60, r: 40, t: 60, b: 120 }
    };

    Plotly.newPlot('barriersChart', data, layout, { responsive: true, displaylogo: false });
}

/**
 * Create Institution Comparison Chart
 */
function createInstitutionChart() {
    const data = [
        {
            x: ['University A', 'College B', 'Polytechnic C'],
            y: [18.2, 12.5, 9.1],
            type: 'bar',
            name: 'Screening Uptake Rate',
            marker: { color: ['#27ae60', '#f39c12', '#e74c3c'] },
            text: ['18.2%', '12.5%', '9.1%'],
            textposition: 'outside'
        },
        {
            x: ['University A', 'College B', 'Polytechnic C'],
            y: [45.6, 38.2, 35.4],
            type: 'bar',
            name: 'Awareness Rate',
            marker: { color: ['rgba(52, 152, 219, 0.7)', 'rgba(52, 152, 219, 0.7)', 'rgba(52, 152, 219, 0.7)'] },
            text: ['45.6%', '38.2%', '35.4%'],
            textposition: 'outside'
        }
    ];

    const layout = {
        title: { text: 'Institutional Performance Comparison', font: { size: 18, color: '#2c3e50' } },
        barmode: 'group',
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)',
        margin: { l: 60, r: 40, t: 60, b: 60 }
    };

    Plotly.newPlot('institutionChart', data, layout, { responsive: true, displaylogo: false });
}

/**
 * Add smooth scrolling for anchor links
 */
function addSmoothScrolling() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/**
 * Handle window resize to make charts responsive
 */
window.addEventListener('resize', function() {
    // Plotly charts are automatically responsive with the config settings
    console.log('Window resized - charts will auto-adjust');
});

/**
 * Error handling for chart loading
 */
window.addEventListener('error', function(e) {
    console.error('Dashboard error:', e.error);
    
    // Show fallback message if charts fail to load
    const chartContainers = document.querySelectorAll('[id$="Chart"]');
    chartContainers.forEach(container => {
        if (!container.hasChildNodes() || container.children.length === 0) {
            container.innerHTML = `
                <div style="display: flex; justify-content: center; align-items: center; height: 400px; background: #f8f9fa; border-radius: 10px; color: #7f8c8d;">
                    <div style="text-align: center;">
                        <i class="fas fa-chart-bar" style="font-size: 2rem; margin-bottom: 1rem;"></i>
                        <p>Chart loading... Please refresh if this persists.</p>
                    </div>
                </div>
            `;
        }
    });
});

// Export functions for potential external use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initializeCharts,
        createSankeyChart,
        createOpportunityChart,
        createAgeGroupChart,
        createAwarenessChart,
        createRegressionChart,
        createBarriersChart,
        createInstitutionChart
    };
}
