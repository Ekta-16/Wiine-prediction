from bs4 import BeautifulSoup
from six.moves import urllib
import sys
import math
import json
import traceback


def getSoup(url):
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers = {'User-Agent': user_agent, }
    request = None
    response = None
    data = None
    try:
        request = urllib.request.Request(url, None, headers)
        response = urllib.request.urlopen(request)
        data = response.read()
        soup = BeautifulSoup(data, "html.parser")
        return soup
    except:
        pass


def getInfo(type, soup):
    items = soup.find_all("li")
    for listItem in items:
        if listItem.find("div", {"class": "info-label"}).find("span").get_text() == type:
            return listItem.find("div", {"class": "info"}).find("span").get_text()


url = "https://www.winemag.com/wine-ratings/"
wine_categories_soup = getSoup(url).find(id="drink-type-filter")

categories = wine_categories_soup.find_all('option')

categories_list = []
item = 0

for category in categories:
    if category['value']:
        categories_list.append(category.text)
category_lower_limit = -1
category_upper_limit = 15

print(categories_list)
try:
    for category in categories_list:
        if category_lower_limit == category_upper_limit:
            break
        else:
            category_lower_limit += 1
        category = str(categories_list[category_lower_limit]).strip().replace(" ", "%20")
        child_url = "https://www.winemag.com/?s=&search_type=reviews&drink_type=wine&varietal=" + category
        response = getSoup(child_url)
        if response is not None:
            reviews_counter = response.find("span", {'class': 'results-count'})
            # print(reviews_counter.get_text().replace(" ", ""))
            # print(reviews_counter.get_text().split(" "))
            index = reviews_counter.get_text().find("of") + 3
            counter = reviews_counter.get_text()[index:]
            pages = None
            # pages = int(math.ceil(float(counter[0] + counter[1])/20))
            # print(counter, "!!", pages)
            if "," in counter:
                counter = counter.split(",")
                pages = int(math.ceil(float(counter[0] + counter[1]) / 20))
            else:
                pages = int(math.ceil(float(counter) / 20))
            print("Pages = ", pages, " | Category = ", category)
            for page in range(1, pages):
                print("Page = ", page)
                targetUrl = "https://www.winemag.com/?s=&search_type=reviews&drink_type=wine&varietal=" + category + "&page=" + str(
                    page)
                reviews = getSoup(targetUrl)
                if reviews is not None:
                    reviews_bag = reviews.find_all("a", {"class": "review-listing row"})
                    # print(reviews_bag)
                    if reviews_bag is not None:
                        for review_item in reviews_bag:
                            try:
                                wine_review_link = review_item['href']
                                wine_review_id = review_item['data-review-id']
                                wine_review_soup = getSoup(wine_review_link)
                                # for attributes
                                wine_review_title = review_item.find("h3", {"class": "title"}).get_text()
                                print (wine_review_title)
                                wine_review_points = review_item.find("span", {"class": "rating"}).find(
                                    "strong").get_text()
                                wine_editors_choice_flag = review_item.find("span", {"class": "badge"})
                                if wine_editors_choice_flag is not None:
                                    wine_editors_choice_flag = "yes"
                                else:
                                    wine_editors_choice_flag = "no"
                                    wine_review_price = review_item.find("span", {"class": "price"}).get_text()
                                    wine_review_description = wine_review_soup.find("p",
                                                                                    {"class": "description"}).get_text()
                                    items = wine_review_soup.find("ul", {"class": "primary-info"})
                                    wine_review_designation = getInfo("Designation", items)
                                    wine_review_appellation = getInfo("Appellation", items)
                                    wine_review_winery = getInfo("Winery", items)
                                    wine_review_variety = getInfo("Variety", items)
                                    sub_items = wine_review_soup.find("ul", {"class": "secondary-info"})
                                    wine_alcohol_percentage = getInfo("Alcohol", sub_items)
                                    wine_type = getInfo("Category", sub_items)
                                    wine_review_publish_date = getInfo("Date Published", sub_items)
                                    wine_review_photo_link = \
                                        wine_review_soup.find("div", {"class": "wine-img-for-medium"}).find("a").find(
                                            "img")["src"]
                                    taster_name = wine_review_soup.find("span", {"class": "taster-area"})
                                    if taster_name is not None:
                                        taster_name = taster_name.find("a").get_text()
                                    else:
                                        taster_name = "N/A"
                                    # taster_img = wine_review_soup.find("div",{"class":"taster"}).find("img")["src"]
                                    # taster_description = wine_review_soup.find("div",{"class":"taster"}).find("div",{"class":"long-description"}).get_text()
                                    # Review Dictionary
                                    review_dict = {wine_review_id: {
                                        "id": wine_review_id,
                                        "title": wine_review_title,
                                        "rating": wine_review_points,
                                        "wine_review_link": wine_review_link,
                                        "editors_choice": wine_editors_choice_flag,
                                        "price": wine_review_price,
                                        "description": wine_review_description,
                                        "designation": wine_review_designation,
                                        "location": wine_review_appellation,
                                        "winery": wine_review_winery,
                                        "variety": wine_review_variety,
                                        "wine_review_image_link": wine_review_photo_link,
                                        "alcohol_percentage": wine_alcohol_percentage,
                                        "wine_type": wine_type,
                                        "wine_review_publish_date": wine_review_publish_date,
                                        "taster_name": taster_name
                                    }
                                    }
                                    print(review_dict)
                                    with open('winemag_crawled_data.json', 'a') as json_file:
                                        if (item != 0):
                                            json_file.write(",")
                                        json.dump(review_dict, json_file)
                                        item += 1
                            except:
                                traceback.print_exc()
                                continue

except Exception as e:
    traceback.print_exc()
finally:
    readJson = None
    with open('winemag_crawled_data.json', 'r') as json_file:
        readJson = json_file.read()
    with open('winemag_crawled_data.json', 'w') as json_file:
        json_file.write("[" + readJson + "]")
