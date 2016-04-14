import os
import re
import requests
from bs4 import BeautifulSoup

from django.core.management import BaseCommand
from django.utils.translation import ugettext as _
from django.conf import settings


class Command(BaseCommand):
    args = ''
    help = _(u"""Parse base.html, \
find links to static files, download these files, \
replace external links to local""")

    APP_NAME = 'students'
    TEMPLATE_NAME = 'base.html'
    PATH_DIR_STATIC_CSS = os.path.join(settings.BASE_DIR, APP_NAME, 'static', 'css')
    PATH_DIR_STATIC_JS = os.path.join(settings.BASE_DIR, APP_NAME, 'static', 'js')
    PATH_TEMPLATE = os.path.join(settings.BASE_DIR, APP_NAME, 'templates', APP_NAME, TEMPLATE_NAME)

    def handle(self, *args, **options):

        # read template to string, make it unicode, and make the soup
        html_template = open(self.PATH_TEMPLATE).read()
        html_template = html_template.decode('utf-8')
        soup = BeautifulSoup(html_template, 'html.parser')

        # find all tags: <link rel='stylesheet'>, <script>
        # get all links
        tags_static_css = soup.findAll('link',
                                       rel='stylesheet',
                                       href=re.compile('^http[s]?.*\.css$'))
        tags_static_js = soup.findAll('script',
                                      src=re.compile('^http[s]?.*\.js$'))
        urls_static_css = [tag.attrs.get('href') for tag in tags_static_css]
        urls_static_js = [tag.attrs.get('src') for tag in tags_static_js]

        # download all the files to <app_name>/static
        # show progress of downloading
        print "Start downloading files:"
        for url in urls_static_css:
            result = self._download_static_file(url, self.PATH_DIR_STATIC_CSS)
            print _(u"Get file: %(filename)s; status: %(status)s" % result)
        for url in urls_static_js:
            result = self._download_static_file(url, self.PATH_DIR_STATIC_JS)
            print _(u"Get file: %(filename)s; status: %(status)s" % result)

        # make middleware for replacement:
        # replace all urls in soup - external to local

    def _download_static_file(self, url, dir_path):
        filename = url.split('/')[-1]
        local_file = os.path.join(dir_path, filename)
        requests.packages.urllib3.disable_warnings() # God blessed me
        try:
            response = requests.get(url, verify=False, stream=True, timeout=10)
            with open(local_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                f.close()
            download_status = 'OK'
        except:
            download_status = 'ERROR'
        return {'filename': filename, 'status': download_status}
