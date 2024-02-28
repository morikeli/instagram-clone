from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View


@method_decorator(login_required(login_url='login'), name='get')
class InboxMessagesView(View):
    template_name = 'core/messages.html'


    def get(self, request, *args, **kwargs):

        context = {}
        return render(request, self.template_name, context)
    
