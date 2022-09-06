from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, FormView

from courses.models import Course

from .forms import CourseEnrollForm


class StudentMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])


class StudentRegistrationView(CreateView):
    template_name = "students/registration.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("students:student_course_list")

    def form_valid(self, form):
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd["username"], password=cd["password1"])
        login(self.request, user)
        return result


class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form):
        self.course = form.cleaned_data["course"]
        self.course.students.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy("students:student_course_detail", args=[self.course.id])


class StudentCourseListView(LoginRequiredMixin, StudentMixin, ListView):
    model = Course
    template_name = "students/student_course_list.html"
    context_object_name = "courses"


class StudentCourseDetailView(LoginRequiredMixin, StudentMixin, DetailView):
    model = Course
    template_name = "students/student_course_detail.html"
    context_object_name = "course"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()

        if "module_id" in self.kwargs:
            context["module"] = course.modules.get(id=self.kwargs["module_id"])
        else:
            context["module"] = course.modules.first()

        return context
