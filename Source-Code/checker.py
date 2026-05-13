import re
import math
from collections import Counter
from difflib import SequenceMatcher
import hashlib
from datetime import datetime
import json
from typing import Dict, List, Tuple, Any

# ------------------- Enhanced Stopwords -------------------
STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "has", "he",
    "in", "is", "it", "its", "of", "on", "that", "the", "to", "was", "were",
    "will", "with", "i", "you", "we", "they", "this", "that", "these", "those",
    "but", "or", "so", "for", "nor", "yet", "do", "does", "did", "have", "had",
    "having", "can", "could", "would", "should", "might", "must", "what", "which",
    "who", "whom", "whose", "there", "their", "they're", "we're", "you're",
    "i'm", "it's", "don't", "can't", "won't", "not", "no", "yes", "very", "just",
    "like", "just", "but", "so", "then", "than", "into", "through", "during",
    "before", "after", "above", "below", "between", "under", "over", "again",
    "further", "once", "here", "there", "where", "when", "why", "how", "both",
    "each", "few", "more", "most", "other", "some", "such", "no", "nor", "only",
    "own", "same", "than", "then", "too", "very", "just"
}

class PlagiarismReport:
    """Generate professional HTML and PDF-style reports"""
    
    @staticmethod
    def generate_html_report(data: dict) -> str:
        """Generate HTML report for download"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Plagiarism Analysis Report - {data.get('report_id', 'N/A')}</title>
            <meta charset="UTF-8">
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ 
                    font-family: 'Segoe UI', Arial, sans-serif; 
                    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                    padding: 40px;
                }}
                .container {{ max-width: 800px; margin: 0 auto; }}
                .header {{ 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white; 
                    padding: 30px; 
                    border-radius: 15px 15px 0 0;
                    text-align: center;
                }}
                .score-card {{ 
                    background: white; 
                    padding: 25px; 
                    border-radius: 10px; 
                    margin: 20px 0; 
                    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                }}
                .metrics-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 20px 0; }}
                .metric {{ 
                    background: #f8f9fa; 
                    padding: 15px; 
                    border-radius: 10px; 
                    text-align: center;
                    border-left: 4px solid #667eea;
                }}
                .metric-value {{ font-size: 24px; font-weight: bold; color: #667eea; }}
                .high-risk {{ color: #dc2626; font-weight: bold; }}
                .moderate-risk {{ color: #f59e0b; font-weight: bold; }}
                .low-risk {{ color: #10b981; font-weight: bold; }}
                table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
                th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #e5e7eb; }}
                th {{ background: #f8f9fa; font-weight: 600; }}
                .footer {{ text-align: center; padding: 20px; color: #6b7280; font-size: 12px; }}
                .recommendation {{ 
                    background: #fef3c7; 
                    padding: 15px; 
                    border-radius: 10px; 
                    border-left: 4px solid #f59e0b;
                    margin: 15px 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔍 Plagiarism Analysis Report</h1>
                    <p>Report ID: {data.get('report_id', 'N/A')}</p>
                    <p>Generated: {data.get('timestamp', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))}</p>
                </div>
                
                <div class="score-card">
                    <h2>Similarity Score: <span class="{'high-risk' if data.get('similarity_percentage', 0) >= 70 else 'moderate-risk' if data.get('similarity_percentage', 0) >= 40 else 'low-risk'}">{data.get('similarity_percentage', 0)}%</span></h2>
                    <p>Risk Level: <strong>{data.get('risk_level', 'N/A')}</strong></p>
                    <p>{data.get('verdict', 'N/A')}</p>
                </div>
                
                <div class="metrics-grid">
                    <div class="metric">
                        <div class="metric-value">{data.get('cosine_similarity', 0)}%</div>
                        <div>Cosine Similarity</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{data.get('jaccard_similarity', 0)}%</div>
                        <div>Jaccard Similarity</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{data.get('ngram_similarity', 0)}%</div>
                        <div>N-Gram Similarity</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{data.get('uniqueness_score', 0)}%</div>
                        <div>Uniqueness Score</div>
                    </div>
                </div>
                
                <div class="recommendation">
                    <strong>📋 Recommendation:</strong><br>
                    {data.get('recommendation', 'N/A')}
                </div>
                
                <div class="footer">
                    <p>© 2024 PlagioScan - Professional Plagiarism Detection System</p>
                </div>
            </div>
        </body>
        </html>
        """

class AdvancedPlagiarismChecker:
    def __init__(self):
        self.n_gram_sizes = [2, 3, 4]
        self.report_generator = PlagiarismReport()
        
    def preprocess(self, text: str) -> dict:
        """Enhanced preprocessing with multiple token types"""
        if not text or len(text.strip()) < 10:
            return {
                'tokens': [],
                'sentences': [],
                'n_grams': {2: [], 3: [], 4: []},
                'original': text,
                'clean_text': ''
            }
        
        # Clean text
        text_clean = re.sub(r'[^\w\s\.\?\!]', ' ', text.lower())
        text_clean = re.sub(r'\s+', ' ', text_clean).strip()
        
        # Word tokens (remove stopwords)
        tokens = [t for t in text_clean.split() if t not in STOPWORDS and len(t) > 2]
        
        # Sentence segmentation
        sentences = re.split(r'[.!?]+', text_clean)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 5]
        
        # N-grams
        n_grams = {size: [] for size in self.n_gram_sizes}
        for size in self.n_gram_sizes:
            for i in range(len(tokens) - size + 1):
                n_gram = ' '.join(tokens[i:i+size])
                n_grams[size].append(n_gram)
        
        return {
            'tokens': tokens,
            'sentences': sentences,
            'n_grams': n_grams,
            'original': text,
            'clean_text': text_clean,
            'token_count': len(tokens),
            'sentence_count': len(sentences)
        }
    
    def compute_tfidf(self, tokens: list[str], corpus: list[list[str]]) -> dict:
        """Compute TF-IDF vector with smoothing"""
        if not tokens:
            return {}
        
        tf = Counter(tokens)
        total = len(tokens)
        tfidf = {}
        N = len(corpus)
        
        for term, count in tf.items():
            tf_score = count / total
            df = sum(1 for doc in corpus if term in doc)
            idf = math.log((N + 1) / (df + 1)) + 1
            tfidf[term] = tf_score * idf
        
        return tfidf
    
    def cosine_similarity(self, vec1: dict, vec2: dict) -> float:
        """Calculate Cosine Similarity"""
        if not vec1 or not vec2:
            return 0.0
        
        all_terms = set(vec1) | set(vec2)
        dot_product = sum(vec1.get(t, 0) * vec2.get(t, 0) for t in all_terms)
        
        mag1 = math.sqrt(sum(v ** 2 for v in vec1.values()))
        mag2 = math.sqrt(sum(v ** 2 for v in vec2.values()))
        
        return dot_product / (mag1 * mag2) if mag1 != 0 and mag2 != 0 else 0.0
    
    def jaccard_similarity(self, tokens1: list, tokens2: list) -> float:
        """Jaccard Similarity"""
        set1 = set(tokens1)
        set2 = set(tokens2)
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        return intersection / union if union != 0 else 0.0
    
    def n_gram_similarity(self, n_grams1: dict, n_grams2: dict) -> float:
        """Average N-gram similarity"""
        scores = []
        for size in self.n_gram_sizes:
            set1 = set(n_grams1[size])
            set2 = set(n_grams2[size])
            if set1 and set2:
                intersection = len(set1 & set2)
                union = len(set1 | set2)
                scores.append(intersection / union if union != 0 else 0.0)
        return sum(scores) / len(scores) if scores else 0.0
    
    def sentence_overlap(self, sentences1: list, sentences2: list) -> dict:
        """Find overlapping sentences with similarity scores"""
        matched_sentences = []
        for s1 in sentences1:
            best_match = None
            best_ratio = 0
            for s2 in sentences2:
                ratio = SequenceMatcher(None, s1, s2).ratio()
                if ratio > best_ratio and ratio > 0.6:
                    best_ratio = ratio
                    best_match = s2
            
            if best_match:
                matched_sentences.append({
                    'original': s1,
                    'match': best_match,
                    'similarity': round(best_ratio, 3)
                })
        
        return {
            'count': len(matched_sentences),
            'total_sentences1': len(sentences1),
            'total_sentences2': len(sentences2),
            'percentage': (len(matched_sentences) / max(len(sentences1), 1)) * 100,
            'matches': matched_sentences[:10]
        }
    
    def lexical_diversity(self, tokens: list) -> float:
        """Calculate lexical diversity (type-token ratio)"""
        if not tokens:
            return 0.0
        return round((len(set(tokens)) / len(tokens)) * 100, 1)
    
    def readability_score(self, text: str) -> dict:
        """Calculate comprehensive readability metrics"""
        sentences = re.split(r'[.!?]+', text)
        sentences = [s for s in sentences if s.strip()]
        words = text.split()
        
        if not sentences or not words:
            return {'score': 0, 'level': 'Unknown', 'grade': 'Unknown', 'flesch_score': 0}
        
        avg_sentence_length = len(words) / len(sentences)
        avg_word_length = sum(len(w) for w in words) / len(words)
        
        # Flesch Reading Ease
        flesch_score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_word_length)
        
        # Flesch-Kincaid Grade Level
        grade_level = 0.39 * avg_sentence_length + 11.8 * avg_word_length - 15.59
        
        if flesch_score >= 90:
            level = "Very Easy"
            audience = "5th Grade"
        elif flesch_score >= 80:
            level = "Easy"
            audience = "6th Grade"
        elif flesch_score >= 70:
            level = "Fairly Easy"
            audience = "7th Grade"
        elif flesch_score >= 60:
            level = "Standard"
            audience = "8th-9th Grade"
        elif flesch_score >= 50:
            level = "Fairly Difficult"
            audience = "10th-12th Grade"
        elif flesch_score >= 30:
            level = "Difficult"
            audience = "College"
        else:
            level = "Very Difficult"
            audience = "College Graduate"
        
        return {
            'flesch_score': round(flesch_score, 1),
            'grade_level': round(grade_level, 1),
            'level': level,
            'target_audience': audience,
            'avg_sentence_length': round(avg_sentence_length, 1),
            'avg_word_length': round(avg_word_length, 2),
            'sentence_count': len(sentences),
            'word_count': len(words)
        }
    
    def find_similarity_zones(self, tokens1: list, tokens2: list) -> dict:
        """Identify zones of high similarity"""
        zones = []
        window_size = 10
        
        for i in range(0, len(tokens1) - window_size, window_size // 2):
            window1 = set(tokens1[i:i+window_size])
            for j in range(0, len(tokens2) - window_size, window_size // 2):
                window2 = set(tokens2[j:j+window_size])
                if window1 and window2:
                    overlap = len(window1 & window2) / len(window1 | window2)
                    if overlap > 0.5:
                        zones.append({
                            'position_1': i,
                            'position_2': j,
                            'similarity': round(overlap * 100, 1)
                        })
        
        return {
            'high_similarity_zones': len(zones),
            'zones': zones[:5]
        }
    
    def generate_summary(self, data: dict) -> dict:
        """Generate executive summary"""
        score = data['similarity_percentage']
        
        if score >= 70:
            summary = "Critical plagiarism detected. Immediate revision required."
            action = "Rewrite significant portions or cite all sources properly."
            priority = "High"
            quality = "Poor"
        elif score >= 40:
            summary = "Moderate similarity detected. Review recommended."
            action = "Paraphrase matching sections and add original content."
            priority = "Medium"
            quality = "Needs Improvement"
        else:
            summary = "Content appears original. Low plagiarism risk."
            action = "Continue maintaining originality in future work."
            priority = "Low"
            quality = "Good"
        
        return {
            'executive_summary': summary,
            'recommended_action': action,
            'priority_level': priority,
            'overall_quality': quality
        }
    
    def check_plagiarism(self, text1: str, text2: str) -> dict:
        """Main plagiarism checking function with enterprise features"""
        
        # Preprocess both texts
        processed1 = self.preprocess(text1)
        processed2 = self.preprocess(text2)
        
        # Handle empty/short texts
        if len(processed1['tokens']) < 5 or len(processed2['tokens']) < 5:
            return {
                "success": False,
                "error": "Text too short for meaningful analysis. Please provide at least 20 characters of meaningful content."
            }
        
        # Compute all similarity metrics
        corpus = [processed1['tokens'], processed2['tokens']]
        vec1 = self.compute_tfidf(processed1['tokens'], corpus)
        vec2 = self.compute_tfidf(processed2['tokens'], corpus)
        
        cosine_sim = self.cosine_similarity(vec1, vec2)
        jaccard_sim = self.jaccard_similarity(processed1['tokens'], processed2['tokens'])
        ngram_sim = self.n_gram_similarity(processed1['n_grams'], processed2['n_grams'])
        sentence_matches = self.sentence_overlap(processed1['sentences'], processed2['sentences'])
        
        # Weighted final score (optimized for accuracy)
        final_score = (
            cosine_sim * 0.35 +
            jaccard_sim * 0.20 +
            ngram_sim * 0.25 +
            (sentence_matches['percentage'] / 100) * 0.20
        )
        
        similarity_percentage = round(final_score * 100, 1)
        
        # Determine risk level with detailed messaging
        if similarity_percentage >= 70:
            risk_level = "HIGH RISK"
            risk_color = "red"
            severity = "Critical"
            verdict = "⚠️ HIGH SIMILARITY DETECTED! Significant overlap found. This content may be plagiarized."
            recommendation = "Immediate action required: Rewrite substantial portions, add citations, or reference original sources."
        elif similarity_percentage >= 40:
            risk_level = "MODERATE RISK"
            risk_color = "orange"
            severity = "Warning"
            verdict = "⚠️ MODERATE SIMILARITY! Considerable matching content detected. Review recommended."
            recommendation = "Suggested action: Paraphrase overlapping sections, add unique insights, and cite references."
        else:
            risk_level = "LOW RISK"
            risk_color = "green"
            severity = "Information"
            verdict = "✓ LOW SIMILARITY! Content appears original with minimal overlap."
            recommendation = "Good work! Document appears authentic. Consider adding more unique examples to strengthen originality."
        
        # Find common elements
        common_words = list(set(processed1['tokens']) & set(processed2['tokens']))
        common_phrases = self.find_common_phrases(processed1['clean_text'], processed2['clean_text'])
        
        # Get similarity zones
        similarity_zones = self.find_similarity_zones(processed1['tokens'], processed2['tokens'])
        
        # Calculate statistics
        unique_words1 = len(set(processed1['tokens']))
        unique_words2 = len(set(processed2['tokens']))
        
        total_unique = len(set(processed1['tokens']) | set(processed2['tokens']))
        uniqueness_score = round(((unique_words1 + unique_words2) / max(total_unique, 1)) * 100, 1) if total_unique > 0 else 0
        
        # Readability analysis
        readability1 = self.readability_score(text1)
        readability2 = self.readability_score(text2)
        
        # Word frequency
        freq1 = Counter(processed1['tokens']).most_common(10)
        freq2 = Counter(processed2['tokens']).most_common(10)
        
        # Generate executive summary
        summary_data = {
            'similarity_percentage': similarity_percentage,
            'risk_level': risk_level
        }
        executive_summary = self.generate_summary(summary_data)
        
        # Get improvement suggestions
        suggestions = self.get_smart_suggestions(
            similarity_percentage, 
            unique_words1, unique_words2,
            readability1, readability2
        )
        
        # Generate report ID
        report_id = hashlib.md5(f"{text1}{text2}{datetime.now()}".encode()).hexdigest()[:8]
        
        return {
            "success": True,
            "report_id": report_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            
            # Core results
            "similarity_percentage": similarity_percentage,
            "risk_level": risk_level,
            "risk_color": risk_color,
            "severity": severity,
            "verdict": verdict,
            "recommendation": recommendation,
            
            # Executive summary
            "executive_summary": executive_summary,
            
            # Detailed metrics
            "cosine_similarity": round(cosine_sim * 100, 1),
            "jaccard_similarity": round(jaccard_sim * 100, 1),
            "ngram_similarity": round(ngram_sim * 100, 1),
            "sentence_match_percentage": round(sentence_matches['percentage'], 1),
            
            # Text statistics
            "statistics": {
                "text1": {
                    "word_count": len(text1.split()),
                    "character_count": len(text1),
                    "sentence_count": processed1['sentence_count'],
                    "unique_words": unique_words1,
                    "lexical_diversity": self.lexical_diversity(processed1['tokens']),
                    "readability": readability1
                },
                "text2": {
                    "word_count": len(text2.split()),
                    "character_count": len(text2),
                    "sentence_count": processed2['sentence_count'],
                    "unique_words": unique_words2,
                    "lexical_diversity": self.lexical_diversity(processed2['tokens']),
                    "readability": readability2
                }
            },
            
            # Similarity details
            "common_words_count": len(common_words),
            "common_words": common_words[:20],
            "common_phrases_count": len(common_phrases),
            "common_phrases": common_phrases[:10],
            "sentence_matches": sentence_matches['matches'][:5],
            "similarity_zones": similarity_zones,
            
            # Word frequency
            "top_words": {
                "text1": [{"word": w, "count": c} for w, c in freq1],
                "text2": [{"word": w, "count": c} for w, c in freq2]
            },
            
            # Quality metrics
            "uniqueness_score": uniqueness_score,
            "content_quality_score": round(100 - similarity_percentage, 1),
            
            # Smart suggestions
            "suggestions": suggestions,
            
            # Raw counts for display
            "word_count1": len(text1.split()),
            "word_count2": len(text2.split()),
            "tokens1": len(processed1['tokens']),
            "tokens2": len(processed2['tokens']),
            
            # Report generation
            "html_report": self.report_generator.generate_html_report({
                'report_id': report_id,
                'similarity_percentage': similarity_percentage,
                'risk_level': risk_level,
                'verdict': verdict,
                'recommendation': recommendation,
                'cosine_similarity': round(cosine_sim * 100, 1),
                'jaccard_similarity': round(jaccard_sim * 100, 1),
                'ngram_similarity': round(ngram_sim * 100, 1),
                'uniqueness_score': uniqueness_score,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        }
    
    def find_common_phrases(self, text1: str, text2: str) -> list:
        """Find common multi-word phrases"""
        words1 = text1.split()
        words2 = text2.split()
        common_phrases = set()
        
        # Find 2-word phrases
        for i in range(len(words1) - 1):
            phrase = f"{words1[i]} {words1[i+1]}"
            for j in range(len(words2) - 1):
                if i < len(words2) - 1 and phrase == f"{words2[j]} {words2[j+1]}":
                    common_phrases.add(phrase)
        
        # Find 3-word phrases
        for i in range(len(words1) - 2):
            phrase = f"{words1[i]} {words1[i+1]} {words1[i+2]}"
            for j in range(len(words2) - 2):
                if i < len(words2) - 2 and phrase == f"{words2[j]} {words2[j+1]} {words2[j+2]}":
                    common_phrases.add(phrase)
        
        return list(common_phrases)
    
    def get_smart_suggestions(self, similarity: float, unique1: int, unique2: int, 
                             readability1: dict, readability2: dict) -> list:
        """Generate intelligent, actionable suggestions"""
        suggestions = []
        
        # Similarity-based suggestions
        if similarity > 70:
            suggestions.append("🚨 **Critical**: High similarity detected - Immediate revision required")
            suggestions.append("✍️ Rewrite significant portions in your own words")
            suggestions.append("📚 Add proper citations for any referenced material")
            suggestions.append("💡 Include original examples and personal insights")
        elif similarity > 40:
            suggestions.append("⚠️ **Warning**: Moderate similarity detected - Review recommended")
            suggestions.append("🔄 Paraphrase matching sections more thoroughly")
            suggestions.append("💭 Add your own analysis and interpretation")
            suggestions.append("📝 Expand on key points with unique examples")
        else:
            suggestions.append("✅ **Good**: Low similarity detected - Content appears original")
            suggestions.append("💪 Strengthen your work by adding more detailed analysis")
            suggestions.append("🎯 Consider adding real-world examples or case studies")
        
        # Vocabulary suggestions
        if unique1 < 30:
            suggestions.append("📖 Expand your vocabulary - Use more diverse word choices")
        if unique2 < 30:
            suggestions.append("📖 Text 2 has limited vocabulary - Consider using synonyms and varied expressions")
        
        # Readability suggestions
        if readability1.get('flesch_score', 0) < 50:
            suggestions.append("📊 Text 1 is complex - Consider simplifying sentence structure")
        if readability2.get('flesch_score', 0) < 50:
            suggestions.append("📊 Text 2 is complex - Break down long sentences for better readability")
        
        # Quality suggestions
        if similarity < 30 and (unique1 > 50 or unique2 > 50):
            suggestions.append("🏆 Excellent! Your content shows strong originality and vocabulary diversity")
        
        return suggestions

# Singleton instance
checker = AdvancedPlagiarismChecker()

def check_plagiarism(text1: str, text2: str) -> dict:
    """Wrapper function for compatibility"""
    return checker.check_plagiarism(text1, text2)