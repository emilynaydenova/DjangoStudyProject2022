import logging

from django.http import Http404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView

from ..models import Category, FoodAndDrinks

logging.basicConfig(level=logging.DEBUG)


# redis_cache
#@method_decorator(cache_page(5), name='dispatch')
class HomeView(ListView):
    model = Category
    template_name = "home.html"
    context_object_name = "categories"
    ordering = ("title",)

    # to test caching
    # def get_context_data(self,**kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['number'] = random.randint(1,2000)
    #     return context


#@method_decorator(cache_page(5), name='dispatch')
class FoodsByCategoryListView(ListView):
    NUMBER_PER_PAGE = 4

    model = FoodAndDrinks
    template_name = "foods_by_category.html"
    context_object_name = "foods"
    ordering = ("title",)
    paginate_by = NUMBER_PER_PAGE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get query parameter from url ?category="..."
        try:
            category_id = self.request.GET.get("category", None)
            context["category"] = Category.objects.get(id=category_id)
            return context
        except self.model.DoesNotExist:
            raise Http404("Not Found Such Category")

    def get_queryset(self):
        queryset = super().get_queryset()
        # filter foods by category and being active
        try:
            category_id = self.request.GET.get("category", None)
            queryset = queryset.filter(is_active=True, category_id=category_id)
            return queryset
        except self.model.DoesNotExist:
            raise Http404("Not Found Such Category")

    def get_allow_empty(self):
        self.allow_empty = True
        return self.allow_empty


class FoodDetailsView(DetailView):
    model = FoodAndDrinks
    template_name = "food_details.html"
    context_object_name = "food"

    def get_success_url(self):
        return reverse_lazy("foods by category")
