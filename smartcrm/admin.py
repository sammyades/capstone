from django.contrib import admin
from .models import Role, User, Lead, Deal, Task, Activity


# Register your models here.

#Role Admin
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display =('id', 'name')
    search_fields = ('name',)

#User Admin
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active')
    serch_fields = ('username', 'email')


# Task Inline
class TaskInline(admin.TabularInline):
    model = Task
    extra = 1

# Activity Inline
class ActivityInline(admin.TabularInline):
    model = Activity
    extra = 1


# Deal Inline
class DealInline(admin.StackedInline):
    model = Deal
    extra = 0
    max_num = 1


#Lead Admin
@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = (
        'company',
        'first_name',
        'last_name',
        'email',
        'phone',
        'status',
        'score',
        'created_at'
    )

    list_filter = ('status', 'score')
    search_fields = ('company__name', 'first_name', 'last_name')

    readonly_fields = ('created_at',)

    inlines = [TaskInline, ActivityInline, DealInline]

    ordering = ('-created_at',)


#Deal Admin
@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ('lead', 'amount', 'stage', 'status', 'expected_close_date')
    list_filter = ('status', 'stage')
    search_fields = ('lead__company__name',)


#Task Admin
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'lead', 'owner', 'priority', 'status', 'due_date')
    list_filter = ('priority', 'status')
    search_fields = ('title', 'lead__company__name')
    ordering = ('due_date',)


# Activity admin
@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('type', 'lead', 'owner', 'created_at')
    list_filter = ('type',)
    search_fields = ('lead__company__name',)


admin.site.site_header = "Smart CRM Admin"
admin.site.site_title = "Smart CRM"
admin.site.index_title = "Welcome to Smart CRM Dashboard"