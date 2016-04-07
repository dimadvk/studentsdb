from datetime import datetime

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
                response.write('<br />Request took: %s' % str(
                    time_delta))
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

        queries_time = 0
        for query in connection.queries:
            query_time = query.get('time')
            queries_time += float(query_time)

        if 'text/html' in response.get('Content-Type', ''):
            response.write('<br />SQL queries took: %s' % str(
                queries_time))

        return response
