import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
import os
from dotenv import load_dotenv
from config import APPLICATIONS

load_dotenv()

def send_notification(title, message):
    access_token = os.getenv('PUSHBULLET_ACCESS_TOKEN')
    if not access_token:
        print("Error: PUSHBULLET_ACCESS_TOKEN not found in environment variables")
        return False
    headers = {
        "Access-Token": access_token,
        "Content-Type": "application/json"
    }
    payload = {
        "type": "note",
        "title": title,
        "body": message
    }
    response = requests.post("https://api.pushbullet.com/v2/pushes", json=payload, headers=headers)
    return response.status_code == 200

def download_ods_files(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    ods_links = []
    base_url = "https://www.ireland.ie"
    
    for link in soup.find_all('a', href=True):
        href = link['href']
        if '.ods' in href:
            full_url = urljoin(base_url, href)
            ods_links.append(full_url)
    
    return ods_links

def search_application_number(file_urls, applications):
    found_any = False
    for url in file_urls:
        filename = None
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                continue
            
            filename = url.split('/')[-1]
            with open(filename, 'wb') as f:
                f.write(response.content)
            
            try:
                df = pd.read_excel(filename, engine='odf')
            except ValueError:
                df = pd.read_excel(filename, engine='openpyxl')
                
            for column in df.columns:
                for app_number, name in applications.items():
                    mask = df[column].astype(str).str.contains(app_number)
                    if mask.any():
                        row_idx = df.index[mask][0]
                        col_idx = df.columns.get_loc(column)
                        found_any = True
                        print(f"Application number {app_number} for {name} found in {filename}")
                        
                        message = f"Application {app_number} for {name} found in {filename}"
                        if col_idx + 1 < len(df.columns):
                            next_cell = df.iloc[row_idx, col_idx + 1]
                            message += f"\nStatus: {next_cell}"
                        
                        send_notification("Visa Status Update", message)
            
        except Exception as e:
            continue
        finally:
            if filename and os.path.exists(filename):
                os.remove(filename)
    return found_any

def main():
    url = "https://www.ireland.ie/en/india/newdelhi/services/visas/processing-times-and-decisions/#Decisions"
    
    ods_files = download_ods_files(url)
    if not ods_files:
        return
    
    found = search_application_number(ods_files, APPLICATIONS)
    if not found:
        print(f"No application numbers were found in any of the ODS files.")

if __name__ == "__main__":
    try:
        main()
    except ImportError:
        print("Please install required libraries:")
        print("pip install requests beautifulsoup4 pandas pyexcel-ods openpyxl")
