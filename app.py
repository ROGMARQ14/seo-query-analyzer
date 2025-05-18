import streamlit as st
import pandas as pd
from utils.content_extractor import ContentExtractor
from utils.seo_analyzer import SEOScorecardAnalyzer
import time

# Page config
st.set_page_config(
    page_title="SEO Query Analyzer",
    page_icon="📊",
    layout="wide"
)

# Initialize session state
if 'scraping_enabled' not in st.session_state:
    st.session_state.scraping_enabled = False

# Initialize services
content_extractor = ContentExtractor()
seo_analyzer = SEOScorecardAnalyzer(content_extractor)

def main():
    st.title("SEO Query Analyzer")
    st.markdown("""
    Upload your Google Search Console (GSC) and Screaming Frog (SF) reports to analyze 
    how well your top queries are represented in your page elements.
    """)
    
    # File uploaders
    st.sidebar.header("Upload Files")
    gsc_file = st.sidebar.file_uploader(
        "Upload GSC Performance Report (CSV)", 
        type=['csv'],
        help="CSV file from Google Search Console"
    )
    
    sf_file = st.sidebar.file_uploader(
        "Upload Screaming Frog Report (CSV)", 
        type=['csv'],
        help="CSV file from Screaming Frog"
    )
    
    # Scraping options
    with st.sidebar.expander("Advanced Options"):
        st.session_state.scraping_enabled = st.checkbox(
            "Scrape content from URLs",
            value=st.session_state.scraping_enabled,
            help="Enable to fetch and analyze content directly from URLs"
        )
    
    if gsc_file and sf_file:
        try:
            # Read files
            gsc_df = pd.read_csv(gsc_file)
            sf_df = pd.read_csv(sf_file)
            
            # Check required columns
            required_gsc_cols = {'Query', 'Landing Page', 'Clicks', 'Impressions'}
            required_sf_cols = {'Address', 'Title 1', 'Meta Description 1', 'H1-1'}
            
            missing_gsc = required_gsc_cols - set(gsc_df.columns)
            missing_sf = required_sf_cols - set(sf_df.columns)
            
            if missing_gsc or missing_sf:
                st.error(f"Missing required columns in:\n"
                        f"GSC: {', '.join(missing_gsc) if missing_gsc else 'None'}\n"
                        f"Screaming Frog: {', '.join(missing_sf) if missing_sf else 'None'}")
                return
            
            # Process data
            with st.spinner('Analyzing data...'):
                results_df = seo_analyzer.generate_scorecard(
                    gsc_df, 
                    sf_df,
                    scrape_urls=st.session_state.scraping_enabled
                )
                metrics = seo_analyzer.calculate_metrics(results_df)
            
            # Display results
            st.subheader("Analysis Results")
            st.dataframe(results_df, use_container_width=True)
            
            # Show metrics
            if metrics:
                st.subheader("SEO Metrics")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Queries", metrics['total_queries'])
                with col2:
                    st.metric("Total URLs Analyzed", metrics['total_urls'])
                with col3:
                    st.metric("Title Coverage", f"{metrics.get('title_coverage', 0):.1f}%")
                with col4:
                    st.metric("Content Coverage", f"{metrics.get('content_coverage', 0):.1f}%")
            
            # Download button
            csv = results_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Results as CSV",
                data=csv,
                file_name="seo_query_analysis.csv",
                mime="text/csv"
            )
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.info(
            "Please upload both GSC and Screaming Frog CSV files to begin analysis. "
            "Make sure they contain the required columns."
        )

if __name__ == "__main__":
    main()
