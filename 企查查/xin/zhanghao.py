import requests,re
url='https://www.yinsiduanxin.com/'
con=requests.get(url).content.decode('utf-8').replace('\n','').replace('\t','').replace('\r','')
conts=re.findall(' <a href="/(\w+)-phone-number/verification-code-(\d+)\.html" class="clickA"',con)
for cont in conts:
    tell=cont[1]
    link='https://www.yinsiduanxin.com/'+cont[0]+f'-phone-number/verification-code-{tell}.html'
    con1 = requests.get(link).content.decode('utf-8').replace('\n', '').replace('\t', '').replace('\r', '')

    print('vv')