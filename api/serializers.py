from rest_framework import serializers
from .models import AuctionItem
from .models import ItemQuestion
from .models import ItemBid

class AuctionItemSerializer(serializers.ModelSerializer):
    """
    Serializer for AuctionItem model.
    """
    class Meta:
        model = AuctionItem
        fields = ['id', 'owner', 'title', 'description', 'starting_bid', 'current_bid', 'image', 'created_at', 'end_datetime']
        read_only_fields = ['id', 'owner', 'created_at', 'current_bid']
    
class ItemQuestionSerializer(serializers.ModelSerializer):
    """
    Serializer for ItemQuestion model.
    """
    class Meta:
        model = ItemQuestion
        fields = ['id', 'item', 'asked_by', 'question_text', 'answer_text', 'asked_at', 'answered_at']
        read_only_fields = ['id', 'asked_by', 'asked_at', 'answered_at']
        
class ItemBidSerializer(serializers.ModelSerializer):
    """
    Serializer for ItemBid model.
    """
    class Meta:
       model = ItemBid
       fields = ['id', 'item', 'bidder', 'amount', 'timestamp']