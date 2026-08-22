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

import turkce as T

SITE = "https://onlinediyetisyen.online"
DYT = "Dyt. Tuğba Şeker Ağaç"
TEL_HREF = "tel:+905070361859"
TEL_GORUNEN = "0507 036 18 59"
WA = "https://wa.me/905070361859"


def _sec(secenekler, tohum):
    return secenekler[tohum % len(secenekler)]


def _tohum(p):
    """İl için karıştırılmış tohum.

    Düz polinom hash yetmiyordu: `% 4` alındığında farklı iller aynı varyasyona
    düşüp aynı çerçeve cümlelerini paylaşıyordu (Mersin ∩ İstanbul). Son karıştırma
    adımı düşük bitleri de dağıtıyor.
    """
    h = 0
    for ch in p["il"]:
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
    ][t % 4]
    kapanis = [
        "Bu yemeklerin hiçbiri tek başına yasak değil; belirleyici olan haftalık düzen içindeki yerleri.",
        "Listede yasak bir yemek yok. Fark, porsiyon ve hangi sıklıkla sofraya geldiği.",
        "Hiçbiri planın dışında kalmak zorunda değil; ölçü ve sıklık ayarlandığında yerini koruyabiliyor.",
        "Buradaki mesele yemeği çıkarmak değil, haftalık düzen içindeki payını belirlemek.",
    ][(t + 2) % 4]
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
    t = _tohum(p)
    baslik = [
        f"{ilDE} Randevuya Gitmenin Zaman Maliyeti",
        f"{ilDE} Takibi Ayakta Tutan Şey: Süreklilik",
        f"{ilDE} Programın Yarıda Kalma Sebebi Genelde Plan Değil",
        f"{ilDE} Zaman Yönetimi ve Beslenme Takibi",
    ][t % 4]
    ek = p.get("ozel") or ""
    acilis = [
        "Bir beslenme programının sonuç vermesini sağlayan şey tek bir mükemmel görüşme değil, "
        "haftalar boyunca kesintisiz süren takiptir.",
        "Programların yarıda kalma sebebi çoğu zaman planın kendisi değil, takip görüşmelerinin "
        "aksamaya başlaması oluyor.",
        "Beslenme takibinde sonucu belirleyen değişken, planın ne kadar iyi olduğundan çok "
        "ne kadar süre uygulanabildiği.",
        "Danışanlarda gördüğümüz en sık kopuş noktası ilk görüşme değil, üçüncü veya dördüncü "
        "takip görüşmesinin ertelenmesi.",
    ][(t + 1) % 4]
    devam = [
        "Takibi bozan en yaygın sebep ise plan değil, program çakışması: iş çıkışı trafiği, "
        "çocuğun okul saati, vardiya değişimi.",
        "Bunu bozan şey genelde motivasyon kaybı değil, takvimin dolması: mesai, okul, yol.",
        "Araya giren şey çoğu zaman isteksizlik değil; randevuya ayrılacak yarım günün bulunamaması.",
        "Erteleme sebebi çoğunlukla programın zorluğu değil, o güne sığmayan bir yolculuk.",
    ][(t + 2) % 4]
    cozum = [
        "Online görüşme bu denklemden ulaşım süresini tamamen çıkarır.",
        "Görüşmenin uzaktan yapılması, takvime yalnızca görüşme süresinin yazılması demek.",
        "Uzaktan takipte programa eklenen tek şey görüşmenin kendisi oluyor; yol süresi devre dışı kalıyor.",
        "Görüşmeler video üzerinden yürütüldüğünde randevu, gününüzün yarısını değil yalnızca o saati kaplıyor.",
    ][(t + 3) % 4]
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
    t = _tohum(p)
    baslik = [
        f"{ilDE} Mevsimler Beslenmeyi Nasıl Etkiliyor?",
        f"{il} İkliminin Öğün Düzenine Etkisi",
        f"{ilDE} Yıl İçinde Değişen Beslenme İhtiyacı",
        f"{il} İçin Mevsime Göre Plan Güncellemesi",
    ][t % 4]
    kapanis = [
        f"Plan hazırlanırken bu döngü hesaba katılır: {il} için yaz ve kış aylarında sıvı ihtiyacı, "
        f"öğün saatleri ve günlük hareket miktarı aynı kalmaz.",
        f"Bu yüzden {il} için hazırlanan planlar tek bir mevsime göre değil, yıl içindeki geçişlere "
        f"göre kurgulanır; sıvı hedefi ve öğün saatleri buna göre ayarlanır.",
        f"{T.bulunma(il)} bu döngü, öğün saatlerinden günlük hareket miktarına kadar planın birkaç "
        f"parçasını aynı anda etkiler.",
        f"Planın {il} koşullarına göre mevsim geçişlerinde gözden geçirilmesi, takip görüşmelerinin "
        f"asıl işlevlerinden biri.",
    ][(t + 1) % 4]
    govde = f"""
<p>{il}, {p['bolge']} Bölgesi'nde yer alır; {p['iklim']} görülür. {p['iklim_notu']}</p>
<p>{kapanis}</p>"""
    aeo = (f"{ilDE} {p['iklim']} görülür. {p['iklim_notu']} Beslenme planı mevsim geçişlerinde "
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
    t = _tohum(p)
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
    """AEO varyantı: sayfanın en üstünde doğrudan cevap kutusu."""
    il = T.baslik(p["il"])
    ilDE, ilDEN = T.bulunma(il), T.ayrilma(il)
    ofis = ("Hizmetin merkezi Adana Seyhan'dadır; dileyen danışanlar yüz yüze de görüşebilir."
            if p.get("ofis_ili") else
            f"{ilDE} fiziksel ofis bulunmadığı için görüşmeler video üzerinden yapılır.")
    govde = f"""
<div class="ozet">
<p><strong>Kısa cevap:</strong> {ilDE} online diyetisyen desteği, {DYT} ile video görüşme
üzerinden yürütülür. Beslenme öyküsü alınır, kişiye özel öğün planı hazırlanır ve düzenli takip
görüşmeleriyle plan güncellenir. {ofis}</p>
</div>"""
    return None, govde, None


BLOKLAR["sss"] = blok_sss
BLOKLAR["ozet_cevap"] = blok_ozet_cevap
