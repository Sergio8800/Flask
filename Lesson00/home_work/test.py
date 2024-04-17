import requests as requests

s = ' 020342<img src="img_girl.jpg" alt="Girl in a jacket" width="500" height="600"> avsdf4v f3214tf'
s = s.split('<')[1].split('>')[0]

print(s)
s = s.split('src="')[1].split('"')[0]
print(s)
urls = ['https://www.britannica.com/animal/cat',
'https://www.cats.org.uk/cats-blog/9-things-to-know-before-getting-your-first-cat',
'https://www.smithsonianmag.com/smart-news/cats-prey-on-more-than-2000-different-species-180983429/',
'https://www.python.org/',
'https://pixabay.com/ru/',
        'https://gb.ru/',
]

for url in urls:
    html = url.replace('//','=').split('/')[0].replace("=","//")
    # html = url.split('/')[0]
    print(html)
    s = requests.get(url).text
    with open('file.txt', 'w', encoding="utf-8") as f:
        # f.write(s)f
        f.writelines(s)
        img = []
        with open('file.txt', 'r', encoding='utf-8') as f:
            coutt = len(f.readline())
            coutt2 = 0
            for s in f:
                coutt2 +=1
                if '<img' in s:
                    s = s.split('<')[1].split('>')[0]
                    if "src=" in s:
                        s = s.split('src="')[1].split('"')[0]
                        img.append((s,coutt2))
            print(img)
                    # print(s)
        print(img)

    # f.readline(s)

import requests # делаем запрос на чтение страницы https://sky.pro/media/
# response = requests.get('https://sky.pro/media/')
# print(response.ok)  # проверяем успешен ли запрос?
# print(response.text)  # выводим полученный ответ на экран
# response = requests.get('https://httpbin.org/image', headers={'Accept': 'image/jpeg'})
# print(response.headers)
# response = requests.get('https://httpbin.org/image/jpeg')
# print(response.content)

# response = requests.get('https://httpbin.org/get') # зарание известно, что это джейсон ответ
# print(response.text)
# json_response = response.json()
# print(json_response)