import requests
from requests.api import head
from bs4 import BeautifulSoup

URL = f'https://stackoverflow.com/jobs?q=python'
headers = {
        'Host': 'hh.ru',
        'User-Agent': 'Safari', 
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }

def extract_max_page():
    request = requests.get(URL)
    soup = BeautifulSoup(request.text, 'html.parser')
    pages = soup.find('div', {'class': 's-pagination'}).find_all('a')
    last_page = int(pages[-2].get_text(strip=True))
    return last_page

def extract_job(html):
    title = html.find('h2').find('a').text
    company_row = html.find('h3').find_all('span', recursive=False)
    company = company_row[0].get_text(strip=True)
    location = company_row[1].get_text(strip=True)
    job_id = html['data-jobid']
    link = f'https://stackoverflow.com/jobs/{job_id}/'
    return {'title': title, 'company': company, 'location': location, 'link': link}
     
def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"StackOverflow: parsing page={page + 1}")
        result = requests.get(f'{URL}&pg={page + 1}')
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find_all('div', {'class': '-job'})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs

def get_jobs():
    max_page = extract_max_page()
    jobs = extract_jobs(max_page)
    return jobs

