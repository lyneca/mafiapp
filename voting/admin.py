from django.contrib import admin
from .models import Vote, VoteCount
# Register your models here.
admin.site.register(Vote)
admin.site.register(VoteCount)