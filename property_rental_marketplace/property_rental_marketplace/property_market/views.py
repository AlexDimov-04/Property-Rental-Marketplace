from django.http import JsonResponse
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
        context['user_profile'] = self.get_user_profile()

        property_type_mapping = PROPERTY_TYPE_MAPPING
        properties = context['properties']
        additional_fields = {}

        for property_obj in properties:
            property_type = property_obj.property_type
            specific_property_info = property_type_mapping.get(property_type)

            if specific_property_info:
                specific_property_model = specific_property_info['model']
                
                try:
                    specific_property = specific_property_model.objects.get(property=property_obj)
                    additional_fields[property_obj.pk] = specific_property
                except ObjectDoesNotExist:
                    additional_fields[property_obj.pk] = None

        context['additional_fields'] = additional_fields

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