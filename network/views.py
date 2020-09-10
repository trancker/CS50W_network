import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import User,Blogpost,Followinfo,Like
from django.core import serializers
from django.core.paginator import Paginator

def index(request):
    try:
        allposts = Blogpost.objects.all()
        allposts = allposts.order_by("-timestamp").all()
        paginator = Paginator(allposts, 10) # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    except:
        page_obj = None
    try:
        likeslist = Like.objects.filter(likedby=request.user.username)
        likedids = []
        for l in likeslist:
            likedids.append(l.postid)
    except:
        likedids =  None
    cuser=[]
    cuser.append(request.user.username)    
    return render(request, 'network/index.html', {'page_obj': page_obj,'likedids':likedids,'cuser':cuser})

@login_required
def writepost(request):
    if request.user.username:
        return render(request,"network/writepost.html")
    else:
        return redirect('index')

@csrf_exempt
@login_required
def submitpost(request):
    if request.user.username:
        if request.method == "POST":
            blog = Blogpost()
            blog.username = request.user
            blog.content = request.POST.get('content')
            blog.likes = 0
            blog.save()
            return redirect('index')
        else:
            return redirect('index')
    else:
        return redirect('index')


def profilepage(request,uname):
    try:
        userposts = Blogpost.objects.filter(username=uname)
        userposts = userposts.order_by("-timestamp").all()
        paginator = Paginator(userposts, 10) # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    except:
        userposts = None
    try:
        if Followinfo.objects.filter(username=uname,follower=request.user.username):
            is_follow = True
        else:
            is_follow = False
    except:
        is_follow = False
    try:
        followerlist = Followinfo.objects.filter(username=uname)
        followers = followerlist.count()
    except:
        followers = 0
    try:
        followinglist = Followinfo.objects.filter(follower=uname)
        following=followinglist.count()
    except:
        following = 0
    try:
        likeslist = Like.objects.filter(likedby=request.user.username)
        likedids = []
        for l in likeslist:
            likedids.append(l.postid)
    except:
        likedids =  None
    cuser=[]
    cuser.append(request.user.username)
    return render(request,'network/profilepage.html', 
    {
        'page_obj': page_obj,
        'profilename': uname,
        'isfollow': is_follow,
        "followers":followers,
        "following":following,
        "likedids":likedids,
        "cuser":cuser
        })


@csrf_exempt
@login_required
def followuser(request,name):
    try:
        flist = Followinfo.objects.get(username=name,follower=request.user.username)
    except:
        flist = Followinfo()
        flist.username = name
        flist.follower = request.user.username
        flist.save()
    return redirect('profilepage',uname=name)

@csrf_exempt
@login_required
def unfollowuser(request,name):
    try:
        flist = Followinfo.objects.get(username=name,follower=request.user.username)
        flist.delete()
    except:
        return redirect('profilepage',uname=name)
    return redirect('profilepage',uname=name)





@login_required
def followingposts(request):
    try:
        following = Followinfo.objects.filter(follower=request.user.username)
        
        item=[]
        items=[]
        funames=[]
        for f in following:
            funames.append(f.username)
        for f in funames:
            bpost = Blogpost.objects.filter(username=f)
            bpost=bpost.order_by("-timestamp").all()
            items.append(bpost)
            
        for n in range(0,len(items)):
            item.extend(items[n])
        
       
        paginator = Paginator(item, 10) # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    except:
        page_obj=None
    
    try:
        likeslist = Like.objects.filter(likedby=request.user.username)
        likedids = []
        for l in likeslist:
            likedids.append(l.postid)
    except:
        likedids =  None
    cuser=[]
    cuser.append(request.user.username)
    return render(request,"network/followingpage.html",{
            "page_obj":page_obj,
            "likedids":likedids,
            "cuser":cuser
        })


@csrf_exempt
@login_required
def followapi(request,name):
    try:
        if User.objects.get(username=name) :
            try:
                followerlist = Followinfo.objects.filter(username=name)
                followers = followerlist.count()
            except:
                followers = 0
            try:
                followinglist = Followinfo.objects.filter(follower=name)
                following=followinglist.count()
            except:
                following = 0
            try:
                if Followinfo.objects.filter(username=name,follower=request.user.username):
                    is_follow = True
                else:
                    is_follow = False
            except:
                is_follow = False
            
    except:
        return JsonResponse({"error":"No such user found"},status=404)
    
    if request.method == "GET":
        return JsonResponse({"user":name,"followers":followers,"following":following,"is_follow":is_follow})
    else:
        return JsonResponse({"error":"INVALID ACCESS"},status=404)

@csrf_exempt
@login_required
def likesapi(request,postid):
    if request.method == "GET":
        try:
            postlike = Like.objects.get(postid=postid,likedby=request.user.username)
            return JsonResponse(postlike.serialize())
        except Like.DoesNotExist:
            return JsonResponse({"error": "No like activity found"}, status=404)
    elif request.method == "POST":
        data = json.loads(request.body)
        if request.user.username == data.get("likedby"):
            likerow = Like()
            likerow.postid = data.get("id")
            likerow.likedby = data.get("likedby")
            likerow.likes = data.get("likes")
            blikes = Blogpost.objects.get(id=data.get("id"))
            blikes.likes = data.get("likes")
            blikes.save()
            likerow.save()
            return JsonResponse({"message": "Success!!!","status":201},status=201)
        else:
            return JsonResponse({"error": "INVALID ACCESS"},status=404)
    elif request.method == "DELETE":
        data=json.loads(request.body)
        if request.user.username == data.get("unlikedby"):
            likerow = Like.objects.get(postid=data.get("id"),likedby=data.get("unlikedby"))
            likerow.delete()
            blikes = Blogpost.objects.get(id=data.get("id"))
            blikes.likes = data.get("likes")
            blikes.save()
            return JsonResponse({"message": "Unlike successful","status":201},status=201)
    else:
        return JsonResponse({"error": "Try GET request"},status=404)


@csrf_exempt
def postapi(request,postid):
    try:
        blogpost = Blogpost.objects.get(id=postid)
    except Blogpost.DoesNotExist:
        return JsonResponse({"error": "post not found."}, status=404)
    if request.method == "GET":
        return JsonResponse(blogpost.serialize())
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("username") == request.user.username :
            if data.get("content") is not None:
                blogpost.content = data["content"]
        else:
            return JsonResponse({"error":"INVALID ACCESS"},status=404)
        blogpost.save()
        return HttpResponse(status=204)
    else:
        return JsonResponse({"error": "try using GET request"}, status=404)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
