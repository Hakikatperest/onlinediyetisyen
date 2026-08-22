# -*- coding: utf-8 -*-
"""İl bazlı GERÇEK bağlam verisi.

Kural: buraya yalnızca doğrulanabilir bilgi girer.
  ✓ Yöresel mutfak (kültürel olgu), iklim karakteri, üniversite varlığı,
    ofise fiziksel erişim gerçeği, idari statü.
  ✗ Nüfus/gelir istatistiği, "şehrin ruhu" klişesi, sahte danışan, sahte şube.

`mutfak_notu` alanı sayfanın özgün değer çekirdeğidir: bir diyetisyenin o
yörenin sofrasına dair söyleyeceği, BAŞKA İL SAYFASINDA GEÇMEYECEK somut şey.
Boş bırakılan il, bölge varsayılanıyla çalışır ve `durum='taslak'` işaretlenir.
"""
from regions import IL_BOLGE, BUYUKSEHIR, OFIS_IL

# ---- Bölge tabanı: il verisi girilmemişse güvenli, genel ama doğru zemin ----
BOLGE_TABAN = {
    "Akdeniz": dict(
        iklim="uzun ve sıcak yazlar, ılık kışlar",
        iklim_notu="Yaz aylarında sıvı kaybı ve iştah dalgalanması belirginleşir; öğün saatleri sıcağa göre kayar.",
        mutfak=["zeytinyağlı sebze yemekleri", "narenciye", "bulgur pilavı"],
        mutfak_notu="Akdeniz sofrası zeytinyağı ve sebze açısından güçlü bir zemin sunar; asıl mesele porsiyon ve tahıl dengesidir.",
    ),
    "Ege": dict(
        iklim="ılıman yazlar, yağışlı ve ılık kışlar",
        iklim_notu="Yıl boyu taze ot ve sebze erişimi yüksektir; mevsimsel çeşitlilik planlamayı kolaylaştırır.",
        mutfak=["zeytinyağlılar", "ot kavurmaları", "deniz ürünleri"],
        mutfak_notu="Ege mutfağı zaten dengeye yakın; kazanç çoğunlukla ekmek-meze miktarının ayarlanmasından gelir.",
    ),
    "Marmara": dict(
        iklim="dört mevsim belirgin, nemli",
        iklim_notu="Uzun ulaşım süreleri ve vardiyalı çalışma düzeni öğün saatlerini düzensizleştirir.",
        mutfak=["hamur işleri", "deniz ürünleri", "dışarıda yeme alışkanlığı"],
        mutfak_notu="Marmara'da asıl zorluk yemeğin içeriği değil, günün hangi saatinde ve nerede yendiğidir.",
    ),
    "İç Anadolu": dict(
        iklim="karasal; sıcak yazlar, sert ve uzun kışlar",
        iklim_notu="Kış aylarında dışarıda hareket süresi kısalır; günlük adım sayısı belirgin düşer.",
        mutfak=["etli hamur yemekleri", "tarhana", "buğday ve bulgur ağırlıklı sofra"],
        mutfak_notu="İç Anadolu sofrasında tahıl payı yüksektir; protein ve sebzeyi öğüne eklemek çoğu zaman çıkarmaktan daha etkilidir.",
    ),
    "Karadeniz": dict(
        iklim="yıl boyu yağışlı, nemli",
        iklim_notu="Yağışlı günlerin çokluğu açık hava hareketini kesintiye uğratır; iç mekân alternatifi planlanmalıdır.",
        mutfak=["hamsi ve diğer balıklar", "mısır ekmeği", "karalahana", "süt ürünleri"],
        mutfak_notu="Karadeniz sofrasının balık ve yeşillik tarafı güçlüdür; mısır ekmeği ve tereyağı miktarı ise takip gerektirir.",
    ),
    "Doğu Anadolu": dict(
        iklim="sert ve uzun kışlar, kısa yazlar",
        iklim_notu="Kış çok uzundur; hareketsiz geçen aylar ve enerji yoğun geleneksel sofra bir arada değerlendirilir.",
        mutfak=["et yemekleri", "süt ve peynir çeşitleri", "kışlık kavurma"],
        mutfak_notu="Doğu Anadolu'da protein erişimi güçlüdür; denge çoğunlukla sebze ve lif tarafının artırılmasıyla kurulur.",
    ),
    "Güneydoğu Anadolu": dict(
        iklim="çok sıcak ve kurak yazlar, ılık kışlar",
        iklim_notu="Yaz sıcağı gündüz iştahını bastırıp akşam öğününü ağırlaştırabilir; sıvı takibi önem kazanır.",
        mutfak=["bulgur temelli yemekler", "acılı ve baharatlı sofra", "tatlı geleneği"],
        mutfak_notu="Güneydoğu sofrasında bulgur ve baklagil zemini değerlidir; asıl konu tatlı sıklığı ve porsiyon büyüklüğüdür.",
    ),
}

# ---- İl özel verisi (doğrulanabilir kültürel/coğrafi olgular) ----
IL_OZEL = {
    "ADANA": dict(
        mutfak=["Adana kebabı", "şalgam suyu", "analı kızlı", "bici bici", "humus"],
        mutfak_notu=(
            "Adana sofrasının kendine has bir dengesi var: kebabın yanında giden şalgam ve bol yeşillik "
            "aslında porsiyonu tamamlayan unsurlar. Danışanlarda sık gördüğümüz mesele etin kendisi değil, "
            "yanındaki lavaş miktarı ve gece geç saatte kurulan sofra düzeni. Analı kızlı gibi bulgur-baklagil "
            "temelli yemekler ise diyet içinde rahatlıkla yer bulabiliyor."
        ),
        ozel="Hizmetin fiziksel merkezi bu ilde: Seyhan'daki ofiste yüz yüze görüşme de mümkün.",
        universite="Çukurova Üniversitesi",
    ),
    "MERSİN": dict(
        mutfak=["tantuni", "cezerye", "kerebiç", "narenciye", "humus"],
        mutfak_notu=(
            "Mersin'de öne çıkan iki şey var: ayaküstü tantuni kültürü ve yıl boyu erişilebilen narenciye. "
            "Tantuni aslında porsiyonu kontrol edilebilir bir seçenek — sorun genelde yanına eklenen "
            "şalgam-ayran-tatlı üçlüsünün alışkanlığa dönüşmesi. Cezerye ise havuç temelli olsa da "
            "şeker yoğunluğu nedeniyle 'sağlıklı atıştırmalık' sanılıp fazla tüketilebiliyor."
        ),
        ozel="Öğün saatlerinin gün içinde kayması, burada en sık düzenlenen başlıklardan biri.",
        universite="Mersin Üniversitesi",
    ),
    "YALOVA": dict(
        mutfak=["deniz ürünleri", "yerel sebze-meyve üretimi", "zeytin ve zeytinyağı"],
        mutfak_notu=(
            "Yalova küçük bir il olmasına rağmen sofrası şaşırtıcı biçimde çeşitli: kendi üretimi sebze-meyve "
            "ile deniz ürünlerine erişim aynı anda mümkün. Buradaki danışanlarda gördüğümüz asıl kalıp, "
            "İstanbul'a düzenli gidiş-geliş yapanlarda öğün saatlerinin vapur ve otobüs saatlerine göre kayması."
        ),
        ozel="Hafta içi ve hafta sonu öğün düzeninin belirgin şekilde ayrışması sık karşılaşılan bir durum.",
        universite="Yalova Üniversitesi",
    ),
    "İSTANBUL": dict(
        mutfak=["dışarıda yeme kültürü", "hamur işleri", "balık-ekmek", "kahvaltı geleneği"],
        mutfak_notu=(
            "İstanbul'da beslenmeyi belirleyen şey mutfak değil, mesafe. Evden çıkışla eve dönüş arasında "
            "geçen sürenin uzunluğu, günün iki öğününü dışarıda yenmeye zorluyor. Danışanlarda en sık "
            "karşılaştığımız tablo: sabah atlanan kahvaltı, ayaküstü öğle ve gece 21.00'den sonra kurulan "
            "asıl sofra. Buradaki çözüm yasak listesi değil, güzergâh üzerinde işleyen bir öğün planı."
        ),
        ozel="Uzun ulaşım süreleri nedeniyle online görüşme, yüz yüze randevuya göre belirgin zaman avantajı sağlıyor.",
        universite=None,
    ),
}


def il_profili(il_adi):
    """Bir il için birleşik bağlam sözlüğü döndürür."""
    bolge = IL_BOLGE[il_adi]
    p = dict(BOLGE_TABAN[bolge])
    p.update(dict(
        il=il_adi, bolge=bolge,
        buyuksehir=il_adi in BUYUKSEHIR,
        ofis_ili=(il_adi == OFIS_IL),
        durum="taslak",
        ozel=None, universite=None,
    ))
    if il_adi in IL_OZEL:
        p.update(IL_OZEL[il_adi])
        p["durum"] = "hazir"
    return p
