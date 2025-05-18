import pandas as pd
from typing import Dict, List, Optional, Set, Any

class SEOScorecardAnalyzer:
    """
    A utility class for analyzing SEO elements against target queries.
    
    This class provides functionality to analyze how well search queries are
    represented in various on-page SEO elements like titles, meta descriptions,
    headings, and content.
    """
    
    def __init__(self, content_extractor=None):
        """
        Initialize the SEOScorecardAnalyzer.
        
        Args:
            content_extractor: Optional ContentExtractor instance for URL content extraction
        """
        self.content_extractor = content_extractor
        
    def clean_text(self, text: Any) -> str:
        """
        Clean and normalize text for comparison.
        
        Args:
            text: Input text to clean (can be any type)
            
        Returns:
            str: Cleaned and normalized text
        """
        if text is None or not isinstance(text, (str, int, float)):
            return ""
            
        # Convert to string and clean
        text = str(text).strip().lower()
        return ' '.join(text.split())
    
    def analyze_query_in_elements(
        self, 
        query: str, 
        row: pd.Series, 
        scraped_content: Optional[Dict[str, str]] = None
    ) -> Dict[str, bool]:
        """
        Check if query exists in various page elements.
        
        Args:
            query: The search query to look for
            row: Pandas Series containing page data from Screaming Frog
            scraped_content: Optional dict mapping URLs to their scraped content
            
        Returns:
            Dict mapping element names to boolean indicating if query was found
        """
        query = self.clean_text(query)
        if not query:
            return {}
            
        results = {}
        
        # Elements to check from Screaming Frog
        elements_to_check = {
            'Title': 'Title 1',
            'Meta Description': 'Meta Description 1',
            'H1': 'H1-1',
        }
        
        # Check H2s (H2-1 to H2-5)
        h2_columns = [f'H2-{i}' for i in range(1, 6)]
        
        # Check in main elements
        for element_name, column in elements_to_check.items():
            if column in row:
                text = self.clean_text(row[column])
                results[element_name] = query in text if text else False
        
        # Check in H2s
        h2_texts = []
        for h2_col in h2_columns:
            if h2_col in row and pd.notna(row[h2_col]):
                h2_texts.append(self.clean_text(row[h2_col]))
        
        results['H2s'] = any(query in h2_text for h2_text in h2_texts if h2_text)
        
        # Check in scraped content if available
        url = row.get('Address')
        if url and scraped_content and url in scraped_content and scraped_content[url]:
            clean_content = self.clean_text(scraped_content[url])
            results['Content'] = query in clean_content if clean_content else False
        # Fallback to Post 1 if available
        elif 'Post 1' in row and pd.notna(row['Post 1']):
            clean_post = self.clean_text(str(row['Post 1']))
            results['Content'] = query in clean_post
        else:
            results['Content'] = False
            
        return results
    
    def generate_scorecard(
        self,
        gsc_df: pd.DataFrame,
        sf_df: pd.DataFrame,
        scrape_urls: bool = False
    ) -> pd.DataFrame:
        """
        Generate an SEO scorecard from GSC and Screaming Frog data.
        
        Args:
            gsc_df: DataFrame containing Google Search Console data
            sf_df: DataFrame containing Screaming Frog crawl data
            scrape_urls: Whether to scrape content from URLs
            
        Returns:
            DataFrame containing the SEO analysis results
        """
        if gsc_df.empty or sf_df.empty:
            return pd.DataFrame()
            
        # Get top 10 queries by clicks and impressions
        top_queries = gsc_df.nlargest(10, ['Clicks', 'Impressions'])['Query'].unique()
        
        # Scrape content if enabled and extractor is available
        scraped_content = {}
        if scrape_urls and self.content_extractor:
            urls_to_scrape = gsc_df[gsc_df['Query'].isin(top_queries)]['Landing Page'].unique()
            scraped_content = self.content_extractor.batch_extract(urls_to_scrape)
        
        # Prepare results
        results = []
        
        for query in top_queries:
            # Get all URLs for this query
            query_urls = gsc_df[gsc_df['Query'] == query]['Landing Page'].unique()
            
            for url in query_urls:
                # Find matching URL in Screaming Frog data
                matching_rows = sf_df[sf_df['Address'] == url]
                
                if not matching_rows.empty:
                    # Get the first matching row
                    row = matching_rows.iloc[0]
                    
                    # Check query in elements
                    element_checks = self.analyze_query_in_elements(query, row, scraped_content)
                    
                    # Prepare result row
                    result = {
                        'Query': query,
                        'URL': url,
                        **element_checks
                    }
                    results.append(result)
        
        return pd.DataFrame(results)
    
    def calculate_metrics(self, results_df: pd.DataFrame) -> Dict[str, float]:
        """
        Calculate metrics from the analysis results.
        
        Args:
            results_df: DataFrame containing the analysis results
            
        Returns:
            Dict containing various SEO metrics
        """
        if results_df.empty:
            return {}
            
        metrics = {
            'total_queries': results_df['Query'].nunique(),
            'total_urls': results_df['URL'].nunique(),
        }
        
        # Calculate coverage for each element type
        elements = ['Title', 'Meta Description', 'H1', 'H2s', 'Content']
        for element in elements:
            if element in results_df:
                metrics[f'{element.lower()}_coverage'] = results_df[element].mean() * 100
                
        # Calculate overall score (average of all coverages)
        coverage_scores = [metrics.get(f'{el.lower()}_coverage', 0) for el in elements]
        metrics['overall_score'] = sum(coverage_scores) / len(coverage_scores) if coverage_scores else 0
        
        return metrics
