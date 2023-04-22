from selenium import webdriver
from selenium.webdriver.common.by import By
from service.WebDriver import WebDriver
import time


def get_cat_urls():
    # url = 'https://shopee./'
    url = 'https://shopee.tw/%E7%81%8C%E5%BF%83%E6%A3%89-%E5%86%B0%E5%B3%B6%E6%AF%9B%E7%B7%9A-2cm-%E5%86%B0%E5%B3%B6%E7%B7%9A-%E8%B6%85%E7%B2%97%E6%AF%9B%E7%B7%9A-%E6%89%8B%E5%B7%A5%E7%B7%A8%E7%B9%94%E5%8C%85%E5%8C%85%E6%AF%AF%E5%AD%90%E5%AF%B5%E7%89%A9%E8%B2%93%E7%AA%A9%E7%8B%97%E7%AA%A9%E6%8A%B1%E6%9E%95%E5%BA%8A%E5%9C%8D-%E7%89%B9%E7%B2%97%E6%AF%9B%E7%B7%9A-%E7%81%8C%E8%8A%AF%E6%A3%89-%E5%86%B0%E6%A2%9D%E7%B7%9A-%E7%B2%97%E6%AF%9B%E7%B7%9A-%E6%A3%89%E7%B7%9A-i.2371119.16188939174?sp_atk=8c56b1a5-7edd-4a86-a8d6-9cccec5b04e9&xptdk=8c56b1a5-7edd-4a86-a8d6-9cccec5b04e9'
    webdriver = WebDriver()
    webdriver.do_init()
    webdriver.driver.get(url)
    time.sleep(10)
    webdriver.driver.get_screenshot_as_file(f'test_2.png')
    # img_rgb = Image.open(f"test.png")

    #
    # visual_api = Visual2wordApi()
    # title_origin = visual_api.visual2word(f'test.png')
    # title_origin = re.sub('\n', '', title_origin).strip()
    # test_word = title_origin.encode('utf-8')
    # print(test_word)
    # driver.get(url)
    # # sleep
    # driver.implicitly_wait(2)
    #
    # urls = []
    # list_cat = driver.find_elements(By.CSS_SELECTOR, 'li.image-carousel__item')
    # for cat in list_cat:
    #     # catcol = cat.find_element(By.CSS_SELECTOR, 'div.home-category-list__group')
    #     list_catcol_item = cat.find_elements(By.CSS_SELECTOR, 'a.home-category-list__category-grid')
    #     for catcol_item_link in list_catcol_item:
    #         urls.append(catcol_item_link.get_attribute('href'))
    # driver.quit()
    # # save to file
    # with open('cat_urls.txt', 'w') as f:
    #     for url in urls:
    #         f.write(str(url))
    #         f.write('\n')
    # return urls


def get_full_urls():
    # load cat urls from file
    with open('cat_urls.txt', 'r') as f:
        urls = f.read().splitlines()

    driver = webdriver.Chrome()
    full_urls = []

    for url in urls:
        driver.get(url)
        driver.implicitly_wait(5)
        number_of_page = int(
            driver.find_element(By.CSS_SELECTOR, 'span.shopee-mini-page-controller__total').get_attribute(
                'textContent'))
        print('Number of page: ', number_of_page)
        for i in range(1, number_of_page):
            print('Page: ', i, 'of', number_of_page)
            list_product = driver.find_elements(By.CSS_SELECTOR, 'div.col-xs-2-4.shopee-search-item-result__item')
            for product in list_product:
                try:
                    # scroll to element
                    driver.execute_script("arguments[0].scrollIntoView();", product)
                    url = product.find_element(By.CSS_SELECTOR, 'a')
                    full_urls.append(url.get_attribute('href'))
                except:
                    pass
            # next page
            driver.find_element(By.CSS_SELECTOR,
                                'button.shopee-button-outline.shopee-mini-page-controller__next-btn').click()

    driver.quit()
    print(len(full_urls))
    print('Done get full urls')
    # save to file
    with open('urls.txt', 'w') as f:
        for url in full_urls:
            f.write(str(url))
            f.write('\n')
    print('Done save to file')


# if __name__ == '__main__':
#     get_cat_urls()