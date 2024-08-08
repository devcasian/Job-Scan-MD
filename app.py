from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import pandas as pd

app = Flask(__name__)

def scrape_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    all_listings = soup.find_all('div', class_=lambda x: x and ('preview preview-search-result previewCard' in x or 'preview preview-search-result result-not-vip previewCard' in x))
    
    data = []
    for listing in all_listings:
        title_tag = listing.find('span', class_='sm:line-clamp-1')
        if not title_tag:
            title_tag = listing.find('a', class_='vacancy vacancy-title')
        title = title_tag.text.strip() if title_tag else 'N/A'
        
        company_tag = listing.find('a', class_='text-black flex items-center gap-3')
        if not company_tag:
            company_tag = listing.find('span', class_='text-primary')
        company = company_tag.text.strip() if company_tag else 'N/A'
        
        salary_tag = listing.find('span', class_='salary-negotiable')
        salary = salary_tag.text.strip() if salary_tag else 'N/A'
        
        data.append({'Title': title, 'Company': company, 'Salary': salary})
    
    return data

def scrape_all_pages(keyword):
    base_url = f'https://www.rabota.md/ru/jobs-moldova-{keyword}'
    all_data = []
    page = 1
    
    while True:
        url = f'{base_url}/{page}' if page > 1 else base_url
        print(f'Scraping page {page}...')
        page_data = scrape_page(url)
        
        if not page_data:
            break
        
        all_data.extend(page_data)
        page += 1
    
    return all_data

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        keyword = request.form['keyword']
        results = scrape_all_pages(keyword)
        
        df = pd.DataFrame(results)
        df = df[['Company', 'Title', 'Salary']]
        df = df.sort_values('Company')
        df.index = range(1, len(df) + 1)
    
        table_html = df.to_html(classes='data', index=True, index_names=['No.'])
        
        return render_template('results.html', table=table_html)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
