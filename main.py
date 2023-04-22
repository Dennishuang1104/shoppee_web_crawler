import requests
from urllib.parse import unquote
from service.Visual2wordApi import Visual2wordApi
import time
from service.WebDriver import WebDriver


def get_ids(url):
    shopid = int(url.split(".")[-2])
    itemid = int(url.split(".")[-1].split("?")[0])
    return itemid, shopid


def get_product_information(url):
    # get id
    itemid, shopid = get_ids(url.strip())
    # get price
    price_list = get_price(url, itemid)
    max_price = max(price_list)
    min_price = min(price_list)

    # get api for items json
    api = f"https://shopee.tw/api/v4/item/get?itemid={itemid}&shopid={shopid}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    }
    response = requests.get(api, headers=headers)
    items_data = response.json().get("data")
    print(items_data)
    name = items_data["name"]
    # price = items_data["price"] # 這是被hash 過後的值
    description = unquote(items_data["description"]).replace("\n", "")
    review = items_data["item_rating"]["rating_count"][0]
    if review == 0:
        rating = 0
    else:
        rating = round(sum([(i+1) * rate for i, rate in enumerate(items_data["item_rating"]["rating_count"][1:])])/review, 1)
    images_id_list = items_data['images']
    images_url_list = []
    for image_id in images_id_list:
        images_url_list.append(f'https://down-tw.img.susercontent.com/file/{image_id}"')

    type = items_data["fe_categories"][-1]["display_name"]
    sale_quantity = items_data["historical_sold"]
    shop_location = unquote(items_data["shop_location"])


    product = {
        "name": name,
        "max_price": max_price,
        "min_price": min_price,
        "description": description,
        "review": review,
        "rating": rating,
        "image_url":images_url_list,
        "type": type,
        "link": url.strip(),
        "sale_quantity": sale_quantity,
        "shop_location": shop_location
    }
    print(product)
    return product


def get_price(url, itemid):
    webdriver = WebDriver()
    webdriver.do_init()
    webdriver.driver.get(url)
    # 強制等待到元素完成再下一步
    # WebDriverWait(webdriver,10).until(EC.presence_of_element_located(By.ID))
    time.sleep(10)

    webdriver.driver.get_screenshot_as_file(f'./img/{itemid}.png')

    # 利用api 將截圖轉出價格
    visual2word = Visual2wordApi()
    price_list = visual2word.visual2word_find_price(f'{itemid}.png')

    return price_list


if __name__ == "__main__":
    url = 'https://shopee.tw/Python%E5%85%A5%E9%96%80%E6%95%99%E5%AE%A4%EF%BC%9A8%E5%A0%82%E5%9F%BA%E7%A4%8E%E8%AA%B2%E7%A8%8B-%E7%A8%8B%E5%BC%8F%E7%AF%84%E4%BE%8B%E7%B7%B4%E7%BF%92%EF%BC%8C%E4%B8%80%E6%AC%A1%E5%AD%B8%E6%9C%83Python%E7%9A%84%E5%8E%9F%E7%90%86%E6%A6%82%E5%BF%B5%E3%80%81%E5%9F%BA%E6%9C%AC%E8%AA%9E%E6%B3%95%E3%80%81%E5%AF%A6%E4%BD%9C%E6%87%89%E7%94%A8-%E5%A4%A7%E6%BE%A4%E6%96%87%E5%AD%9D%E3%80%90%E5%9F%8E%E9%82%A6%E8%AE%80%E6%9B%B8%E8%8A%B1%E5%9C%92%E3%80%91-i.206483013.4022517339'
    get_product_information(url)


