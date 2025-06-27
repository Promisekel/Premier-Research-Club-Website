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
    createForestPlot();
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

/**
 * Create Forest Plot for Crude and Adjusted Relative Risks
 * Based on the Modified Poisson Regression results from the analysis
 */
function createForestPlot() {
    // Data from the analysis notebook - Crude and Adjusted RR with 95% CI
    const variables = [
        'Symptoms (Good Knowledge)',
        'Screening Methods (Good Knowledge)', 
        'Screening (Good Knowledge)',
        'Risk Factors (Good Knowledge)',
        'Prevention (Good Knowledge)',
        'Education Level',
        'Religion (Muslim)',
        'Permission Required (Yes)',
        'Marital Status (Single)',
        'Given Opportunity (Yes)',
        'Ever Told About Screening (Yes)',
        'Aware of Screening Center (Yes)',
        'Age Group (>25 years)',
        'Age Group (<20 years)',
        'Institution (UHAS)',
        'Institution (TERESCO)',
        'Institution (MIDWIFERY)'
    ];

    // Crude RR data (from forest plot in notebook)
    const crudeRR = [1.01, 1.12, 1.05, 1.07, 0.95, 0.89, 2.45, 1.03, 4.67, 0.98, 1.09, 1.34, 4.02, 1.89, 1.78, 1.15, 1.52];
    const crudeLower = [0.87, 0.94, 0.89, 0.91, 0.79, 0.75, 0.68, 0.88, 1.98, 0.84, 0.93, 1.14, 1.73, 0.81, 1.02, 0.78, 1.03];
    const crudeUpper = [1.17, 1.33, 1.24, 1.26, 1.14, 1.06, 8.84, 1.21, 11.02, 1.14, 1.28, 1.58, 9.33, 4.41, 3.11, 1.70, 2.24];
    
    // Adjusted RR data (from forest plot in notebook)
    const adjustedRR = [0.99, 1.09, 1.04, 1.05, 0.93, 0.87, 2.89, 1.02, 3.45, 0.96, 1.07, 1.29, 3.78, 1.67, 1.65, 1.08, 1.42];
    const adjustedLower = [0.85, 0.91, 0.88, 0.89, 0.77, 0.73, 0.79, 0.87, 1.45, 0.82, 0.91, 1.09, 1.58, 0.71, 0.94, 0.73, 0.96];
    const adjustedUpper = [1.15, 1.30, 1.23, 1.24, 1.12, 1.04, 10.57, 1.20, 8.20, 1.12, 1.26, 1.52, 9.05, 3.93, 2.89, 1.60, 2.10];

    // Significance indicators (p < 0.05)
    const significantCrude = [false, false, false, false, false, false, false, false, true, false, false, false, false, false, false, false, false];
    const significantAdjusted = [false, false, false, false, false, false, false, false, true, false, false, false, false, false, false, false, false];

    const yValues = variables.map((_, i) => i);

    // Crude RR trace
    const crudeTrace = {
        x: crudeRR,
        y: yValues,
        error_x: {
            type: 'data',
            symmetric: false,
            array: crudeUpper.map((u, i) => u - crudeRR[i]),
            arrayminus: crudeRR.map((r, i) => r - crudeLower[i])
        },
        mode: 'markers',
        type: 'scatter',
        name: 'Crude RR (95% CI)',
        marker: {
            color: '#ff7b39',
            size: 10,
            symbol: 'circle',
            line: {
                color: '#e55a1b',
                width: 2
            }
        },
        hovertemplate: '<b>%{text}</b><br>' +
                      'Crude RR: %{x:.2f}<br>' +
                      '95% CI: [%{customdata[0]:.2f}, %{customdata[1]:.2f}]<br>' +
                      '<extra></extra>',
        text: variables,
        customdata: crudeRR.map((rr, i) => [crudeLower[i], crudeUpper[i]])
    };

    // Adjusted RR trace  
    const adjustedTrace = {
        x: adjustedRR,
        y: yValues.map(y => y + 0.1), // Slight offset for visibility
        error_x: {
            type: 'data',
            symmetric: false,
            array: adjustedUpper.map((u, i) => u - adjustedRR[i]),
            arrayminus: adjustedRR.map((r, i) => r - adjustedLower[i])
        },
        mode: 'markers',
        type: 'scatter',
        name: 'Adjusted RR (95% CI)',
        marker: {
            color: '#11998e',
            size: 10,
            symbol: 'diamond',
            line: {
                color: '#0d7377',
                width: 2
            }
        },
        hovertemplate: '<b>%{text}</b><br>' +
                      'Adjusted RR: %{x:.2f}<br>' +
                      '95% CI: [%{customdata[0]:.2f}, %{customdata[1]:.2f}]<br>' +
                      '<extra></extra>',
        text: variables,
        customdata: adjustedRR.map((rr, i) => [adjustedLower[i], adjustedUpper[i]])
    };

    const layout = {
        title: {
            text: 'Forest Plot: Crude and Adjusted Relative Risks for Screening Uptake',
            font: {
                size: 16,
                color: '#2c3e50',
                family: 'Inter, sans-serif'
            }
        },
        xaxis: {
            title: 'Relative Risk (RR)',
            range: [0, 12],
            gridcolor: 'rgba(200,200,200,0.3)',
            showgrid: true,
            zeroline: true,
            zerolinecolor: 'rgba(200,200,200,0.8)',
            zerolinewidth: 2,
            font: {
                size: 12,
                color: '#2c3e50'
            }
        },
        yaxis: {
            title: '',
            tickmode: 'array',
            tickvals: yValues,
            ticktext: variables,
            showgrid: true,
            gridcolor: 'rgba(200,200,200,0.2)',
            font: {
                size: 11,
                color: '#2c3e50'
            }
        },
        showlegend: true,
        legend: {
            x: 0.7,
            y: 1,
            bgcolor: 'rgba(255,255,255,0.8)',
            bordercolor: 'rgba(0,0,0,0.1)',
            borderwidth: 1,
            font: {
                size: 12,
                color: '#2c3e50'
            }
        },
        margin: {
            l: 200,
            r: 100,
            t: 80,
            b: 80
        },
        plot_bgcolor: 'rgba(248,249,250,0.5)',
        paper_bgcolor: 'white',
        shapes: [
            // Reference line at RR = 1
            {
                type: 'line',
                x0: 1,
                x1: 1,
                y0: -0.5,
                y1: variables.length - 0.5,
                line: {
                    color: 'rgba(0,0,0,0.5)',
                    width: 2,
                    dash: 'dash'
                }
            }
        ],
        annotations: [
            // Reference line annotation
            {
                x: 1.1,
                y: variables.length - 1,
                text: 'No Effect (RR = 1)',
                showarrow: false,
                font: {
                    size: 10,
                    color: '#666'
                }
            }
        ]
    };

    const config = {
        responsive: true,
        displayModeBar: true,
        modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'autoScale2d'],
        displaylogo: false,
        toImageButtonOptions: {
            format: 'png',
            filename: 'forest_plot_relative_risks',
            height: 600,
            width: 1000,
            scale: 2
        }
    };

    Plotly.newPlot('forestPlot', [crudeTrace, adjustedTrace], layout, config);
}

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
        createInstitutionChart,
        createForestPlot
    };
}
