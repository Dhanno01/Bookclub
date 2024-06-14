from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from django.db.models import Q
from django.core.paginator import Paginator

from .models import User,Club, Book,Comment, ClubMembership,Message,Forum

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        try:
          user = User.objects.create_user(username, email, password)
          user.save()
        except IntegrityError:
            return render(request, "club/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "club/register.html")
        

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
            return render(request, "club/login.html", {
                "message": "Invalid username and/or password."
            })
   else:
        return render(request, "club/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def index(request):
    activeClub = Club.objects.filter(isActive=True).order_by('-id')[:3]
    books = Book.objects.all().order_by('-id')[:4]
    latest_comments = Comment.objects.all().order_by('-id')[:4]
    return render(request, "club/index.html", {
        "activeClub": activeClub,
        "books": books,
        "latest_comments": latest_comments,
    })


def create_club(request):
    if request.method == 'GET':
        all_users = User.objects.all()
        all_books = Book.objects.all()
        return render(request, "club/createclub.html", {
            'all_users': all_users, 
            'all_books': all_books
            })
    else:
        name = request.POST['name']
        description = request.POST['description']
        imageUrl=request.POST["imageUrl"]
        profileUrl=request.POST["profileUrl"]
        
        # Assuming 'members' is a ManyToManyField to User
        members = request.POST.getlist('members')
        
        # Assuming 'book' is a ManyToManyField to Book
        books = request.POST.getlist('books')

        # Get the current user as the owner of the club
        owner = request.user

        # Create the club
        new_club = Club(
            name=name,
            description=description,
            owner=owner,
            imageUrl = imageUrl,
            profileUrl = profileUrl
        )
        new_club.save()

        # Add members and books to the club
        new_club.members.add(*members)
        new_club.books.set(books)

        # Redirect to the club detail page or any other desired page
        return HttpResponseRedirect(reverse('clubprofile', args=[new_club.id]))


def clubprofile(request, club_id):
    club = Club.objects.get(pk=club_id)
    owner = club.owner
    books = Book.objects.all()
    
    if request.user.is_authenticated:
        is_owner = (request.user == owner)
        is_join = ClubMembership.objects.filter(user=request.user, club=club).exists()
    else:
        is_owner = False
        is_join = False

    return render(request, 'club/clubprofile.html',{
        "club": club,
        'books': books,
        "owner":owner,
        "is_owner": is_owner,
        "is_join": is_join,
    })

def add_book(request):
    if request.method == 'GET':
       return render(request, 'club/bookform.html')
    else:
        title = request.POST['title']
        author = request.POST['author']
        cover_image=request.POST["cover_image"]
        description = request.POST["description"]

        new_book = Book(
            title=title, 
            author=author, 
            cover_image=cover_image,
            description=description
            )
        new_book.save()
        return HttpResponseRedirect(reverse('index'))
    
def find_club(request):
    activeClub = Club.objects.filter(isActive=True)
    return render(request, 'club/findclub.html',{
        "activeClub": activeClub,
    })
    
def books(request):
    all_books = Book.objects.filter().order_by('id').reverse()
    
    user = request.user
    if user.is_authenticated:
        book_watchlist = Book.objects.filter(watchlist=user)
    else:
        book_watchlist = None

    pagination = Paginator(all_books, 5)
    page_number = request.GET.get('page')
    posts_in_page = pagination.get_page(page_number)

    return render(request, 'club/books.html', {
        'books': posts_in_page,  # Use posts_in_page instead of all_books
        'book_watchlist': book_watchlist,
        'posts_in_page': posts_in_page
    })

def search_books(request):
    query = request.GET.get('q', '')
    books = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))

    # Paginate the search results
    pagination = Paginator(books, 5)
    page_number = request.GET.get('page')
    posts_in_page = pagination.get_page(page_number)

    return render(request, 'club/books.html', {
        'books': posts_in_page,
        'query': query
    })

def comments(request):
   if request.method == 'GET':
      comments = Comment.objects.all()
      return render(request, 'club/comments.html', {
      'comments': comments
      })
   
   else:
        user = request.user
        message = request.POST["message"]

        newcomment = Comment(
        author = user,
        message = message
        )
        newcomment.save()
        return HttpResponseRedirect(reverse('comments'))
   
def join_club(request, club_id):
    try:
        user = request.user
        club = Club.objects.get(pk=club_id)

        # Check if the user is already a member
        if ClubMembership.objects.filter(user=user, club=club).exists():
            # Handle the case where the user is already a member
            return redirect('clubprofile', club_id=club_id)

        # Create a new ClubMembership instance
        membership = ClubMembership(user=user, club=club)
        membership.save()

        # Redirect to the club profile page
        return HttpResponseRedirect(reverse('clubprofile', args=[club_id]))
    except Club.DoesNotExist:
        # Handle the case where the club doesn't exist
        return redirect('index') 
    
def leave_club(request, club_id):
    try:
        user = request.user
        club = Club.objects.get(pk=club_id)

        # Check if the user is a member
        if ClubMembership.objects.filter(user=user, club=club).exists():
            # Remove the user from the club
            ClubMembership.objects.filter(user=user, club=club).delete()

        # Redirect to the club profile page
        return HttpResponseRedirect(reverse('clubprofile', args=[club_id]))
    except Club.DoesNotExist:
        # Handle the case where the club doesn't exist
        return redirect('index')



def club_chat(request, club_id):
    if request.method == 'GET':
        club = Club.objects.get(id=club_id)
        content = Message.objects.filter(club=club)
        return render(request, 'club/chat.html', {
            'contents': content,
            'club': club,
        })
    elif request.method == 'POST':
        user = request.user
        content = request.POST["content"]
        club = Club.objects.get(id=club_id)

        newchat = Message(
            user=user,
            club=club,
            content=content
        )
        newchat.save()
        return HttpResponseRedirect(reverse('club_chat', args=[club_id]))
    

def remove(request, id):
   bookdata = Book.objects.get(pk=id)
   user=request.user
   bookdata.watchlist.remove(user)
   return HttpResponseRedirect(reverse('index')) 

def add(request, id):
   bookdata = Book.objects.get(pk=id)
   user=request.user
   bookdata.watchlist.add(user)
   return HttpResponseRedirect(reverse('index'))

def displaywatchlist(request):
    user = request.user
    books = user.tbr.all()
    return render(request, 'club/watchlist.html',{
        "books": books
    })


def book_chat(request, book_id):
    if request.method == 'GET':
        book = Book.objects.get(id=book_id)
        content = Forum.objects.filter(book_id=book_id)
        return render(request, 'club/forum.html', {
            'contents': content,
            'book': book,
        })
    elif request.method == 'POST':
        user = request.user
        content = request.POST["content"]
        book = Book.objects.get(id=book_id)

        newchat = Forum(
            user=user,
            book=book,
            content=content
        )
        newchat.save()
        return HttpResponseRedirect(reverse('book_chat', args=[book_id]))


def my_clubs(request):
    user_clubs = Club.objects.filter(owner=request.user)
    return render(request, 'club/createdclubs.html', {
        'user_clubs': user_clubs
    })

def joined_clubs(request):
    joined_clubs = ClubMembership.objects.filter(user=request.user).select_related('club')
    return render(request, 'club/joinedclubs.html', {
        'joined_clubs': joined_clubs
    })
