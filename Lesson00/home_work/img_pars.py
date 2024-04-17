
from io import BytesIO
import requests
from PIL import Image

from bs4 import BeautifulSoup
# pip install lxml

# url = 'https://en.wikipedia.org/wiki/Cat'
#
# response = requests.get(url)
# html = response.text
#
# soup = BeautifulSoup(html, 'lxml')
# img_tags = soup.find_all('img')
#
# img_links = [img['src'] for img in img_tags]
# print(img_links)
# url = "https://cdn.britannica.com/mendel/eb-logo/MendelNewThistleLogo.png"
#
# img = url.split('/')[-1]
# response = requests.get(url)
# image = Image.open(BytesIO(response.content))
# image.save(img)
# res = requests.get(url).text
# file_name = url[-12:]
# with open("Logo.png", 'w', encoding="utf-8") as f:
#     f.write(res)
str = "/media/icyb342r/cats-protection_master-logo_purple_rgb-110.png"
str2 = "https://www.cats.org.uk"
st = str2.join(str)
print(st)

