from rest_framework.pagination import PageNumberPagination

class LessonCoursePagination(PageNumberPagination):
    page_size = 10  # Количество элементов по умолчанию
    page_size_query_param = 'page_size'  # Параметр для изменения размера страницы
    max_page_size = 100  # Максимально допустимое количество элементов на странице
