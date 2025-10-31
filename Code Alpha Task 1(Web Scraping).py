#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin

BASE = "http://quotes.toscrape.com/"

def scrape_quotes(base_url=BASE, max_pages=None):
    page = 1
    results =[]
    url = base_url
    while True:
        print(f"Fetching: {url}")
        resp = requests.get(url,timeout= 15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")
        quotes = soup.select(".quote")
        for q in quotes:
            text = q.select_one(".text").get_text(strip=True)
            author = q.select_one(".author").get_text(strip=True)
            tags = [t.get_text(strip=True) for t in q.select(".tags a.tag")]
            results.append({"text": text, "author": author, "tags": ";".join(tags)})

        next_btn = soup.select_one("li.next > a")
        if next_btn and (max_pages is None or page < max_pages):
            href = next_btn["href"]
            url = urljoin(base_url, href)
            page += 1
        else:
            break
        return results


        def save_csv(rows, path="quotes.csv"):
            keys = ["text", "author", "tags"]
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f,fieldnames=keys)
                writer.writeheader()
                writer.writerows(rows)
            print(f"Saved {len(rows)} rows to {path}")

        if __name__ == "__main__":
           rows = scrape_quotes(max_pages=10)
           save_csv(rows,"quotes.csv")


# In[ ]:




