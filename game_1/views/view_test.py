from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView
from ..serializers import *

# //////////////////////////// TESTS ////////////////////////////////////////

class FindMethodsView(TemplateView):
    """Узнаем в каком порядке вызываютя методы"""
    """
    __init__
    setup
    dispatch
    get
    get_context_data
    render_to_response
    get_template_names
    """

    template_name = 'game_1/find_methods.html'

    def __init__(self, **kwargs):
        print("__init__")
        self.find_method = "I am here"
        super().__init__(**kwargs)

    def setup(self, request, *args, **kwargs):
        print("setup__113")
        print("**kwargs -", kwargs)
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        print("dispatch")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        print("get")
        kwargs['find_method'] = ":::::::::"
        messages.success(request, '1 Profile updated successfully')
        messages.success(request, '2 Profile updated successfully')
        messages.success(request, '3 Profile updated successfully')

        return HttpResponseRedirect(reverse("find_2"))
        return super().get(request, *args, **kwargs)

    # def get_queryset(self):
    #     print("get_queryset")
    #     return super().get_queryset()

    def get_context_data(self, **kwargs):
        print("get_context_data")
        return super().get_context_data(**kwargs)

    def get_template_names(self):
        print("get_template_names")
        return super().get_template_names()

    # def get_context_object_name(self, object_list):
    #     print("get_context_object_name")
    #     return super().get_context_object_name(object_list)

    def render_to_response(self, context, **response_kwargs):
        print("render_to_response")
        return super().render_to_response(context, **response_kwargs)

    # def as_view(cls, **initkwargs):
    #     print("as_view")
    #     return super().as_view(cls, **initkwargs)


class FindMethodsSecondView(TemplateView):
    """Проверка реверса"""

    template_name = 'game_1/find_methods.html'

    def get(self, request, *args, **kwargs):
        # kwargs['find_method_2'] = "3333333333"
        return super().get(request, *args, **kwargs)