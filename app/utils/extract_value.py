def get_base_url_till_given_string(request,string):
    return ''.join(request.base_url.split(string)[0])+string+'/'
