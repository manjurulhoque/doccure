from django.contrib import admin
from .models import (
    Education,
    Experience,
    TimeRange,
    Saturday,
    Sunday,
    Monday,
    Wednesday,
    Thursday,
    Friday,
)

admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(TimeRange)
admin.site.register(Saturday)
admin.site.register(Sunday)
admin.site.register(Monday)
admin.site.register(Wednesday)
admin.site.register(Thursday)
admin.site.register(Friday)
