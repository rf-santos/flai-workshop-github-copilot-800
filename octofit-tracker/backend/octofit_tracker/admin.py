from django.contrib import admin
from .models import User, Team, Activity, Leaderboard, Workout


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'team', 'created_at')
    list_filter = ('team', 'created_at')
    search_fields = ('name', 'email', 'team')
    ordering = ('-created_at',)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'captain', 'members_count', 'total_points', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'captain')
    ordering = ('-total_points',)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'team', 'activity_type', 'duration', 'calories', 'points', 'date')
    list_filter = ('activity_type', 'team', 'date')
    search_fields = ('user_name', 'team', 'activity_type')
    ordering = ('-date',)


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ('team', 'rank', 'total_points', 'total_activities', 'total_calories', 'total_distance', 'updated_at')
    list_filter = ('updated_at',)
    search_fields = ('team',)
    ordering = ('rank',)


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('name', 'activity_type', 'difficulty', 'duration', 'calories_estimate', 'created_at')
    list_filter = ('activity_type', 'difficulty', 'created_at')
    search_fields = ('name', 'activity_type', 'difficulty')
    ordering = ('-created_at',)
