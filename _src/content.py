# -*- coding: utf-8 -*-
"""Bölüm metni üreticileri.

Her fonksiyon (baslik_html, govde_html, aeo_cevap) döndürür.
`aeo_cevap` = AI/AI Overviews'in doğrudan alıntılayabileceği 2-4 cümlelik net cevap.

Özgünlük üç kaynaktan gelir:
  1. il/ilçe profilindeki elle yazılmış benzersiz veri (mutfak_notu, ozel)
  2. varyanta göre değişen bölüm sırası ve giriş açısı
  3. deterministik ama profile bağlı cümle kalıbı seçimi
Hiçbiri "şehir adını değiştir" mantığıyla çalışmaz.
"""

import json
import os

import turkce as T
from dagitim import profil_dagit, kume_dagit

# Havuz sırası — indeksler PROFIL tuple'ındaki konumla eşleşir.
# TEK profil: content.py ve build.py havuzları birlikte dağıtılır.
# Ayrı dağıtıldıklarında her biri kendi içinde kısıtı sağlıyor ama toplamda
# üç ortak cümle çıkabiliyordu (altı il çifti bu yüzden denetimden geçmemişti).
HAVUZLAR = ["mutfak_giris", "mutfak_kapanis", "mesafe_baslik", "mesafe_acilis",
            "mesafe_devam", "mesafe_cozum", "iklim_baslik", "iklim_kapanis",
            "pratik_baslik",
            "title", "desc", "anadomain", "rehber", "ilcelist", "yakinil",
            "ctabaslik", "ctametin"]
HAVUZ_BOYUT = [12, 12, 12, 12, 12, 12, 12, 12, 6,
               10, 8, 12, 10, 9, 8, 12, 12]

_VERI_YOLU = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "turkiye.json")
_ILLER = sorted(json.load(open(_VERI_YOLU, encoding="utf-8")))

# Çerçeve seçimleri artık hash'e değil, kısıtlı bir dağıtıma dayanıyor:
# iki il en fazla bir havuzda aynı çerçeve cümlesini paylaşabilir.
_CACHE_YOLU = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "data", "profil_cache.json")


def _profilleri_yukle():
    """Dağıtım pahalı (81 il x 40.000 aday); sonucu diske yazıp yeniden kullanırız.

    Önbellek anahtarı havuz yapısını içerir — havuz sayısı veya boyutu değişirse
    önbellek otomatik geçersiz olur ve yeniden hesaplanır.
    """
    anahtar = f"{len(_ILLER)}|{','.join(map(str, HAVUZ_BOYUT))}|36,5"
    try:
        with open(_CACHE_YOLU, encoding="utf-8") as f:
            veri = json.load(f)
        if veri.get("anahtar") == anahtar:
            return ({k: tuple(v) for k, v in veri["profil"].items()},
                    {k: tuple(v) for k, v in veri["sss"].items()})
    except (OSError, ValueError, KeyError):
        pass
    profil = profil_dagit(_ILLER, HAVUZ_BOYUT, azami_ortak=2)
    sss = kume_dagit(_ILLER, 36, 5, azami_ortak=2)
    try:
        with open(_CACHE_YOLU, "w", encoding="utf-8") as f:
            json.dump({"anahtar": anahtar,
                       "profil": {k: list(v) for k, v in profil.items()},
                       "sss": {k: list(v) for k, v in sss.items()}},
                      f, ensure_ascii=False)
    except OSError:
        pass
    return profil, sss


PROFIL, SSS_DAGITIM = _profilleri_yukle()


def _idx(p, havuz):
    """İlin bu havuz için atanmış çerçeve indeksi."""
    return PROFIL[p["il"]][HAVUZLAR.index(havuz)]

SITE = "https://onlinediyetisyen.online"
DYT = "Dyt. Tuğba Şeker Ağaç"
TEL_HREF = "tel:+905070361859"
TEL_GORUNEN = "0507 036 18 59"
WA = "https://wa.me/905070361859"


def _sec(secenekler, tohum):
    return secenekler[tohum % len(secenekler)]


def _tohum(p, tuz=""):
    """İl için karıştırılmış tohum. `tuz` havuz adıdır.

    Tuz olmadan bütün havuzlar aynı sayıdan türüyordu: `t % 12` değeri çakışan
    iki il, mutfak/mesafe/iklim havuzlarının HEPSİNDE aynı çerçeve cümlesini
    alıyor ve sayfa başına 3-4 ortak cümle çıkıyordu. Havuz adı tohuma karışınca
    bir havuzdaki çakışma diğerlerine taşınmıyor.

    Ayrıca düz polinom hash tek başına yetmiyor: `% 4` alındığında farklı iller
    aynı varyasyona düşüp aynı çerçeve cümlelerini paylaşıyordu. Sondaki
    karıştırma adımları düşük bitleri de dağıtıyor.
    """
    h = 0
    for ch in p["il"] + "|" + tuz:
        h = (h * 131 + ord(ch)) & 0xFFFFFFFF
    h ^= (h >> 15)
    h = (h * 2246822519) & 0xFFFFFFFF
    h ^= (h >> 13)
    h = (h * 3266489917) & 0xFFFFFFFF
    return h ^ (h >> 16)


# ------------------------------------------------------------------ BLOKLAR
def blok_mutfak(p):
    il = T.baslik(p["il"])
    ilDE, ilDEN = T.bulunma(il), T.ayrilma(il)
    tG, tK = _tohum(p, "mutfak_giris"), _tohum(p, "mutfak_kapanis")
    baslik = _sec([
        f"{il} Sofrası ve Diyet: Neyi Değiştirmek Gerekiyor?",
        f"{il} Mutfağını Diyete Uyarlamak",
        f"{ilDE} Yerel Sofra Nasıl Dengeye Getirilir?",
    ], _tohum(p))
    liste = "".join(f"<li>{m}</li>" for m in p["mutfak"])
    t = _tohum(p)
    giris = [
        f"Planı kurarken yemekleri listeden silmek yerine ölçüsünü ve sıklığını düzenliyoruz. "
        f"{ilDE} sık karşılaştığımız sofra unsurları:",
        f"Çalışma yöntemimiz, alışık olunan sofrayı bozmadan dengeyi kurmak üzerine. "
        f"{ilDE} öne çıkan başlıklar:",
        f"Bir planın uygulanabilir olması için kişinin zaten yediği yemeklerle kurulması gerekiyor. "
        f"{ilDE} bu sofranın öğeleri:",
        f"Yerel sofrayı diyetin dışına atmak yerine planın içine almayı tercih ediyoruz. "
        f"{ilDE} sık karşımıza çıkanlar:",
        f"Beslenme planının ilk kuralı, kişinin gerçekten yediği yemekler üzerine kurulmuş olması. "
        f"{ilDE} bu listeyi şunlar oluşturuyor:",
        f"Sofrayı değiştirmek yerine sofradaki dengeyi değiştiriyoruz. "
        f"{ilDE} plana giren başlıca yemekler:",
        f"Alışkanlıkları kökten değiştiren planlar birkaç hafta içinde bırakılıyor; biz mevcut "
        f"düzeni esas alıyoruz. {ilDE} düzenli sofrada yer alanlar:",
        f"Danışan görüşmelerinde ilk konuştuğumuz şey mutfakta gerçekten ne olduğu. "
        f"{ilDE} verilen cevaplarda öne çıkanlar:",
        f"Uygulanabilir bir plan, market alışkanlığını ve mutfaktaki gerçeği tanımak zorunda. "
        f"{ilDE} karşımıza çıkan tablo:",
        f"Planın içine alınacak yemekleri belirlemek, çıkarılacakları belirlemekten daha önemli. "
        f"{ilDE} bu listede yer alanlar:",
        f"Bir sofrayı diyete uyarlamak, onu tanımakla başlıyor. "
        f"{ilDE} düzenli olarak karşılaştığımız yemekler:",
        f"Kişinin damak tadını yok sayan plan uzun ömürlü olmuyor. "
        f"{ilDE} hesaba kattığımız yemekler:",
    ][_idx(p, 'mutfak_giris')]
    kapanis = [
        "Bu yemeklerin hiçbiri tek başına yasak değil; belirleyici olan haftalık düzen içindeki yerleri.",
        "Listede yasak bir yemek yok. Fark, porsiyon ve hangi sıklıkla sofraya geldiği.",
        "Hiçbiri planın dışında kalmak zorunda değil; ölçü ve sıklık ayarlandığında yerini koruyabiliyor.",
        "Buradaki mesele yemeği çıkarmak değil, haftalık düzen içindeki payını belirlemek.",
        "Yemeklerin kendisi değil, hangi sıklıkla ve ne kadarlık porsiyonla geldiği belirleyici.",
        "Planda yasak listesi tutmuyoruz; tuttuğumuz şey haftalık denge.",
        "Bunların hepsi planın içinde kalabilir — koşul, ölçünün baştan belirlenmiş olması.",
        "Hiçbiri sorunun kaynağı değil; sorun genelde ölçünün belirsiz bırakılmasında.",
        "Yemeği çıkarmak kısa vadede işe yarıyor, sürdürmek ise ancak ölçüyle mümkün oluyor.",
        "Bu listedeki her şey plana girebilir; belirlenmesi gereken tek şey ne sıklıkla gireceği.",
        "Sofrayı daraltmak yerine porsiyonu netleştirmek, uzun vadede daha iyi sonuç veriyor.",
        "Yasaklamak yerine yerini belirlemek — planın kalıcı olmasını sağlayan fark burada.",
    ][_idx(p, 'mutfak_kapanis')]
    govde = f"""
<p>{p['mutfak_notu']}</p>
<p>{giris}</p>
<ul class="chk">{liste}</ul>
<p>{kapanis}</p>"""
    aeo = (f"{il} mutfağı diyete uyarlanabilir. {p['mutfak_notu'].split('.')[0]}. "
           f"Yerel yemekleri listeden çıkarmak yerine porsiyon ve sıklık düzenlenir.")
    return baslik, govde, aeo


def blok_nedir(p):
    il = T.baslik(p["il"])
    ilDE, ilDEN = T.bulunma(il), T.ayrilma(il)
    baslik = _sec([
        "Online Diyetisyen Ne Demek?",
        "Online Diyetisyen Hizmeti Nedir?",
        f"{ilDE} Online Diyetisyen Ne Anlama Geliyor?",
    ], _tohum(p) + 1)
    govde = f"""
<p>Online diyetisyen, beslenme danışmanlığını yüz yüze randevu yerine video görüşme ve dijital takip
üzerinden yürüten diyetisyendir. Görüşmenin içeriği değişmez: öykü alınır, hedef belirlenir,
kişiye özel plan hazırlanır ve düzenli aralıklarla takip yapılır. Değişen tek şey, bunun için
bir adrese gitme zorunluluğunun ortadan kalkmasıdır.</p>
<p>{ilDE} yaşayıp bu yolu tercih eden kişilerin ortak gerekçesi genelde aynı: süreklilik.
Bir beslenme planının işe yaraması için haftalarca takip edilmesi gerekir ve takibi bozan en yaygın
sebep, randevuya gidecek zamanın bulunamamasıdır.</p>"""
    aeo = ("Online diyetisyen, beslenme danışmanlığını video görüşme ve dijital takip üzerinden yürüten "
           "diyetisyendir. Öykü alma, hedef belirleme, kişiye özel plan ve düzenli takip aşamaları "
           "yüz yüze görüşmeyle aynıdır; yalnızca görüşme uzaktan yapılır.")
    return baslik, govde, aeo


def blok_kimler(p):
    il = T.baslik(p["il"])
    ilDE, ilDEN = T.bulunma(il), T.ayrilma(il)
    baslik = _sec([
        f"{ilDE} Kimler Online Diyetisyen Desteği Alabilir?",
        "Bu Hizmet Kimler İçin Uygun?",
        f"{ilDE} Hangi Yaşam Düzenlerine Uyuyor?",
    ], _tohum(p) + 2)
    ek = ""
    if p.get("universite"):
        ek = f"<li>{p['universite']} çevresinde öğrenci düzeninde yaşayanlar</li>"
    govde = f"""
<p>Online takip, düzenli görüşmeye devam edebilecek yetişkinler için uygundur. Sık başvurulan durumlar:</p>
<ul class="chk">
<li>Kilo yönetimi hedefleyen ve sürdürülebilir bir düzen kurmak isteyen yetişkinler</li>
<li>Öğün saatleri iş temposu nedeniyle dağılmış çalışanlar</li>
<li>Evden çalışıp gün boyu mutfağa erişimi olan kişiler</li>
<li>Düzenli spor yapan ve beslenmesini buna göre kurgulamak isteyenler</li>
<li>Daha önce çeşitli diyetler deneyip kalıcı bir düzene geçemeyenler</li>
{ek}</ul>
<p class="note"><strong>Önemli:</strong> Gebelik, emzirme, böbrek veya karaciğer hastalığı, yeme
bozukluğu öyküsü ya da düzenli ilaç kullanımı gibi durumlarda beslenme planı hekim değerlendirmesiyle
birlikte yürütülmelidir. Bu sayfadaki bilgiler genel bilgilendirme amaçlıdır ve kişisel tıbbi
tavsiye yerine geçmez.</p>"""
    aeo = ("Online diyetisyen desteği; kilo yönetimi hedefleyen, öğün düzeni iş temposu nedeniyle bozulan, "
           "evden çalışan veya düzenli spor yapan yetişkinler için uygundur. Gebelik, kronik hastalık ve "
           "yeme bozukluğu öyküsü olan kişilerde süreç hekim değerlendirmesiyle birlikte yürütülür.")
    return baslik, govde, aeo


def blok_surec(p):
    baslik = _sec([
        "Görüşme Nasıl İşliyor?",
        "İlk Görüşmeden Takibe: Süreç",
        "Online Diyetisyen Görüşmesi Adım Adım",
    ], _tohum(p) + 3)
    govde = """
<ol class="steps">
<li><strong>İletişim.</strong> Telefon veya WhatsApp üzerinden uygun görüşme saati belirlenir.</li>
<li><strong>Ön değerlendirme.</strong> Beslenme öyküsü, günlük düzen, varsa tahlil sonuçları ve
sağlık geçmişi konuşulur.</li>
<li><strong>Hedef belirleme.</strong> Gerçekçi ve ölçülebilir bir hedef birlikte tanımlanır.</li>
<li><strong>Kişiye özel plan.</strong> Kişinin mutfağına, bütçesine ve çalışma saatlerine göre
uygulanabilir bir öğün planı hazırlanır.</li>
<li><strong>Takip görüşmeleri.</strong> Düzenli aralıklarla ilerleme değerlendirilir.</li>
<li><strong>Güncelleme.</strong> Plan; sonuçlara, mevsime ve değişen yaşam düzenine göre revize edilir.</li>
</ol>"""
    aeo = ("Online diyetisyen görüşmesi altı adımda ilerler: iletişim ve randevu, beslenme öyküsünün "
           "alındığı ön değerlendirme, hedef belirleme, kişiye özel öğün planı, düzenli takip görüşmeleri "
           "ve sonuçlara göre planın güncellenmesi.")
    return baslik, govde, aeo


def blok_karsilastirma(p):
    il = T.baslik(p["il"])
    ilDE, ilDEN = T.bulunma(il), T.ayrilma(il)
    ofis = p.get("ofis_ili")
    baslik = _sec([
        "Online mı, Yüz Yüze mi?",
        "Online Görüşme ile Yüz Yüze Görüşmenin Farkı",
        f"{il} İçin Hangisi Daha Uygun?",
    ], _tohum(p) + 4)
    ofis_satir = (
        "<tr><td>Yüz yüze seçeneği</td><td>Seyhan'daki ofiste mümkün</td><td>—</td></tr>"
        if ofis else
        f"<tr><td>Yüz yüze seçeneği</td><td>{ilDE} fiziksel ofis bulunmuyor</td><td>Görüşmeler uzaktan yapılır</td></tr>"
    )
    govde = f"""
<div class="tablo-kaydir"><table class="cmp">
<thead><tr><th>Ölçüt</th><th>Online görüşme</th><th>Yüz yüze görüşme</th></tr></thead>
<tbody>
<tr><td>Ulaşım süresi</td><td>Yok</td><td>Gidiş-dönüş süresi eklenir</td></tr>
<tr><td>Görüşme içeriği</td><td>Aynı</td><td>Aynı</td></tr>
<tr><td>Takip sıklığı</td><td>Esnek, saat seçimi kolay</td><td>Randevu takvimine bağlı</td></tr>
<tr><td>Vücut ölçümü</td><td>Kişi kendi ölçümünü paylaşır</td><td>Ofiste yapılır</td></tr>
<tr><td>Mutfak üzerinden çalışma</td><td>Kişi kendi mutfağındadır</td><td>Anlatıma dayanır</td></tr>
{ofis_satir}
</tbody></table></div>
<p>Bu bir üstünlük sıralaması değil. Vücut kompozisyonu ölçümünün cihazla yapılması öncelikliyse
yüz yüze görüşme avantajlıdır; sürekliliğin korunması öncelikliyse online takip öne geçer.</p>"""
    aeo = ("Online ve yüz yüze diyetisyen görüşmesinin içeriği aynıdır. Online görüşme ulaşım süresini "
           "ortadan kaldırır ve takip sıklığını esnetir; yüz yüze görüşme ise cihazla vücut kompozisyonu "
           "ölçümüne imkân verir.")
    return baslik, govde, aeo


def blok_ucret(p):
    baslik = _sec([
        "Ücretler Neye Göre Değişiyor?",
        "Online Diyetisyen Ücreti Nasıl Belirlenir?",
        "Fiyatlandırma Mantığı",
    ], _tohum(p) + 5)
    govde = f"""
<p>Online diyetisyen ücreti tek bir sabit rakam değildir; birkaç değişkene göre belirlenir:</p>
<ul class="chk">
<li><strong>Program süresi.</strong> Tek görüşme ile aylık takip paketi farklı fiyatlanır.</li>
<li><strong>Görüşme sıklığı.</strong> Haftalık takip ile iki haftada bir takip aynı değildir.</li>
<li><strong>Kapsam.</strong> Yalnızca beslenme planı mı, yoksa tahlil değerlendirmesi ve
düzenli ölçüm takibi de dâhil mi?</li>
<li><strong>Özel durum.</strong> İnsülin direnci, PCOS veya sporcu beslenmesi gibi başlıklar
farklı bir planlama emeği gerektirir.</li>
</ul>
<p>Güncel ücretler ve size uygun takip modeli için
<a href="{SITE}/#fiyatlar">fiyatlar bölümüne</a> bakabilir ya da doğrudan
<a href="{TEL_HREF}">{TEL_GORUNEN}</a> numarasından bilgi alabilirsiniz.</p>"""
    aeo = ("Online diyetisyen ücreti; program süresi, görüşme sıklığı, hizmet kapsamı ve insülin direnci "
           "veya sporcu beslenmesi gibi özel durumlara göre değişir. Tek bir sabit rakam yerine "
           "takip modeline göre fiyatlandırma yapılır.")
    return baslik, govde, aeo


def blok_mesafe(p):
    il = T.baslik(p["il"])
    ilDE, ilDEN = T.bulunma(il), T.ayrilma(il)
    t = _tohum(p, "mesafe_baslik")
    tA = _tohum(p, "mesafe_acilis")
    tD = _tohum(p, "mesafe_devam")
    tC = _tohum(p, "mesafe_cozum")
    baslik = [
        f"{ilDE} Randevuya Gitmenin Zaman Maliyeti",
        f"{ilDE} Takibi Ayakta Tutan Şey: Süreklilik",
        f"{ilDE} Programın Yarıda Kalma Sebebi Genelde Plan Değil",
        f"{ilDE} Zaman Yönetimi ve Beslenme Takibi",
        f"{ilDE} Takip Neden Yarıda Kalıyor?",
        f"{il} İçin Sürdürülebilir Bir Takip Düzeni",
        f"{ilDE} Programı Bırakma Noktası Nerede?",
        f"{il} Koşullarında Takibin Devamlılığı",
        f"{ilDE} Randevu Değil, Süreklilik Meselesi",
        f"{il} İçin Haftalık Takip Nasıl Kurulur?",
        f"{ilDE} Görüşme Sıklığını Ne Belirliyor?",
        f"{il} Planında Zamanın Rolü",
    ][_idx(p, 'mesafe_baslik')]
    ek = p.get("ozel") or ""
    # Çerçeve cümlelerinde il adının geçmesi bilinçli: aynı havuz indeksine düşen
    # iki il, aksi hâlde birebir aynı cümleyi üretiyordu.
    acilis = [
        f"{ilDE} bir beslenme programının sonuç vermesini sağlayan şey tek bir mükemmel görüşme "
        f"değil, haftalar boyunca kesintisiz süren takiptir.",
        f"{il} için programların yarıda kalma sebebi çoğu zaman planın kendisi değil, takip "
        f"görüşmelerinin aksamaya başlaması oluyor.",
        f"{ilDE} beslenme takibinde sonucu belirleyen değişken, planın ne kadar iyi olduğundan "
        f"çok ne kadar süre uygulanabildiği.",
        f"{ilDEN} görüşen danışanlarda en sık kopuş noktası ilk görüşme değil, üçüncü veya "
        f"dördüncü takip görüşmesinin ertelenmesi.",
        f"{il} koşullarında iyi bir plan tek başına yeterli olmuyor; sonucu belirleyen, o planın "
        f"kaç hafta uygulanabildiği.",
        f"{ilDE} beslenme programlarında kritik eşik ilk aydır: bu süre boyunca takip aksamazsa "
        f"düzen büyük ölçüde oturuyor.",
        f"{ilDEN} katılan danışanların çoğu programı bilgi eksikliğinden değil, takip zinciri "
        f"koptuğu için bırakıyor.",
        f"{il} için bir planın başarısı, ilk hafta ne kadar iyi uygulandığından çok altıncı hafta "
        f"hâlâ uygulanıp uygulanmadığıyla ölçülüyor.",
        f"{ilDE} de geçerli olan şu: beslenme değişikliği bir olay değil süreç; süreci taşıyan "
        f"şey düzenli görüşmeler.",
        f"{ilDEN} gelen danışanlarda tablo net: plan değişmeden takip sıklığı düzeldiğinde sonuç "
        f"da düzeliyor.",
        f"{il} için kilo yönetiminde en pahalı şey yeniden başlamak; bunu önleyen tek şey "
        f"kesintisiz takip.",
        f"{ilDE} programın hangi hafta bırakıldığına bakınca ortaya çıkan kalıp hep aynı: takvim "
        f"doldu, görüşme ertelendi, plan durdu.",
    ][_idx(p, 'mesafe_acilis')]
    devam = [
        f"{ilDE} takibi bozan en yaygın sebep plan değil, program çakışması: iş çıkışı trafiği, "
        f"çocuğun okul saati, vardiya değişimi.",
        f"{il} için bunu bozan şey genelde motivasyon kaybı değil, takvimin dolması: mesai, okul, yol.",
        f"{ilDE} araya giren şey çoğu zaman isteksizlik değil; randevuya ayrılacak yarım günün "
        f"bulunamaması.",
        f"{il} koşullarında erteleme sebebi çoğunlukla programın zorluğu değil, o güne sığmayan "
        f"bir yolculuk.",
        f"{ilDE} kopuşun sebebi neredeyse hiç plan olmuyor; genelde o hafta takvime sığmayan bir randevu.",
        f"{il} için engel çoğu zaman kararlılık değil, işten çıkıp randevuya yetişmeye çalışmanın kendisi.",
        f"{ilDE} görüşme ertelendiğinde plan da askıya alınıyor — asıl kayıp burada başlıyor.",
        f"{ilDEN} gelen danışanlarda aksama genelde tek bir kaçırılan randevuyla başlıyor ve arkası gelmiyor.",
        f"{il} için sorun isteğin azalması değil; o gün için ayrılması gereken sürenin bulunamaması.",
        f"{ilDE} takvim doldukça ilk feda edilen şey, sonucu doğrudan belirleyen takip görüşmesi oluyor.",
        f"{il} koşullarında yol, mesai ve ev düzeni bir araya geldiğinde randevu en kolay ertelenen "
        f"madde haline geliyor.",
        f"{ilDE} bırakma kararı çoğu zaman verilmiyor bile; sadece bir sonraki görüşme hiç ayarlanmıyor.",
    ][_idx(p, 'mesafe_devam')]
    cozum = [
        f"Online görüşme {il} için bu denklemden ulaşım süresini tamamen çıkarır.",
        f"{ilDE} görüşmenin uzaktan yapılması, takvime yalnızca görüşme süresinin yazılması demek.",
        f"{il} için uzaktan takipte programa eklenen tek şey görüşmenin kendisi oluyor; yol süresi "
        f"devre dışı kalıyor.",
        f"{ilDE} görüşmeler video üzerinden yürütüldüğünde randevu, gününüzün yarısını değil "
        f"yalnızca o saati kaplıyor.",
        f"Video görüşme {il} için takvimden silinen tek şeyin yol olmasını sağlıyor.",
        f"{ilDE} uzaktan yürütülen takipte ertelenecek bir yolculuk kalmıyor.",
        f"{il} için görüşme evden yapıldığında, randevuyu ertelemenin en yaygın sebebi ortadan kalkıyor.",
        f"{ilDE} ulaşım denklemden çıkınca geriye yalnızca görüşmeye ayrılacak süre kalıyor.",
        f"{il} için uzaktan takipte plan, yolculuk değil yalnızca bir saat gerektiriyor.",
        f"{ilDE} görüşmenin yerini değil zamanını ayarlamak yeterli hâle geliyor.",
        f"{il} için randevuya ayrılan süre yol dâhil yarım günden, görüşme süresine iniyor.",
        f"{ilDE} takvimde yer açmak gerekmiyor; görüşme mevcut günün içine yerleşiyor.",
    ][_idx(p, 'mesafe_cozum')]
    govde = f"""
<p>{acilis} {devam}</p>
<p>{cozum} {ek}</p>"""
    aeo = ("Online görüşme, randevuya gidiş-dönüş süresini ortadan kaldırdığı için takip sürekliliğini "
           "korumayı kolaylaştırır. Beslenme programlarında sonucu belirleyen temel etken takibin "
           "kesintisiz sürmesidir.")
    return baslik, govde, aeo


def blok_iklim(p):
    il = T.baslik(p["il"])
    ilDE, ilDEN = T.bulunma(il), T.ayrilma(il)
    t = _tohum(p, "iklim_baslik")
    tK = _tohum(p, "iklim_kapanis")
    _n = p["iklim_notu"]
    iklim_notu = _n[_idx(p, "iklim_baslik") % len(_n)] if isinstance(_n, list) else _n
    baslik = [
        f"{ilDE} Mevsimler Beslenmeyi Nasıl Etkiliyor?",
        f"{il} İkliminin Öğün Düzenine Etkisi",
        f"{ilDE} Yıl İçinde Değişen Beslenme İhtiyacı",
        f"{il} İçin Mevsime Göre Plan Güncellemesi",
        f"{il} İkliminde Öğün Saatleri Nasıl Kayıyor?",
        f"{ilDE} Mevsim Geçişlerinde Plan Ne Değişir?",
        f"{il} Koşullarında Sıvı ve Öğün Dengesi",
        f"{ilDE} Kış ve Yaz Aynı Planla Yürür mü?",
        f"{il} İçin Mevsimsel Beslenme Notları",
        f"{ilDE} Hava Koşulları Planı Nasıl Etkiliyor?",
        f"{il} İkliminin Günlük Harekete Etkisi",
        f"{ilDE} Yıl Boyu Aynı Plan Uygulanır mı?",
    ][_idx(p, 'iklim_baslik')]
    kapanis = [
        f"Plan hazırlanırken bu döngü hesaba katılır: {il} için yaz ve kış aylarında sıvı ihtiyacı, "
        f"öğün saatleri ve günlük hareket miktarı aynı kalmaz.",
        f"Bu yüzden {il} için hazırlanan planlar tek bir mevsime göre değil, yıl içindeki geçişlere "
        f"göre kurgulanır; sıvı hedefi ve öğün saatleri buna göre ayarlanır.",
        f"{T.bulunma(il)} bu döngü, öğün saatlerinden günlük hareket miktarına kadar planın birkaç "
        f"parçasını aynı anda etkiler.",
        f"Planın {il} koşullarına göre mevsim geçişlerinde gözden geçirilmesi, takip görüşmelerinin "
        f"asıl işlevlerinden biri.",
        f"{il} için hazırlanan planda mevsim, öğün saatleri kadar sıvı hedefini de belirleyen bir değişken.",
        f"Yılın hangi ayında olunduğu, {T.tamlayan(il)} koşullarında planın kaç maddesini "
        f"etkileyeceğini doğrudan belirliyor.",
        f"{il} koşullarında aynı planı yıl boyu uygulamak yerine, mevsim geçişlerinde revizyon yapmak "
        f"sonucu koruyor.",
        f"Takip görüşmelerinde {il} için gözden geçirilen ilk maddelerden biri, mevsime bağlı "
        f"sıvı ve hareket dengesi.",
        f"{T.bulunma(il)} mevsim değişimi çoğu zaman planın kendisinden önce günlük rutini değiştiriyor.",
        f"{il} için plan kurulurken hangi mevsimde başlandığı, ilk ayın hedeflerini de belirliyor.",
        f"Mevsim geçişleri {T.bulunma(il)} planın en sık güncellenen bölümü oluyor.",
        f"{il} koşullarında yaz ve kış planları arasındaki fark, çoğu danışanın beklediğinden büyük.",
    ][_idx(p, 'iklim_kapanis')]
    govde = f"""
<p>{il}, {p['bolge']} Bölgesi'nde yer alır; {p['iklim']} görülür. {iklim_notu}</p>
<p>{kapanis}</p>"""
    aeo = (f"{ilDE} {p['iklim']} görülür. {iklim_notu} Beslenme planı mevsim geçişlerinde "
           f"sıvı ihtiyacı, öğün saatleri ve hareket miktarı dikkate alınarak güncellenir.")
    return baslik, govde, aeo


BLOKLAR = {
    "mutfak": blok_mutfak, "nedir": blok_nedir, "kimler": blok_kimler,
    "surec": blok_surec, "karsilastirma": blok_karsilastirma, "ucret": blok_ucret,
    "mesafe": blok_mesafe, "iklim": blok_iklim,
}


# ------------------------------------------------------------------- SSS
# Havuz geniş tutulur; her sayfa profiline göre 5 farklı soru seçer.
# Aynı soru iki komşu sayfada tekrar etmesin diye seçim tohuma bağlıdır.
def sss_havuzu(p):
    il = T.baslik(p["il"])
    ilDE, ilDEN = T.bulunma(il), T.ayrilma(il)
    h = [
        (f"{ilDE} online diyetisyen görüşmesi için hangi cihaz gerekiyor?",
         "Kamerası ve mikrofonu çalışan bir telefon, tablet veya bilgisayar yeterlidir. "
         "Ayrı bir program kurmanız gerekmez; görüşme bağlantısı önceden paylaşılır."),
        (f"{ilDEN} katılırken görüşme saatini kendim seçebiliyor muyum?",
         "Evet. Uygun saat aralıkları önceden paylaşılır ve çalışma düzeninize göre birlikte belirlenir. "
         "Vardiyalı çalışanlar için akşam saatleri de değerlendirilebilir."),
        ("Tahlil sonuçlarımı nasıl iletiyorum?",
         "Tahlil sonuçlarınızı görüşmeden önce WhatsApp üzerinden iletebilirsiniz. "
         "Değerlendirme, beslenme planı hazırlanırken dikkate alınır."),
        ("Kilo takibimi evde nasıl yapacağım?",
         "Ölçümlerin haftanın aynı günü, sabah aç karnına ve aynı tartıyla yapılması yeterlidir. "
         "Takip görüşmelerinde bu ölçümler birlikte değerlendirilir."),
        (f"{ilDE} yaşıyorum ama sık seyahat ediyorum, program bozulur mu?",
         "Seyahat eden kişiler için plan, dışarıda yenebilecek seçenekler üzerinden kurgulanır. "
         "Program bozulduğunda yapılacak şey baştan başlamak değil, takip görüşmesinde düzeni yeniden kurmaktır."),
        ("Görüşmeden sonra plan elime nasıl ulaşıyor?",
         "Beslenme planı görüşmenin ardından yazılı olarak paylaşılır. "
         "Uygulama sırasında ortaya çıkan sorular için takip görüşmesini beklemeniz gerekmez."),
        ("Daha önce birçok diyet denedim ve kilo geri geldi, farkı ne olacak?",
         "Kısa süreli kısıtlamalar bittiğinde eski düzene dönülür ve kilo geri alınır. "
         "Buradaki yaklaşım, mevcut sofranızı koruyup ölçü ve sıklığı düzenlemek üzerine kuruludur; "
         "amaç uygulanabilir ve sürdürülebilir bir düzendir."),
        ("Online görüşme yüz yüze kadar etkili mi?",
         "Görüşmenin içeriği aynıdır: öykü alma, hedef belirleme, plan ve takip. "
         "Cihazla vücut kompozisyonu ölçümü yüz yüze görüşmenin avantajıdır; buna karşılık online takipte "
         "sürekliliğin korunması daha kolaydır."),
        ("Çocuğum için de plan hazırlanıyor mu?",
         "Çocuk ve ergen beslenmesi ayrı bir değerlendirme gerektirir ve büyüme takibiyle birlikte yürütülür. "
         "Bu konudaki uygunluk ön görüşmede değerlendirilir."),
        (f"{il} dışına taşınırsam takip devam eder mi?",
         "Evet. Görüşmeler uzaktan yapıldığı için şehir değişikliği takibi kesintiye uğratmaz."),
        ("Programı uygularken canım çok tatlı çekerse ne yapmalıyım?",
         "Tatlı isteği planın dışında bir kaza değil, planın içinde yeri olması gereken bir durum. "
         "Sıklığı ve porsiyonu baştan belirlendiğinde süreç bozulmuyor."),
        ("Dışarıda yemek zorunda kaldığım günlerde ne yapacağım?",
         "Plan, dışarıda yenebilecek seçenekleri de kapsayacak şekilde hazırlanır. "
         "Hangi menülerden ne seçilebileceği önceden konuşulur."),
        ("Spor yapmadan da sonuç alınır mı?",
         "Beslenme düzeni tek başına da değişim sağlar; hareket eklendiğinde süreç desteklenir. "
         "Hareket planı kişinin mevcut durumuna göre kademeli önerilir."),
        ("Su tüketimimi nasıl takip edeceğim?",
         "Günlük hedef kişiye göre belirlenir ve basit bir takip yöntemiyle izlenir. "
         "Sıcak dönemlerde hedef yeniden değerlendirilir."),
        ("Ailemle aynı yemeği yiyebilir miyim?",
         "Evet. Plan mümkün olduğunca ortak sofra üzerinden kurulur; fark porsiyon ve "
         "tamamlayıcılarda olur. Ayrı yemek yapma zorunluluğu planın bırakılma sebeplerinden biridir."),
        ("Kilo vermem duraklarsa ne yapılıyor?",
         "Duraklama sürecin beklenen bir aşamasıdır. Takip görüşmesinde beslenme kaydı, uyku ve "
         "hareket birlikte değerlendirilir ve plan buna göre güncellenir."),
        ("Takviye veya vitamin öneriliyor mu?",
         "Takviye kullanımı ancak gerekli görülen durumlarda ve hekim değerlendirmesiyle birlikte "
         "gündeme gelir. Öncelik, ihtiyacın beslenmeyle karşılanmasıdır."),
        ("Görüşmeler kayıt altına alınıyor mu?",
         "Görüşmeler kayda alınmaz. Paylaştığınız sağlık bilgileri gizlilik kapsamında değerlendirilir."),
        ("Hafta sonu düzenim tamamen değişiyor, plan buna uyar mı?",
         "Uyar. Hafta içi ve hafta sonu için ayrı akış kurgulanabilir; iki düzenin de plana yazılması "
         "sürdürülebilirliği artırır."),
        ("İlk görüşmeye nasıl hazırlanmalıyım?",
         "Son birkaç güne ait beslenme kaydınızı ve varsa güncel tahlil sonuçlarınızı hazır "
         "bulundurmanız yeterlidir."),
        ("Diyet sırasında kahve içebilir miyim?",
         "Şekersiz kahve genelde plana engel değildir. Belirleyici olan yanına eklenen şeker, "
         "krema ve şurupların günlük toplama katkısı."),
        ("Akşam saat kaçtan sonra yemek yememeliyim?",
         "Belirleyici olan saat değil, gün içindeki toplam alım ve öğün dağılımı. Geç saatte "
         "yenen öğün, günün toplamı içinde planlanmışsa sorun oluşturmaz."),
        ("Diyette ekmek tamamen kesilir mi?",
         "Kesilmesi gerekmez. Ekmek bir karbonhidrat kaynağıdır ve günlük plan içinde miktarı "
         "belirlenerek yer alır."),
        ("Kilo verirken kas kaybı nasıl önlenir?",
         "Yeterli protein alımı ve düzenli hareket, kas kaybını sınırlamanın temel iki bileşenidir. "
         "Çok hızlı kilo kaybı hedeflemek bu riski artırır."),
        ("Tartıda değişim yok ama kıyafetlerim bollaştı, normal mi?",
         "Evet. Vücut kompozisyonu değişirken ağırlık aynı kalabilir. Bu yüzden takipte yalnızca "
         "tartıya değil, ölçüm ve genel duruma birlikte bakılır."),
        ("Diyet listesi her hafta değişiyor mu?",
         "Plan sabit bir liste değildir. Takip görüşmelerinde ilerlemeye ve değişen düzene göre "
         "gerekli olduğunda güncellenir."),
        ("Öğün aralarında acıkırsam ne yapmalıyım?",
         "Açlık düzenli tekrarlıyorsa bu, ana öğünlerin içeriğinin gözden geçirilmesi gerektiğini "
         "gösterir. Ara öğün eklemek çoğu zaman ilk çözüm olur."),
        ("Gece geç saatte çalışıyorum, planım buna göre kurulabilir mi?",
         "Evet. Plan saatlere değil, uyanma ve uyku düzeninize göre kurgulanabilir."),
        ("Şeker yerine tatlandırıcı kullanabilir miyim?",
         "Kullanılabilir, ancak tatlandırıcı tek başına bir çözüm değildir. Asıl hedef tatlı "
         "tüketiminin sıklığını dengelemektir."),
        ("Diyet yaparken vitamin eksikliği olur mu?",
         "Besin çeşitliliği korunan bir planda beklenmez. Bir besin grubunu tamamen dışlayan "
         "düzenlerde ise risk artar; bu yüzden plan çeşitlilik gözetilerek hazırlanır."),
        ("Yemek yerken ne kadar yavaş yemeliyim?",
         "Tokluk hissinin oluşması zaman aldığı için öğünü aceleye getirmemek porsiyon kontrolüne "
         "doğrudan katkı sağlar."),
        ("Aynı yemekleri her gün yemek zorunda mıyım?",
         "Hayır. Plan, aynı besin gruplarından farklı seçeneklerle kurulabilir; tekdüzelik "
         "planın bırakılma sebeplerinden biridir."),
        ("Kahvaltıyı atlamak zararlı mı?",
         "Herkes için tek bir cevap yok. Belirleyici olan, atlanan öğünün gün içindeki toplam "
         "alımı ve öğleden sonraki porsiyonu nasıl etkilediği."),
        ("Diyet süresince alkol tüketilebilir mi?",
         "Alkol hem enerji hem de öğün kararlarını etkilediği için plan içinde ayrıca "
         "değerlendirilir; sıklık ve miktar birlikte konuşulur."),
    ]
    if p.get("ofis_ili"):
        h.insert(0, ("Ofiste yüz yüze görüşme de yapabiliyor muyum?",
                     "Evet. Seyhan'daki ofiste yüz yüze görüşme mümkündür; online takiple birlikte de yürütülebilir."))
    if p.get("universite"):
        h.append((f"{p['universite']} öğrencisiyim, yurtta kalıyorum. Plan uygulanabilir mi?",
                  "Yurt ve yemekhane düzenine göre plan hazırlanabilir. "
                  "Belirleyici olan, gün içinde erişebildiğiniz seçeneklerin baştan bilinmesidir."))
    return h


def sss_sec(p, adet=5):
    """Havuzdan profile göre `adet` farklı soru seçer.

    Deterministik ama sonsuz döngüye giremez: indeksler tek seferde
    sıralanır, bu yüzden seçim her zaman `min(adet, len(h))` farklı
    eleman döndürür. (Önceki sabit-adımlı versiyon, havuz uzunluğu
    adıma bölündüğünde tüm indeksleri gezemiyordu.)
    """
    h = sss_havuzu(p)
    n = len(h)
    if p["il"] in SSS_DAGITIM:
        # Kısıtlı dağıtım: iki il en fazla 2 ortak soru paylaşır.
        return [h[i % n] for i in SSS_DAGITIM[p["il"]]][:adet]
    t = _tohum(p, "sss")
    sira = sorted(range(n), key=lambda i: ((t + 1) * (i * i * 7 + i * 13 + 5)) % 1000003)
    return [h[i] for i in sira[:min(adet, n)]]


def blok_sss(p):
    sorular = sss_sec(p)
    ic = "".join(
        f'<details class="faq"><summary>{s}</summary><div>{c}</div></details>'
        for s, c in sorular
    )
    return "Sık Sorulan Sorular", ic, None


def blok_ozet_cevap(p):
    """AEO varyantı: sayfanın en üstünde doğrudan cevap kutusu.

    Metin varyantlı: sabit bırakıldığında bu blok, IL-03 varyantını alan bütün
    illerde birebir aynı iki cümleyi üretiyordu.
    """
    il = T.baslik(p["il"])
    ilDE, ilDEN = T.bulunma(il), T.ayrilma(il)
    i = _idx(p, "mutfak_giris")   # mevcut kısıtlı dağıtımı yeniden kullanır
    ofis = ("Hizmetin merkezi Adana Seyhan'dadır; dileyen danışanlar yüz yüze de görüşebilir."
            if p.get("ofis_ili") else
            f"{ilDE} fiziksel ofis bulunmadığı için görüşmeler video üzerinden yapılır.")
    cevaplar = [
        f"{ilDE} online diyetisyen desteği {DYT} ile video görüşme üzerinden yürütülür; "
        f"öykü alınır, kişiye özel plan hazırlanır ve düzenli takiple güncellenir.",
        f"{ilDE} yaşayanlar {DYT} ile uzaktan görüşerek kişiye özel beslenme planı alabilir; "
        f"takip düzenli görüşmelerle sürdürülür.",
        f"{il} için online diyetisyen hizmeti video görüşmeyle veriliyor: beslenme geçmişi "
        f"değerlendiriliyor, plan kişiye göre hazırlanıyor ve takipte güncelleniyor.",
        f"{ilDEN} katılan danışanlar {DYT} ile uzaktan görüşüyor; plan kişinin mutfağına ve "
        f"günlük düzenine göre kuruluyor.",
        f"{ilDE} beslenme danışmanlığı uzaktan yürütülüyor. Görüşmede öykü alınıyor, hedef "
        f"belirleniyor ve plan takip görüşmeleriyle güncelleniyor.",
        f"{il} için süreç şöyle işliyor: video görüşme, kişiye özel öğün planı ve düzenli "
        f"aralıklarla yapılan takip.",
        f"{ilDE} online diyetisyen görüşmesi, yüz yüze görüşmenin içeriğini uzaktan yürütür; "
        f"plan kişinin kendi verileri üzerine kurulur.",
        f"{ilDEN} alınan online diyetisyen desteğinde plan hazır liste değil, kişiye özel "
        f"hazırlanan ve takiple güncellenen bir düzendir.",
        f"{il} için beslenme takibi video görüşmeyle yapılıyor; öykü, hedef, plan ve düzenli "
        f"takip aşamaları yüz yüze görüşmeyle aynı.",
        f"{ilDE} uzaktan beslenme danışmanlığı alınabiliyor: görüşme, kişiye özel plan ve "
        f"düzenli takip.",
        f"{il} için online diyetisyen desteği {DYT} tarafından uzaktan veriliyor; plan mutfak "
        f"ve çalışma düzenine göre kuruluyor.",
        f"{ilDE} görüşmeler video üzerinden yapılıyor ve plan, takip görüşmelerinde ilerlemeye "
        f"göre yeniden düzenleniyor.",
    ][i]
    govde = f"""
<div class="ozet">
<p><strong>Kısa cevap:</strong> {cevaplar} {ofis}</p>
</div>"""
    return None, govde, None


BLOKLAR["sss"] = blok_sss
BLOKLAR["ozet_cevap"] = blok_ozet_cevap


def blok_pratik(p):
    """İle özgü somut uygulama önerisi.

    Sayfanın ikinci özgün çekirdeği. Çerçeve havuzlarını büyütmek yerine her ile
    gerçekten farklı bir içerik yazmak, hem duplicate sorununu kökten çözüyor hem
    de sayfanın "neden ayrı URL" sorusuna verdiği cevabı güçlendiriyor.
    Verisi olmayan ilde blok hiç basılmaz.
    """
    if not p.get("pratik"):
        return None, None, None
    il = T.baslik(p["il"])
    t = _tohum(p, "pratik")
    baslik = [
        f"{il} İçin Pratik Bir Öneri",
        f"{T.bulunma(il)} İşe Yarayan Bir Düzenleme",
        f"{il} Sofrasında Küçük Bir Değişiklik",
        f"{T.bulunma(il)} Sık Uyguladığımız Bir Ayar",
        f"{il} İçin Uygulanabilir Bir Adım",
        f"{T.bulunma(il)} Denenmiş Bir Yaklaşım",
    ][_idx(p, 'pratik_baslik')]
    return baslik, f"<p>{p['pratik']}</p>", None


BLOKLAR["pratik"] = blok_pratik
