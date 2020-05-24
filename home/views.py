from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from blog.models import Post
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    allPosts = Post.objects.all()[0:5]
    params={'allPosts':allPosts}
    return render(request,'home/home.html',params)

def about(request):
    return render(request,'home/about.html')

def contact(request):
    messages.success(request,'Welcome to Contact')
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        if len(name<2) or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request,"Please fill the form correctly!")
        else:    
            contact = Contact(name=name,email=email,phone=phone,content=content)
            contact.save()
            messages.success(request,'Your message has been successfully sent!')
    return render(request,'home/contact.html')

def search(request):
    query = request.GET['query']
    if len(query)>78:
        allPosts= Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains = query)
        allPostsContent = Post.objects.filter(content__icontains = query)
        allPosts = allPostsTitle.union(allPostsContent)
    if allPosts.count() == 0:
        messages.warning(request,'No matching Result found for your Query!')
    params = {'allPosts':allPosts,'query':query}
    return render(request,'home/search.html',params)

def handleSignup(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']

        if len(username) > 10 or len(username)<3:
            messages.error(request,'Your username is too long or too short!')
            return redirect('home')

        if not username.isalnum():
            messages.error(request,'Your username should only be alphanumeric!')
            return redirect('home')

        newUser = User.objects.create_user(username,email,password)
        newUser.first_name = fname
        newUser.last_name = lname
        newUser.save()
        messages.success(request,'Your iCoder Account has been Successfully Created!')
        return redirect('home')
    else:
        return HttpResponse('Error - 404 Not Found!')

def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username = loginusername,password = loginpassword)

        if user is not None:
            login(request,user)
            messages.success(request,'Sucessfully Logged In!')
            return redirect('home')
        else:
            messages.error(request,'No such User found!')
            return redirect('home')
    else:
        return HttpResponse('Error - 404 Not Found!')

def handleLogout(request):
        logout(request)
        messages.success(request,'Sucessfully Logged Out!')
        return redirect('home')
    