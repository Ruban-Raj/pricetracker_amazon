import requests
from bs4 import BeautifulSoup
import lxml
import smtplib

#url = "https://www.amazon.com/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6"
iphone_amazon_url = "https://www.amazon.in/Apple-iPhone-15-Pro-256/dp/B0CHX5J2ND/ref=sr_1_1_sspa?crid=2ZV8KTV45ZYCB&keywords=iphone%2B15%2Bpro&qid=1703104163&sprefix=iphone%2Caps%2C248&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&"
#from https://myhttpheader.com/ header
my_useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
accept_lang = "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,kn;q=0.6"
accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
cookie = "PHPSESSID=bafb20166ddf18f765a5c0c9032b820b; _ga=GA1.2.899350711.1703101842; _gid=GA1.2.604778690.1703249266; _gat=1; _ga_VL41109FEB=GS1.2.1703273186.3.0.1703273186.0.0.0"
target = 200000

header = {
    "User-Agent": my_useragent,
    "Accept-Language": accept_lang,
    # "Accept": accept,
    # "Cookie": cookie,
    # "Request Line": "GET / HTTP/1.1",
    # "sec-ch-ua": "'Not_A Brand';v='8', 'Chromium';v='120', 'Google Chrome';v='120'",
    # "x-forwarded-proto": "https",
    # "Accept-Encoding": "gzip, deflate, br",
    # "x-https": "on",
    # "X-Forwarded-For": "136.185.31.51",
    # "sec-ch-ua-platform": "macOS",
    # "sec-fetch-dest": "document",
    # "sec-fetch-user": "?1",
    # "sec-fetch-mode": "navigate",
    # "sec-fetch-site": "none",
    # "upgrade-insecure-requests": "1",
    # "dnt": "1",
    # "ec-ch-ua-mobile": "?0",
    # "Cache-Control": "max-age=0",
}

iphone_html = requests.get(iphone_amazon_url, headers=header)
iphone_html.raise_for_status()
amazon_data = iphone_html.text
#print(amazon_data)

soup = BeautifulSoup(amazon_data, "lxml")
#print(soup.prettify())
iphone_price_data = soup.find(class_="a-offscreen").get_text()
iphone_price = iphone_price_data.split("₹")[1]
# iphone_price = iphone_price_data.get_text()
iphone_price_clean = iphone_price.replace(',', '')
iphone_price_float = float(iphone_price_clean)
print(iphone_price_float)
#print(type(iphone_price_float))

#email server config
my_email = "rubanmercy1@gmail.com"
password = "yjgtvdwnpoealdra"
receiver_email = "ruban.raj@amagi.com"

product_title = soup.find(class_="a-size-large product-title-word-break").get_text()
print(product_title)


if iphone_price_float < target:
    with  smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=my_email, password=password)
                connection.sendmail(from_addr=my_email, to_addrs=[receiver_email], msg=f"Subject:PRICE DROP ALERT FOR {product_title}\n\nPrice dropped for {product_title}\nThe current price is {iphone_price_float}\nURL to book {iphone_amazon_url}")

