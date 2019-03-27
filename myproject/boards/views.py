from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse, Http404
from .models import Board, Topic, Post
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    #return HttpResponse('Hello, World!')
    boards=Board.objects.all()
    return render(request,'home.html',{'boards':boards})


def board_topics(request,pk):
    # try:
    #     board=Board.objects.get(pk=pk)
    # except Board.DoesNotExist:
    #     raise Http404
    board=get_object_or_404(Board,pk=pk)
    return render(request,'topics.html',{'board':board})


def new_topic(request,pk):
    board=get_object_or_404(Board,pk=pk)

    if request.method == 'POST':
        subject = request.POST['subject']
        message = request.POST['message']

        user=User.objects.first()   #临时使用一个账号作为登入用户

        topic=Topic.objects.create(
            subject=subject,
            board=board,
            starter=user
        )

        post=Post.objects.create(
            message=message,
            topic=topic,
            created_by=user
        )

        return redirect('board_topics',pk=board.pk) #redirect to the created topic page

    return render(request,'new_topic.html',{'board':board})