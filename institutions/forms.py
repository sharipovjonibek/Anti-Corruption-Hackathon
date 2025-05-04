from django import forms
from .models import Viloyat, District, Institution

class InstitutionSearchForm(forms.Form):
    viloyat = forms.ModelChoiceField(queryset=Viloyat.objects.all(), required=False, label="Viloyat")
    district = forms.ModelChoiceField(queryset=District.objects.none(), required=False, label="Tuman")
    institution_type = forms.ChoiceField(choices=[('', 'Barchasi')] + Institution.INSTITUTION_TYPES, required=False, label="Muassasa turi")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'viloyat' in self.data:
            try:
                viloyat_id = int(self.data.get('viloyat'))
                self.fields['district'].queryset = District.objects.filter(viloyat_id=viloyat_id).order_by('name')
            except (ValueError, TypeError):
                self.fields['district'].queryset = District.objects.none()
        elif self.initial.get('viloyat'):
            viloyat_id = self.initial.get('viloyat').id
            self.fields['district'].queryset = District.objects.filter(viloyat_id=viloyat_id).order_by('name')

from .models import Complaint

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['first_name', 'last_name', 'phone_number', 'passport_number', 'description', 'attachment']

