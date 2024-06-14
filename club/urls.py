from django.urls import path
from . import views

urlpatterns = [

    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path('create_club', views.create_club, name='create_club'),
    path('club_detail/<int:club_id>', views.clubprofile, name='clubprofile'),
    path('find_club',views.find_club, name='find_club'),
    path('books',views.books, name='books'),
    path('add_book',views.add_book, name='add_book'),
    path('search/', views.search_books, name='search_books'),
    path("comments",views.comments, name='comments'),
    path('clubprofile/<int:club_id>/join/', views.join_club, name='join_club'),
    path('clubprofile/<int:club_id>/leave/', views.leave_club, name='leave_club'),
    path('clubs/<int:club_id>/chat/', views.club_chat, name='club_chat'),
    path("remove/<int:id>", views.remove,name="remove"),
    path("add/<int:id>", views.add,name="add"),
    path("displaywatchlist",views.displaywatchlist,name="displaywatchlist"),
    path('books/<int:book_id>/chat/', views.book_chat, name='book_chat'),
    path('user_clubs/', views.my_clubs, name='user_clubs'),
    path('joined_clubs/', views.joined_clubs, name='joined_clubs'),


]