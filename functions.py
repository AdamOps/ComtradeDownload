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
    """Set all the parameters for the data you wish to retrieve. Everything has a default value, so
    it's not necessary to set every single parameter. The options per parameter are:
        reporter: id number of reporting country. Pass as string, e.g. "258" or "All"
        partners: id number of partner country. Pass as string, e.g. "97" or "All"
        frequency: Either annual "A" or monthly "M"
        year: The year you wish to get data for. Pass as string, e.g. "2011". If you're grabbing monthly data,
            pass it as YYYYMM here, e.g. "201206"
        imports_or_exports: Get either imports "1" or exports "2"
        goods_or_services: Fetch either goods "C" or services "S"
        classification: Pass whether you want to use the harmonised system "HS" or another format here. "HS" is
            by far the best default, so only change this if you're really sure.
            The options are:
            "HS", "H0", "H1", "H2", "H3", "H4", "ST", "S1", "S2", "S3", "S4", "BEC", "EB02"
        classification_code: Digit level of data. "AG6" is 6-digits. The options are:
            "TOTAL", "AG1", "AG2", "AG3", "AG4", "AG5", "AG6", "ALL"
        return_format: Return the data as either "csv" or "json".
        max_return: Maximum length of the returned file. UN also maintains its own limits.
            For guests this is 100000, for licensed users 250000.
        heading_style: Whether the returned file has human "H" or machine "M" headers.
        auth_token: Your authorization token, if you have one. This is optional.
        imts_definition: Either "2010", or "orig". Best to stick to 2010 here.
        """
    parameters = {
        "reporter": reporter,
        "frequency": frequency,
        "year": year,
        "classification": classification,
        "partners": partners,
        "imports_or_exports": imports_or_exports,
        "classification_code": classification_code,
        "return_format": return_format,
        "max_return": max_return,
        "goods_or_services": goods_or_services,
        "heading_style": heading_style,
        "auth_token": auth_token,
        "imts_definition": imts_definition,
    }

    # parameters = {
    #     "r": reporter,
    #     "freq": frequency,
    #     "ps": year,
    #     "px": classification,
    #     "p": partners,
    #     "rg": imports_or_exports,
    #     "cc": classification_code,
    #     "fmt": return_format,
    #     "max": max_return,
    #     "type": goods_or_services,
    #     "head": heading_style,
    #     "token": auth_token,
    #     "IMTS": imts_definition,
    # }

    return parameters


def generate_link(parameters, use_token):
    url = "http://comtrade.un.org/api/get?" + \
          "r=" + parameters['reporter'] + \
          "&ps=" + parameters['year'] + \
          "&freq=" + parameters['frequency'] + \
          "&px=" + parameters['classification'] + \
          "&p=" + parameters['partners'] + \
          "&rg=" + parameters['imports_or_exports'] + \
          "&cc=" + parameters['classification_code'] + \
          "&fmt=" + parameters['return_format'] + \
          "&max=" + parameters['max_return'] + \
          "&type=" + parameters['goods_or_services'] + \
          "&head=" + parameters['heading_style'] + \
          "&IMTS=" + parameters['imts_definition']

    if parameters['auth_token'] != "":
        url += "&token=" + parameters['auth_token']

    return url
