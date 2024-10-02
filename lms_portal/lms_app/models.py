from django.db import models

# Create your models here.
class Reader(models.Model):
    def __str__(self):
        return self.reader_name
    reader_id = models.CharField(max_length=200)
    reader_name = models.CharField(max_length=200)
    reader_contact = models.CharField(max_length=200)
    reader_address = models.TextField()
    account_bal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    active = models.BooleanField(default=True)

class Book(models.Model):
    def __str__(self):
        return self.title
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    book_year = models.IntegerField(default=2000)
    isbn = models.CharField(max_length=13, unique=True)
    description = models.TextField()
    copies = models.IntegerField(default=1)

class CheckoutRecord(models.Model):
    
    checkout_id = models.AutoField(primary_key=True)
    reader_id = models.CharField(max_length=255)
    reader_name = models.CharField(max_length=255)
    num_books = models.IntegerField()
    book_list = models.TextField()
    borrow_date = models.DateField()
    return_date = models.DateField()
    total_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    class Meta:
        verbose_name = "CheckoutRecord"
        verbose_name_plural = "CheckoutRecords"
    def __str__(self):
        return f'CheckoutRecord {self.checkout_id}'
    
    return_status = models.CharField(max_length=10, default='pending')  # can be 'pending', 'returned'
    is_overdue = models.BooleanField(default=False)
