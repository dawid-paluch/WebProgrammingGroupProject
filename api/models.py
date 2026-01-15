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
        owner (ForeignKey): The owner of the auction item.
        title (str): The title of the auction item.
        description (str): A detailed description of the auction item.
        starting_bid (Decimal): The starting bid amount for the auction item.
        current_bid (Decimal): The current highest bid for the auction item.
        image (Image): An optional image of the auction item.
        created_at (datetime): The date and time when the auction item was created.
        end_datetime (datetime): The date and time when the auction ends.

    """
    owner = models.ForeignKey('User', on_delete=models.CASCADE)
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
    

class ItemQuestion(models.Model):

    """
    Model representing a question asked about an auction item.

    Attributes:
        item (ForeignKey): The auction item the question is about.
        asked_by (ForeignKey): The user who asked the question.
        question_text (str): The text of the question.
        answer_text (str): The text of the answer (if answered).
        asked_at (datetime): The date and time when the question was asked.
        answered_at (datetime): The date and time when the question was answered (if answered).
    """
    
    item = models.ForeignKey(
        AuctionItem, 
        related_name='questions', 
        on_delete=models.CASCADE
    )

    asked_by = models.ForeignKey('User', on_delete=models.CASCADE)
    question_text = models.TextField()
    answer_text = models.TextField(null=True, blank=True)
    asked_at = models.DateTimeField(auto_now_add=True)
    answered_at = models.DateTimeField(null=True, blank=True)
    

    def __str__(self):
        return f"Question by {self.asked_by} on {self.item.title}"

class ItemBid(models.Model):
    """
    Model representing a bid placed on an auction item.
    """

    item = models.ForeignKey(
        AuctionItem, 
        related_name='bids', 
        on_delete=models.CASCADE
    )
    
    bidder = models.ForeignKey('User', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-amount', 'timestamp']

    def __str__(self):
        return f"Bid of {self.amount} by {self.bidder} on {self.item.title}"
