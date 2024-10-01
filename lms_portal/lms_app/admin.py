from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Reader)
admin.site.register(Book)
class CheckoutRecordAdmin(admin.ModelAdmin):
    list_display = ('checkout_id', 'reader_id', 'reader_name', 'num_books', 'borrow_date', 'return_date', 'total_charge')
    readonly_fields = ('checkout_id', 'reader_id', 'reader_name', 'num_books', 'book_list', 'borrow_date', 'return_date', 'total_charge')
    search_fields = ('reader_id', 'reader_name')  

admin.site.register(CheckoutRecord, CheckoutRecordAdmin)