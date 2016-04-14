from datetime import datetime
import re
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
                soup = BeautifulSoup(response.content)
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
            soup = BeautifulSoup(response.content)
            time_measure_tag = soup.new_tag('code', style='margin-left:20px')
            time_measure_tag.append('SQL queries took: %s' % str(time_queries))
            soup.body.insert(0, time_measure_tag)
            response.content = soup.prettify(soup.original_encoding)

        return response
