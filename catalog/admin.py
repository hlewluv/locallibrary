from django.contrib import admin
from .models import Author, Genre, Book, BookInstance

# admin.site.register(Author)
admin.site.register(Genre)
# admin.site.register(Book)
admin.site.register(BookInstance)

# 1. Tùy chỉnh Tác giả
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields  = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
admin.site.register(Author, AuthorAdmin)

# 2. Định nghĩa Inline cho Bản sao Sách (BỎ @admin.register)
class BookInstanceInline(admin.TabularInline):
    model = BookInstance

# 3. Tùy chỉnh Sách
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    # Thêm lại hàm bị thiếu
    def display_genre(self, obj):
        return ', '.join(genre.name for genre in obj.genre.all())
    display_genre.short_description = 'Genre' 

    # Sửa lỗi tên lớp: BookInstanceAdmin -> BookInstanceInline
    inlines = [BookInstanceInline]