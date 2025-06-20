# Scrape Data

A versatile web scraping tool that extracts structured data from websites through an intuitive web interface.

## 🚀 Features

- **Web Interface**: User-friendly UI for entering URLs and viewing results
- **Smart Content Extraction**: Automatically identifies and extracts:
  - Page title and headings
  - Main paragraphs
  - Links with text and URLs
  - Meta information
- **Results Visualization**: View extracted data in multiple formats:
  - Summary view
  - Raw JSON data
  - Structured paragraphs and links

## 📋 Requirements

- Python 3.6+
- Flask
- BeautifulSoup4
- Requests

## 🔧 Installation

### From PyPI

```bash
pip install scrape_dat
```

### From Source

```bash
git clone https://github.com/yourusername/scrape_dat.git
cd scrape_dat
pip install -e .
```

## 🖥️ Usage

### Web Interface

1. Start the web server:

```bash
python web_app.py
```

2. Open your browser and navigate to http://127.0.0.1:5000
3. Enter a URL to scrape and click "Scrape Data"
4. View the structured results

### Command Line (if implemented)

```bash
# Basic usage
scrape-dat https://example.com

# For more options
scrape-dat --help
```

## 🧩 How It Works

1. The application sends a request to the specified URL
2. It parses the HTML content using BeautifulSoup
3. Various elements are extracted:
   - Title from the `<title>` tag
   - Headings from `<h1>`, `<h2>`, and `<h3>` tags
   - Paragraphs from `<p>` tags
   - Links from `<a>` tags
   - Meta information from `<meta>` tags
4. The extracted data is presented in a structured format

## Screenshot

![image](https://github.com/user-attachments/assets/c4bb8f39-3a26-4fa1-a47c-c7a40009dbfa)

![Screenshot 2025-06-20 105252](https://github.com/user-attachments/assets/b7c70aa8-1c70-4a20-9b33-c1c6f6e18638)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
