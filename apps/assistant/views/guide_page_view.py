from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class GuidePageView(LoginRequiredMixin, TemplateView):
    """
    User guide and documentation page for Dandi AI Assistant.
    Explains capabilities, prompting tips, multi-turn memory, and safety.
    """
    template_name = 'assistant/guide.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'راهنمای جامع دستیار هوشمند دَندی'
        return context
