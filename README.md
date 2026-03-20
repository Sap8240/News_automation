# News Automation Dashboard

A comprehensive news aggregation and filtering dashboard built with Streamlit that monitors important news stories across Indian news sources.

## Features

- 📰 **Multi-Source News Aggregation**: Pulls news from 20+ Indian news sources
- 🎯 **Priority Filtering**: Identifies critical news related to:
  - Sexual violence and crimes against women
  - Student issues and education
  - Legal and court matters
  - Infrastructure and disasters
  - Economic news and jobs
  - Environmental concerns

- 🖼️ **Rich Media Support**: Displays images from news articles where available
- 📊 **Analytics Dashboard**: 
  - Top news sources visualization
  - Priority breakdown charts
  - Story statistics (average summary length, images count)
  - Publication trends over time

- 🔍 **Advanced Search**: Filter news by:
  - Date range
  - Keywords
  - News source
  - Priority level

- 📱 **User-Friendly Interface**: Clean, intuitive design with:
  - Detailed news cards with summaries
  - Source attribution
  - Publication timestamps
  - Image galleries

## Installation

### Prerequisites
- Python 3.9+
- pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/news-automation.git
cd news-automation
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the dashboard locally:
```bash
streamlit run news_dashboard.py
```

The app will be available at `http://localhost:8501`

## News Sources Monitored

- NDTV (Breaking, Top Stories, India)
- India Today
- Times of India
- Indian Express
- The Hindu
- Scroll
- The Print
- The Wire
- Mint
- Economic Times
- Down to Earth
- Google News India
- BBC India

## Deployment

This app is deployed on [Streamlit Community Cloud](https://share.streamlit.io) and is automatically updated with the latest code from GitHub.

## Technologies Used

- **Streamlit**: Web app framework
- **Feedparser**: RSS feed parsing
- **BeautifulSoup4**: HTML parsing
- **Pandas**: Data manipulation
- **Plotly**: Interactive visualizations
- **Requests**: HTTP client

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Feedback

For feedback or issues, please open an issue on GitHub.
