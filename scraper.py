import requests
import re
import json
from bs4 import BeautifulSoup
import utils


class Auto():

    def __init__(self, soup, href):
        self.id = utils.get_id()
        self.href = href
        self.title = self.get_title_from_soup(soup)
        self.price = self.get_price_from_soup(soup)
        self.mileage = self.get_mileage_from_soup(soup)
        self.color, self.power = self.get_color_and_power_from_soup(soup)
        self.description = self.get_description_from_soup(soup)
        self.download_picture(soup)


    def get_dict_data(self):
        data = {
            'id': self.id,
            'href': self.href,
            'title': self.title,
            'price': self.price,
            'mileage': self.mileage,
            'color': self.color,
            'power': self.power,
            'description': self.description
        }
        return data


    def get_title_from_soup(self, soup):
        title_elem = soup.find_all("h1", {"class": "sc-ellipsis sc-font-xl"})
        return title_elem[0].text


    def get_price_from_soup(self, soup):
        price_elem = soup.find_all("h2", {"class": "sc-highlighter-xl"})
        return re.sub("[^0-9]", "", price_elem[0].text)


    def get_color_and_power_from_soup(self, soup):
        color = ''
        power = ''
        elems = soup.find_all("ul", {'class': 'columns'})
        for elem in elems:
            li_elems = elem.find_all('li')
            for li in li_elems:
                div_elems = li.find_all('div')
                for i in range(len(div_elems)):
                    text = div_elems[i].text
                    if text == 'Farbe':
                        color = div_elems[i + 1].text
                    if text == 'Leistung':
                        power = int(div_elems[i + 1].text.split(' kW')[0])
        return (color, power)


    def get_mileage_from_soup(self, soup):
        mileage = ''
        elems = soup.find("div", {"class": "data-basic1"})
        elem_div = elems.find_all('div', {'class': 'itemspace'})
        for el in elem_div:
            divs = el.find_all('div')
            for i in range(len(divs)):
                text = divs[i].text
                if text == 'Kilometer':
                    mileage = divs[i + 1].text
        return float(mileage.split(' km')[0]) if not isinstance(mileage, str) else 0


    def get_description_from_soup(self, soup):
        text = soup.find("div", {"data-target": "[data-item-name='description']"}).text
        return re.sub(r'[^A-z0-9]', ' ', text)


    def download_picture(self, soup):
        elems = soup.find_all("img", {"class": "gallery-picture__image"})
        if elems != []:
            folder_name = '\\data\\' + str(self.id)
            utils.create_folder(folder_name)
            for i in range(4):
                img_link = elems[i].get('data-src')
                resp = requests.get(img_link)
                out = open(f"data\\{self.id}\\auto_img_{i}.jpg", "wb")
                out.write(resp.content)
                out.close()


def get_auto_links():
    links_list = []
    counter = 1
    while True:
        url = f'https://www.truckscout24.de/transporter/gebraucht/kuehl-iso-frischdienst/renault?currentpage={counter}'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        elements = soup.find_all('a', {'data-item-name': 'detail-page-link'})
        if elements != []:
            link = "https://www.truckscout24.de/" + elements[0].get('href')
            links_list.append(link)
            counter += 1
        else: break
    return links_list


def get_auto_info():
    result = []
    auto_links = get_auto_links()
    for link in auto_links:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        auto = Auto(soup, link).get_dict_data()
        result.append(auto)
    return result


def write_json_data(data):
    new_date = {'data':[i for i in data]}
    with open('data/data.json', 'w') as f:
        json.dump(new_date, f, ensure_ascii=True)


def start_scraper():
    utils.create_folder('\\data')
    info = get_auto_info()
    write_json_data(info)



start_scraper()