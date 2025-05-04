from django.contrib import admin
from .models import Viloyat, District, Institution, MaintenanceRecord, ExpenseBreakdown, Complaint,FreeMedication


@admin.register(Viloyat)
class ViloyatAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'viloyat')
    list_filter = ('viloyat',)
    search_fields = ('name',)


class ExpenseBreakdownInline(admin.TabularInline):
    model = ExpenseBreakdown
    extra = 1


@admin.register(MaintenanceRecord)
class MaintenanceRecordAdmin(admin.ModelAdmin):
    list_display = ('institution', 'year', 'amount', 'reason')
    list_filter = ('year', 'institution__district__viloyat')
    search_fields = ('institution__name', 'reason')
    inlines = [ExpenseBreakdownInline]

class FreeMedicationInline(admin.TabularInline):
    model = FreeMedication
    extra = 1

@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'institution_type', 'district', 'maintenance_budget', 'maintenance_reason')
    list_filter = ('institution_type', 'district__viloyat')
    search_fields = ('name', 'maintenance_reason')
    inlines = [FreeMedicationInline]  # ← bu yerga qo‘shdik!
    def get_fields(self, request, obj=None):
        fields = ['name', 'institution_type', 'district', 'maintenance_budget', 'maintenance_reason']
        if obj and obj.institution_type == 'hospital':
            fields.append('ree_medications_list')
        return fields

    def get_fields(self, request, obj=None):
        fields = ['name', 'institution_type', 'district']
        if obj and obj.institution_type == 'hospital':
            fields.append('ree_medications_list')
        else:
            fields += ['maintenance_budget', 'maintenance_reason']
        return fields

    def get_readonly_fields(self, request, obj=None):
        return []


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "institution",
        "first_name",
        "last_name",
        "phone_number",
        "created_at",
    )
    list_filter = ("institution__district__viloyat", "created_at")
    search_fields = (
        "first_name",
        "last_name",
        "phone_number",
        "passport_number",
        "description",
        "institution__name",
    )
    readonly_fields = ("created_at",)

    fieldsets = (
        (None, {
            "fields": (
                "institution",
                ("first_name", "last_name"),
                "phone_number",
                "passport_number",
                "description",
                "attachment",
                "created_at",
            )
        }),
    )
