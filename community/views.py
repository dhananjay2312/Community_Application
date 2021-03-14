from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404,redirect
from .models import Post
from .forms import Queryform
from django.utils import timezone
from .forms import PostFrom
from django.http import HttpResponse
from .models import QueryForm
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from .models import Question,Answer,Comment,UpVote,DownVote
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import AnswerForm,QuestionForm
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth import views as auth_views

# Create your views here.
def indexView(request):
    return render(request,'index.html')

def about_us(request):
    return render(request,'about_us.html')
def services(request):
    posts=Post.objects.all()
    return render(request,'services.html',{'posts':posts})
def queries(request):
    return render(request,'query.html')
def contact_us(request):
    return render(request,'contact_us.html')






@login_required
def dashboardView(request):
    return render(request,'dashboard.html')

def registerView(request):
    if request.method=="POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login_url")
    else:
        form = UserCreationForm()
    return render(request,'registration/register.html',{'form':form})


def post_detail(request,pk):
    post=get_object_or_404(Post,pk=pk)
    return render(request,'postdetail.html',{'post':post})


def post_new(request):
    if request.method == "POST":
        form = PostFrom(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date=timezone.now()
            post.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = PostFrom()
    return render(request,'post_edit.html',{'form': form})



def post_edit(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method == "POST":
        form = PostFrom(request.POST,instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = PostFrom(instance=post)
    return render(request,'post_edit.html',{'form':form})
    # return HttpResponse(form)


def post_remove(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.delete()
    return redirect('post_list')


def post_list(request):
    posts=Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    #posts=Post.objects.order_by('created_date')
    return render(request,'post_list.html',{'posts':posts})

"""
def queries(request):
    query = QueryForm.objects.all()
    if request.method == 'POST':
        form = Queryform(request.POST)
        if form.is_valid():
            form.save()
            # send email code goes here
            return HttpResponse('Thanks for contacting us!')
    else:
        form = Queryform()

    return render(request, 'queries.html',{'form':form,'query':query})"""


def save_comment(request):
    if request.method=='POST':
        comment=request.POST['comment']
        answerid=request.POST['answerid']
        answer=Answer.objects.get(pk=answerid)
        user=request.user
        Comment.objects.create(
            answer=answer,
            comment=comment,
            user=user
        )
        return JsonResponse({'bool':True})

def save_upvote(request):
    if request.method=='POST':
        answerid=request.POST['answerid']
        answer=Answer.objects.get(pk=answerid)
        user=request.user
        check=UpVote.objects.filter(answer=answer,user=user).count()
        if check > 0:
            return JsonResponse({'bool':False})
        else:
            UpVote.objects.create(
                answer=answer,
                user=user
            )
            return JsonResponse({'bool':True})


def save_downvote(request):
    if request.method=='POST':
        answerid=request.POST['answerid']
        answer=Answer.objects.get(pk=answerid)
        user=request.user
        check=DownVote.objects.filter(answer=answer,user=user).count()
        if check > 0:
            return JsonResponse({'bool':False})
        else:
            DownVote.objects.create(
                answer=answer,
                user=user
            )
            return JsonResponse({'bool':True})






def ask_form(request):
    form=QuestionForm
    if request.method=='POST':
        questForm=QuestionForm(request.POST)
        if questForm.is_valid():
            questForm=questForm.save(commit=False)
            questForm.user=request.user
            questForm.save()
            messages.success(request,'Question has been added.')
    return render(request,'ask-question.html',{'form':form})



def tag(request,tag):
    quests=Question.objects.annotate(total_comments=Count('answer__comment')).filter(tags__icontains=tag).order_by('-id')
    paginator=Paginator(quests,10)
    page_num=request.GET.get('page',1)
    quests=paginator.page(page_num)
    return render(request,'tag.html',{'quests':quests,'tag':tag})



def tags(request):
    quests=Question.objects.all()
    tags=[]
    for quest in quests:
        qtags=[tag.strip() for tag in quest.tags.split(',')]
        for tag in qtags:
            if tag not in tags:
                tags.append(tag)
    # Fetch Questions
    tag_with_count=[]
    for tag in tags:
        tag_data={
            'name':tag,
            'count':Question.objects.filter(tags__icontains=tag).count()
        }
        tag_with_count.append(tag_data)
    return render(request,'tags.html',{'tags':tag_with_count})



# Detail
def detail(request,id):
    quest=Question.objects.get(pk=id)
    tags=quest.tags.split(',')
    answers=Answer.objects.filter(question=quest)
    answerform=AnswerForm
    if request.method=='POST':
        answerData=AnswerForm(request.POST)
        if answerData.is_valid():
            answer=answerData.save(commit=False)
            answer.question=quest
            answer.user=request.user
            answer.save()
            messages.success(request,'Answer has been submitted.')
    return render(request,'detail.html',{
        'quest':quest,
        'tags':tags,
        'answers':answers,
        'answerform':answerform
    })



# Home Page
def queries(request):
    if 'q' in request.GET:
        q=request.GET['q']
        quests=Question.objects.annotate(total_comments=Count('answer__comment')).filter(title__icontains=q).order_by('-id')
    else:
        quests=Question.objects.annotate(total_comments=Count('answer__comment')).all().order_by('-id')
    paginator=Paginator(quests,10)
    page_num=request.GET.get('page',1)
    quests=paginator.page(page_num)
    return render(request,'query.html',{'quests':quests})




def profile(request):
    quests=Question.objects.filter(user=request.user).order_by('-id')
    answers=Answer.objects.filter(user=request.user).order_by('-id')
    comments=Comment.objects.filter(user=request.user).order_by('-id')
    upvotes=UpVote.objects.filter(user=request.user).order_by('-id')
    downvotes=DownVote.objects.filter(user=request.user).order_by('-id')
    return render(request,'profile.html',{
        #'form':form,
        'quests':quests,
        'answers':answers,
        'comments':comments,
        'upvotes':upvotes,
        'downvotes':downvotes,
    })
