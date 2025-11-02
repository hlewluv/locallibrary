from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from catalog.models import Book, Author, BookInstance, Genre
# Create your views here.
from django.views import generic

class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book 
    paginate_by = 1
    login_url = '/accounts/login/'  # Optional: chỉ định URL login
    redirect_field_name = 'next'    # Optional: tên parameter redirect
    
class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book
    login_url = '/accounts/login/'
    redirect_field_name = 'next'
    
class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """View hiển thị danh sách sách mà user hiện tại đang mượn"""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed.html'
    paginate_by = 10

    def get_queryset(self):
        """Lấy danh sách sách mà user hiện tại đang mượn"""
        return BookInstance.objects.filter(
            borrower=self.request.user
        ).filter(
            status__exact='o'  # 'o' = On loan (đang cho mượn)
        ).order_by('due_back')


def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()  # The 'all()' is implied by default.

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable.
    return render(request, 'index.html', context=context)