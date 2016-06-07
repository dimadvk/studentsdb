#from time import sleep
from django.views.generic import ListView

from ..models.action import Action

# from ..util import paginate


class ActionListView(ListView):
    model = Action
    template_name = 'students/action_journal.html'
    queryset = Action.objects.all().order_by('timestamp').reverse()[:100]
    context_object_name = 'actions'
    #
    # def get_context_data(self, **kwargs):
    #     context = super(ActionListView, self).get_context_data(**kwargs)
    #     context = paginate(self.queryset, 10, self.request, context, var_name='actions')
    #     # sleep(1)
    #     return context


