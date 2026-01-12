from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class PageView(models.Model):
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"Page view count: {self.count}"
    

class AuctionItem(models.Model):
    """
    Model representing an item listed for auction.

    Attributes:
        owner (str): The owner of the auction item.
        title (str): The title of the auction item.
        description (str): A detailed description of the auction item.
        starting_bid (Decimal): The starting bid amount for the auction item.
        current_bid (Decimal): The current highest bid for the auction item.
        image (Image): An optional image of the auction item.
        created_at (datetime): The date and time when the auction item was created.
        end_datetime (datetime): The date and time when the auction ends.

    """
    owner = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='auction_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    end_datetime = models.DateTimeField()

    def __str__(self):
        """
        String representation of the AuctionItem model.
        """

        return self.title


class User(AbstractUser):
    """
    Model representing a custom user in the system.
    
    Attributes:
        username (str): The username of the user.
        email (str): The email address of the user.
        password (str): The password for the user account.
        date_of_birth (date): The date of birth of the user.

    """
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def __str__(self):
        """
        Return a string representation of the User.
        """
        return self.username