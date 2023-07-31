from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic as views
from property_rental_marketplace.property_market.models import BaseProperty, Apartment \
    ,Villa, Shop, Building, Office
from property_rental_marketplace.profile_management.views import UserProfileMixin
from property_rental_marketplace.property_market.forms import BasePropertyForm, ApartmentForm \
    ,VillaForm, OfficeForm, ShopForm, BuildingForm
from django.core.exceptions import ObjectDoesNotExist

PROPERTY_TYPE_MAPPING = {
    'Apartment': {
        'model': Apartment,
        'form': ApartmentForm,
    },
    'Villa': {
        'model': Villa,
        'form': VillaForm,
    },
    'Office': {
        'model': Office,
        'form': OfficeForm,
    },
    'Shop': {
        'model': Shop,
        'form': ShopForm,
    },
    'Building': {
        'model': Building,
        'form': BuildingForm,
    },
}

class PropertyListView(UserProfileMixin, views.ListView):
    model = BaseProperty
    template_name = 'properties/property_list.html'
    context_object_name = 'properties'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset().select_related(
            'apartment', 'villa', 'office', 'shop', 'building'
        )
        
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(title__icontains=search)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['user_profile'] = self.get_user_profile()
        return context
    
class PropertyCreateView(UserProfileMixin, views.CreateView):
    model = BaseProperty
    form_class = BasePropertyForm
    template_name = 'properties/property_create.html'
    success_url = reverse_lazy('property_list')

    def form_valid(self, form):
        property_type = form.cleaned_data['property_type']

        specific_property_info = PROPERTY_TYPE_MAPPING.get(property_type)

        if specific_property_info:
            specific_property_model = specific_property_info['model']
            specific_property_form = specific_property_info['form']

            specific_form = specific_property_form(self.request.POST)
            if specific_form.is_valid():
                base_property = form.save(commit=False)
                base_property.property_type = property_type
                base_property.save()

                specific_property = specific_form.save(commit=False)
                specific_property.property = base_property  
                specific_property.save()

                return super().form_valid(form)
            
        return JsonResponse({'error': 'Invalid property type'}, status=400)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_profile'] = self.get_user_profile()
        return context

def get_additional_form_fields(request):
    property_type = request.GET.get('property_type')
    form_classes = {
        'Apartment': ApartmentForm,
        'Villa': VillaForm,
        'Office': OfficeForm,
        'Shop': ShopForm,
        'Building': BuildingForm,
    }

    form_class = form_classes.get(property_type)
    if form_class:
        form = form_class()
        html = form.as_p()
    else:
        html = ''

    return JsonResponse({'html': html})