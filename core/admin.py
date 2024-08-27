from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core.models import User, ExerciseRoutine, FoodRecipe

class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active', 'diet', 'weight', 'height', 'smoker', 'weekly_exercise_hours', 'imc', 'goal')
    list_filter = ('is_staff', 'is_active', 'diet', 'smoker')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'diet', 'weight', 'height', 'smoker', 'weekly_exercise_hours', 'imc', 'goal')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'diet', 'weight', 'height', 'smoker', 'weekly_exercise_hours', 'imc', 'goal')}
        ),
    )
    search_fields = ('email', 'first_name', 'last_name', 'diet')
    ordering = ('email',)

admin.site.register(User, UserAdmin)
admin.site.register(ExerciseRoutine)
admin.site.register(FoodRecipe)