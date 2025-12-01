from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Aidat, Daire, Sakin
from django.contrib.auth.models import User
from django.contrib import messages
import datetime
from .forms import UserRegisterForm 
from django.db import IntegrityError 
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            telefon = form.cleaned_data['telefon']

            try:
                # 1. Django User modelini oluştur
                user = User.objects.create_user(username=username, email=email, password=password)
                
                # 2. Sakin (Profil) modelini oluştur ve rolü varsayılan 'Sakin' ('S') yap
                Sakin.objects.create(user=user, telefon=telefon, rol='S')
                
                messages.success(request, f'Hesabınız oluşturuldu. Giriş yapabilirsiniz.')
                return redirect('login') # Başarılı kayıttan sonra giriş sayfasına yönlendir
            
            except IntegrityError:
                messages.error(request, 'Bu kullanıcı adı zaten alınmış.')
        else:
            messages.error(request, 'Formda hatalar var. Lütfen kontrol edin.')
    else:
        form = UserRegisterForm()
    
    return render(request, 'yonetim/register.html', {'form': form})
@login_required
def aidat_listesi(request):
    """Kullanıcının rolüne göre aidatları listeler."""
    try:
        sakin_profil = request.user.sakin 
    except:
        messages.error(request, "Kullanıcı profiliniz eksik. Lütfen yöneticiye başvurun.")
        return redirect('/accounts/login/')


    if sakin_profil.rol == 'Y':
        # Yönetici tüm aidatları görür
        aidatlar = Aidat.objects.all().order_by('-vade_tarihi')
    else:
        # Sakin sadece kendi dairelerinin aidatlarını görür
        daireler = Daire.objects.filter(sahibi=request.user) | Daire.objects.filter(kiraci=request.user)
        aidatlar = Aidat.objects.filter(daire__in=daireler).order_by('-vade_tarihi')
    
    context = {'aidatlar': aidatlar, 'rol': sakin_profil.rol}
    return render(request, 'yonetim/aidat_listesi.html', context)

@login_required
def aidat_ode(request, aidat_id):
    """Aidat ödeme simülasyonu."""
    aidat = get_object_or_404(Aidat, id=aidat_id)
    
    # Gerçek uygulamada burada bir ödeme kuruluşu API'si kullanılacaktır.
    
    if not aidat.odendi_mi:
        # Ödeme başarılı olursa (simülasyon)
        aidat.odendi_mi = True
        aidat.odeme_tarihi = datetime.date.today()
        aidat.save()
        messages.success(request, f"{aidat.tutar} TL tutarındaki aidat ödemeniz başarıyla kaydedildi.")
        
    else:
        messages.info(request, "Bu aidat zaten daha önce ödenmiş.")

    return redirect('aidat_listesi')

# YÖNETİCİ İŞLEVLERİ
@login_required
def toplu_borclandirma(request):
    """Sadece yöneticinin kullanabileceği toplu aidat borçlandırma işlevi."""
    if request.user.sakin.rol != 'Y':
        messages.error(request, "Bu işleme yetkiniz yoktur.")
        return redirect('aidat_listesi') 

    if request.method == 'POST':
        aidat_tutari = request.POST.get('tutar')
        vade_tarihi = request.POST.get('vade_tarihi')
        
        try:
            aidat_tutari = float(aidat_tutari)
            vade_date = datetime.date.fromisoformat(vade_tarihi)
        except (ValueError, TypeError):
            messages.error(request, "Lütfen geçerli bir tutar ve tarih girin.")
            return render(request, 'yonetim/toplu_borclandirma.html')

        daireler = Daire.objects.all()
        borclandirma_sayisi = 0
        for daire in daireler:
            Aidat.objects.get_or_create(
                daire=daire,
                aciklama="Aylık Aidat Borcu",
                vade_tarihi=vade_date,
                defaults={'tutar': aidat_tutari}
            )
            borclandirma_sayisi += 1
        
        messages.success(request, f"{borclandirma_sayisi} daireye {vade_tarihi} vadeli aidat borcu yansıtıldı.")
        return redirect('aidat_listesi')

    return render(request, 'yonetim/toplu_borclandirma.html')

# Create your views here.
