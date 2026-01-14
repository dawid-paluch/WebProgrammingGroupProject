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
    
