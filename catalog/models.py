from django.db import models
from django.urls import reverse
import uuid

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=200, help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)")

    def __str__(self):
        return self.name
    
class Book(models.Model):
    """
    Model đại diện cho một cuốn sách (nhưng không phải một bản sao cụ thể của sách).
    """
    title = models.CharField(max_length=200)

    # Khóa ngoại đến Model 'Author' (giả định Model này đã được định nghĩa)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True) 

    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    
    # ISBN phải là duy nhất
    isbn = models.CharField('ISBN', max_length=13, unique=True, 
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    
    # Mối quan hệ nhiều-nhiều với Model 'Genre' (giả định Model này đã được định nghĩa)
    genre = models.ManyToManyField('Genre', help_text='Select a genre for this book')

    def __str__(self):
        """
        Chuỗi đại diện cho đối tượng Model.
        """
        return self.title

    def get_absolute_url(self):
        """
        Trả về url để truy cập bản ghi chi tiết cho cuốn sách này.
        (Giả định có một URL pattern tên là 'book-detail')
        """
        return reverse('book-detail', args=[str(self.id)])
    
class BookInstance(models.Model):
    """
    Model đại diện cho một bản sao cụ thể của sách (tức là có thể được mượn từ thư viện).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, 
                         help_text='ID duy nhất cho bản sách cụ thể này trong toàn thư viện')
                         
    # Khóa ngoại: liên kết với Model Book. RESTRICT nghĩa là không cho phép xóa Book nếu nó còn BookInstance.
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True) 
    
    imprint = models.CharField(max_length=200)
    
    # Ngày sách dự kiến được trả lại
    due_back = models.DateField(null=True, blank=True) 
    
    # Định nghĩa các lựa chọn cho trạng thái mượn sách
    LOAN_STATUS = (
        ('m', 'Maintenance'), # Đang bảo trì
        ('o', 'On loan'),     # Đang cho mượn
        ('a', 'Available'),   # Sẵn có
        ('r', 'Reserved'),    # Đã đặt trước
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Tình trạng sẵn có của sách'
    )

    class Meta:
        # Sắp xếp các bản sao theo ngày dự kiến trả lại
        ordering = ['due_back']

    def __str__(self):
        """
        Chuỗi đại diện cho đối tượng Model.
        """
        # Trả về ID của bản sao và tiêu đề của cuốn sách mà nó thuộc về
        return f'{self.id} ({self.book.title})'
    

class Author(models.Model):
    """
    Model đại diện cho một tác giả.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    
    # Ngày sinh và ngày mất là tùy chọn (có thể để trống)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        # Sắp xếp mặc định theo Họ, sau đó là Tên
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """
        Trả về url để truy cập bản ghi chi tiết của tác giả cụ thể.
        (Giả định có một URL pattern tên là 'author-detail')
        """
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """
        Chuỗi đại diện cho đối tượng Model. Định dạng: Họ, Tên
        """
        return f'{self.last_name}, {self.first_name}'