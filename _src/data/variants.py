# -*- coding: utf-8 -*-
"""Şablon varyasyon sistemi — duplicate content'i tesadüfe bırakmadan önler.

Mantık: iki sayfanın farklı olması yazarın "farklı yazmaya çalışmasına"
bırakılmaz. Her sayfa, bölüm SIRASI ve giriş AÇISI birbirinden farklı 10
iskeletten birine deterministik olarak atanır. Aynı varyantı paylaşan iki il
bile, `city_context` verisi farklı olduğu için farklı gövde üretir.

Atama deterministiktir (plaka + ad hash) → build tekrarlanabilir, URL'ler sabit.
"""

IL_VARYANT = [
    dict(kod="IL-01", ad="Mutfak merkezli",
         aci="yöresel sofranın diyet içindeki yeri",
         blok_sirasi=["mutfak", "nedir", "kimler", "surec", "karsilastirma", "ucret", "ilceler", "sss"]),
    dict(kod="IL-02", ad="Zaman ve mesafe merkezli",
         aci="randevuya gidip gelmenin gerçek zaman maliyeti",
         blok_sirasi=["mesafe", "surec", "nedir", "mutfak", "kimler", "ucret", "ilceler", "sss"]),
    dict(kod="IL-03", ad="Doğrudan cevap önce (AEO)",
         aci="sayfanın en üstünde soruya net cevap",
         blok_sirasi=["ozet_cevap", "nedir", "surec", "kimler", "mutfak", "karsilastirma", "ilceler", "sss"]),
    dict(kod="IL-04", ad="Süreç merkezli",
         aci="ilk görüşmeden takibe kadar akış",
         blok_sirasi=["surec", "kimler", "mutfak", "nedir", "ucret", "karsilastirma", "ilceler", "sss"]),
    dict(kod="IL-05", ad="Karşılaştırma merkezli",
         aci="online ile yüz yüze görüşmenin tarafsız kıyası",
         blok_sirasi=["karsilastirma", "nedir", "mesafe", "surec", "mutfak", "ucret", "ilceler", "sss"]),
    dict(kod="IL-06", ad="Persona merkezli",
         aci="ildeki farklı yaşam düzenlerine göre kimler için uygun",
         blok_sirasi=["kimler", "mutfak", "surec", "nedir", "karsilastirma", "ucret", "ilceler", "sss"]),
    dict(kod="IL-07", ad="Mevsim ve iklim merkezli",
         aci="ilin iklim düzeninin beslenmeye etkisi",
         blok_sirasi=["iklim", "mutfak", "kimler", "surec", "nedir", "ucret", "ilceler", "sss"]),
    dict(kod="IL-08", ad="Ücret şeffaflığı merkezli",
         aci="fiyatın neye göre değiştiğinin açık anlatımı",
         blok_sirasi=["ucret", "nedir", "surec", "kimler", "mutfak", "karsilastirma", "ilceler", "sss"]),
    dict(kod="IL-09", ad="İlçe kılavuzu merkezli",
         aci="çok ilçeli ilde hangi ilçeden nasıl ulaşılacağı",
         blok_sirasi=["ilceler", "nedir", "surec", "mutfak", "kimler", "ucret", "karsilastirma", "sss"]),
    dict(kod="IL-10", ad="Sade rehber",
         aci="küçük ilde yalın ve kısa anlatım",
         blok_sirasi=["nedir", "surec", "mutfak", "kimler", "ucret", "ilceler", "sss"]),
]

ILCE_VARYANT = [
    dict(kod="ILC-01", ad="Öğün düzeni", persona="öğün saatleri dağılmış kişi",
         blok_sirasi=["ogun_duzeni", "porsiyon", "surec", "komsu", "sss"]),
    dict(kod="ILC-02", ad="Porsiyon kontrolü", persona="porsiyon ölçüsünü kuramayan kişi",
         blok_sirasi=["porsiyon", "mutfak_hazirlik", "surec", "komsu", "sss"]),
    dict(kod="ILC-03", ad="Ara öğün", persona="öğün arası açlık yaşayan kişi",
         blok_sirasi=["ara_ogun", "ogun_duzeni", "surec", "komsu", "sss"]),
    dict(kod="ILC-04", ad="Tatlı isteği", persona="tatlı isteğiyle plan bozan kişi",
         blok_sirasi=["tatli", "porsiyon", "surec", "komsu", "sss"]),
    dict(kod="ILC-05", ad="Su tüketimi", persona="sıvı tüketimi yetersiz kişi",
         blok_sirasi=["su", "ogun_duzeni", "surec", "komsu", "sss"]),
    dict(kod="ILC-06", ad="Tartı takibi", persona="ölçüm sonuçlarını yorumlayamayan kişi",
         blok_sirasi=["tarti", "hedef", "surec", "komsu", "sss"]),
    dict(kod="ILC-07", ad="Mutfak hazırlığı", persona="planı evde uygulamakta zorlanan kişi",
         blok_sirasi=["mutfak_hazirlik", "porsiyon", "surec", "komsu", "sss"]),
    dict(kod="ILC-08", ad="Hedef belirleme", persona="daha önce başlayıp bırakmış kişi",
         blok_sirasi=["hedef", "ogun_duzeni", "surec", "komsu", "sss"]),
    dict(kod="ILC-09", ad="Öğün düzeni + tartı", persona="düzen ve ölçüm birlikte sorun olan kişi",
         blok_sirasi=["ogun_duzeni", "tarti", "surec", "komsu", "sss"]),
    dict(kod="ILC-10", ad="Ara öğün + tatlı", persona="gün içi atıştırma kalıbı olan kişi",
         blok_sirasi=["ara_ogun", "tatli", "surec", "komsu", "sss"]),
]


def _hash(s):
    h = 0
    for ch in s:
        h = (h * 131 + ord(ch)) & 0xFFFFFFFF
    return h


def il_varyanti(il_adi, plaka, ilce_sayisi):
    """İl → varyant. Yapısal uygunluk önce, sonra deterministik dağıtım."""
    if ilce_sayisi >= 20:
        return IL_VARYANT[8]
    if ilce_sayisi <= 6:
        return IL_VARYANT[9]
    return IL_VARYANT[(plaka + _hash(il_adi)) % 8]


def ilce_varyanti(ilce_adi, il_adi, plaka, ozellik=None):
    """İlçe → varyant.

    `ozellik` yalnızca DOĞRULANABİLİR bir olguysa geçerlidir (bugün sadece 'merkez').
    Varyant adları ilçenin karakterini değil, sayfanın hedeflediği kullanıcı personasını
    anlatır — bir ilçeye 'kıyı ilçesi' demek doğrulanamaz bir iddia olurdu.
    """
    # Not: ilçenin 'merkez' olması diyet ekseninde bir şey ifade etmiyor; bu yüzden
    # artık özel muamele yok. Dağıtım tamamen il düzeyinde yapılıyor (build.py).
    return ILCE_VARYANT[(plaka + _hash(ilce_adi)) % 6]
