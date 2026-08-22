# -*- coding: utf-8 -*-
"""Türkiye'nin 81 ili için doğrulanabilir coğrafi/idari sınıflandırma.

Buradaki hiçbir alan tahmin değildir: coğrafi bölge, büyükşehir statüsü ve
plaka kodu resmî idari yapıdan gelir. Nüfus, gelir, "şehrin ruhu" gibi
doğrulanamayan veya uydurmaya açık alanlar BİLEREK yoktur.
"""

# 7 coğrafi bölge — resmî sınıflandırma
BOLGE = {
    "Akdeniz": ["ADANA","ANTALYA","BURDUR","HATAY","ISPARTA","KAHRAMANMARAŞ","MERSİN","OSMANİYE"],
    "Doğu Anadolu": ["AĞRI","ARDAHAN","BİNGÖL","BİTLİS","ELAZIĞ","ERZİNCAN","ERZURUM","HAKKARİ",
                     "IĞDIR","KARS","MALATYA","MUŞ","TUNCELİ","VAN"],
    "Ege": ["AFYONKARAHİSAR","AYDIN","DENİZLİ","İZMİR","KÜTAHYA","MANİSA","MUĞLA","UŞAK"],
    "Güneydoğu Anadolu": ["ADIYAMAN","BATMAN","DİYARBAKIR","GAZİANTEP","KİLİS","MARDİN","SİİRT",
                          "ŞANLIURFA","ŞIRNAK"],
    "İç Anadolu": ["AKSARAY","ANKARA","ÇANKIRI","ESKİŞEHİR","KARAMAN","KAYSERİ","KIRIKKALE",
                   "KIRŞEHİR","KONYA","NEVŞEHİR","NİĞDE","SİVAS","YOZGAT"],
    "Karadeniz": ["AMASYA","ARTVİN","BARTIN","BAYBURT","BOLU","ÇORUM","DÜZCE","GİRESUN","GÜMÜŞHANE",
                  "KARABÜK","KASTAMONU","ORDU","RİZE","SAMSUN","SİNOP","TOKAT","TRABZON","ZONGULDAK"],
    "Marmara": ["BALIKESİR","BİLECİK","BURSA","ÇANAKKALE","EDİRNE","İSTANBUL","KIRKLARELİ","KOCAELİ",
                "SAKARYA","TEKİRDAĞ","YALOVA"],
}
IL_BOLGE = {il: b for b, iller in BOLGE.items() for il in iller}

# 30 büyükşehir belediyesi — resmî statü
BUYUKSEHIR = {
    "ADANA","ANKARA","ANTALYA","AYDIN","BALIKESİR","BURSA","DENİZLİ","DİYARBAKIR","ERZURUM",
    "ESKİŞEHİR","GAZİANTEP","HATAY","İSTANBUL","İZMİR","KAHRAMANMARAŞ","KAYSERİ","KOCAELİ","KONYA",
    "MALATYA","MANİSA","MARDİN","MERSİN","MUĞLA","ORDU","SAKARYA","SAMSUN","ŞANLIURFA","TEKİRDAĞ",
    "TRABZON","VAN",
}

# Hizmetin gerçek fiziksel merkezi — sitenin şemasındaki doğrulanmış adres
OFIS_IL, OFIS_ILCE = "ADANA", "Seyhan"
