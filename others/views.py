from django import shortcuts
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, View, RedirectView


class AboutView(TemplateView):
    template_name = 'others/aboutkamper.html'


class MemberView(TemplateView):
    template_name = 'others/members.html'


class UseragreementView(TemplateView):
    template_name = 'others/useragreement.html'


class PrivacypolicyView(TemplateView):
    template_name = 'others/privacypolicy.html'


class ContactusView(TemplateView):
    template_name = 'others/contactusView.html'

class PrivacypolicyKRView(TemplateView):
    template_name = 'others/privacypolicyKR.html'

class UseragreementKRView(TemplateView):
    template_name = 'others/useragreementKR.html'

# 여기
# test
# class OrderRouteView(RedirectView):
#     def get(self, request, *args, **kwargs):
#         # [get] method isn't approved
#         return shortcuts.redirect("promotions:home")
#         # return "잘못된 접근입니다."
#
#     def post(self, request, *args, **kwargs):
#         product_pk = kwargs['pk']
#         print("scheme: ", request.scheme)
#         print("body: ", request.body)
#         print("path: ", request.path)
#         print("path_info: ",request.path_info)
#         print("method:", request.method)
#         print("encoding:", request.encoding)
#         print("GET: ", request.GET)
#         print("POST: ", request.POST)
#         print("COOKIES: ", request.COOKIES)
#         print("FILES: ", request.FILES)
#         print("META: ", request.META)
#         # print("urlconf: ", request.urlconf)  없어요
#         print("resolver_match: ", request.resolver_match)
#         # print("current_app: ", request.current_app) 없어요
#         # Attributes set by middleware
#         print("session: ", request.session)
#         # print("site: ", request.site)
#         print("user: ", request.user)
#
#         print(request.read)
#
#         for item in request:
#             print(item)
#

