from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import BoardModel, Comment, Reply
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.http import HttpResponseRedirect
from .forms import CommentForm, ReplyForm

# Create your views here.
def signupfunc(request):
    if request.method == 'POST':
        username2 = request.POST['username']
        password2 = request.POST['password']       
        try:
            User.objects.get(username=username2)
            return render(request,'signup.html',{'error':'This user is already registered'})        
        except :            
            user = User.objects.create_user(username2, '', password2)
            print(request.POST)
        return render(request,'signup.html',{'some':100})
    return render(request,'signup.html',{'some':100})

def loginfunc(request):
    if request.method == 'POST':
        username2 = request.POST['username']
        password2 = request.POST['password'] 

        user = authenticate(request, username=username2, password=password2)
        if user is not None:
            login(request, user)
            # Redirect to a success page.   
            return redirect('list')         
        else:
            # Return an 'invalid login' error message.
            return redirect('login')
    return render(request,'login.html')
   
@login_required
def listfunc(request):
    object_list = BoardModel.objects.all()
    return render(request,'list.html',{'object_list':object_list})

def logoutfunc(request):
    logout(request)
    return redirect('login')

def detailfunc(request,pk):
    object = BoardModel.objects.get(pk=pk)
    return render(request,'detail.html',{'object':object})

def goodfunc(request,pk):
    post = BoardModel.objects.get(pk=pk)
    post.good = post.good+1
    post.save()
    return redirect('list')

def readfunc(request, pk):
    post = BoardModel.objects.get(pk=pk)
    post2 = request.user.get_username()
    if post2 in post.readtext:
        return redirect('list')
    else:
        post.read += 1
        post.readtext = post.readtext + '' + post2
        post.save()
        return redirect('list')

class BoardCreate(CreateView):
    template_name = 'create.html'
    model = BoardModel
    fields = ('title','content','author','images')
    success_url = reverse_lazy('list')

class CommentCreate(CreateView):
    template_name = 'comment_form.html'
    model = Comment
    form_class = CommentForm
    
    def form_valid(self, form):
        comment = form.save(commit=False)
        post_pk = self.kwargs['pk']
        comment.post = get_object_or_404(BoardModel, pk=post_pk)
        comment.save()
        return redirect('detail', pk=post_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_pk = self.kwargs['pk']
        context['post'] = get_object_or_404(BoardModel, pk=post_pk)
        return context
    
class ReplyCreate(CreateView):
    template_name = 'reply_form.html'
    model = Reply
    form_class = ReplyForm

    def form_valid(self, form):
        reply = form.save(commit=False)
        comment_pk = self.kwargs['pk']
        reply.comment = get_object_or_404(Comment, pk=comment_pk)
        reply.save()
        return redirect('detail', pk=reply.comment.post.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment_pk = self.kwargs['pk']
        context['comment'] = get_object_or_404(Comment, pk=comment_pk)
        return context


