// Update text statistics
function updateStats() {
    const text1 = document.getElementById('text1').value;
    const text2 = document.getElementById('text2').value;
    
    const words1 = text1.trim().split(/\s+/).filter(w => w.length > 0).length;
    const words2 = text2.trim().split(/\s+/).filter(w => w.length > 0).length;
    const chars1 = text1.length;
    const chars2 = text2.length;
    
    document.getElementById('count1').textContent = `${words1} words`;
    document.getElementById('count2').textContent = `${words2} words`;
    document.getElementById('char1').textContent = `${chars1} chars`;
    document.getElementById('char2').textContent = `${chars2} chars`;
}

// Swap texts
function swapTexts() {
    const text1 = document.getElementById('text1');
    const text2 = document.getElementById('text2');
    const temp = text1.value;
    text1.value = text2.value;
    text2.value = temp;
    updateStats();
}

// Show loading
function showLoading() {
    document.getElementById('loadingOverlay').style.display = 'flex';
}

// Hide loading
function hideLoading() {
    document.getElementById('loadingOverlay').style.display = 'none';
}

// Show error
function showError(message) {
    const errorDiv = document.getElementById('error');
    const errorText = document.getElementById('errorText');
    errorText.textContent = message;
    errorDiv.style.display = 'flex';
    setTimeout(() => {
        errorDiv.style.display = 'none';
    }, 5000);
}

// Hide error
function hideError() {
    document.getElementById('error').style.display = 'none';
}

// Update score gauge
function updateScoreGauge(percentage) {
    const gauge = document.getElementById('scoreGauge');
    const angle = (percentage / 100) * 360;
    const color = percentage >= 70 ? '#EF4444' : (percentage >= 40 ? '#F59E0B' : '#10B981');
    gauge.style.background = `conic-gradient(${color} 0deg ${angle}deg, #E5E7EB ${angle}deg 360deg)`;
    document.getElementById('scorePercent').textContent = `${percentage}%`;
}

// Display results
function displayResults(data) {
    // Show results section
    document.getElementById('results').style.display = 'block';
    
    // Update score gauge
    updateScoreGauge(data.similarity_percentage);
    
    // Risk indicator
    const riskIndicator = document.getElementById('riskIndicator');
    riskIndicator.className = `risk-indicator risk-${data.risk_color === 'red' ? 'high' : (data.risk_color === 'orange' ? 'moderate' : 'low')}`;
    riskIndicator.textContent = data.risk_level;
    
    // Verdict and quality
    document.getElementById('verdictText').innerHTML = `<strong>Verdict:</strong> ${data.verdict}`;
    document.getElementById('qualityScore').innerHTML = `Content Quality Score: ${data.content_quality_score}%`;
    document.getElementById('recommendationBox').innerHTML = `<strong>📋 Recommendation:</strong> ${data.recommendation}`;
    
    // Executive Summary
    document.getElementById('executiveSummary').innerHTML = `
        <div style="padding: 1rem; background: linear-gradient(135deg, #F3F4F6 0%, #FFFFFF 100%); border-radius: 12px;">
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                <div>
                    <div style="font-size: 0.75rem; color: #6B7280;">REPORT ID</div>
                    <div style="font-size: 1rem; font-weight: 600;">${data.report_id}</div>
                </div>
                <div>
                    <div style="font-size: 0.75rem; color: #6B7280;">ANALYZED ON</div>
                    <div style="font-size: 1rem; font-weight: 600;">${data.timestamp}</div>
                </div>
                <div>
                    <div style="font-size: 0.75rem; color: #6B7280;">PRIORITY</div>
                    <div style="font-size: 1rem; font-weight: 600;">${data.executive_summary.priority_level}</div>
                </div>
            </div>
            <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #E5E7EB;">
                <strong>Summary:</strong> ${data.executive_summary.executive_summary}
            </div>
            <div style="margin-top: 0.5rem;">
                <strong>Action Required:</strong> ${data.executive_summary.recommended_action}
            </div>
        </div>
    `;
    
    // Metrics Grid
    document.getElementById('metricsGrid').innerHTML = `
        <div class="metric-card">
            <div class="metric-value">${data.cosine_similarity}%</div>
            <div class="metric-label">Cosine Similarity</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">${data.jaccard_similarity}%</div>
            <div class="metric-label">Jaccard Similarity</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">${data.ngram_similarity}%</div>
            <div class="metric-label">N-Gram Similarity</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">${data.sentence_match_percentage}%</div>
            <div class="metric-label">Sentence Match</div>
        </div>
    `;
    
    // Analytics Grid
    document.getElementById('analyticsGrid').innerHTML = `
        <div class="metric-card">
            <div class="metric-value">${data.uniqueness_score}%</div>
            <div class="metric-label">Uniqueness Score</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">${data.statistics.text1.lexical_diversity}%</div>
            <div class="metric-label">Text 1 Diversity</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">${data.statistics.text2.lexical_diversity}%</div>
            <div class="metric-label">Text 2 Diversity</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">${data.similarity_zones.high_similarity_zones}</div>
            <div class="metric-label">Similarity Zones</div>
        </div>
    `;
    
    // Comparison Grid
    document.getElementById('comparisonGrid').innerHTML = `
        <div class="comparison-card">
            <div class="comparison-title">📄 Text 1 Statistics</div>
            <div class="comparison-stats">
                <div class="comparison-item">
                    <span class="comparison-label">Word Count:</span>
                    <span class="comparison-value">${data.statistics.text1.word_count}</span>
                </div>
                <div class="comparison-item">
                    <span class="comparison-label">Character Count:</span>
                    <span class="comparison-value">${data.statistics.text1.character_count}</span>
                </div>
                <div class="comparison-item">
                    <span class="comparison-label">Sentence Count:</span>
                    <span class="comparison-value">${data.statistics.text1.sentence_count}</span>
                </div>
                <div class="comparison-item">
                    <span class="comparison-label">Unique Words:</span>
                    <span class="comparison-value">${data.statistics.text1.unique_words}</span>
                </div>
                <div class="comparison-item">
                    <span class="comparison-label">Readability:</span>
                    <span class="comparison-value">${data.statistics.text1.readability.level}</span>
                </div>
            </div>
        </div>
        <div class="comparison-card">
            <div class="comparison-title">📄 Text 2 Statistics</div>
            <div class="comparison-stats">
                <div class="comparison-item">
                    <span class="comparison-label">Word Count:</span>
                    <span class="comparison-value">${data.statistics.text2.word_count}</span>
                </div>
                <div class="comparison-item">
                    <span class="comparison-label">Character Count:</span>
                    <span class="comparison-value">${data.statistics.text2.character_count}</span>
                </div>
                <div class="comparison-item">
                    <span class="comparison-label">Sentence Count:</span>
                    <span class="comparison-value">${data.statistics.text2.sentence_count}</span>
                </div>
                <div class="comparison-item">
                    <span class="comparison-label">Unique Words:</span>
                    <span class="comparison-value">${data.statistics.text2.unique_words}</span>
                </div>
                <div class="comparison-item">
                    <span class="comparison-label">Readability:</span>
                    <span class="comparison-value">${data.statistics.text2.readability.level}</span>
                </div>
            </div>
        </div>
    `;
    
    // Similarity Details
    let detailsHtml = '';
    
    if (data.common_words.length > 0) {
        detailsHtml += `
            <div class="common-words">
                <h3>📝 Common Words (${data.common_words_count})</h3>
                <div>
                    ${data.common_words.map(word => `<span class="word-tag">${word}</span>`).join('')}
                </div>
            </div>
        `;
    }
    
    if (data.common_phrases.length > 0) {
        detailsHtml += `
            <div class="common-phrases">
                <h3>🔗 Common Phrases (${data.common_phrases_count})</h3>
                <div>
                    ${data.common_phrases.map(phrase => `<span class="phrase-tag">"${phrase}"</span>`).join('')}
                </div>
            </div>
        `;
    }
    
    document.getElementById('similarityDetails').innerHTML = detailsHtml || '<p>No significant common words or phrases detected.</p>';
    
    // Sentence Matches
    if (data.sentence_matches && data.sentence_matches.length > 0) {
        document.getElementById('sentenceMatchCard').style.display = 'block';
        let matchesHtml = '<div class="sentence-matches">';
        data.sentence_matches.forEach((match, index) => {
            matchesHtml += `
                <div style="background: #F3F4F6; padding: 1rem; margin-bottom: 1rem; border-radius: 8px;">
                    <div style="font-size: 0.75rem; color: #6B7280; margin-bottom: 0.5rem;">Match #${index + 1} (${match.similarity * 100}% similar)</div>
                    <div style="margin-bottom: 0.5rem;"><strong>Original:</strong> "${match.original}"</div>
                    <div><strong>Match:</strong> "${match.match}"</div>
                </div>
            `;
        });
        matchesHtml += '</div>';
        document.getElementById('sentenceMatches').innerHTML = matchesHtml;
    }
    
    // Word Frequency
    document.getElementById('frequencyContainer').innerHTML = `
        <div class="freq-card">
            <div class="freq-title">Top 10 Words - Text 1</div>
            <div class="freq-list">
                ${data.top_words.text1.map(item => `
                    <div class="freq-item">
                        <span class="freq-word">${item.word}</span>
                        <span class="freq-count">${item.count}×</span>
                    </div>
                `).join('')}
            </div>
        </div>
        <div class="freq-card">
            <div class="freq-title">Top 10 Words - Text 2</div>
            <div class="freq-list">
                ${data.top_words.text2.map(item => `
                    <div class="freq-item">
                        <span class="freq-word">${item.word}</span>
                        <span class="freq-count">${item.count}×</span>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
    
    // Suggestions
    document.getElementById('suggestionsList').innerHTML = `
        <ul class="suggestions-list">
            ${data.suggestions.map(suggestion => `<li>${suggestion}</li>`).join('')}
        </ul>
    `;
    
    // Metadata
    document.getElementById('metadataGrid').innerHTML = `
        <div class="metadata-item">
            <span>🆔 Report ID: ${data.report_id}</span>
        </div>
        <div class="metadata-item">
            <span>📅 Analyzed: ${data.timestamp}</span>
        </div>
        <div class="metadata-item">
            <span>⚡ Severity: ${data.severity}</span>
        </div>
        <div class="metadata-item">
            <span>🎯 Priority: ${data.executive_summary.priority_level}</span>
        </div>
    `;
}

// Main check function
async function checkPlagiarism() {
    const text1 = document.getElementById('text1').value.trim();
    const text2 = document.getElementById('text2').value.trim();
    
    if (!text1 || !text2) {
        showError('Please enter text in both fields.');
        return;
    }
    
    if (text1.length < 20 || text2.length < 20) {
        showError('Please enter at least 20 characters in each text field for accurate analysis.');
        return;
    }
    
    showLoading();
    hideError();
    
    try {
        const response = await fetch('/check', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text1, text2 })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayResults(data);
            window.scrollTo({ top: document.getElementById('results').offsetTop - 100, behavior: 'smooth' });
        } else {
            showError(data.error || 'An error occurred during analysis.');
            document.getElementById('results').style.display = 'none';
        }
    } catch (error) {
        showError('Failed to connect to server. Please make sure the Flask application is running.');
        document.getElementById('results').style.display = 'none';
    } finally {
        hideLoading();
    }
}

// Download report
function downloadReport() {
    const reportHtml = document.getElementById('executiveSummary').innerHTML;
    const blob = new Blob([reportHtml], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `plagiarism-report-${Date.now()}.html`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Clear all fields
function clearAll() {
    document.getElementById('text1').value = '';
    document.getElementById('text2').value = '';
    document.getElementById('results').style.display = 'none';
    hideError();
    updateStats();
}

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        checkPlagiarism();
    }
});

// Initialize
updateStats();