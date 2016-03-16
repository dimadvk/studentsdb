from django.views.generic import ListView

from ..models.action import Action

from ..util import paginate


class ActionListView(ListView):
    model = Action
    template_name = 'students/action_journal.html'
    queryset = Action.objects.all().order_by('timestamp').reverse()
    context_object_name = 'actions'

    def get_context_data(self, **kwargs):
        # get context dara from TemplateView class
        context = super(ActionListView, self).get_context_data(**kwargs)
        #context = paginate(self.queryset, 10, self.request, context)
        return context


