from geopy.geocoders import Nominatim
import folium
import pandas as pd
import os.path


def find_latitude_and_longtitude(tup):
    """
    This function finds latitude and longitude of city.
    >>> find_latitude_and_longtitude(('USA', 'New York'))
    (40.7127281, -74.0060152)
    """
    geolocator = Nominatim(user_agent="map")
    loc = geolocator.geocode(tup[1])
    if loc is not None:
        lat = loc.latitude
        longt = loc.longitude
        location = lat, longt
        return tup[0], location
    else:
        return None


def create_dictionary(lst):
    dictionary = {}
    for tup in lst:
        tupl = find_latitude_and_longtitude(tup)
        if tupl != None:
            dictionary[tupl[0]] = tupl[1]
    return dictionary


def create_map(diction, user_loc):
    """
    This function returns html map with two layers:
    'Film locations' shows user's location on the map and locations of films;
    'Population' shows population in countries.
    >>> create_map(os.path.realpath('locations.csv'), (43.9876, 22.9873))
    'map1.html'
    """
    map = folium.Map()
    same = []
    friends_loc = folium.FeatureGroup(name='Friends locations')
    diff = -0.02
    for friend in diction.keys():
        lt = diction[friend][0]
        lg = diction[friend][1]
        same.append(lt)
        if lt in same:
            lt += diff
            lg += diff
            diff -= 0.02
        friends_loc.add_child(folium.Marker(location=[lt, lg],
                                         popup=friend,
                                         icon=folium.Icon()))
    lat = user_loc[1][0]
    if lat in same:
        lat += diff
        diff -= 0.02
    friends_loc.add_child(folium.Marker(location=[lat, user_loc[1][1]],
                                        popup=user_loc[0],                                        
                                        icon=folium.Icon(color='red')))
    map.add_child(friends_loc)
    map.add_child(folium.LayerControl())
    map.save('map.html')
    return 'map.html'
# print(create_map(create_dictionary([('Медиазона', 'Москва'), ('Татьяна Щукина', 'http://m.vk.com/tanchaizer2327'), ('ден(дэн)', 'Санкт-Петербург, Россия'), ('Леван Горозия', 'Moscow'), ('Артём Ионов', 'Самара, Россия'), ('Катя Клэп', 'Russia'), ('Anthony Jeselnik', 'Los Angeles'), ('Cyberpunk 2077', 'Night City, Free State of California'), ('kass', 'Амстердам'), ('Restorator', 'SPB'), ('ли🌈🌈ка', 'Saint Petersburg, Russia'), ('Гаер Андрей', 'Россия'), ('Денис Чужой', 'Москва'), ('ЕГОР', 'Russia'), ('Юрий Дудь', 'Москва')])))
