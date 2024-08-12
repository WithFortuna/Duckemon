# -*- coding: utf-8 -*-

import requests

from pokebase.cache import get_sprite_path, load, load_sprite, save, save_sprite
from pokebase.common import api_url_build, sprite_url_build


#함수: resource 반환
def _call_api(endpoint, resource_id=None, subresource=None):
    url = api_url_build(endpoint, resource_id, subresource)
    # print(f"=========================================위치: before call request , \n url: {url} \n resource_id: {resource_id}, soubresource = {subresource}============================================")

    # Get a list of resources at the endpoint, if no resource_id is given.
    get_endpoint_list = resource_id is None

    response = requests.get(url)
    response.raise_for_status()

    data = response.json() #case 1: resource 1개
    # print(f"=========================================위치: _call_api , \n url: {url}============================================")
    if get_endpoint_list and data["count"] != len(data["results"]): #case 2: resource 2개 이상
        # We got a section of all results; we want ALL of them.
        items = data["count"]
        num_items = dict(limit=items)

        response = requests.get(url, params=num_items)
        response.raise_for_status()

        data = response.json()

    return data


#함수: 리소스 fetch (있으면 캐시, 없으면 call_api 후 캐싱)
def get_data(endpoint, resource_id=None, subresource=None, **kwargs): #**kwargs: 딕셔너리 자료형을 의미
    # print(f"==========================위치: get_data, endpoint:{endpoint} resource_id: {resource_id}, subresource: {subresource}")

    if not kwargs.get("force_lookup", False):
        try:
            data = load(endpoint, resource_id, subresource)
            return data
        except KeyError:
            pass
    data = _call_api(endpoint, resource_id, subresource)
    save(data, endpoint, resource_id, subresource)

    return data


#함수: api호출하여 sprite 리소스 반환
def _call_sprite_api(sprite_type, sprite_id, **kwargs):
    url = sprite_url_build(sprite_type, sprite_id, **kwargs)

    response = requests.get(url)
    response.raise_for_status()

    abs_path = get_sprite_path(sprite_type, sprite_id, **kwargs)
    data = dict(img_data=response.content, path=abs_path)

    return data

#함수: sprite 리소스 fetch(있으면 캐시, 없으면 call_sprite_api 후 캐싱)
def get_sprite(sprite_type, sprite_id, **kwargs):
    if not kwargs.get("force_lookup", False):
        try:
            data = load_sprite(sprite_type, sprite_id, **kwargs)
            return data
        except FileNotFoundError:
            pass

    data = _call_sprite_api(sprite_type, sprite_id, **kwargs)
    save_sprite(data, sprite_type, sprite_id, **kwargs)

    return data
