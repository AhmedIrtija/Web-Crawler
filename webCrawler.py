from browsermobproxy import Server
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import csv
import json
import random
from urllib.parse import urlparse
import os
import tldextract
from collections import Counter

# Change this variable for the amount of website you want to crawl
max_crawl = 10

# create a browsermob server instance
server = Server('browsermob-proxy\\bin\\browsermob-proxy')
server.start()
proxy = server.create_proxy(params=dict(trustAllServers=True))


# open the csv and read from it
urls = []
with open('top-1m.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        urls.append(row[1].strip())


# create a new chromedriver instance
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--proxy-server={}".format(proxy.proxy))
chrome_options.add_argument('--headless')
chrome_options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome(options=chrome_options)


# Randomize the urls in the list
random.shuffle(urls)

folder_name = "har/"
crawl = 0

for url in urls:
    if  crawl >= max_crawl:
        break

    try:
        proxy.new_har("myhar", options={'captureCookies': True})

        driver.set_page_load_timeout(45)
        driver.get("http://"+url)

        if "This site can’t be reached" in driver.title:
            continue
        
        file_path = f'{folder_name}{url.replace("://", "_").replace("/", "_")}.har'
        with open(file_path, 'w') as f:
            f.write(json.dumps(proxy.har))

        crawl += 1

    except TimeoutException:
        continue
    except Exception:
        continue


server.stop()
driver.quit()


def thirdParty(domain, base_domain):
    extracted_domain = tldextract.extract(domain)
    extracted_base = tldextract.extract(base_domain)
    return extracted_domain.domain != extracted_base.domain


def processHAR(file_path, base_domain, third_party_counts, cookie_counts):
    with open(file_path, 'r') as f:
        har_data = json.load(f)

    for entry in har_data['log']['entries']:
        url = entry['request']['url']
        domain = urlparse(url).hostname

        if thirdParty(domain, base_domain):
            third_party_counts[domain] += 1

            # Check for cookies
            for cookie in entry['request'].get('cookies', []):
                cookie_name = cookie['name']
                cookie_counts[cookie_name] += 1


#Counting Domain and Cookies from the har folder
def main():
    har_folder = "har/"
    third_party_counts = Counter()
    cookie_counts = Counter()

    for file_name in os.listdir(har_folder):
        if file_name.endswith(".har"):
            file_path = os.path.join(har_folder, file_name)
            base_domain = file_name.split('.')[0]  
            processHAR(file_path, base_domain, third_party_counts, cookie_counts)

 
    print("Top 10 Third-Party Domains:")
    for domain, count in third_party_counts.most_common(10):
        print(f"{domain}: {count}")

    print("\nTop 10 Third-Party Cookies:")
    for cookie, count in cookie_counts.most_common(10):
        print(f"{cookie}: {count}")


if __name__ == "__main__":
    main()