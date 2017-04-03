from django.contrib import admin

from .models import Filing, Person, Mention

admin.site.register(Filing)
admin.site.register(Person)
admin.site.register(Mention)
