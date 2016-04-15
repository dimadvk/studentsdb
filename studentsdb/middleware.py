import re
import os
from datetime import datetime
from bs4 import BeautifulSoup

from django.http import HttpResponse
from django.conf import settings
from django.db import connection


class RequestTimeMiddleware(object):
    """Display request time on a page"""

    def process_request(self, request):
        if settings.DEBUG == False:
            return None
        request.start_time = datetime.now()
        return None

    def process_response(self, request, response):
        if settings.DEBUG == False:
            return response
        # if our process_request was canceled somewhere within
        # middleware stack, we can not calculate request time

        if not hasattr(request, 'start_time'):
            return response

        request.end_time = datetime.now()
        time_delta = request.end_time - request.start_time
        if 'text/html' in response.get('Content-Type', ''):
            if time_delta.seconds < 2:
                #response.write('<br />Request took: %s' % str(
                #    time_delta))
                # -
                #insert_text = '<body><code style="margin-left:20px;">Request took: ' + str(time_delta) + '</code>'
                #response.content = re.sub('\<body\>', insert_text, response.content)
                # -
                soup = BeautifulSoup(response.content, 'lxml')
                # response.content may be empty in case of HttpResponseRedirct object
                if soup.body:
                    time_measure_tag = soup.new_tag('code', style='margin-left:20px')
                    time_measure_tag.append('Request took: %s' % str(time_delta))
                    soup.body.insert(0, time_measure_tag)
                    response.content = soup.prettify(soup.original_encoding)
            else:
                response = HttpResponse('''
                    <h2>It took more than 2 seconds to make the response.<br>
                    Please, remaster your code!<h2>''')

        return response

    def process_view(self, request, view, args, kwargs):
        return None

    def process_template_response(self, request, response):
        return response

    def process_exception(self, request, exception):
        return HttpResponse('Exception found: %s' % exception)


class SqlQueriesTimeMiddleware(object):
    """Display on a page the time of sql queries"""

    def process_response(self, request, response):
        if settings.DEBUG == False:
            return response

        time_queries = 0
        for query in connection.queries:
            query_time = query.get('time')
            time_queries += float(query_time)

        if 'text/html' in response.get('Content-Type', ''):
            #insert_text = '<body><code style="margin-left:20px;">SQL queries took: ' + str(time_queries) + '</code>'
            #response.content = re.sub('\<body\>', insert_text, response.content)
            # -
            #response.write('<br />SQL queries took: %s' % str(
            #    time_queries))
            soup = BeautifulSoup(response.content, 'lxml')
            # response.content may be empty in case of HttpResponseRedirct object
            if soup.body:
                time_measure_tag = soup.new_tag('code', style='margin-left:20px')
                time_measure_tag.append('SQL queries took: %s' % str(time_queries))
                soup.body.insert(0, time_measure_tag)
                response.content = soup.prettify(soup.original_encoding)

        return response


class LocalizeStaticMiddleware(object):
    """Process links for static files, replase external links to local links if file exists."""

    def process_response(self, request, response):
        if settings.DEBUG == False:
            return response
        if not hasattr(settings, 'LOCALIZE_STATIC'):
            return response
        # 
        #LOCALIZE_STATIC = {
        #    'app_name': 'students',
        #    'static_css_dir': 'css',
        #    'static_js_dir': 'js'
        #}

        if 'text/html' in response.get('Content-Type', ''):
            # get initial data
            localize_data = settings.LOCALIZE_STATIC

            # create soup:
            soup = BeautifulSoup(response.content, 'lxml')

            ## process css
            # get all links to static files
            tags_static_css = soup.findAll(
                'link',
                rel='stylesheet',
                href=re.compile('^http[s]?.*\.css$'))
            # for every link:
                # get construct filename + absolute path
                # check with os.path.isfile
                # if True - replace link
            for tag in tags_static_css:
                url = tag.attrs.get('href')
                filename = url.split('/')[-1]
                file_path = os.path.join(
                    settings.BASE_DIR,
                    localize_data.get('app_name'),
                    'static',
                    localize_data.get('static_css_dir'),
                    filename)

                if os.path.isfile(file_path):
                    tag.attrs.update(
                        {'href': os.path.join(
                            settings.STATIC_URL,
                            localize_data.get('static_css_dir'),
                            filename)
                        }
                    )
            ## process js
            # get all links to static files
            tags_static_js = soup.findAll(
                'script',
                src=re.compile('^http[s]?.*\.js$'))
            # for every link:
                # get construct filename + absolute path
                # check with os.path.isfile
                # if True - replace link
            for tag in tags_static_js:
                url = tag.attrs.get('src')
                filename = url.split('/')[-1]
                file_path = os.path.join(
                    settings.BASE_DIR,
                    localize_data.get('app_name'),
                    'static',
                    localize_data.get('static_js_dir'),
                    filename)

                if os.path.isfile(file_path):
                    tag.attrs.update(
                        {'src': os.path.join(
                            settings.STATIC_URL,
                            localize_data.get('static_js_dir'),
                            filename)
                        }
                    )

            response.content = soup.prettify(soup.original_encoding)
        return response
