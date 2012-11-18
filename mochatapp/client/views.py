from django.views.generic.base import TemplateView

class ChatPageView(TemplateView):
    template_name = "client/chat_page.html"
