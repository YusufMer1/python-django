from django.db import models
from django.contrib.auth.models import User

# Sakin (Kullanıcı Profili)
class Sakin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefon = models.CharField(max_length=15, blank=True, null=True)
    
    # Rol: Y = Yönetici, S = Sakin
    ROL_SECENEKLERI = [('Y', 'Yönetici'), ('S', 'Sakin')]
    rol = models.CharField(max_length=1, choices=ROL_SECENEKLERI, default='S')

    def __str__(self):
        return self.user.username

# Daireler Tablosu
class Daire(models.Model):
    daire_no = models.CharField(max_length=5, unique=True)
    sahibi = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sahip_oldugu_daireler')
    kiraci = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='kiraci_oldugu_daireler')
    metrekare = models.IntegerField(default=0)

    def __str__(self):
        return f"Daire No: {self.daire_no}"

# Aidat ve Finansal Hareketler Tablosu
class Aidat(models.Model):
    daire = models.ForeignKey(Daire, on_delete=models.CASCADE)
    tutar = models.DecimalField(max_digits=10, decimal_places=2)
    aciklama = models.CharField(max_length=200, default="Aylık Aidat")
    vade_tarihi = models.DateField()
    odendi_mi = models.BooleanField(default=False)
    odeme_tarihi = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.daire.daire_no} - {self.vade_tarihi.month}/{self.vade_tarihi.year} - {self.tutar} TL"
    
    class Meta:
        unique_together = ('daire', 'aciklama', 'vade_tarihi')


