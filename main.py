import requests
from bs4 import BeautifulSoup
from replit import db

print(db.keys())

URL = input("Input Website: ")
try:
  URL_HTML = db[URL.upper()]
except KeyError:
  print("Not in List")


def printInfo(header, hyperLink):
  print("\n=================================================================",
        end="\n")
  print("Heading:\n", header)
  print("\nSummary:\n\t", summaryScrape(hyperLink))
  print("\nLink: ", hyperLink)
  print("=================================================================",
        end="\n" * 2)


def summaryScrape(URL):
  page = requests.get(URL)
  webContent = BeautifulSoup(page.text, "html.parser")

  # BBC
  if URL_HTML == db["BBC"]:
    try:
      summary = webContent.find("main")
      summary = summary.find("div", class_="ssrcss-1ocoo3l-Wrap e42f8511")
      summary = summary.find("b").string
    except AttributeError:
      paragraphs = webContent.find("article")
      paragraphs = paragraphs.find_all("p")
      summary = ""
      for i in range(3):
        summary += "- "
        summary += paragraphs[i].text
        summary += "\n\t"
    return summary

  # 9 News
  if URL_HTML == db["9NEWS"]:
    paragraphs = webContent.find("div", class_="article__body-croppable")
    paragraphs = paragraphs.find("div", class_="block-content")
    summary = "- "
    summary += paragraphs.text
    summary += "\t\n"
    return summary

  # ABC
  if URL_HTML == db["ABC"]:
    try:
      dot_points = webContent.find("div", class_="EOO2n Mznbg")
      dot_points = dot_points.find("ul", class_="LoaHX")
      summary = ""
      for li in dot_points:
        summary += "- "
        summary += li.text
        summary += "\n\t"
    except TypeError:
      paragraphs = webContent.find("div", class_="EOO2n Mznbg")
      paragraphs = paragraphs.find_all("p")
      for i in range(3):
        summary += "- "
        summary += paragraphs[i].text
        summary += "\n\t"
    return summary

  if URL_HTML == db["ANIMENEWSNETWORK"]:
    return 0


def webScrape(URL):

  if URL.upper() not in db:
    return 1

  page = requests.get(URL_HTML)
  webContent = BeautifulSoup(page.text, "html.parser")

  if URL_HTML == db["BBC"]:
    most_read = webContent.find("div", class_="gs-u-pb++ gs-u-box-size")
    most_read = most_read.find(
      "div", class_="nw-c-most-read__items gel-layout gel-layout--no-flex")
    most_read_articles = most_read.find("ol")

    for i in most_read_articles:
      hyperLink = i.find("a")
      hyperLink = "https://www.bbc.com" + hyperLink.get('href')
      header = requests.get(hyperLink)
      header = BeautifulSoup(header.text, "html.parser")
      header = header.find("h1").string
      printInfo(header, hyperLink)

  if URL_HTML == db["9NEWS"]:
    most_read = webContent.find("div", class_="content")
    most_read = most_read.find("div", class_="layout__inner")
    most_read_articles = most_read.find("div", class_="feed__stories")
    counter = 0
    for i in most_read_articles:
      counter += 1
      header = i.find("h3").string
      hyperLink = i.find("a")
      hyperLink = hyperLink.get('href')
      printInfo(header, hyperLink)
      if counter == 10:
        break  
  if URL_HTML == db["ABC"]:
    most_read = webContent.find("div", class_="hEpq+ +6EL2")

    for i in most_read:
      header = i.find("a").string
      hyperLink = i.find("a")
      hyperLink = "https://www.abc.net.au" + hyperLink.get('href')
      printInfo(header, hyperLink)

  if URL_HTML == db["ANIMENEWSNETWORK"]:
    most_read = webContent.find("div", id="mainfeed")


if URL:
  webScrape(URL)