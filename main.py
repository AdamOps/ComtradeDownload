import pandas as pd
import requests

urlList = []


def set_params(reporter="all",
               partners="97",
               frequency="A",
               year="2021",
               imports_or_exports="1",
               goods_or_services="C",
               classification="HS",
               classification_code="AG6",
               return_format="csv",
               max_return="10000",
               heading_style="H",
               auth_token="",
               imts_definition="2010"):
    parameters = {
        "r": reporter,
        "freq": frequency,
        "ps": year,
        "px": classification,
        "p": partners,
        "rg": imports_or_exports,
        "cc": classification_code,
        "fmt": return_format,
        "max": max_return,
        "type": goods_or_services,
        "head": heading_style,
        "token": auth_token,
        "IMTS": imts_definition,
    }

    return parameters


def generate_link(parameters, use_token):
    url = "http://comtrade.un.org/api/get?" + \
          "r=" + parameters['r'] + \
          "&ps=" + parameters['ps'] + \
          "&freq=" + parameters['freq'] + \
          "&px=" + parameters['px'] + \
          "&p=" + parameters['p'] + \
          "&rg=" + parameters['rg'] + \
          "&cc=" + parameters['cc'] + \
          "&fmt=" + parameters['fmt'] + \
          "&max=" + parameters['max'] + \
          "&type=" + parameters['type'] + \
          "&head=" + parameters['head'] + \
          "&IMTS=" + parameters['IMTS']

    if parameters['token'] != "":
        url += "&token=" + parameters['token']

    print(url)
    return url


new_request_params = set_params(reporter="528",
                                year="2021",
                                frequency="A",
                                classification="HS",
                                partners="4",
                                imports_or_exports="1",
                                classification_code="AG6",
                                return_format="csv",
                                max_return="10000",
                                goods_or_services="C",
                                heading_style="H",
                                imts_definition="2010")


new_request_url = generate_link(new_request_params, False)
response = requests.get(new_request_url)



# http://comtrade.un.org/api/get?max=50000&type=C&freq=A&px=HS&ps=2013&r=826&p=0&rg=all&cc=AG2&fmt=json
