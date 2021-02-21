import urllib.request
import urllib.parse
import urllib.error
import twurl
import json
import ssl
import geo
import webbrowser
import os.path
# https://apps.twitter.com/
# Create App and get the four strings, put them in hidden.py

TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'
TWITTER_URL_2 = 'https://api.twitter.com/1.1/users/show.json'


def infos_about_friends(twitter_account):
    """
    This function returns informstion about user`s friends and their locations.
    """
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    url = twurl.augment(TWITTER_URL,
                        {'screen_name': twitter_account, 'count': '20'})
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()
    js = json.loads(data)
    lst = []
    for friend in js['users']:
        if friend['location'] != '':
            tup = friend['screen_name'], friend['location']
            lst.append(tup)
    return lst


def infos_about_user(twitter_account):
    """
    This function returns informstion about user location.
    """
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    url = twurl.augment(TWITTER_URL_2, {'screen_name': twitter_account})
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()
    js = json.loads(data)
    return js['screen_name'], js['location']


def main(account):
    """
    This function creates the map.
    """
    lst_of_friends = infos_about_friends(account)
    user = infos_about_user(account)
    diction = geo.create_dictionary(lst_of_friends)
    user_location = geo.find_latitude_and_longtitude(user)
    html = geo.create_map(diction, user_location)
    path = os.path.abspath(html)
    url = 'file://' + path
    webbrowser.open(url)
    return html
