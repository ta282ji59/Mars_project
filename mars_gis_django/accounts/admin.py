from django.contrib import admin
from .models import CustomUser, Project


# class ProjectsAdmin(admin.ModelAdmin):
#     list_display = ('project_name','project_admin_user','project_normal_user')
#     # list_display_links = ('instrument','data_id','latitude','longitude','created_date','permission')

#     def user_get(self, obj):
#         return obj.user.project_name
    
# admin.site.register(CustomUser)
# admin.site.register(Projects)
# admin.site.register(Projects, ProjectsAdmin)
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    model = Project
    list_display = ["username", "email"]

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    model = Project
    list_display = ["name"]