from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView
from .forms import CommentForm
# Create your views here.
class CommentView(TemplateView):
    http_method_names = ['post']
    template_name = 'comment/result.html'

    def post(self,request,*args,**kwargs):
        target=request.POST.get('target')
        comment_form=CommentForm(request.POST)

        if comment_form.is_valid():
            instance=comment_form.save(commit=True)
            instance.target=target
            instance.save()
            succeed=True
            return redirect(target)
        else:
            succeed=False
            context={
                'succeed':succeed,
                'comment_form':comment_form,
                'target':target,
            }
            return self.render_to_response(context)
