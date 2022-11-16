from django.contrib import admin

from .models import Comment, Lis, Bids, Watchlist, ClosedLis, AllLis

# Register your models here.

admin.site.register(Comment)
admin.site.register(Lis)
admin.site.register(Bids)
admin.site.register(Watchlist)
admin.site.register(ClosedLis)
admin.site.register(AllLis)