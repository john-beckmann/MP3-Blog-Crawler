import requests
import os
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse
from time import sleep
import re


def fetch(url){
    response = requests.get(url)

    if not response or not response.status_code or response.status_code != 200:
        return ""
    else:
        return response.text
}


def crawlBlog(url):
    global numFound

    if len(foundBlogs) >= 5:
        return
    
    searchURL = urlPrefix + url + urlMiddle + htmlMimeType + urlSuffix
    response = fetch(searchURL)

    if not response:
        return

    entry = response.partition('\n')[0]
    archiveUrl = formatUrl(entry)
    htmlResponse = fetch(archiveUrl)

    if not htmlResponse:
        return

    htmlString = htmlResponse.replace("\n", " ")
    blogRollList = re.findall("href=\"(https://web.archive.org/web/.*?)\"", htmlString)

    for blogUrl in blogRollList:
        if len(foundBlogs) >= 5:
            return
        if blogUrl.find(url) == -1 and blogUrl.find("myspace") == -1 and blogUrl.find("beatport") == -1 and blogUrl.find("junodownload") == -1 and blogUrl.find("soundcloud") == -1 and blogUrl.find("html") == -1 and blogUrl.find("php") == -1 and blogUrl.find("?") == -1 and blogUrl.find("djdownload") == -1 and blogUrl.find("beatsdigital") == -1 and blogUrl.find(".mp3") == -1:
            blog = re.sub("https://web.archive.org/web/(.*?)/", "", blogUrl)
            
            if "/" == blog[len(blog) - 1] and blog.find("http") != -1:
                searchAudioURL = urlPrefix + blog + urlMiddle + audioMimeType + urlSuffix
                audioList = fetch(searchAudioURL)

                if audioList:    
                    foundBlogs.add(blog)
                
                    if len(foundBlogs) > numFound:
                        numFound = len(foundBlogs)
                        print(str(numFound) + ": " + blog)
                        crawlBlog(blog)

def formatUrl(url):
    tokens = url.split(" ")
    webId = tokens[0]
    
    webTokens = tokens[1].split(")")
    pathUrl = webTokens[1]
    brokenDomain = webTokens[0]

    domainTokens = brokenDomain.split(",")
    domainTokens = domainTokens[::-1]

    domain = "http://"

    for tok in domainTokens:
        domain = domain + tok + "."

    domainLen = len(domain)
    domain = domain[:domainLen-1]
    mp3Url = "https://web.archive.org/web/" + webId + "/" + domain + pathUrl
    return mp3Url


urlPrefix = "https://web.archive.org/cdx/search/cdx?url="
urlMiddle = "*&filter=statuscode:200&filter=mimetype:"
urlSuffix = "&collapse=urlkey&fl=timestamp,urlkey"
audioMimeType = "audio/mpeg"
htmlMimeType = "text/html"

numFound = 1
rootBlog = "http://kidcityblog.com/"
print(str(numFound) + ": " + blog)
foundBlogs = {rootBlog}
crawlBlog(rootBlog)
print(foundBlogs)