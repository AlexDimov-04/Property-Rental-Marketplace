from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic as views
from property_rental_marketplace.property_market.models import BaseProperty, SavedProperty, Apartment \
    ,Villa, Shop, Building, Office
from property_rental_marketplace.profile_management.views import UserProfileMixin
from property_rental_marketplace.property_market.forms import BasePropertyForm, ApartmentForm \
    ,VillaForm, OfficeForm, ShopForm, BuildingForm, SavePropertyForm

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
        
        search_by_title = self.request.GET.get('search_by_title', '')
        search_by_property_type = self.request.GET.get('property_type', '')
        search_by_location = self.request.GET.get('location', '')

        if search_by_title:
            queryset = queryset.filter(title__icontains=search_by_title)

        if search_by_property_type:
            queryset = queryset.filter(property_type__icontains=search_by_property_type)

        if search_by_location:
            queryset = queryset.filter(location__icontains=search_by_location)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_by_title'] = self.request.GET.get('search_by_title', '')
        context['search_by_property_type'] = self.request.GET.get('property_type', '')
        context['search_by_location'] = self.request.GET.get('location', '')
        context['property_types'] = BaseProperty.TYPE_CHOICES

        if self.request.user.is_authenticated:
            context['user_profile'] = self.get_user_profile()
            user_profile = self.get_user_profile()
            saved_properties = SavedProperty.objects.filter(user=user_profile.user).values_list('property', flat=True)

            context['saved_properties'] = saved_properties

        return context
 
class PropertyCreateView(UserProfileMixin, views.CreateView):
    model = BaseProperty
    form_class = BasePropertyForm
    template_name = 'properties/property_create.html'
    success_url = reverse_lazy('property_list')

    def form_valid(self, form):
        property_type = form.cleaned_data['property_type']
        form.instance.owner = self.request.user

        specific_property_info = PROPERTY_TYPE_MAPPING.get(property_type)

        if specific_property_info:
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
            
        return super().form_invalid(form)
    
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
        html = ''
        for field in form:
            html += str(field)
    else:
        html = ''

    return JsonResponse({'html': html})

class PropertyDetailsView(UserProfileMixin, views.DetailView):
    model = BaseProperty
    template_name = 'properties/property_details.html'
    context_object_name = 'property'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_profile'] = self.get_user_profile()
        context['owner_first_name'] = self.object.owner.userprofile.first_name
        context['owner_last_name'] = self.object.owner.userprofile.last_name
        context['owner_phone'] = self.object.owner.userprofile.phone  
        context['owner_email'] = self.object.owner.userprofile.email

        if self.request.user.is_authenticated:
            property_object = self.object
            user_profile = self.get_user_profile() 

            property_saved = SavedProperty.objects.filter(user=user_profile.user, property=property_object).exists()
            context['property_saved'] = property_saved

        return context

class PropertyUpdateView(UserProfileMixin, views.UpdateView):
    model = BaseProperty
    form_class = BasePropertyForm
    template_name = 'properties/property_update.html'
    context_object_name = 'property'

    def get_success_url(self):
        return reverse('property_details', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.object.pk
        context['user_profile'] = self.get_user_profile()
        property_object = self.object

        additional_fields = None
        if property_object.property_type:
            if property_object.property_type == 'Apartment':
                additional_fields = get_object_or_404(Apartment, property=property_object)
            elif property_object.property_type == 'Villa':
                additional_fields = get_object_or_404(Villa, property=property_object)
            elif property_object.property_type == 'Office':
                additional_fields = get_object_or_404(Office, property=property_object)
            elif property_object.property_type == 'Shop':
                additional_fields = get_object_or_404(Shop, property=property_object)
            elif property_object.property_type == 'Building':
                additional_fields = get_object_or_404(Building, property=property_object)

        context['additional_fields'] = additional_fields

        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Property updated successfully.')

        self.object = form.save()

        additional_fields = None
        if self.object.property_type:
            if self.object.property_type == 'Apartment':
                additional_fields = get_object_or_404(Apartment, property=self.object)
                additional_form = ApartmentForm(self.request.POST, instance=additional_fields)
            elif self.object.property_type == 'Villa':
                additional_fields = get_object_or_404(Villa, property=self.object)
                additional_form = VillaForm(self.request.POST, instance=additional_fields)
            elif self.object.property_type == 'Office':
                additional_fields = get_object_or_404(Office, property=self.object)
                additional_form = OfficeForm(self.request.POST, instance=additional_fields)
            elif self.object.property_type == 'Shop':
                additional_fields = get_object_or_404(Shop, property=self.object)
                additional_form = ShopForm(self.request.POST, instance=additional_fields)
            elif self.object.property_type == 'Building':
                additional_fields = get_object_or_404(Building, property=self.object)
                additional_form = BuildingForm(self.request.POST, instance=additional_fields)

        if additional_fields:
                if additional_form.is_valid():
                    additional_form.save()

        return super().form_valid(form)
 
class PropertyDeleteView(views.DeleteView):
    model = BaseProperty
    template_name = 'properties/property_delete.html'
    success_url = reverse_lazy('property_list')

    def form_valid(self, form):
        messages.success(self.request, 'Property successfully deleted.')
        return super().form_valid(form)

class SavePropertyView(views.View):
    model = BaseProperty
    form_class = SavePropertyForm

    def post(self, request, pk):
        property_object = get_object_or_404(self.model, pk=pk)
        user_profile = request.user.userprofile

        if SavedProperty.objects.filter(user=user_profile.user, property=property_object).exists():
            messages.error(request, 'This property is already saved.')
        else:
            form = self.form_class(request.POST)

            saved_property = form.save(commit=False)
            saved_property.user = user_profile.user
            saved_property.property = property_object
            saved_property.save()

            messages.success(request, 'Property saved successfully.')

        return redirect('property_list')

class UnsavePropertyView(views.View):
    model = BaseProperty

    def post(self, request, pk):
        property_object = get_object_or_404(self.model, pk=pk)
        user_profile = request.user.userprofile

        try:
            saved_property = SavedProperty.objects.get(user=user_profile.user, property=property_object)
            saved_property.delete()
            messages.success(request, 'Property unsaved successfully.')
        except SavedProperty.DosesNotExist:
            messages.error(request, 'This property is not saved.')

        return redirect('property_list')
