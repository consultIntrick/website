from django.shortcuts import render
from models import Entry, SubscriberNewsletter
from utils import get_paginated_objects
from hitcount.models import HitCount
from hitcount.views import HitCountMixin
from hitcount.views import HitCountDetailView
from hitcount import models as hit_models
from django.http import HttpResponse, HttpResponseRedirect
from itertools import chain
import smtplib


class PostCountHitDetailView(HitCountDetailView):
    model = Entry
    count_hit = True


def home_view(request):
    try:
        recent_three_blogs= Entry.objects.all().order_by('-created_at')[:3]
        template_name = 'index.html'
        return render(request, template_name, {'recent_three_blogs': recent_three_blogs})
    except:
        template_name = '404.html'
        return render(request, template_name)


def send_message(request):
    fromaddr = 'praneshps1@gmail.com'
    toaddrs  = 'kprabu@gladminds.co'
    sub = 'jgjk'
    msg = 'hai folders created'
    # Credentials (if needed)
    username = 'admin@int.com'
    password = '******'

    # The actual mail send
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()


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
    # popular_posts = Entry.objects.filter(id__in=popular_post_ids)
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
