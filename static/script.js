document.addEventListener('DOMContentLoaded', function() {
    // Form submission handler for the content generation request
    const generateForm = document.getElementById('generateForm');
    if (generateForm) {
        generateForm.addEventListener('submit', handleGenerate);
    }

    // Load analytics if on the analytics or home page
    if (window.location.pathname === '/' || window.location.pathname === '/history') {
        loadAnalytics();
    }

    // Handle the load history data on the history page
    if (window.location.pathname === '/history') {
        loadHistory();
    }

    // Check if there's saved content and display it
    const savedContent = sessionStorage.getItem('generatedContent');
    if (savedContent) {
        displayResults(JSON.parse(savedContent));
    }
});

async function handleGenerate(e) {
    e.preventDefault();

    const url = document.getElementById('url').value;
    const loading = document.getElementById('loading');
    const error = document.getElementById('error');
    const resultsSection = document.querySelector('.results-section');
    
    // Reset UI
    error.style.display = 'none';
    resultsSection.style.display = 'none';
    loading.style.display = 'block';
    
    try {
        const response = await fetch('/generate_content', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url })
        });

        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to generate content');
        }
        
        // Save the generated content in sessionStorage
        sessionStorage.setItem('generatedContent', JSON.stringify(data));
        
        displayResults(data);
    } catch (err) {
        error.textContent = err.message;
        error.style.display = 'block';
    } finally {
        loading.style.display = 'none';
    }
}

function displayResults(data) {
    const resultsSection = document.querySelector('.results-section');
    const keywordsDiv = document.getElementById('keywords');
    const contentDiv = document.getElementById('generatedContent');
    
    // Display keywords
    keywordsDiv.innerHTML = data.keywords
        .map(keyword => `<span class="keyword">${keyword}</span>`)
        .join(' ');

    // Display content
    contentDiv.innerHTML = data.generated_content
        .split('\n')
        .map(para => `<p>${para}</p>`)
        .join(' ');

    resultsSection.style.display = 'block';
}

// Load the analytics data
async function loadAnalytics() {
    try {
        const response = await fetch('/api/analytics');
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to load analytics');
        }

        updateAnalyticsDashboard(data);
    } catch (err) {
        console.error('Failed to load analytics:', err);
    }
}

// Update the analytics dashboard with the fetched data
function updateAnalyticsDashboard(data) {
    // Update statistics
    document.getElementById('totalGenerations').textContent = data.total_generations;
    document.getElementById('averageWordCount').textContent = 
        Math.round(data.average_word_count);
    document.getElementById('averageKeywords').textContent = 
        Math.round(data.average_keywords);
    
    // Update timeline
    const timeline = document.getElementById('timeline');
    if (timeline && data.timeline.length > 0) {
        // Add timeline entries
        const timelineHtml = data.timeline
            .map(entry => ` 
                <div class="timeline-entry">
                    <span class="date">${entry.date}</span>
                    <span class="count">${entry.count} generations</span>
                </div>
            `)
            .join('');
        timeline.innerHTML = timelineHtml;
    }

    // Render charts
    renderCharts(data);
}

// Render the charts using Chart.js
function renderCharts(data) {
    // Prepare the data for charts
    const totalGenerationsData = data.total_generations_over_time;
    const averageWordCountData = data.average_word_count_over_time;
    const averageKeywordsData = data.average_keywords_over_time;

    const totalGenerationsConfig = {
        type: 'line',
        data: {
            labels: data.months, // Months or timeline labels
            datasets: [{
                label: 'Total Generations',
                data: totalGenerationsData,
                fill: false,
                borderColor: '#3182ce',
                tension: 0.1
            }]
        }
    };

    const averageWordCountConfig = {
        type: 'bar',
        data: {
            labels: data.months, // Months or timeline labels
            datasets: [{
                label: 'Average Word Count',
                data: averageWordCountData,
                backgroundColor: '#4299e1',
                borderColor: '#3182ce',
                borderWidth: 1
            }]
        }
    };

    const averageKeywordsConfig = {
        type: 'radar',
        data: {
            labels: data.months, // Months or timeline labels
            datasets: [{
                label: 'Average Keywords',
                data: averageKeywordsData,
                borderColor: '#e53e3e',
                pointBackgroundColor: '#e53e3e',
                fill: true
            }]
        }
    };

    // Create chart instances
    new Chart(document.getElementById('totalGenerationsChart'), totalGenerationsConfig);
    new Chart(document.getElementById('averageWordCountChart'), averageWordCountConfig);
    new Chart(document.getElementById('averageKeywordsChart'), averageKeywordsConfig);
}

// Check if we're on the history page and load history
if (window.location.pathname === '/history') {
    loadHistory();
}

// Load history data for the /history page
async function loadHistory() {
    try {
        const response = await fetch('/history');  // Fetch history data in JSON format from '/history' route
        const data = await response.json(); // Expect JSON response
        
        const historyContainer = document.getElementById('history-container');
        
        if (data && data.history && data.history.length > 0) {
            // Dynamically generate history content based on the JSON data
            historyContainer.innerHTML = data.history
                .map(entry => `
                    <div class="history-item">
                        <div class="history-header">
                            <h3>${entry.url}</h3>
                            <span class="timestamp">${entry.timestamp.slice(0, 10)}</span>
                        </div>
                        <div class="keywords">
                            ${entry.keywords.map(keyword => `<span class="keyword">${keyword}</span>`).join('')}
                        </div>
                        <div class="content">${entry.generated_content}</div>
                    </div>
                `)
                .join('');
        } else {
            historyContainer.innerHTML = '<p>No history available.</p>';
        }
    } catch (err) {
        console.error('Failed to load history:', err);
        document.getElementById('history-container').innerHTML = '<p>Error loading history.</p>';
    }
}
