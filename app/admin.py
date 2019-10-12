from django.contrib import admin
from .models import Contact
from django.contrib.auth.models import Group
from import_export.admin import ImportExportModelAdmin

# Register your models here.
class ContactAdmin(ImportExportModelAdmin):   # 'id', it will create unique id for every object.
    list_display = ('id','name','gender','email','info','phone') # It will display all the columns.
    list_display_links = ('id','name')
    list_editable = ('info',)  # It will give you the editing opportunity
    list_per_page = 10  # It will show the item you give.Like, you gave 10.That means you will can see the 10 items of all the items.
    search_fields = ('name','gender','email','info','phone') # It will create a search filed
    list_filter = ('gender','date_added') # It will allow you to filtering each item.

admin.site.register(Contact, ContactAdmin)  # It will register these items in admin panel
admin.site.unregister(Group)  # It will remove the Group section from Authentication and authorization in admin panel.
