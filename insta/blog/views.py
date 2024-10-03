from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseBadRequest,HttpResponseNotAllowed
from django.template import loader
from .models import Post,Comment
from .forms import PostForm,CommentForm


def listOfPosts(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            poste = form.save(commit=False)
            poste.author = request.user
            poste.save()
    else:
        form = PostForm()

    posts=Post.objects.all().values()
    template=loader.get_template('listofPosts.html')
    context = {
        'myposts':posts,
        'form': form
    }

    return HttpResponse(template.render(context, request))



def createPost(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            poste = form.save(commit=False)
            poste.author = request.user
            poste.save()
            return redirect('list_of_posts') 
    else:
        form = PostForm()

    template = loader.get_template('create_post.html')
    context = {'form': form}
    return HttpResponse(template.render(context, request))


def editPost(request, id):
    post = get_object_or_404(Post, id=id)
    if post.author!=request.user:
        return HttpResponseNotAllowed("not allowed.")
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('details', id=post.id) 
    else:
        form = PostForm(instance=post)

    return render(request, 'edit_post.html', {'form': form, 'post': post})

def delete_post(request, id):
    if request.method == 'POST': 
        post = get_object_or_404(Post, id=id)
        if post.author!=request.user:
            return HttpResponseNotAllowed("not allowed.")
        post.delete()
        return redirect('list_of_posts')  
    return HttpResponseBadRequest("Invalid request method.")

def postDetails(request, id):
    post = get_object_or_404(Post, id=id)
    comments=post.comments.all()

    return render(request, 'details.html', {'mypost': post, 'comments':comments})

def addComment(request, id):
    post = Post.objects.get(id=id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('details', id=id)
    else:
        form = CommentForm()

    template = loader.get_template('add_comment.html')
    context = {'form': form, 'post': post}
    return HttpResponse(template.render(context, request))

def main(request):
  template = loader.get_template('main.html')
  return HttpResponse(template.render())
    