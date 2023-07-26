import requests
from bs4 import BeautifulSoup
import csv

murl= "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"
c=0
pages = []
pages.append(murl)
while True:
    if(c>=20):
        break
    url = murl
    #print("main",murl)
    page = requests.get(url)
    soup = BeautifulSoup(page.content,'html.parser')
    link = soup.findAll('a', class_='s-pagination-item s-pagination-button')
    for i in link:
        surl = "https://www.amazon.in" + str(i['href'])
        if surl not in pages:
            pages.append(surl)
            murl=surl
            #print(murl)
            c=c+1
            break

for pages_url in pages:
    sub_page = requests.get(pages_url)
    soup = BeautifulSoup(sub_page.content,'html.parser')
    # Product urls / links
    product_urls = []
    link = soup.findAll('h2', class_='a-size-mini a-spacing-none a-color-base s-line-clamp-2')
    for i in link:
        j= "https://www.amazon.in" + str(i.a['href'])
        product_urls.append(j)
       # print(j)
    #print(product_urls)

    # Product names
    product_names = []
    name = soup.findAll('h2', class_='a-size-mini a-spacing-none a-color-base s-line-clamp-2')
    for i in name:
        j=i.a.text
        product_names.append(j)
    #    print(j)

    # Product Price

    product_price = []
    price = soup.findAll('span', class_='a-price')
    for i in price:
        j=i.span.text
        product_price.append(j)
       # print(j)
#    print(product_price)

    #Product Ratings
    product_rating = []
    rating = soup.findAll('span', class_='a-icon-alt')
    for j in rating:
        i=j.text
        product_rating.append(i)
       # print(i)
#    print(product_rating)

    # Number of Reviews
    reviews = []
    review = soup.findAll('span', class_='a-size-base s-underline-text')
    for i in review:
        j=i.text
        reviews.append(j)
       # print(j)
#    print(reviews)

    products = []
    for i, j, k, l , m in zip(product_urls,product_names,product_price,product_rating,reviews):
        details = {}
        details["page_number"] = pages_url
        details["product_url"]=i
        details["product_name"]=j
        details["product_price"]=k
        details["product_rating"]=l
        details["product_reviews"]=m
        products.append(details)
#    print(products)

    # Creating a CSV File
    with open('Amazon_Bags_products.csv', 'a', newline='', encoding='utf-8') as csvfile:
        write = csv.writer(csvfile)
        for product in products:
            write.writerow(products)
