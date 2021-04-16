from django.contrib import admin
from .models import Candidate, Position

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('user','position')
    list_filter = ('position',)
    search_fields = ('user','position')
    readonly_fields = ('total_vote',)