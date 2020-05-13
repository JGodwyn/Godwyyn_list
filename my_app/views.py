from urllib.parse import quote_plus

from django.shortcuts import render
from . import models
import requests
from bs4 import BeautifulSoup
from requests.compat import quote_plus

BASE_CRAIGLIST_URL = 'https://accra.craigslist.org/search/?query={}'
BASE_CRAIGLIST_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'


def index(request):
    return render(request, 'my_app/index.html')


def search(request):
    search_input = request.POST.get('search')
    models.Search.objects.create(search = search_input)
    final_url = BASE_CRAIGLIST_URL.format(quote_plus(search_input))
    # quote_plus adds a '+' whenever a space is encountered in writing the text
    response = requests.get(final_url)
    # requests encapsulates a 'request' object
    # meaning that you can call stuffs like:
    # requests.status_code, requests.content, request.text
    data = response.text
    # get the textual data related with the object (that is, the HTML declarations)
    soup = BeautifulSoup(data, features='html.parser')
    # create a 'BeautifulSoup' object that takes all the HTMl declarations
    # 'html.parser' in features' means that it should be taken as a HTML doc

    post_listings = soup.find_all('li', {'class': 'result-row'})
    # find all the 'list' that belongs to the class 'result-row' as defined in the HTML doc

    post_list = []
    # dont really mind this file i opened, it is just to pull all the data-ids into a file
    # since they are large and i don't wanna print them on my console

    for post in post_listings:
        post_title = post.find(class_='result-title').text  # get the text in the class called 'result-title'
        post_url = post.find('a').get('href')  # get the 'text of the link'

        if post.find(class_='result-price'):
            post_price = post.find(
                class_='result-price').text  # if there is a price, get the text written in the class called 'result-price'
        else:
            post_price = 'N/A'

        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            # what the above code essentially does is that it gets the text written in the 'data-ids' of a 'result-image' class
            # the text returned is a long list where each id is separated by a comma.
            # the split method takes the string and splits it into a list wherever it sees a comma.
            # the first item in the list is called and further split where the string ':' is encountered
            # the 2nd item in the resulting list is then taken
            post_image = BASE_CRAIGLIST_IMAGE_URL.format(post_image_id)
        else:
            post_image = 'https://accra.craigslist.org/images/peace.jpg'

        post_list.append((post_title, post_url, post_price, post_image))

    stuff_for_frontend = {'search_input': search_input,
                          'post_list': post_list
                          }

    return render(request, 'my_app/new_search.html', stuff_for_frontend)


def craiglist(request):
    return render(request, 'my_app/craiglist.html')
