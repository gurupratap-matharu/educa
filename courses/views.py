import json
import logging
import pdb

from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Count
from django.forms.models import modelform_factory
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from students.forms import CourseEnrollForm

from .forms import ModuleFormSet
from .models import Content, Course, Module, Subject

logger = logging.getLogger(__name__)

# Mixins


class OwnerMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin:
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin, PermissionRequiredMixin):
    model = Course
    fields = ("subject", "title", "slug", "overview")
    context_object_name = "course_list"
    success_url = reverse_lazy("courses:manage_course_list")


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    template_name = "courses/course_form.html"
    context_object_name = "course"


# Public facing Course list/detail views


class CourseListView(TemplateResponseMixin, View):
    model = Course
    template_name: str = "courses/course_list.html"

    def get(self, request, subject=None):
        subjects = Subject.objects.annotate(total_courses=Count("courses"))
        courses = Course.objects.annotate(total_modules=Count("modules"))

        if subject:
            subject = get_object_or_404(Subject, slug=subject)
            courses = courses.filter(subject=subject)

        return self.render_to_response(
            {
                "subject": subject,
                "subjects": subjects,
                "courses": courses,
            }
        )


class CourseDetailView(DetailView):
    model = Course
    context_object_name = "course"
    template_name: str = "courses/course_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["enroll_form"] = CourseEnrollForm(initial={"course": self.object})
        return context


# Instructor facing course CRUD views


class ManageCourseListView(OwnerCourseMixin, ListView):
    """
    Instructor facing course list view which allows instructors to manage their courses.
    """

    template_name = "courses/course_manage_list.html"
    permission_required = "courses.view_course"


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    permission_required = "courses.add_course"


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    permission_required = "courses.change_course"


class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = "courses/course_delete.html"
    permission_required = "courses.delete_course"
    context_object_name = "course"


# Module CRUD views

# Veer Module Delete is happening in the ModuleCreateUpdateView itself using a
# checkbox of the formset that django provides. So we do not have a view for that.


class ModuleCreateUpdateView(TemplateResponseMixin, View):
    """
    View that allows instructors to create/update multiple modules for a single course
    in one go using formsets.
    """

    template_name = "courses/module_formset.html"
    course = None

    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course, data=data)

    def dispatch(self, request, pk):
        logger.info(self.__class__.__name__, "Veer DISPATCH called")
        self.course = get_object_or_404(Course, id=pk, owner=request.user)
        return super().dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        logger.info(self.__class__.__name__, "Veer GET called")
        formset = self.get_formset()
        return self.render_to_response({"course": self.course, "formset": formset})

    def post(self, request, *args, **kwargs):
        logger.info(self.__class__.__name__, "Veer POST called")
        formset = self.get_formset(data=request.POST)

        if formset.is_valid():
            logger.info(self.__class__.__name__, "Veer formset valid")
            formset.save()
            return redirect("courses:manage_course_list")

        return self.render_to_response({"course": self.course, "formset": formset})


class ModuleContentListView(TemplateResponseMixin, View):
    """
    View to display all modules for a course and list the contents of a specific
    module.
    So this is a Read/List View for both Module and Content models!
    """

    template_name: str = "courses/content_list.html"

    def get(self, request, module_id):
        module = get_object_or_404(Module, id=module_id, course__owner=request.user)
        return self.render_to_response({"module": module})


# Content CRUD views


class ContentCreateUpdateView(TemplateResponseMixin, View):
    """
    Generic view to create or update any type of content (text, image, video, file)
    and link it to a Module.
    """

    module = None  # The Module this content is for
    model = None  # The type of content (text, image, video, file)
    obj = None  # Unsure about this... TODO
    template_name = "courses/content_form.html"
    valid_content_types = ("text", "image", "video", "file")

    def get_model(self, model_name):
        """
        Check whether the model name is one of the four content models -
        text, image, video or file.
        """

        if model_name in self.valid_content_types:
            return apps.get_model(app_label="courses", model_name=model_name)

        return None

    def get_form(self, model, *args, **kwargs):
        """
        Builds a dynamic form for any content model.
        """

        Form = modelform_factory(
            model, exclude=["owner", "order", "created", "updated"]
        )

        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):
        """
        This method is triggered by the parent `View` class which passes the arguments
        parsed from the urlconf to this method namely - module_id, model_name and id.

        As this is generic view to create or update Content of any type i.e text, image,
        video, file; We use the arguments passed in to internally identify the

            - module: to which this content is to be linked
            - model: what is the type of content
            - obj: a particular object of the model (optional)
        """

        self.module = get_object_or_404(
            Module, id=module_id, course__owner=request.user
        )

        self.model = self.get_model(model_name)

        if id:
            self.obj = get_object_or_404(self.model, id=id, owner=request.user)

        return super().dispatch(request, module_id, model_name, id)

    def get(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({"form": form, "object": self.obj})

    def post(self, request, module_id, model_name, id=None):
        form = self.get_form(
            self.model, instance=self.obj, data=request.POST, files=request.FILES
        )

        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()

            if not id:
                # new content
                Content.objects.create(module=self.module, item=obj)

            return redirect("courses:module_content_list", self.module.id)

        return self.render_to_response({"form": form, "object": self.obj})


class ContentDeleteView(View):
    def post(self, request, id):
        content = get_object_or_404(Content, id=id, module__course__owner=request.user)
        module = content.module

        content.item.delete()
        content.delete()

        return redirect("courses:module_content_list", module.id)


# Ajax views to order Module and Content
@method_decorator(csrf_exempt, name="dispatch")
class ModuleOrderView(View):
    """
    Reorders modules of a course.
    """

    def post(self, request):
        request_json = json.loads(request.body)
        for id, order in request_json.items():
            Module.objects.filter(id=id, course__owner=request.user).update(order=order)
        return JsonResponse({"saved": "OK"})


@method_decorator(csrf_exempt, name="dispatch")
class ContentOrderView(View):
    """
    Reorders contents of a module.
    """

    def post(self, request):
        request_json = json.loads(request.body)
        for id, order in request_json.items():
            Content.objects.filter(id=id, module__course__owner=request.user).update(
                order=order
            )
        return JsonResponse({"saved": "OK"})
