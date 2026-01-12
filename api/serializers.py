from rest_framework import serializers
from .models import AuctionItem

class AuctionItemSerializer(serializers.ModelSerializer):
    """
    Serializer for AuctionItem model.
    """
    class Meta:
        model = AuctionItem
        fields = ['id', 'owner', 'title', 'description', 'starting_bid', 'current_bid', 'image', 'created_at', 'end_datetime']
        read_only_fields = ['id', 'created_at', 'current_bid']

    def create(self, validated_data):
        validated_data['owner'] = 'test_user'  # Placeholder for actual user assignment logic
        return super().create(validated_data)