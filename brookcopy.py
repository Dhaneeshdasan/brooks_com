import requests
from bs4 import BeautifulSoup
import csv

class brooky():
    base_url = 'https://angelheartboutique.com{}'
    def __init__(self,homeurl):
        self.home_url=homeurl
        self.soup=self.get_soup(self.home_url)
        self.all_products=[]
    def get_soup(self,link_url):
        res=requests.get(link_url)
        return BeautifulSoup(res.content,"lxml")
    
    
    def write_to_csv(self, file_name:str ,data:list) -> None:
        with open(file_name,'w') as file:
            keys = data[0].keys()
            print('starting to write to '+ file_name)
            csv_file = csv.DictWriter(file,keys)
            csv_file.writeheader()
            csv_file.writerows(data)
            print('written successfully')
    
    def get_category(self):
        homepage_url=self.soup
        category_urls = [each.a['href'] for each in homepage_url.find('ul',class_="m-main-nav__items").findAll('li',class_="m-main-nav__item") if each]
        needed_url=category_urls[0:4]
        print(needed_url)
        
        
        if needed_url:
            for each in needed_url:
                url = self.base_url.format(each) if 'http' not in each else each
                if url:
                    listpage_response = self.get_soup(url)
                    if listpage_response:
                        page_counter = 2
                        self.category_listpage(listpage_response,url)
            if self.all_products:
                self.write_to_csv('brooks_com.csv' , self.all_products)

                        
    def category_listpage(self,listpage_response,current_url):

        products = listpage_response.select(".m-product-tile")
        if products:
            print(current_url)
            for product in products:
                
                try:
                    item={}
                    try:
                        item['title'] = product.find('h2', 'a-type-h5 a-type-h5--big m-product-tile__name').text
                    except:
                        item['title'] = None
                     
                    try:
                        item['offer_price'] = product.find('span', 'pricing__sale small--red').text
                    except:
                        item['offer_price'] = None
                        
                    try: 
                        item['price'] = product.find('span','pricing__base small--strike').text if not '\n' else product.find('span','pricing__sale small--red' ).text
                    except:
                        item['price'] = None   
                   
        
     
                    try:
                        item['image_url'] = product.find('picture', 'a-responsive-image').img['src']
                    except:
                        item['image_url'] = None
                    try:
                        item['product_url'] = product.find('div','o-products-grid__item-content').div.a['href']
                    except:
                        item['product_url'] = None
                except Exception as e:
                    print('Exception found {}'.format(e))
                print('scrapped ',item['title'])
                self.all_products.append(item)
                
        print(self.all_products)

        
    
obj=brooky("https://www.brooksrunning.com/en_us")
obj.get_category()