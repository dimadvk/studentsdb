from django.http import HttpResponseRedirect
from django.conf import settings


def set_language(request):
    # get path refferer
    return_path = request.GET.get('return-path', '/')
    response = HttpResponseRedirect(return_path)
    # get lang_code of selected language
    selected_language = request.GET.get('lang', 'en')
    # set cookie
    max_age = 10*365*24*60*60 # ten years
    response.set_cookie(
        settings.LANGUAGE_COOKIE_NAME,
        selected_language,
        max_age=max_age)
    return response

