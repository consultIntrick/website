from django.contrib import admin
from blog.models import Entry, SubscriberNewsletter
# from redactor.widgets import RedactorEditor

#
# class EntryAdmin(admin.ModelAdmin):
#     list_display = ['title']

admin.site.register(Entry)
admin.site.register(SubscriberNewsletter)

