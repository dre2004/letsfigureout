import bs4
import csv
import requests
import re

def get_products(url: str):
    """
    Read html from Webscraper.io and return a product list. 
    Returns a list of products and a link for the next page (if it exists)
    """
    # Read the HTML from the url and get the main container
    raw = requests.get(url).text
    soup = bs4.BeautifulSoup(raw, 'html.parser')
    main_container = soup.find("div", {"class": "container test-site"})
    products = main_container.findAll("div", {"class": "col-sm-4 col-lg-4 col-md-4"})
    
    # Check if there is a next page
    pagination = main_container.find('ul', {"class": "pagination"})
    next = pagination.find('a', {"rel": "next"})
    if next:
        next = next["href"]

    # Iterate through the products and build a list
    product_list = [{"Name": p.find("a", {"class": "title"}).text,
                   "Description": p.find("p", {"class": "description"}).text,
                   "Price": p.find("h4", {"class": "price"}).text,
                   "Rating": p.find("p", attrs={"data-rating": re.compile(r".*")})['data-rating']}
                  for p in products]

    return product_list, next

def main():
    # this is the page wwe are going to be scraping
    base = "https://www.webscraper.io/"
    target = "test-sites/e-commerce/static/computers/laptops"
    raw = requests.get(base+target).text
    soup = bs4.BeautifulSoup(raw, 'html.parser')
    
    # get first products page
    products, next = get_products(base+target)

    # Loop through remaining pages
    while next:
        more_products, next = get_products(base+next)
        products += more_products
  
    with open('output.csv', 'w', newline='') as csvfile:
        title = ['Name', 'Description', 'Price', 'Rating']
        wr = csv.DictWriter(csvfile, fieldnames=title, delimiter='|', quotechar="'", quoting=csv.QUOTE_ALL)
        wr.writeheader()
        for p in products:
            wr.writerow(p)
  
if __name__ == "__main__":
  main()
