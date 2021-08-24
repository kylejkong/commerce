from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.messages.views import SuccessMessageMixin


class User(AbstractUser):
    pass

    def get_queryset(self, *args, **kwargs):
            return self.request.user.notifications.all()
   
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, )
    
    comment = models.CharField(max_length=300)
    time = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f"{self.user}: {self.comment}"

    class Meta:
        ordering = ['-time']  ### this displays comments from most recent time first. 
    



#represents category of listings
class Category(models.Model):
    
    category = models.CharField(max_length=44)

    def __str__(self):
        return f"{self.category}"




  


# listings model
class Listing(models.Model):


   
    seller = models.ForeignKey('User', on_delete=models.CASCADE, related_name="sellers")
    item_name = models.CharField(max_length=44)
    item_description = models.TextField(max_length=888)
    price = models.IntegerField(null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="listing_category")
    start_time = models.DateTimeField(auto_now_add=True)
    closed = models.BooleanField(default=False)
    image = models.ImageField(upload_to='uploaded_images',null=True, blank=True)
    img_url = models.URLField(blank = True)
    bids = models.IntegerField(null=True)
    comments = models.ManyToManyField(Comment, blank=True, related_name="comments")
    close_listing = models.BooleanField(default=False)
    bid_winner = models.CharField(max_length=44, default="Default_Value")

     
    def __str__(self):
        return f"{self.item_name}"

    class Meta:
        ordering = ['-start_time'] 

class Watchlist(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='watchlist' )
    listing = models.ForeignKey('Listing', on_delete = models.CASCADE)

    def __str__(self):
       return f"{self.user}'s WatchList"


class Bid(models.Model):
    time = models.DateTimeField(auto_now_add=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=3)
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name = "listing_bid")

    def __str__(self):
        return f"{self.user} has placed a bid in for {self.price}"