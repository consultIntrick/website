from itertools import chain

from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from hitcount import models as hit_models
from hitcount.models import HitCount
from hitcount.views import HitCountDetailView
from hitcount.views import HitCountMixin

from .models import Entry, SubscriberNewsletter, ViewerMessage
from .utils import get_paginated_objects


class PostCountHitDetailView(HitCountDetailView):
    model = Entry
    count_hit = True


def home_view(request):
    try:
        recent_three_blogs = Entry.objects.all().order_by('-created_at')[:3]
        template_name = 'index.html'
        return render(request, template_name, {'recent_three_blogs': recent_three_blogs})
    except:
        template_name = '404.html'
        return render(request, template_name)


def bloglist_view(request):
    """
        requests:page_num
        bl:
         return : it will get all blogs from db and paginate by 2 per single page
        :param request:
        :return:
        """
    search_query = request.GET.get('search')
    if search_query:
        result_1 = Entry.objects.filter(title__istartswith=search_query)
        result_2 = Entry.objects.filter(title__icontains=search_query).exclude(title__istartswith=search_query)
        blog_results = [list(chain(result_1, result_2))]
        all_blogs = blog_results[0]
    else:
        all_blogs = Entry.objects.all()
    page = request.GET.get('page')
    all_blogs, pagination_info = get_paginated_objects(all_blogs, page, 3)
    template_name = 'blog-archive.html'
    popular_posts = popular_post()
    return render(request, template_name, {'all_blogs': all_blogs,
                                           'pagination_info': pagination_info,
                                           'search_query': search_query,
                                           'popular_posts': popular_posts})


def blog_view(request, blog_id, slug):
    blog = Entry.objects.get(id=blog_id)
    popular_posts = popular_post()
    template_name = 'blog-single.html'
    hit_count = HitCount.objects.get_for_object(blog)
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    return render(request, template_name, {'blog': blog, 'popular_posts': popular_posts}, )


def popular_post():
    popular_post_ids = hit_models.HitCount.objects.filter().order_by('-hits')[:3]. \
        values_list('object_pk', flat=True)
    popular_posts = []
    for post_id in popular_post_ids:
        popular_posts.append(Entry.objects.get(id=post_id))
    return popular_posts


def subscribe_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email_id')
        if not SubscriberNewsletter.objects.filter(email_id=email).exists():
            SubscriberNewsletter.objects.create(email_id=email)
            return HttpResponse('subscribed', status=200)
        else:
            return HttpResponse('exists', status=302)


def get_message_from_viewer(request):
    name = str(request.POST.get('name')).strip()
    email = str(request.POST.get('email')).strip()
    message = str(request.POST.get('message')).strip()
    ViewerMessage.objects.create(name=name, email=email, message=message)
    email_to_viewer = EmailMessage('Thank you! ' + name,
                                   'Hi ' + name + ',\r\n'
                                                  '\r\nThanks for reaching us. Will get back to you shortly.\r\n'
                                                  '\r\n\r\nRegards,\r\n'
                                                  'Intrick Success Team\r\n',
                                   'Intrick Success Team',
                                   [email],
                                   reply_to=['support@intrick.com'], )
    email_to_viewer.send(fail_silently=False)
    email_to_intrick = EmailMessage('A message from ' + name + "(" + email + ")",
                                    message,
                                    'Intrick Bot',
                                    ['info.intrick@gmail.com'])
    email_to_intrick.send(fail_silently=False)
    return HttpResponse('success', status=200)
