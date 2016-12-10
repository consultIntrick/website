from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage


def get_paginated_objects(objects, page, obj_per_page):
    paginator = Paginator(objects, obj_per_page) # paginator stores the list of objects and objests per page
    try:
        paginated_objects = paginator.page(page)
    except PageNotAnInteger:
        paginated_objects = paginator.page(1)
    except EmptyPage:
        paginated_objects = paginator.page(paginator.num_pages)
    pagination_info = {
        'has_previous': paginated_objects.has_previous,
        'previous_page_number': paginated_objects.previous_page_number,
        'number': paginated_objects.number,
        'num_pages': paginated_objects.paginator.num_pages,
        'has_next': paginated_objects.has_next,
        'next_page_number': paginated_objects.next_page_number
    }
    return paginated_objects, pagination_info