// Profile dropdown toggle
function toggleProfileMenu() {
    const menu = document.getElementById('profileMenu');
    menu.classList.toggle('show');
}

// Close profile menu when clicking outside
window.addEventListener('click', function(event) {
    if (!event.target.matches('.profile-circle') && !event.target.closest('.profile-dropdown')) {
        const menu = document.getElementById('profileMenu');
        if (menu && menu.classList.contains('show')) {
            menu.classList.remove('show');
        }
    }
});

// Show all jobs modal
function showAllJobs() {
    document.getElementById('allJobsModal').style.display = 'flex';
}

function closeAllJobsModal() {
    document.getElementById('allJobsModal').style.display = 'none';
}

// Show all users modal
function showAllUsers() {
    document.getElementById('allUsersModal').style.display = 'flex';
}

function closeAllUsersModal() {
    document.getElementById('allUsersModal').style.display = 'none';
}

// Initialize all admin charts with system-wide data
function initializeAdminCharts(adminStats, jobStats, users) {
    // Chart 1: Application Status Distribution
    createStatusChart(adminStats);
    
    // Chart 2: ATS Score Distribution
    createATSChart(adminStats);
    
    // Chart 3: Top Jobs by Applications
    createTopJobsChart(adminStats);
    
    // Chart 4: Applications Timeline (Last 7 Days)
    createTimelineChart(adminStats);
    
    // Chart 5: Top Skills Across All Resumes
    createSkillsChart(adminStats);
    
    // Chart 6: User Engagement Rate
    createEngagementChart(adminStats);
}

// Chart 1: Application Status Distribution (Doughnut)
function createStatusChart(adminStats) {
    const ctx = document.getElementById('statusChart');
    if (!ctx) return;
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Pending', 'Shortlisted', 'Rejected'],
            datasets: [{
                data: [
                    adminStats.pending_apps,
                    adminStats.shortlisted_apps,
                    adminStats.rejected_apps
                ],
                backgroundColor: ['#f59e0b', '#10b981', '#ef4444'],
                borderWidth: 3,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 15,
                        font: {
                            size: 12,
                            weight: 'bold'
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed || 0;
                            const total = adminStats.total_applications;
                            const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : 0;
                            return `${label}: ${value} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

// Chart 2: ATS Score Distribution (Bar)
function createATSChart(adminStats) {
    const ctx = document.getElementById('atsChart');
    if (!ctx) return;
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Excellent\n(70%+)', 'Good\n(50-69%)', 'Needs Work\n(<50%)'],
            datasets: [{
                label: 'Applications',
                data: [
                    adminStats.ats_excellent,
                    adminStats.ats_good,
                    adminStats.ats_needs_work
                ],
                backgroundColor: ['#10b981', '#f59e0b', '#ef4444'],
                borderRadius: 8,
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1,
                        font: {
                            weight: 'bold'
                        }
                    },
                    grid: {
                        color: '#e2e8f0'
                    }
                },
                x: {
                    ticks: {
                        font: {
                            size: 11,
                            weight: 'bold'
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
                            const value = context.parsed.y;
                            const total = adminStats.total_applications;
                            const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : 0;
                            return `Applications: ${value} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

// Chart 3: Top Jobs by Applications (Horizontal Bar)
function createTopJobsChart(adminStats) {
    const ctx = document.getElementById('jobsChart');
    if (!ctx) return;
    
    const jobsData = adminStats.jobs_with_apps || [];
    const labels = jobsData.length > 0 ? jobsData.map(j => {
        const name = j.name;
        return name.length > 30 ? name.substring(0, 30) + '...' : name;
    }) : ['No Data'];
    const data = jobsData.length > 0 ? jobsData.map(j => j.count) : [0];
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Applications',
                data: data,
                backgroundColor: '#6366f1',
                borderRadius: 8,
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                x: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1,
                        font: {
                            weight: 'bold'
                        }
                    },
                    grid: {
                        color: '#e2e8f0'
                    }
                },
                y: {
                    ticks: {
                        font: {
                            size: 10,
                            weight: 'bold'
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
                            return `Applications: ${context.parsed.x}`;
                        }
                    }
                }
            }
        }
    });
}

// Chart 4: Applications Timeline (Line Chart)
function createTimelineChart(adminStats) {
    const ctx = document.getElementById('timelineChart');
    if (!ctx) return;
    
    const timelineData = adminStats.applications_timeline || [];
    const labels = timelineData.map(t => t.date);
    const data = timelineData.map(t => t.count);
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels.length > 0 ? labels : ['No Data'],
            datasets: [{
                label: 'Applications',
                data: data.length > 0 ? data : [0],
                backgroundColor: 'rgba(99, 102, 241, 0.1)',
                borderColor: '#6366f1',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: '#6366f1',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 5,
                pointHoverRadius: 7
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1,
                        font: {
                            weight: 'bold'
                        }
                    },
                    grid: {
                        color: '#e2e8f0'
                    }
                },
                x: {
                    ticks: {
                        font: {
                            size: 10,
                            weight: 'bold'
                        }
                    },
                    grid: {
                        display: false
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
                            return `Applications: ${context.parsed.y}`;
                        }
                    }
                }
            }
        }
    });
}

// Chart 5: Top Skills Across All Resumes (Horizontal Bar)
function createSkillsChart(adminStats) {
    const ctx = document.getElementById('skillsChart');
    if (!ctx) return;
    
    const skillsData = adminStats.top_skills || [];
    const labels = skillsData.length > 0 ? skillsData.map(s => s.skill) : ['No Data'];
    const data = skillsData.length > 0 ? skillsData.map(s => s.count) : [0];
    
    // Create gradient colors
    const colors = [
        '#10b981', '#3b82f6', '#8b5cf6', '#f59e0b', '#ef4444',
        '#06b6d4', '#ec4899', '#14b8a6', '#f97316', '#a855f7'
    ];
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Candidates',
                data: data,
                backgroundColor: colors.slice(0, labels.length),
                borderRadius: 8,
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                x: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1,
                        font: {
                            weight: 'bold'
                        }
                    },
                    grid: {
                        color: '#e2e8f0'
                    }
                },
                y: {
                    ticks: {
                        font: {
                            size: 11,
                            weight: 'bold'
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
                            return `Candidates with this skill: ${context.parsed.x}`;
                        }
                    }
                }
            }
        }
    });
}

// Chart 6: User Engagement Rate (Doughnut)
function createEngagementChart(adminStats) {
    const ctx = document.getElementById('engagementChart');
    if (!ctx) return;
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Active Users', 'Inactive Users'],
            datasets: [{
                data: [
                    adminStats.active_users,
                    adminStats.inactive_users
                ],
                backgroundColor: ['#10b981', '#94a3b8'],
                borderWidth: 3,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 15,
                        font: {
                            size: 12,
                            weight: 'bold'
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed || 0;
                            const total = adminStats.total_users;
                            const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : 0;
                            return `${label}: ${value} (${percentage}%)`;
                        },
                        afterLabel: function(context) {
                            if (context.dataIndex === 0) {
                                return 'Users who have applied to jobs';
                            } else {
                                return 'Users who haven\'t applied yet';
                            }
                        }
                    }
                }
            }
        }
    });
}
