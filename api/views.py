from urllib import request
from django.utils import timezone
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render
from rest_framework import permissions, viewsets
from .models import AuctionItem
from .serializers import AuctionItemSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q
from .models import ItemQuestion
from .serializers import ItemQuestionSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import ItemBid
from .serializers import ItemBidSerializer
from decimal import Decimal

def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index.html', {})


class AuctionItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing AuctionItem instances.
    Provides CRUD operations for auction items.
    """
    queryset = AuctionItem.objects.all()
    serializer_class = AuctionItemSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        """
        Optionally filters auction items by a 'search' query parameter
        matching title or description.
        """
        queryset = AuctionItem.objects.all()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner='test_user')  # Placeholder for actual user assignment logic

    @action(detail=True, methods=['post'])
    def place_bid(self, request, pk=None):
        """
        Custom action to place a bid on an auction item.
        """
        try:
            item = self.get_object()
            bid_amount = request.data.get('bid_amount', None)
            if bid_amount is None:
                return Response({'error': 'Bid amount is required.'}, status=400)

            bid_amount = float(bid_amount)
            current = item.current_bid or item.starting_bid
            if bid_amount <= current:
                return Response({'error': 'Bid must be higher than current bid.'}, status=400)

            item.current_bid = bid_amount
            item.save()

            bidder = request.data.get('bidder', 'test_bidder')
            ItemBid.objects.create(item=item, bidder=bidder, amount=Decimal(bid_amount))

            serializer = self.get_serializer(item)
            return Response(serializer.data)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({'error': str(e)}, status=500)
    

class ItemQuestionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing ItemQuestion instances.
    Provides CRUD operations for item questions.
    """

    queryset = ItemQuestion.objects.all()
    serializer_class = ItemQuestionSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        serializer.save()  # Placeholder for actual user assignment logic

    def get_queryset(self):
        """
        Returns only questions related to a specific auction item
        """

        item_id = self.request.query_params.get('item_id', None)
        if item_id:
            return ItemQuestion.objects.filter(item_id=item_id)
        return ItemQuestion.objects.all()
    
    @action(detail=True, methods=['patch', 'post'])
    def answer(self, request, pk=None):
        """
        Custom action to answer a question.
        """
        question = self.get_object()
        answer_text = request.data.get('answer_text', '').strip()

        if not answer_text:
            return Response({'error': 'Answer text is required.'}, status=status.HTTP_400_BAD_REQUEST)  
        
        question.answer_text = answer_text
        question.answered_at = timezone.now()
        question.save()

        serializer = self.get_serializer(question)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
