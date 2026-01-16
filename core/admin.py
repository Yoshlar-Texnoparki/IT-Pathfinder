from django.contrib import admin
from .models import UserProfile, Question, Choice, Result

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'test_status', 'telegram_id')
    search_fields = ('name', 'phone_number')
    list_filter = ('test_status',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'category')
    list_filter = ('category',)
    inlines = [ChoiceInline]

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'top_category', 'created_at')
    list_filter = ('top_category', 'created_at')
    readonly_fields = ('created_at',)

admin.site.register(Choice)
