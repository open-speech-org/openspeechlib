"""
Utility functions for HTTP

This will be used as proxy in case we don't want to rely on requests in the future
"""
from urllib import parse
import requests

get = requests.get

HTTPError = requests.exceptions.HTTPError

def extract_query_param_from_url_string(url, param):
    parsed_url = parse.urlparse(url)
    return parse.parse_qs(parsed_url.query).get(param)
