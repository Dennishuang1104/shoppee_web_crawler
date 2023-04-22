import os
import Environment as envi
from google.cloud import vision
import io
import re


class Visual2wordApi:
    def __init__(self):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = envi.GOOGLE_API_CRED
        vision.ImageAnnotatorClient()

    def visual2word(self, img_name):
        text_content = ''
        try:
            client = vision.ImageAnnotatorClient()
            file_name = os.getcwd() + '/img/' + img_name
            with io.open(file_name, 'rb') as image_file:
                content = image_file.read()
            image = vision.Image(content=content)
            response = client.text_detection(image=image)
            text_content = response.text_annotations[0].description
        except Exception as e:
            print(e)
        return text_content

    def visual2word_find_price(self, img_name):
        # price_regex_1 = re.compile(r'\$\d\d\s-\s\$\d\d\d')
        price_list = []
        try:
            client = vision.ImageAnnotatorClient()
            file_name = os.getcwd() + '/img/' + img_name
            with io.open(file_name, 'rb') as image_file:
                content = image_file.read()
                # print(content)
            image = vision.Image(content=content)
            response = client.text_detection(image=image)
            text_content = response.text_annotations[0].description
            price_regex = re.compile(r'\$[\d]{2}\s-\s\$[\d]{3}|\$[\d]{3}\s-\s\$[\d]{3}|\$[\d]{3}\s-\s\$[\d]{4}|\$[\d]{4}\s-\s\$[\d]{4}|\$[\d]{4}\s-\s\$[\d]{5}|\$[\d]{5}\s-\s\$[\d]{5}')
            price_list = price_regex.findall(text_content)
            if len(price_list) == 1:
                '''如果遇到有價格range時 例如：$12- $ 100'''
                print('get price (ranges)')
                price_list = price_list[0].replace('$', '').replace(' - ', ' ').split(' ', 1)
                price_list = list(map(int, price_list))
            else:
                '''如果遇到 單一價格 例如: $500'''
                price_regex = re.compile(r'\$[\d]{2}\s|\$[\d]{3}|\$[\d]{4}|\$[\d]{5}')
                price_list = price_regex.findall(text_content)
                price_list = price_list[1].replace('$', '').split(' ', 1)
                price_list = list(map(int, price_list))
                print('get price (single)')

        except Exception as e:
            print(e)

        return price_list


# if __name__ == '__main__':
#     test = Visual2wordApi()
#     text_content = test.visual2word('test.png')
#     test.visual2word_find_price(text_content)