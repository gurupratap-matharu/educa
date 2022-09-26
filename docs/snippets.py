from django.contrib.auth import get_user_model
from django.test import RequestFactory
from django.urls import reverse

from courses import views

# Simulate a django request and send it to view in the shell
request_factory = RequestFactory()
user = get_user_model().objects.get(username__icontains="superuser")

url = reverse("courses:module_order")

request = request_factory.post(url, data={"name": "veer"})
response = views.ModuleOrderView.as_view()(request)
