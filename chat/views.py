from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden
from django.shortcuts import render


@login_required
def course_chat_room(request, course_id):
    try:
        # Retrieve the course the student has joined
        course = request.user.courses_joined.get(id=course_id)

    except ObjectDoesNotExist:
        # User is not a student of the course or the course itself does not exists
        return HttpResponseForbidden()

    return render(request, "chat/room.html", {"course": course})
