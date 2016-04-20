from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.urlresolvers import reverse


def set_language(request):
    if request.method == "POST":
        # get path refferer
        return_path = request.POST.get('return-path', reverse('home'))
        response = HttpResponseRedirect(return_path)
        # get lang_code of selected language
        selected_language = request.POST.get('lang', settings.LANGUAGE_CODE)
        # set cookie
        max_age = 10*365*24*60*60 # ten years
        response.set_cookie(
            settings.LANGUAGE_COOKIE_NAME,
            selected_language,
            max_age=max_age)
        return response

