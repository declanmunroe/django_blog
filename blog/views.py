from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from .forms import BlogPostForm, BlogCommentForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.

def show_posts(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, "blogposts.html", { 'posts': posts })
    
def view_post(request, id):
    this_post = get_object_or_404(Post, pk=id)
    comments = Comment.objects.filter(post=this_post)
    form = BlogCommentForm()

    return render(request, "viewpost.html", {'post': this_post, 'comments': comments, "form" : form})
    
def add_post(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            """
            #(commit=False) means the form saves but does not get added to the database because we need to
            #add the author and the created date which were not specified in the forms.py
            #We then add that in the lines below and then do a post.save() which writes to
            #the database because all the neccesercery fields from the model are now specified.
            """
            post.author = request.user
            post.created_date = timezone.now()
            post.published_date = timezone.now()
            post.save()
            return redirect(view_post, post.pk) # points to the function get_index above
    else:
        # GET Request so just give them a blank form
        form = BlogPostForm()    
    
    return render(request, "addform.html", { 'form': form })
    
# def edit_post(request, id):
#     post = get_object_or_404(Post, pk=id)
    
#     if request.method == "POST":
#         form = BlogPostForm(request.POST, instance=post)
#         if form.is_valid():
#             #post = form.save(commit=False)
#             form.save()
#             return redirect(view_post, id)
#     else:
#         form = BlogPostForm(instance=post)
#     """
#     The if else statement above. When I am on the homepage and i can see all the blog posts when i click on read more it is performing
#     a get request from the view post function. When i click the edit button it runs the edit_post function. After the get object404 it
#     runs the else part of the if else statment because it is getting the form from the database in its current state. If i make no changes
#     or make a change once i hit the save/submit button it fires off the POST and in that case it runs the if statement. So in this case
#     the if else statement is back to front. We can if we want split the edit post function into two functions. One for GET and one for POST.
#     """
    
#     return render(request, "addform.html", { 'form': form })
@login_required(login_url="/accounts/login")
def edit_post(request, id):
    post = get_object_or_404(Post, pk=id)
    
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.created_date = timezone.now()
            post.published_date = timezone.now()
            post.save()
            return redirect(view_post, post.pk)
    else:
        form = BlogPostForm(instance=post)
    
    return render(request, "addform.html", { 'form': form })
    
def add_comment(request, id):
    post = get_object_or_404(Post, pk=id)
    form = BlogCommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        return redirect(view_post, post.pk) # points to the function get_index above



