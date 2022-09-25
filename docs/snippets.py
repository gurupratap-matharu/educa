from django.contrib.auth import get_user_model
from django.test import RequestFactory
from django.urls import reverse

from courses import views

request_factory = RequestFactory()
user = get_user_model().objects.get(username__icontains="superuser")

url = reverse("courses:module_order")

request = request_factory.post(url, data={"name": "veer"})
response = views.ModuleOrderView.as_view()(request)


from urllib.parse import parse_qs, urlparse

url_data = urlparse("http://www.youtube.com/watch?v=z_AbfPXTKms&NR=1")
query = parse_qs(url_data.query)
video = query["v"][0]
