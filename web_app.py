from flask import Flask, render_template_string, request, jsonify
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

app = Flask(__name__)

def scrape(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.title.text.strip() if soup.title else "No title found"
        
        headings = []
        for h in soup.find_all(['h1', 'h2', 'h3']):
            text = h.get_text().strip()
            if text and len(text) > 3:\
                headings.append(text)
        
        paragraphs = []
        for p in soup.find_all('p'):
            text = p.get_text().strip()
            if text and len(text) > 10:
                paragraphs.append(text)
        
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            text = a.get_text().strip()
            if text and href and not href.startswith('#'):
                links.append({
                    'text': text,
                    'href': href
                })
        
        meta_data = {}
        for meta in soup.find_all('meta'):
            if meta.get('name') and meta.get('content'):
                meta_data[meta['name']] = meta['content']
        
        data = {
            'url': url,
            'title': title,
            'headings': headings[:5],
            'paragraphs': paragraphs[:5],
            'links': links[:10],
            'meta': meta_data,
            'timestamp': datetime.now().isoformat()
        }
        
        return data
    
    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")
        return None

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Scrape Dat - Web Scraper</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .container {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        .form-container {
            background-color: #f5f5f5;
            padding: 20px;
            border-radius: 5px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input[type="text"] {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background-color: #45a049;
        }
        .results {
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 5px;
            border: 1px solid #ddd;
        }
        .section {
            margin-bottom: 20px;
        }
        .section h3 {
            margin-top: 0;
            border-bottom: 1px solid #ddd;
            padding-bottom: 5px;
        }
        .links-table {
            width: 100%;
            border-collapse: collapse;
        }
        .links-table th, .links-table td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        .links-table th {
            background-color: #f2f2f2;
        }
        .error {
            color: red;
            font-weight: bold;
        }
        .loading {
            text-align: center;
            padding: 20px;
            font-style: italic;
            color: #666;
        }
    </style>
</head>
<body>
    <h1>Scrape Dat - Web Scraper</h1>
    
    <div class="container">
        <div class="form-container">
            <form id="scrape-form">
                <div class="form-group">
                    <label for="url">URL to Scrape:</label>
                    <input type="text" id="url" name="url" placeholder="https://example.com" required>
                </div>
                <button type="submit">Scrape</button>
            </form>
        </div>
        
        <div id="loading" class="loading" style="display: none;">
            Scraping in progress... Please wait.
        </div>
        
        <div id="results" class="results" style="display: none;">
            <div class="section">
                <h3>Basic Information</h3>
                <p><strong>URL:</strong> <span id="result-url"></span></p>
                <p><strong>Title:</strong> <span id="result-title"></span></p>
                <p><strong>Timestamp:</strong> <span id="result-timestamp"></span></p>
            </div>
            
            <div class="section">
                <h3>Headings</h3>
                <ul id="result-headings"></ul>
            </div>
            
            <div class="section">
                <h3>Paragraphs</h3>
                <div id="result-paragraphs"></div>
            </div>
            
            <div class="section">
                <h3>Links</h3>
                <table class="links-table">
                    <thead>
                        <tr>
                            <th>Text</th>
                            <th>URL</th>
                        </tr>
                    </thead>
                    <tbody id="result-links"></tbody>
                </table>
            </div>
            
            <div class="section">
                <h3>Meta Data</h3>
                <pre id="result-meta"></pre>
            </div>
        </div>
        
        <div id="error" class="error" style="display: none;"></div>
    </div>
    
    <script>
        document.getElementById('scrape-form').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const url = document.getElementById('url').value;
            
            document.getElementById('loading').style.display = 'block';
            document.getElementById('results').style.display = 'none';
            document.getElementById('error').style.display = 'none';
            
            fetch('/api/scrape', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url: url }),
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('loading').style.display = 'none';
                
                if (data.success) {
                    document.getElementById('results').style.display = 'block';
                    
                    document.getElementById('result-url').textContent = data.data.url;
                    document.getElementById('result-title').textContent = data.data.title;
                    document.getElementById('result-timestamp').textContent = data.data.timestamp;
                    
                    const headingsList = document.getElementById('result-headings');
                    headingsList.innerHTML = '';
                    data.data.headings.forEach(heading => {
                        const li = document.createElement('li');
                        li.textContent = heading;
                        headingsList.appendChild(li);
                    });
                    
                    const paragraphsDiv = document.getElementById('result-paragraphs');
                    paragraphsDiv.innerHTML = '';
                    data.data.paragraphs.forEach(paragraph => {
                        const p = document.createElement('p');
                        p.textContent = paragraph;
                        paragraphsDiv.appendChild(p);
                    });
                    
                    const linksTable = document.getElementById('result-links');
                    linksTable.innerHTML = '';
                    data.data.links.forEach(link => {
                        const tr = document.createElement('tr');
                        
                        const tdText = document.createElement('td');
                        tdText.textContent = link.text;
                        tr.appendChild(tdText);
                        
                        const tdHref = document.createElement('td');
                        const a = document.createElement('a');
                        a.href = link.href;
                        a.textContent = link.href;
                        a.target = '_blank';
                        tdHref.appendChild(a);
                        tr.appendChild(tdHref);
                        
                        linksTable.appendChild(tr);
                    });
                    
                    document.getElementById('result-meta').textContent = JSON.stringify(data.data.meta, null, 2);
                } else {
                    document.getElementById('error').style.display = 'block';
                    document.getElementById('error').textContent = data.error || 'An unknown error occurred';
                }
            })
            .catch(error => {
                document.getElementById('loading').style.display = 'none';
                
                document.getElementById('error').style.display = 'block';
                document.getElementById('error').textContent = 'Network error: ' + error.message;
            });
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/scrape', methods=['POST'])
def api_scrape():
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({'success': False, 'error': 'URL is required'})
    
    try:
        result = scrape(url)
        if result:
            return jsonify({'success': True, 'data': result})
        else:
            return jsonify({'success': False, 'error': 'Failed to scrape the URL'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
