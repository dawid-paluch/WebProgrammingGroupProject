from urllib import request
from django.utils import timezone
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from rest_framework import permissions, viewsets
from .models import AuctionItem
from .serializers import AuctionItemSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import login, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db.models import Q
from .models import ItemQuestion
from .serializers import ItemQuestionSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import ItemBid
from .serializers import ItemBidSerializer
#from decimal import Decimalfrom django.contrib.auth
#from decimal import login, get_user_model
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_http_methods


@login_required
def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index.html', {})

def root_view(request):
    if request.user.is_authenticated:
        return redirect("/app/")
    return redirect("/login/")

User = get_user_model()

@login_required
def current_user(request):
    return JsonResponse({
        "username": request.user.username
    })

@login_required
@require_http_methods(["GET", "POST"])
def profile_api(request):
    user = request.user

    if request.method == "GET":
        return JsonResponse({
            "username": user.username,
            "email": user.email,
            "date_of_birth": getattr(user, "date_of_birth", None),
            "profile_image": user.profile_picture.url if getattr(user, "profile_picture", None) else None,
        })

    if request.method == "POST":
        email = request.POST.get("email")
        date_of_birth = request.POST.get("date_of_birth")
        profile_image = request.FILES.get("profile_image")

        if email:
            user.email = email

        if date_of_birth:
            user.date_of_birth = date_of_birth

        if profile_image:
            user.profile_picture = profile_image

        user.save()

        return JsonResponse({
            "username": user.username,
            "email": user.email,
            "date_of_birth": getattr(user, "date_of_birth", None),
            "profile_image": user.profile_picture.url if getattr(user, "profile_picture", None) else None,
        })

class AuctionItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing AuctionItem instances.
    Provides CRUD operations for auction items.
    """
    queryset = AuctionItem.objects.all()
    serializer_class = AuctionItemSerializer
    permission_classes = [permissions.IsAuthenticated]
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
        serializer.save(owner=self.request.user)  # Placeholder for actual user assignment logic

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

            ItemBid.objects.create(item=item, bidder=request.user, amount=Decimal(bid_amount))

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
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(asked_by=self.request.user)

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
        user = request.user

        if question.item.owner != user:
            return Response({'error': 'Only the item owner can answer questions.'}, status=status.HTTP_403_FORBIDDEN)
        answer_text = request.data.get('answer_text', '').strip()

        if not answer_text:
            return Response({'error': 'Answer text is required.'}, status=status.HTTP_400_BAD_REQUEST)  
        
        question.answer_text = answer_text
        question.answered_at = timezone.now()
        question.save()

        serializer = self.get_serializer(question)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class SignUpForm(UserCreationForm):
    """
    Custom user signup form to include email field.
    Maintains default username, email, password1, and password2 fields.
    """
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
    
    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email



def signup(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
    else:
        form = SignUpForm()

    return render(request, "signup.html", {"form": form})