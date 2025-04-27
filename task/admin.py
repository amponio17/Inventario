from django.contrib import admin
from .models import supliers
from .models import categories
from .models import items
from .models import positions
from .models import users
from .models import stock
from .models import stock_tracking
# Register your models here.




#admin.site.register(supliers),
admin.site.register(supliers),
admin.site.register(categories),
admin.site.register(items),
admin.site.register(positions),
admin.site.register(users),
admin.site.register(stock),
admin.site.register(stock_tracking),

