import re
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
import string
import json
from datetime import datetime


def sifre_gucu(sifre):
    guc = 0

    # Uzunluk kontrolü
    if len(sifre) >= 8:
        guc += 20

    # Büyük harf kontrolü
    if re.search("[A-Z]", sifre):
        guc += 20

    # Küçük harf kontrolü
    if re.search("[a-z]", sifre):
        guc += 20

    # Sayı kontrolü
    if re.search("[0-9]", sifre):
        guc += 20

    # Özel karakter kontrolü
    if re.search("[!@#$%^&*(),.?\":{}|<>]", sifre):
        guc += 20

    return guc


def log_kaydi(sifre, guc):
    log = {
        'tarih': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'sifre': sifre,
        'guc': guc
    }

    with open('olusturulan_sifreler.json', 'a') as log_file:
        json.dump(log, log_file)
        log_file.write('\n')


def hesapla():
    sifre = sifre_giris.get()
    guc = sifre_gucu(sifre)
    yuzde_guc = (guc / 100) * 100
    sonuc_label.config(text=f"Şifre Gücü: {yuzde_guc:.2f}%")

    if yuzde_guc < 65:
        oneri_label.config(text="Şifre gücü düşük. Daha güçlü bir şifre kullanmanızı öneririm.")
        olustur_buton.grid(row=5, column=0, pady=10)
        kopyala_buton.grid_forget()
        goster_buton.grid_forget()
    else:
        oneri_label.config(text="")
        olustur_buton.grid_forget()
        kopyala_buton.grid(row=5, column=0, pady=10)
        goster_buton.grid(row=5, column=1, pady=10)

    # Log kaydı ekle
    log_kaydi(sifre, yuzde_guc)


def olustur_sifre():
    global rastgele_sifre
    rastgele_sifre = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=12))
    sifre_giris.delete(0, tk.END)
    sifre_giris.insert(0, rastgele_sifre)
    messagebox.showinfo("Rastgele Şifre Oluşturuldu", "Rastgele bir şifre oluşturuldu.")
    kopyala_buton.grid(row=5, column=0, pady=10)
    goster_buton.grid(row=5, column=1, pady=10)


def kopyala_sifre():
    pencere.clipboard_clear()
    pencere.clipboard_append(rastgele_sifre)
    pencere.update()
    messagebox.showinfo("Şifre Kopyalandı", "Şifre panoya kopyalandı.")


def goster_sifre():
    sifre_giris.delete(0, tk.END)
    sifre_giris.insert(0, rastgele_sifre)
    goster_buton.config(command=gizle_sifre, text="Gizle")
    kopyala_buton.grid(row=5, column=0, pady=10)
    goster_buton.grid(row=5, column=1, pady=10)


def gizle_sifre():
    sifre_giris.delete(0, tk.END)
    sifre_giris.insert(0, '*' * 12)
    goster_buton.config(command=goster_sifre, text="Göster")
    kopyala_buton.grid(row=5, column=0, pady=10)
    goster_buton.grid(row=5, column=1, pady=10)


# Tkinter penceresi oluştur
pencere = tk.Tk()
pencere.title("Şifre Gücü Ölçer")

# Arka plan rengini değiştir
pencere.configure(bg='#f0f0f0')

# Giriş ve buton widget'ları
sifre_etiket = ttk.Label(pencere, text="Şifrenizi Girin:", font=("Helvetica", 12), background='#f0f0f0')
sifre_giris = ttk.Entry(pencere, font=("Helvetica", 12))
hesapla_buton = ttk.Button(pencere, text="Hesapla", command=hesapla, style='TButton', cursor='hand2')

# Sonuç ve öneri widget'ları
sonuc_label = ttk.Label(pencere, text="Şifre Gücü: ", font=("Helvetica", 12), background='#f0f0f0')
oneri_label = ttk.Label(pencere, text="", font=("Helvetica", 12), foreground='red', background='#f0f0f0')
olustur_buton = ttk.Button(pencere, text="Oluştur", command=olustur_sifre, style='TButton', cursor='hand2')
olustur_buton.grid_forget()

# Kopyala ve Göster butonları
kopyala_buton = ttk.Button(pencere, text="Kopyala", command=kopyala_sifre, style='TButton', cursor='hand2')
goster_buton = ttk.Button(pencere, text="Göster", command=goster_sifre, style='TButton', cursor='hand2')
kopyala_buton.grid_forget()
goster_buton.grid_forget()

# Yüzde oranı widget'ı
oran_label = ttk.Label(pencere, text="", font=("Helvetica", 10), foreground='#555555', background='#f0f0f0')

# Stil oluştur
style = ttk.Style()
style.configure('TButton', font=('Helvetica', 12))

# Widget'ları yerleştir
sifre_etiket.grid(row=0, column=0, pady=10)
sifre_giris.grid(row=0, column=1, pady=10)
hesapla_buton.grid(row=1, column=0, columnspan=2, pady=10)
sonuc_label.grid(row=2, column=0, columnspan=2, pady=10)
oneri_label.grid(row=3, column=0, columnspan=2, pady=10)
olustur_buton.grid(row=4, column=0, pady=10)

# Pencereyi başlat
pencere.mainloop()
