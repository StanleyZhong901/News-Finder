import requests
from bs4 import BeautifulSoup
from replit import db
'''
Websites added to the Database:
  type in db.keys() in the console
  
What to work on:
  webScrape()
  - Make ABC work

  articleScrape()
  - Differentiate websites
  - Incorporate 9 News and ABC
'''
print(db.keys())
URL = input("Input Website: ")


def printInfo(header, hyperLink):
  print("\n=================================================================",
        end="\n")
  print("Heading:\n", header)
  # print("\nSummary:\n\t", articleScrape(hyperLink))
  print("\nLink: ", hyperLink)
  print("=================================================================",
        end="\n" * 2)


def webScrape(URL):
  if URL.upper() not in db:
    print("Website currently not available")
    return 1

  URL_HTML = db[URL.upper()]
  page = requests.get(URL_HTML)
  webContent = BeautifulSoup(page.text, "html.parser")

  # BBC

  if URL_HTML == db["BBC"]:
    most_read = webContent.find("div", class_="nw-c-most-read__items")
    most_read_articles = most_read.find("ol")

    for i in most_read_articles:
      header = i.find("span", class_="gs-c-promo-heading__title").string
      hyperLink = i.find("a")
      hyperLink = "https://www.bbc.com" + hyperLink.get('href')
      printInfo(header, hyperLink)

  # 9 News

  if URL_HTML == db["9NEWS"]:
    most_read = webContent.find("div", class_="content")
    most_read = most_read.find("div", class_="layout__inner")
    most_read_articles = most_read.find("article").parent

    for i in most_read_articles:
      header = i.find("h3").string
      hyperLink = i.find("a")
      hyperLink = hyperLink.get('href')
      printInfo(header, hyperLink)

  # ABC

  if URL_HTML == db["ABC"]:
    # most_read = webContent.find("div", class_="hEpq+ +6EL2").parent

    # for i in most_read:
    #   header = i.find("a").string
    #   hyperLink = i.find("a")
    #   hyperLink = "https://www.abc.net.au/" + hyperLink.get('href')
    #   printInfo(header, hyperLink)
    return 0


def articleScrape(URL):
  page = requests.get(URL)
  webContent = BeautifulSoup(page.text, "html.parser")

  # BBC
  summary = webContent.find("main")
  summary = summary.find("div", class_="ssrcss-1ocoo3l-Wrap e42f8511")
  summary = summary.find("b")
  return summary.string


webScrape(URL)
