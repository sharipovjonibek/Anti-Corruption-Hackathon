from django.db import models

class Viloyat(models.Model):
    """Viloyat modeli: hudud nomi"""
    name = models.CharField(max_length=100, verbose_name="Viloyat nomi")

    def __str__(self):
        return self.name


class District(models.Model):
    """Tuman modeli: viloyatga tegishli tuman"""
    name = models.CharField(max_length=100, verbose_name="Tuman nomi")
    viloyat = models.ForeignKey(Viloyat, on_delete=models.CASCADE, null=True, verbose_name="Viloyat")

    def __str__(self):
        return f"{self.name} ({self.viloyat.name})"
    

class Institution(models.Model):
    """Davlat muassasasi modeli: maktab, bog‘cha, shifoxona va boshqalar"""
    INSTITUTION_TYPES = [
        ('school', 'Maktab'),
        ('kindergarten', 'Bog\'cha'),
        ('hospital', 'Shifoxona'),
    ]
    name = models.CharField(max_length=200, verbose_name="Muassasa nomi")
    institution_type = models.CharField(max_length=50, choices=INSTITUTION_TYPES, verbose_name="Muassasa turi")
    district = models.ForeignKey(District, on_delete=models.CASCADE, verbose_name="Tuman")
    maintenance_budget = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name="Umumiy ta'mirlash budjeti")
    maintenance_reason = models.CharField(max_length=255, blank=True, verbose_name="Ta'mirlash sababi")
    ree_medications_list = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} | {self.get_institution_type_display()} | {self.district.name} | {self.district.viloyat.name}"
    
class FreeMedication(models.Model):
    """Shifoxonadagi bepul dorilar ro'yxati"""
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='free_medications', verbose_name="Muassasa")
    name = models.CharField(max_length=200, verbose_name="Dori nomi")
    description = models.TextField(blank=True, verbose_name="Qo'shimcha ma'lumot (ixtiyoriy)")
    
    def __str__(self):
        return self.name

class MaintenanceRecord(models.Model):
    """Ta'mirlash tarixi modeli"""
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='maintenance_records', verbose_name="Muassasa")
    year = models.PositiveIntegerField(verbose_name="Yil")
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Ajratilgan summa")
    reason = models.CharField(max_length=255, verbose_name="Ta'mirlash sababi")

    def __str__(self):
        return f"{self.institution.name} ({self.year}) - {self.amount:,} so'm - {self.reason}"


class ExpenseBreakdown(models.Model):
    """Ta'mirlash uchun xarajatlar taqsimoti"""
    maintenance_record = models.ForeignKey(MaintenanceRecord, on_delete=models.CASCADE, related_name='breakdowns', verbose_name="Ta'mirlash tarixi")
    category = models.CharField(max_length=100, verbose_name="Xarajat kategoriyasi")
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Xarajat summasi")

    def __str__(self):
        return f"{self.category}: {self.amount:,} so'm"


class Complaint(models.Model):
    """Foydalanuvchi shikoyati"""
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='complaints', verbose_name="Muassasa")
    first_name = models.CharField(max_length=100, verbose_name="Ism")
    last_name = models.CharField(max_length=100, verbose_name="Familiya")
    phone_number = models.CharField(max_length=20, verbose_name="Telefon raqami")
    passport_number = models.CharField(max_length=20, verbose_name="Pasport raqami")
    description = models.TextField(verbose_name="Shikoyat matni")
    attachment = models.FileField(upload_to='complaints/', blank=True, null=True, verbose_name="Ilova (foto, hujjat)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yuborilgan sana")

    def __str__(self):
        return f"Shikoyat: {self.first_name} {self.last_name} - {self.institution.name}"
