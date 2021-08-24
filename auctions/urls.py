from auctions.models import Category
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_Listing, name="create"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("listing/<int:listing_id>", views.listing_view, name="listing_view"),
    path("category", views.category_index, name="category"),
    path("seller", views.seller_index, name="seller"),
    path("comment/<int:listing_id>", views.add_comment, name="comment"),
    # path("listing/<str:seller>/<int:listing_id>", views.seller_view, name="seller_view"),
    # path("listing/remove/<int:listing_pk>", views.delete_comment, name="delete_comment"),
    path('delete/<listing_id>',views.delete_listing,name='delete'),
    path('delete/comment/', views.delete_comment, name='delete_comment'),
    
    path("test", views.test, name='test' ),
   
    path("listing/<int:listing_id>/watch", views.watchlist_add_remove, name="watchlist_add_remove"),
    path("listing/<str:listing>/close", views.listing_close, name="close_listing"),
    path("listing/<str:listing>/unclose", views.listing_unclose, name="unclose_listing"),
    path("archive", views.index2, name="index2"),
    path("listing/<int:listing_id>/newbid", views.new_bid, name="new_bid"),
    path("bidlist", views.mybids, name="bidlist"),
    path("listing/<int:listing_id>/viewbids", views.view_bids, name="view_bids"),
]   
