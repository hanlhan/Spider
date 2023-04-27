import re

from github import Github
from bs4 import BeautifulSoup



def find_html_images(html):
    a = re.findall("<img.*/>", html)
    return a

def find_html_image_src(html):
    soup = BeautifulSoup(html, 'html.parser')
    image_src=soup.img["src"]
    return image_src


def find_md_images(md):
    b = re.findall("!.*\)", md)
    return b


def find_md_image_src(md):
    b = re.findall("\(.*\)", md)
    return b


if __name__ == "__main__":
    html = "dddd<img src=\"/i/eg_tulip.jpg\"  alt=\"上海鲜花港 - 郁金香\" />eeee"

    images_html=find_html_images(html)
    print(images_html)
    print(find_html_image_src(images_html[0]))
    str_url = "['![Result Pic](./cang.jpg)']"

    print(find_md_images(str_url))
    image_md=find_md_images(str_url)
    print(find_md_image_src(image_md[0]))
