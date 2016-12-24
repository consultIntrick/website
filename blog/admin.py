from django.contrib import admin

from blog.models import Entry, SubscriberNewsletter, ViewerMessage

admin.site.register(Entry)
admin.site.register(SubscriberNewsletter)
admin.site.register(ViewerMessage)
