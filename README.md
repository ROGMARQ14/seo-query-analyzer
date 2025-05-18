# SEO Query Analyzer

A Streamlit application that analyzes how well your top search queries from Google Search Console are represented in your website's on-page elements, using data from Screaming Frog.

## 🚀 Features

- **Query Analysis**: Check if your top search queries appear in key on-page elements
- **Content Extraction**: Optionally fetch live content from URLs for up-to-date analysis
- **Comprehensive Reports**: View results in an interactive table with coverage metrics
- **Export Results**: Download analysis as CSV for further processing

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/seo-query-analyzer.git
   cd seo-query-analyzer
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## 🚦 Usage

1. **Export your data**:
   - From Google Search Console: Go to Performance > Export > CSV
   - From Screaming Frog: After crawling your site, go to Export > CSV

2. **Run the app**:
   ```bash
   streamlit run app.py
   ```

3. **Upload your files**:
   - Upload the GSC export (CSV)
   - Upload the Screaming Frog export (CSV)
   - Toggle "Scrape content from URLs" if you want fresh content

4. **View and export results**:
   - The app will display the analysis
   - Click "Download Results as CSV" to save the report

## 🛠 Requirements

- Python 3.8+
- Required packages are listed in `requirements.txt`

## 🌐 Deploy to Streamlit Cloud

You can easily deploy this app to Streamlit Cloud:

1. Fork this repository
2. Go to [Streamlit Cloud](https://share.streamlit.io/)
3. Click "New app" and connect your GitHub repository
4. Select the main branch and set the main file to `app.py`
5. Click "Deploy!"

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Uses [Trafilatura](https://trafilatura.readthedocs.io/) for content extraction
- Inspired by SEO best practices for on-page optimization
