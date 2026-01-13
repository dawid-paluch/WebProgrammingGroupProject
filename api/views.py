from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render
from rest_framework import permissions, viewsets
from .models import AuctionItem
from .serializers import AuctionItemSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q
from .models import ItemQuestion
from .serializers import ItemQuestionSerializer



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
        Returns onlt questions related to a specific auction item
        """

        item_id = self.request.query_params.get('item_id', None)
        if item_id:
            return ItemQuestion.objects.filter(item_id=item_id)
        return ItemQuestion.objects.all()
    