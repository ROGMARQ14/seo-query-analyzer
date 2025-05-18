import streamlit as st

def main():
    st.title("About SEO Query Analyzer")
    
    st.markdown("""
    ## 📊 SEO Query Analyzer
    
    This tool helps you analyze how well your top search queries from Google Search Console (GSC) 
    are represented in your website's on-page elements, as crawled by Screaming Frog.
    
    ### 🔍 How It Works
    1. Upload your Google Search Console performance report (CSV)
    2. Upload your Screaming Frog crawl data (CSV)
    3. The tool will analyze your top 10 queries and check if they appear in:
       - Page titles
       - Meta descriptions
       - H1 headings
       - H2 subheadings
       - Page content
    
    ### 📂 File Requirements
    
    **Google Search Console Export:**
    - Must include columns: 'Query', 'Landing Page', 'Clicks', 'Impressions'
    - Export as CSV from GSC's Performance report
    
    **Screaming Frog Export:**
    - Must include columns: 'Address', 'Title 1', 'Meta Description 1', 'H1-1', 'H2-1' to 'H2-5', 'Post 1'
    - Export as CSV after crawling your site
    
    ### ⚙️ Advanced Options
    - **Scrape content from URLs**: When enabled, the tool will fetch the latest content directly from your live URLs
      instead of using the Screaming Frog crawl data. This is useful for ensuring you're analyzing the most 
      up-to-date content.
    
    ### 📊 Understanding the Results
    - **True**: The query was found in the specified element
    - **False**: The query was not found in the specified element
    - **Coverage Percentage**: The percentage of queries that appear in each element
    
    ### ⚠️ Note
    - The tool is case-insensitive when matching queries to content
    - For best results, ensure your Screaming Frog crawl is up-to-date
    - URL scraping is rate-limited to be respectful to web servers
    
    ### 📄 License
    This tool is provided as-is under the MIT License.
    """)

if __name__ == "__main__":
    main()
