from django.urls import reverse_lazy
from django.views import generic as views
from property_rental_marketplace.property_market.models import BaseProperty, Apartment, Villa, Shop, Building, Office
from property_rental_marketplace.property_market.forms import BasePropertyForm

class PropertyListView(views.ListView):
    model = BaseProperty
    template_name = 'properties/property_list.html'
    context_object_name = 'properties'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        search_keyword = self.request.GET.get('search', '')
        property_type = self.request.GET.get('property_type', '')
        location = self.request.GET.get('location', '')

        if search_keyword:
            queryset = queryset.filter(title__icontains=search_keyword)

        if property_type:
            queryset = queryset.filter(property_type=property_type)

        if location:
            queryset = queryset.filter(location=location)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        return context
    
class PropertyCreateView(views.CreateView):
    model = BaseProperty
    template_name = 'properties/property_list.html'
    fields = '__all__'
    success_url = reverse_lazy('property_list')

    def form_valid(self, form):
        return super().form_valid(form)