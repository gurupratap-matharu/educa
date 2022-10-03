import logging

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from courses.models import Course

logger = logging.getLogger(__name__)


def subdomain_course_middleware(get_response):
    """
    Subdomains for courses
    """

    def middleware(request):

        # Code executed for each request before the view (and later middleware) are called
        host_parts = request.get_host().split(".")

        logger.debug("host_parts: %s" % host_parts)

        if len(host_parts) > 2 and host_parts[0] != "www":
            # get course for the given domain
            course = get_object_or_404(Course, slug=host_parts[0])

            course_url = reverse("courses:course_detail", args=[course.slug])  # type: ignore

            # redirect the current request to the course detail view
            url = "{}://{}{}".format(
                request.scheme, ".".join(host_parts[1:]), course_url
            )

            logger.debug("constructed url: %s" % url)

            return redirect(url)

        response = get_response(request)
        return response

        # Code executed for each request/response after the view is called

    return middleware
