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

// Toggle collapsible sections
function toggleSection(sectionId) {
    const section = document.getElementById(sectionId);
    const header = section.previousElementSibling;
    const icon = header.querySelector('.toggle-icon');
    
    if (section.style.display === 'none' || section.style.display === '') {
        section.style.display = 'block';
        icon.textContent = '▲';
    } else {
        section.style.display = 'none';
        icon.textContent = '▼';
    }
}

// Show all jobs modal
function showAllJobs() {
    document.getElementById('allJobsModal').style.display = 'flex';
}

function closeAllJobsModal() {
    document.getElementById('allJobsModal').style.display = 'none';
}

// Show all applications modal
function showAllApplications() {
    document.getElementById('allApplicationsModal').style.display = 'flex';
}

function closeAllApplicationsModal() {
    document.getElementById('allApplicationsModal').style.display = 'none';
}

// Show apply modal
function showApplyModal(jobId, companyName, position) {
    const modal = document.getElementById('applyModal');
    const title = document.getElementById('applyModalTitle');
    const form = document.getElementById('applyForm');
    
    title.textContent = `Apply to ${companyName} - ${position}`;
    form.action = `/apply_job/${jobId}`;
    
    modal.style.display = 'flex';
}

function closeApplyModal() {
    document.getElementById('applyModal').style.display = 'none';
    document.getElementById('applyForm').reset();
}

// Close modals when clicking outside
window.addEventListener('click', function(event) {
    const applyModal = document.getElementById('applyModal');
    if (event.target === applyModal) {
        closeApplyModal();
    }
});

// Initialize all charts
function initializeCharts(applications, resumes) {
    // Chart 1: Application Status Distribution
    createStatusChart(applications);
    
    // Chart 2: ATS Score Distribution
    createATSChart(applications);
    
    // Chart 3: Applications by Company
    createCompanyChart(applications);
    
    // Chart 4: Resume Performance
    createResumeChart(applications, resumes);
    
    // Chart 5: Application Timeline
    createTimelineChart(applications);
    
    // Chart 6: Success Rate
    createSuccessChart(applications);
}

// Chart 1: Application Status (Pie Chart)
function createStatusChart(applications) {
    const ctx = document.getElementById('statusChart');
    if (!ctx) return;
    
    const pending = applications.filter(app => app.status === 'pending').length;
    const shortlisted = applications.filter(app => app.status === 'shortlisted').length;
    const rejected = applications.filter(app => app.status === 'rejected').length;
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Pending', 'Shortlisted', 'Rejected'],
            datasets: [{
                data: [pending, shortlisted, rejected],
                backgroundColor: ['#f59e0b', '#10b981', '#ef4444'],
                borderWidth: 2,
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
                            size: 12
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed || 0;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : 0;
                            return `${label}: ${value} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

// Chart 2: ATS Score Distribution (Bar Chart)
function createATSChart(applications) {
    const ctx = document.getElementById('atsChart');
    if (!ctx) return;
    
    const excellent = applications.filter(app => app.ats_score >= 70).length;
    const good = applications.filter(app => app.ats_score >= 50 && app.ats_score < 70).length;
    const needsImprovement = applications.filter(app => app.ats_score < 50).length;
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Excellent (70%+)', 'Good (50-69%)', 'Needs Work (<50%)'],
            datasets: [{
                label: 'Applications',
                data: [excellent, good, needsImprovement],
                backgroundColor: ['#10b981', '#f59e0b', '#ef4444'],
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
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

// Chart 3: Top Companies Applied (Horizontal Bar)
function createCompanyChart(applications) {
    const ctx = document.getElementById('companyChart');
    if (!ctx) return;
    
    // Count applications per company
    const companyCounts = {};
    applications.forEach(app => {
        const company = app.job.company_name;
        companyCounts[company] = (companyCounts[company] || 0) + 1;
    });
    
    // Sort and get top 5
    const sortedCompanies = Object.entries(companyCounts)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 5);
    
    const labels = sortedCompanies.map(item => item[0]);
    const data = sortedCompanies.map(item => item[1]);
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels.length > 0 ? labels : ['No Data'],
            datasets: [{
                label: 'Applications',
                data: data.length > 0 ? data : [0],
                backgroundColor: '#6366f1',
                borderRadius: 8
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
                        stepSize: 1
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

// Chart 4: Resume Performance (Line Chart)
function createResumeChart(applications, resumes) {
    const ctx = document.getElementById('resumeChart');
    if (!ctx) return;
    
    // Calculate average ATS score per resume
    const resumeScores = {};
    const resumeNames = {};
    
    resumes.forEach(resume => {
        resumeNames[resume.id] = resume.original_filename;
        resumeScores[resume.id] = [];
    });
    
    applications.forEach(app => {
        if (resumeScores[app.resume_id] !== undefined) {
            resumeScores[app.resume_id].push(app.ats_score);
        }
    });
    
    const labels = [];
    const avgScores = [];
    const colors = [];
    
    Object.entries(resumeScores).forEach(([resumeId, scores]) => {
        if (scores.length > 0) {
            const avgScore = scores.reduce((a, b) => a + b, 0) / scores.length;
            labels.push(resumeNames[resumeId].substring(0, 20) + (resumeNames[resumeId].length > 20 ? '...' : ''));
            avgScores.push(avgScore.toFixed(1));
            
            // Color based on score
            if (avgScore >= 70) colors.push('#10b981');
            else if (avgScore >= 50) colors.push('#f59e0b');
            else colors.push('#ef4444');
        }
    });
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels.length > 0 ? labels : ['No Data'],
            datasets: [{
                label: 'Avg ATS Score',
                data: avgScores.length > 0 ? avgScores : [0],
                backgroundColor: colors.length > 0 ? colors : ['#6366f1'],
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        callback: function(value) {
                            return value + '%';
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
                            return `Avg Score: ${context.parsed.y}%`;
                        }
                    }
                }
            }
        }
    });
}


// Chart 5: Application Timeline (Line Chart)
function createTimelineChart(applications) {
    const ctx = document.getElementById('timelineChart');
    if (!ctx) return;
    
    if (applications.length === 0) {
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['No Data'],
                datasets: [{
                    label: 'Applications',
                    data: [0],
                    borderColor: '#6366f1',
                    backgroundColor: 'rgba(99, 102, 241, 0.1)',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: { legend: { display: false } }
            }
        });
        return;
    }
    
    // Group applications by date
    const dateCount = {};
    applications.forEach(app => {
        const date = new Date(app.applied_at);
        const dateStr = date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
        dateCount[dateStr] = (dateCount[dateStr] || 0) + 1;
    });
    
    // Sort by date
    const sortedDates = Object.keys(dateCount).sort((a, b) => {
        return new Date(a) - new Date(b);
    });
    
    const labels = sortedDates;
    const data = sortedDates.map(date => dateCount[date]);
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Applications',
                data: data,
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
                        stepSize: 1
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

// Chart 6: Success Rate (Doughnut Chart)
function createSuccessChart(applications) {
    const ctx = document.getElementById('successChart');
    if (!ctx) return;
    
    const shortlisted = applications.filter(app => app.status === 'shortlisted').length;
    const others = applications.length - shortlisted;
    
    const successRate = applications.length > 0 ? ((shortlisted / applications.length) * 100).toFixed(1) : 0;
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Shortlisted', 'Others'],
            datasets: [{
                data: [shortlisted, others],
                backgroundColor: ['#10b981', '#e2e8f0'],
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
                            size: 12
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed || 0;
                            const total = applications.length;
                            const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : 0;
                            return `${label}: ${value} (${percentage}%)`;
                        },
                        afterLabel: function(context) {
                            if (context.dataIndex === 0) {
                                return `Success Rate: ${successRate}%`;
                            }
                            return '';
                        }
                    }
                }
            }
        }
    });
}
