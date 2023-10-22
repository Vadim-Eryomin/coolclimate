from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Categories)
admin.site.register(Cards)
admin.site.register(CardVariants)
admin.site.register(CardImages)
admin.site.register(Filters)
admin.site.register(FilterValues)
