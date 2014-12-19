#from .settings import PORTAL_URL
def students_proc(request):
    current_uri = '{scheme}://{host}'.format(scheme=request.scheme, host=request.get_host())
    return {'PORTAL_URL': current_uri}
#    return {'PORTAL_URL': PORTAL_URL}

