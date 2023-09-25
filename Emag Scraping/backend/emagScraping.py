from selenium.webdriver.chrome.options import Options

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient


def launchBrowser():
    chrome_options = Options()
    chrome_options.add_argument("start-maximized")
    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://www.emag.ro/")
    return driver

global driver
driver = launchBrowser()


a = ActionChains(driver)

megamenu_titles_list = []

labeled_subcategories_links_list = []

product_names = []


def get_megamenu_titles_list(megamenu_list):

    returned_megamenu_titles = []
    megamenu_list_titles = megamenu_list.find_elements(By.TAG_NAME, "li")
    for item in megamenu_list_titles:
        title = item.find_element(By.CLASS_NAME, "megamenu-list-department__department-name")

        if title.text != "":
            returned_megamenu_titles.append(title.text.split("\n"))

    return returned_megamenu_titles

def remove_special_characters(string,special_characters):

    for l in special_characters:
        string = string.replace(l, '')

    return string


def get_labeled_subcategories_links(subcategories):

    for s in subcategories:
        megamenu_items = s.find_elements(By.CSS_SELECTOR, ".megamenu-item")
        for m in megamenu_items:
            labels = m.find_elements(By.CSS_SELECTOR, ".megamenu-item .label")
            if labels != []:

                for l in labels:
                    if l.text == "Nou" or l.text == "Promo":

                        selected_subcategory = m
                        labeled_subcategories_links_list.append(selected_subcategory.get_attribute("href"))

    return labeled_subcategories_links_list

def create_product_dictionary(category,name,link,image_source):

    dictionary = {}

    dictionary["category"] = category
    dictionary["name"] = name
    dictionary["link"] = link
    dictionary["image_source"] = image_source

    return dictionary

def remove_duplicates_from_list(list):

    return [i for j, i in enumerate(list) if i not in list[j + 1:]]


def insert_into_db(list1,list2):

    cluster = MongoClient("mongodb+srv://ioana:scraper123@cluster0.v8fml.mongodb.net/scraper?retryWrites=true&w=majority")

    db = cluster["scraper"]
    collection = db["products"]

    collection.drop()

    if list1 != []:
        collection.insert_many(list1)

    if list2 != []:
        collection.insert_many(list2)


try:
        megamenu_list = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "megamenu-list")),
        )


        megamenu_titles_list = get_megamenu_titles_list(megamenu_list)

        for title in megamenu_titles_list:
            title_string = str(title)

            title_string = remove_special_characters(title_string, "[']")

            hover_title = driver.find_element(By.LINK_TEXT, title_string)
            a.move_to_element(hover_title).perform()


            megamenu_hover_details = WebDriverWait(driver, 30).until(
             EC.presence_of_element_located((By.CLASS_NAME, "megamenu-details"))
             )

            megamenu_hover_details_list = megamenu_hover_details.find_elements(By.TAG_NAME, "li")

            for item in megamenu_hover_details_list:

                subcategories = item.find_elements(By.CSS_SELECTOR, ".megamenu .collapse")
                labeled_subcategories_links_list = get_labeled_subcategories_links(subcategories)

        super_pret_dictionary_list = []
        top_favorite_dictionary_list = []


        for link in labeled_subcategories_links_list:
            driver.get(link)

            page = 1
            while True:

                products_collection = driver.find_elements(By.CSS_SELECTOR, ".card-collection")
                if products_collection != []:
                    products = driver.find_elements(By.CSS_SELECTOR, ".card-collection .card-item")

                    for product in products:
                        badges = product.find_elements(By.CSS_SELECTOR, ".card-v2-badge-cmp")
                        if badges != []:
                            for badge in badges:

                                product_details = product.find_element(By.CSS_SELECTOR, ".card-v2 .card-v2-title")
                                name = product_details.text
                                link = product_details.get_attribute("href")
                                image_source = product.find_element(By.CSS_SELECTOR,".card-v2 .card-v2-thumb img").get_attribute("src")
                                category = badge.text

                                if category == "Super Pret":
                                    super_pret_dictionary_list.append(create_product_dictionary(category, name, link, image_source))

                                elif category == "Top Favorite":
                                    top_favorite_dictionary_list.append(create_product_dictionary(category, name, link, image_source))

                else:
                    break


                page += 1

                if page > 2:
                    break
                else:
                    next_page = driver.find_element(By.CSS_SELECTOR, ".pagination-sm>li>a")
                    a.move_to_element(next_page).click().perform()


finally:
        driver.quit()


super_pret_dictionary_list = remove_duplicates_from_list(super_pret_dictionary_list)
top_favorite_dictionary_list = remove_duplicates_from_list(top_favorite_dictionary_list)


insert_into_db(super_pret_dictionary_list, top_favorite_dictionary_list)



