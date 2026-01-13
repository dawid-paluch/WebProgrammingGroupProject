from typing import Any, Dict
from django.http import HttpRequest, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core.files.uploadedfile import UploadedFile
from django.utils.dateparse import parse_date

@login_required
@require_http_methods(["GET"])
def profile_data(request: HttpRequest) -> JsonResponse:
    '''Retrieve user profile information'''
    user = request.user

    profile_info: Dict[str, Any] = {
        "username": user.username,
        "email": user.email,
        "date_of_birth": getattr(user, "date_of_birth", None),
        "profile_image": (user.profile.image.url
                          if hasattr(user, "profile") and user.profile.image
                          else None),
    }
    return JsonResponse(profile_info)
    
@login_required
@require_http_methods(["POST"])
def update_profile(request: HttpRequest) -> JsonResponse:
    '''Update user profile information'''

    user = request.user

    email: str | None = request.POST.get('email')
    dob_raw: str | None = request.POST.get('date_of_birth')
    image: UploadedFile | None = request.FILES.get('profile_image')

    if email:
        user.email = email

    if dob_raw:
        parsed = parse_date(dob_raw)
        if parsed:
            user.date_of_birth = parsed

    if image:
        user.profile.image = image

    user.save()

    return JsonResponse({"status": "success", "message": "Profile updated successfully."})