from flask import Flask, render_template, request, redirect, url_for
from bs4 import BeautifulSoup
import requests
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
        
        url_tag = listing.find('a', href=lambda x: x and (x.startswith('/ru/locuri-de-munca/') or x.startswith('/ru/joburi/')))
        url = 'https://www.rabota.md' + url_tag['href'] if url_tag else 'N/A'
        
        data.append({'Title': title, 'Company': company, 'Salary': salary, 'URL': url})
    
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
        try:
            results = scrape_all_pages(keyword)
            
            df = pd.DataFrame(results)
            df = df[['Company', 'Title', 'Salary', 'URL']]
            df = df.sort_values('Company')
            df.index = range(1, len(df) + 1)
            
            df['URL'] = df['URL'].apply(lambda x: f'<a href="{x}" target="_blank">View Job</a>' if x != 'N/A' else 'N/A')
            
            table_html = df.to_html(classes='data', index=True, index_names=['No.'], escape=False)
            
            return render_template('results.html', table=table_html)
        except Exception as e:
            print(f"An error occurred: {e}")
            return redirect(url_for('index'))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
