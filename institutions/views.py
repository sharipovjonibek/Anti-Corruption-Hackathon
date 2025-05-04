from django.shortcuts import render, get_object_or_404,redirect
from django.http import JsonResponse
from .models import Institution, District,Complaint
from .forms import InstitutionSearchForm,ComplaintForm
from django.contrib.auth.decorators import login_required

@login_required
def institution_search(request):
    form = InstitutionSearchForm(request.GET or None)
    institutions = Institution.objects.all()

    if form.is_valid():
        viloyat = form.cleaned_data.get('viloyat')
        district = form.cleaned_data.get('district')
        institution_type = form.cleaned_data.get('institution_type')

        if district:
            institutions = institutions.filter(district=district)
        elif viloyat:
            districts_in_viloyat = District.objects.filter(viloyat=viloyat)
            institutions = institutions.filter(district__in=districts_in_viloyat)

        if institution_type:
            institutions = institutions.filter(institution_type=institution_type)

    return render(request, 'institution_search.html', {'form': form, 'institutions': institutions})


def load_districts(request):
    viloyat_id = request.GET.get('viloyat_id')
    if viloyat_id:
        districts = District.objects.filter(viloyat_id=viloyat_id).order_by('name')
        district_list = [{'id': d.id, 'name': d.name} for d in districts]
        return JsonResponse({'districts': district_list})
    return JsonResponse({'districts': []})

def format_money(amount):
    if amount >= 1_000_000_000:
        return f"{amount // 1_000_000_000} milliard so'm"
    elif amount >= 1_000_000:
        return f"{amount // 1_000_000} mln so'm"
    else:
        return f"{amount:,} so'm"


def institution_detail(request, pk):
    institution = Institution.objects.get(pk=pk)
    maintenance_records = institution.maintenance_records.all()
    complaints = Complaint.objects.filter(institution=institution)  

    for record in maintenance_records:
        record.formatted_amount = format_money(record.amount)

        breakdowns = list(record.breakdowns.all())
        for breakdown in breakdowns:
            breakdown.formatted_amount = format_money(breakdown.amount)

        record.breakdowns_list = breakdowns

    return render(request, 'institution_detail.html', {
        'institution': institution,
        'maintenance_records': maintenance_records,
        'complaints': complaints, 
    })


def complaint_create(request, institution_id):
    institution = get_object_or_404(Institution, pk=institution_id)
    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.institution = institution
            complaint.save()
            return redirect('institution_detail', pk=institution.id)
    else:
        form = ComplaintForm()
    return render(request, 'complaint_form.html', {
        'form': form, 
        'institution': institution,
    })
