from django.contrib import admin

from .models import AuctionItem, User, PageView


admin.site.register(AuctionItem)
admin.site.register(User)
admin.site.register(PageView)