from django.shortcuts import render, HttpResponse, redirect
from blog.models import Post, BlogComment
from django.contrib import messages
from blog.templatetags import extras

# Create your views here.
def blogHome(request):
    allPosts = Post.objects.all()
    params={'allPosts':topPosts}
    return render(request,'blog/blogHome.html',params)

def blogPost(request,slug):
    post = Post.objects.filter(slug=slug).first()
    post.views = post.views +1
    post.save()
    comments = BlogComment.objects.filter(post=post,parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict={}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    count = comments.count()
    if count == 0:
        params={'post':post,'comments':comments,'count':count,'noComments':True}
    else:
        if len(replyDict)!=0:
            params={'post':post,'comments':comments,'count':count,'noComments':False,'replyDict':replyDict,'replies':True}
        else:
            params={'post':post,'comments':comments,'count':count,'noComments':False,'replyDict':replyDict,'replies':False}
    return render(request,'blog/blogPost.html',params)

def postComment(request):
    if request.method == 'POST':
        try:
            comment = request.POST.get('comment')
            user = request.user 
            postSno = request.POST.get('postSno')
            parentSno = request.POST.get('parentSno')
            post = Post.objects.get(sno = postSno)
            if len(comment) < 3:
                messages.error(request,'Comment is either blank or too short!')
                return redirect(f'/blog/{post.slug}')
            if parentSno == '':
                newComment = BlogComment(comment=comment,user=user,post=post)
                newComment.save()
                messages.success(request,'Your comment has been successfully posted!')
            else:
                sno = request.POST.get('sno')
                parent = BlogComment.objects.get(sno=sno)
                newComment = BlogComment(comment=comment,user=user,post=post,parent=parent)
                newComment.save()
                messages.success(request,'Your reply has been successfully posted!')

            return redirect(f'/blog/{post.slug}')
        except Exception as e:
            messages.error(request,'You must be logged in to post comments or replies!')
            return redirect(f'/blog/{post.slug}')
    else:
        return HttpResponse('Error - 404 not found')