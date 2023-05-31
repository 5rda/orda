from django import template
from bs4 import BeautifulSoup

register = template.Library()

@register.filter
def get_first_image_from_content(content):
    soup = BeautifulSoup(content, 'html.parser')
    img_tag = soup.find('img')
    if img_tag:
        return img_tag['src']
    else:
        return None