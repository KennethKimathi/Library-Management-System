from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
from datetime import datetime
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.contrib import messages
import logging


# Create your views here.
logger = logging.getLogger(__name__)
def home (request):
    return render(request,"home.html", context={"current_tab": "home"})

def readers(request):
    readers = Reader.objects.all()  # Fetch all readers from the database
    print(f"Number of readers: {readers.count()}")  # To verify that readers are being fetched
    return render(request, "readers.html", context={"current_tab": "readers", "readers": readers})

def reader_search(request):
    query = request.GET.get('query', '')  # Get the search query from the request
    if query:
        # Filter readers by name or reader_id (use __icontains for case-insensitive search)
        readers = Reader.objects.filter(
            models.Q(reader_name__icontains=query) | models.Q(reader_id__icontains=query)
        )
    else:
        readers = Reader.objects.all()  # Get all readers if no query is provided

    return render(request, 'reader_search_results.html', {
        'readers': readers,
        'current_tab': 'reader_search'
    })

def books (request):
    books = Book.objects.all()
    return render(request, "books.html", context={"current_tab": "books", "books": books})

def save_book(request):
    if request.method == 'POST':
        book = Book(
            title=request.POST['book_title'],
            author=request.POST['book_author'],
            isbn=request.POST['book_isbn'],
            description=request.POST['book_description']
        )
        book.save()
        return redirect('/books')

def search_books(request):
    query = request.GET.get('search')
    if query:
        books = Book.objects.filter(title__icontains=query)  # Search based on title
    else:
        books = Book.objects.all()
    return render(request, "books.html", context={"books": books})

def returns(request):
    query = request.GET.get('query', '')
    if query:
        # Filter records by reader_id or reader_name
        checkout_records = CheckoutRecord.objects.filter(
            models.Q(reader_id__icontains=query) | models.Q(reader_name__icontains=query)
        )
    else:
        checkout_records = CheckoutRecord.objects.all()  # Get all records if no query

    return render(request, 'returns.html', {
        'checkout_records': checkout_records,
        'current_tab': 'returns'
    })
  
def readers_tab(request):
    readers = Reader.object.all()
    return render(request,"readers.html", 
                  context={"current_tab":"readers", 
                           "readers":readers}
                )
def save_reader(request):
    reader_item = Reader(
            reader_id=request.POST['reader_id'],
            reader_name=request.POST['reader_name'],
            reader_contact=request.POST['reader_contact'],
            reader_address=request.POST['reader_address'],
            active=True
        )
    reader_item.save()
    return redirect('/readers')

@require_POST
def add_to_bag(request, book_id):
    bag = request.session.get('bag', [])
    if book_id not in bag:
        bag.append(book_id)
        request.session['bag'] = bag
    return JsonResponse({'status': 'success'})

@csrf_exempt
def remove_from_bag(request, book_id):
    if request.method == 'POST':
        try:
            # `request.session['bag']` holds the list of book IDs
            bag = request.session.get('bag', [])
            if book_id in bag:
                bag.remove(book_id)
                request.session['bag'] = bag  
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'message': 'Book not found in bag.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


def mybag(request):
    bag = request.session.get('bag', [])
    bag_books = Book.objects.filter(id__in=bag)
    reader = None

    if request.method == 'POST':
        reader_id = request.POST.get('reader_id')
        try:
            reader = Reader.objects.get(reader_id=reader_id)
        except Reader.DoesNotExist:
            reader = None

    context = {
        'bag_books': bag_books,
        'reader': reader,
        'current_tab': 'mybag'
    }
    return render(request, 'mybag.html', context)

def checkout(request):
    if request.method == 'POST':
        reader_id = request.POST['reader_id']
        borrow_date = request.POST['borrow_date']
        return_date = request.POST['return_date']

        try:
            reader = Reader.objects.get(reader_id=reader_id)
        except Reader.DoesNotExist:
            messages.error(request, "Reader not found.")
            return redirect('/mybag/')

        # Convert dates
        try:
            borrow_date = datetime.strptime(borrow_date, "%Y-%m-%d").date()
            return_date = datetime.strptime(return_date, "%Y-%m-%d").date()
        except ValueError:
            messages.error(request, "Invalid date format.")
            return redirect('/mybag/')

        # Validate that return date is after borrow date
        if return_date <= borrow_date:
            messages.error(request, "Return date must be after borrow date.")
            return redirect('/mybag/')

        # Calculate the borrowing period
        borrowing_days = (return_date - borrow_date).days
        charge_per_day = 0.50

        # Get the books in the bag
        bag = request.session.get('bag', [])
        bag_books = Book.objects.filter(id__in=bag)

        if not bag_books:
            messages.error(request, "No books in the bag to checkout.")
            return redirect('/mybag/')

        # Calculate total charges
        total_charge = len(bag_books) * borrowing_days * charge_per_day

        # Check if the reader's account balance is sufficient
        if reader.account_bal < 500:
            messages.warning(request, "Your account balance is below Ksh.500. Please top-up to continue.")
            return redirect('/mybag/')

        # Check if the balance is sufficient to cover the borrowing charges
        if reader.account_bal < total_charge:
            messages.error(request, f"Insufficient balance to cover borrowing charges. You need Ksh.{total_charge}.")
            return redirect('/mybag/')

        # Proceed with checkout
        try:
            # Create a checkout record
            checkout_record = CheckoutRecord.objects.create(
                reader_id=reader_id,
                reader_name=reader.reader_name,
                borrow_date=borrow_date,
                return_date=return_date,
                num_books=len(bag_books),
                book_list=', '.join(book.title for book in bag_books),
                total_charge=total_charge
            )
            
            # Update book inventory and save book details to the checkout record
            book_titles = []
            for book in bag_books:
                if book.copies > 0:
                    book.copies -= 1  # Reduce the number of available copies
                    book.save()  # Save the changes to the database
                    book_titles.append(book.title)
                else:
                    messages.warning(request, f"{book.title} is currently unavailable.")
                    return redirect('/mybag/')

            # Save the list of books to the checkout record
            checkout_record.book_list = ', '.join(book_titles)
            checkout_record.save()

            # Deduct the total charge from the reader's account balance
            reader.account_bal -= total_charge
            reader.save()  # Save the changes to the reader's account balance

            # Clear the bag
            request.session['bag'] = []

            messages.success(request, "Checkout completed successfully!")
            return redirect('/returns/')  # Redirect to the returns page after successful checkout

        except Exception as e:
            logger.error(f"Checkout error: {e}")
            messages.error(request, "An error occurred during checkout. Please try again.")
            return redirect('/mybag/')
