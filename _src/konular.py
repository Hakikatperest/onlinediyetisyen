# -*- coding: utf-8 -*-
"""Konu kümesi (pillar) sayfaları — FAZ 1.

Bu sayfalar lokasyondan BAĞIMSIZ bilginin tek adresidir. Amaç ikili:
  1. Kullanıcı için: "online diyetisyen nedir / nasıl çalışır / ne kadar" sorularının
     tam ve derli toplu cevabı.
  2. Mimari için: bu içerik burada durduğu sürece 81 il sayfasında tekrarlanmaz.
     Duplicate content sorunu şablon hilesiyle değil, doğru bilgi mimarisiyle çözülür.

Her il/ilçe sayfası buraya link verir; buradan da illere dönülür.
"""
from content import SITE, DYT, TEL_HREF, TEL_GORUNEN

HUB = "online-diyetisyen"

KONULAR = [
    dict(
        slug="online-diyetisyen-nedir",
        h1="Online Diyetisyen Nedir?",
        title="Online Diyetisyen Nedir? Nasıl Çalışır, Kimler İçin Uygun",
        desc="Online diyetisyen ne demek, görüşme nasıl yapılır, yüz yüze görüşmeden farkı nedir "
             "ve kimler için uygundur? Diyetisyen gözünden açık bir anlatım.",
        aeo="Online diyetisyen, beslenme danışmanlığını yüz yüze randevu yerine video görüşme ve "
            "dijital takip üzerinden yürüten diyetisyendir. Öykü alma, hedef belirleme, kişiye özel "
            "plan hazırlama ve düzenli takip aşamaları yüz yüze görüşmeyle aynıdır.",
        bolumler=[
            ("Tanım", """
<p>Online diyetisyen, beslenme ve diyet danışmanlığını uzaktan yürüten diyetisyendir.
Görüşme video üzerinden yapılır, beslenme planı dijital olarak paylaşılır ve takip
düzenli görüşmelerle sürdürülür.</p>
<p>Burada sık karıştırılan bir nokta var: online diyetisyen, internette bulunan hazır
diyet listesi demek değildir. Hazır liste kişiye özel değildir; kimin uyguladığını,
hangi tahlil değerlerine sahip olduğunu, günün hangi saatinde ne yiyebildiğini bilmez.
Online danışmanlıkta ise plan, kişinin kendi verileri üzerine kurulur.</p>"""),
            ("Görüşme Nasıl Yapılır?", """
<ol class="steps">
<li><strong>Randevu.</strong> Telefon veya WhatsApp üzerinden uygun saat belirlenir.</li>
<li><strong>Ön görüşme.</strong> Beslenme öyküsü, günlük düzen, sağlık geçmişi ve varsa
tahlil sonuçları değerlendirilir.</li>
<li><strong>Hedef.</strong> Ölçülebilir ve gerçekçi bir hedef birlikte belirlenir.</li>
<li><strong>Plan.</strong> Kişinin mutfağına, bütçesine ve çalışma saatlerine uyan öğün
planı hazırlanır.</li>
<li><strong>Takip.</strong> Düzenli görüşmelerle ilerleme değerlendirilir.</li>
<li><strong>Güncelleme.</strong> Plan; sonuçlara, mevsime ve değişen düzene göre revize edilir.</li>
</ol>
<p>Görüşme için kamerası ve mikrofonu çalışan bir telefon, tablet veya bilgisayar yeterlidir.
Ayrı bir program kurmanız gerekmez.</p>"""),
            ("Kimler İçin Uygun?", """
<ul class="chk">
<li>Kilo yönetimi hedefleyen ve sürdürülebilir bir düzen kurmak isteyen yetişkinler</li>
<li>Çalışma temposu nedeniyle öğün saatleri dağılmış kişiler</li>
<li>Evden çalışanlar ve gün boyu mutfağa erişimi olanlar</li>
<li>Düzenli spor yapan ve beslenmesini buna göre kurgulamak isteyenler</li>
<li>Bulunduğu yerde diyetisyene ulaşımı zor olanlar</li>
</ul>
<p class="note"><strong>Önemli:</strong> Gebelik, emzirme, böbrek veya karaciğer hastalığı,
yeme bozukluğu öyküsü ya da düzenli ilaç kullanımı gibi durumlarda beslenme planı hekim
değerlendirmesiyle birlikte yürütülmelidir. Bu sayfadaki bilgiler genel bilgilendirme
amaçlıdır; kişisel tıbbi tavsiye yerine geçmez.</p>"""),
        ],
        sss=[
            ("Online diyetisyen ile hazır diyet listesi arasındaki fark nedir?",
             "Hazır liste herkes için aynıdır ve kişinin sağlık geçmişini, günlük düzenini veya "
             "tahlil değerlerini bilmez. Online danışmanlıkta plan kişinin kendi verileri üzerine "
             "kurulur ve takip görüşmeleriyle güncellenir."),
            ("Online görüşme için hangi cihaz gerekiyor?",
             "Kamerası ve mikrofonu çalışan bir telefon, tablet veya bilgisayar yeterlidir. "
             "Görüşme bağlantısı önceden paylaşılır."),
            ("Diyetisyenin gerçekten diyetisyen olduğunu nasıl anlarım?",
             "Diyetisyenlik, üniversitelerin Beslenme ve Diyetetik bölümünden lisans mezuniyeti "
             "gerektiren bir sağlık mesleğidir. Danışmanlık almadan önce mezuniyet bilgisini "
             "sormanız ve doğrulamanız önerilir."),
            ("Kaç görüşmede sonuç alınır?",
             "Bu kişiye, hedefe ve başlangıç durumuna göre değişir; tek bir süre vermek doğru olmaz. "
             "Belirleyici olan görüşme sayısından çok takibin kesintisiz sürmesidir."),
        ],
    ),
    dict(
        slug="online-diyetisyen-fiyatlari",
        h1="Online Diyetisyen Ücretleri Neye Göre Değişir?",
        title="Online Diyetisyen Ücretleri | Fiyat Neye Göre Belirlenir?",
        desc="Online diyetisyen ücreti neye göre değişir? Program süresi, görüşme sıklığı, "
             "hizmet kapsamı ve özel durumların fiyata etkisi açıkça anlatılıyor.",
        aeo="Online diyetisyen ücreti; program süresi, görüşme sıklığı, hizmet kapsamı ve insülin "
            "direnci veya sporcu beslenmesi gibi özel durumlara göre değişir. Tek sabit bir rakam "
            "yerine takip modeline göre fiyatlandırma yapılır.",
        bolumler=[
            ("Fiyatı Belirleyen Dört Etken", """
<div class="tablo-kaydir"><table class="cmp">
<thead><tr><th>Etken</th><th>Fiyata etkisi</th></tr></thead>
<tbody>
<tr><td>Program süresi</td><td>Tek görüşme ile aylık takip paketi farklı fiyatlanır</td></tr>
<tr><td>Görüşme sıklığı</td><td>Haftalık takip, iki haftada bir takipten farklıdır</td></tr>
<tr><td>Hizmet kapsamı</td><td>Yalnızca plan mı, tahlil değerlendirmesi ve ölçüm takibi de dâhil mi</td></tr>
<tr><td>Özel durum</td><td>İnsülin direnci, PCOS, sporcu beslenmesi farklı planlama emeği gerektirir</td></tr>
</tbody></table></div>"""),
            ("Ucuz Diyet Programlarında Dikkat Edilmesi Gerekenler", """
<p>Çok düşük fiyatlı "diyet listesi" satan hizmetlerde genellikle hazır bir şablon paylaşılır
ve takip yapılmaz. Bu tür programlarda iki risk vardır: plan kişinin sağlık durumuna uygun
olmayabilir ve takip olmadığı için ilk zorlukta bırakılır.</p>
<p>Fiyat karşılaştırırken bakılması gereken şey rakamın kendisi değil, o rakama neyin dâhil
olduğudur: kaç görüşme, ne kadar takip, plan güncellemesi var mı?</p>"""),
            ("Paket mi, Tek Görüşme mi?", """
<p>Tek görüşme, mevcut düzenini büyük ölçüde kurmuş ve yalnızca yön doğrulaması isteyen
kişiler için yeterli olabilir. Ancak kilo yönetimi gibi süreç gerektiren hedeflerde tek
görüşmenin karşılığı sınırlıdır: plan verilir, uygulamada çıkan sorular cevapsız kalır.</p>
<p>Takip paketlerinde ödenen şey liste değil, sürecin kendisi: planın uygulanabilirliğinin
kontrol edilmesi, tıkanan noktada revizyon ve ölçümlerin birlikte yorumlanması. Diyet
programlarında bırakma çoğunlukla ilk üç hafta içinde olur; takip tam olarak bu aralığı
kapatmak içindir.</p>"""),
            ("Fiyat Karşılaştırırken Sorulacak 5 Soru", """
<ul class="chk">
<li>Ücrete kaç görüşme dâhil ve görüşmeler ne kadar sürüyor?</li>
<li>Plan kişiye özel mi hazırlanıyor, yoksa hazır bir şablon mu paylaşılıyor?</li>
<li>Tahlil sonuçları değerlendiriliyor mu?</li>
<li>Görüşmeler arasında soru sorma imkânı var mı?</li>
<li>Plan hedefe göre güncelleniyor mu, yoksa tek seferlik mi?</li>
</ul>
<p>Bu beş sorunun cevabı iki hizmet arasındaki gerçek farkı, fiyat etiketinden daha iyi
gösterir. Aynı rakama karşılık gelen kapsam, sağlayıcıya göre belirgin şekilde değişebilir.</p>"""),
            ("Güncel Ücret Bilgisi", f"""
<p>Ücretler hizmet kapsamına göre belirlendiği için bu sayfada sabit bir rakam yer almaz.
Size uygun takip modelini ve güncel ücreti öğrenmek için
<a href="{SITE}/#fiyatlar">fiyatlar bölümüne</a> bakabilir veya
<a href="{TEL_HREF}">{TEL_GORUNEN}</a> numarasından doğrudan bilgi alabilirsiniz.</p>"""),
        ],
        sss=[
            ("Online diyetisyen yüz yüze görüşmeden daha mı ucuz?",
             "Zorunlu olarak değil. Ücret hizmet kapsamına göre belirlenir. Ancak online görüşmede "
             "ulaşım masrafı ve yol süresi ortadan kalktığı için toplam maliyet çoğu kişide daha düşük olur."),
            ("Yaşadığım şehre göre ücret değişiyor mu?",
             "Hayır. Görüşmeler uzaktan yapıldığı için ücret bulunduğunuz il veya ilçeye göre değişmez."),
            ("Paket bitmeden bırakırsam ne oluyor?",
             "Bu, başlangıçta üzerinde anlaşılan çalışma koşullarına bağlıdır ve ilk görüşmede açıkça konuşulur."),
            ("Tahlil masrafı ücrete dâhil mi?",
             "Hayır. Tahliller sağlık kuruluşunda yapılır ve danışmanlık ücretinden ayrıdır."),
        ],
    ),
    dict(
        slug="online-diyetisyen-avantajlari",
        h1="Online Diyetisyenin Avantajları ve Sınırları",
        title="Online Diyetisyenin Avantajları ve Sınırları | Tarafsız Bakış",
        desc="Online diyetisyenin gerçek avantajları neler, hangi durumlarda yüz yüze görüşme "
             "daha uygun? Abartısız ve tarafsız bir karşılaştırma.",
        aeo="Online diyetisyenin başlıca avantajı ulaşım süresinin ortadan kalkması ve takip "
            "sürekliliğinin korunmasıdır. Cihazla vücut kompozisyonu ölçümü gerektiren durumlarda "
            "ise yüz yüze görüşme daha uygundur.",
        bolumler=[
            ("Avantajlar", """
<ul class="chk">
<li><strong>Ulaşım süresi yok.</strong> Takibi bozan en yaygın sebep plan değil, program çakışmasıdır.</li>
<li><strong>Kendi mutfağınızdasınız.</strong> Dolabınızda ne olduğu anlatıya değil, gerçeğe dayanır.</li>
<li><strong>Saat esnekliği.</strong> Vardiyalı çalışanlar için akşam saatleri değerlendirilebilir.</li>
<li><strong>Şehir değişikliğinden etkilenmez.</strong> Taşınma takibi kesintiye uğratmaz.</li>
<li><strong>Erişim.</strong> Bulunduğu yerde diyetisyene ulaşımı zor olanlar için engel ortadan kalkar.</li>
</ul>"""),
            ("Sınırlar — Dürüst Olmak Gerekirse", """
<p>Online takibin her durumda üstün olduğunu söylemek doğru olmaz. Şu başlıklarda yüz yüze
görüşme avantajlıdır:</p>
<ul class="chk">
<li>Cihazla vücut kompozisyonu ölçümü gereken durumlar</li>
<li>Fiziksel değerlendirme gerektiren özel durumlar</li>
<li>Teknolojiye erişimi veya kullanım rahatlığı sınırlı kişiler</li>
</ul>
<p>Ayrıca hiçbir beslenme programı, hekim takibi gerektiren bir durumun yerine geçmez.
Kronik hastalık, gebelik veya yeme bozukluğu öyküsü varsa süreç hekim değerlendirmesiyle
birlikte yürütülmelidir.</p>"""),
            ("Online Takipte Süreç Nasıl İşliyor?", """
<p>Uzaktan takipte en sık merak edilen şey, diyetisyenin kişiyi görmeden nasıl
değerlendirdiği. Pratikte değerlendirme üç veri üzerinden yürüyor: kişinin tuttuğu beslenme
kaydı, düzenli aralıklarla paylaşılan ölçümler ve görüşmelerde konuşulan günlük düzen.</p>
<p>Bu üçü bir araya geldiğinde, plandaki hangi maddenin uygulanabildiği ve hangisinin
tıkandığı görülebiliyor. Tıkanan madde değiştirilerek plan yeniden kuruluyor — asıl
takip işi bu.</p>"""),
            ("Kimler İçin Online Takip Daha Uygun?", """
<ul class="chk">
<li>Çalışma saatleri randevu saatleriyle çakışanlar</li>
<li>Bulunduğu yerde beslenme danışmanlığına erişimi sınırlı olanlar</li>
<li>Sık şehir değiştiren veya seyahat edenler</li>
<li>Daha önce başlayıp ulaşım/zaman nedeniyle bırakmış olanlar</li>
<li>Kendi mutfağı üzerinden çalışmayı tercih edenler</li>
</ul>
<p>Bu liste bir üstünlük iddiası değil; yalnızca hangi koşulda uzaktan takibin pratik
avantaj sağladığını gösteriyor.</p>"""),
        ],
        sss=[
            ("Online takipte motivasyon düşer mi?",
             "Motivasyonu belirleyen şey görüşmenin online veya yüz yüze olması değil, takibin "
             "düzenli sürmesidir. Görüşme aralıkları uzadığında her iki modelde de bırakma oranı artar."),
            ("Ölçümlerimi evde doğru yapabilir miyim?",
             "Haftanın aynı günü, sabah aç karnına ve aynı tartıyla yapılan ölçüm takip için yeterlidir. "
             "Önemli olan tek bir ölçüm değil, ölçümlerin zaman içindeki eğilimidir."),
            ("Hangi durumlarda yüz yüze görüşmeye yönlendiriliyorum?",
             "Fiziksel değerlendirme veya cihazla ölçüm gerektiren durumlarda ve hekim takibi gereken "
             "tablolarda yönlendirme yapılır."),
        ],
    ),
]


# --- Diyet nişi konu sayfaları -------------------------------------------------
# Bu üç sayfa diyet.py'deki blokları taşır. Lokasyondan bağımsız oldukları için
# il sayfalarında değil burada dururlar.
def _diyet_konulari():
    import diyet as DY
    from city_context import il_profili
    p = il_profili("ADANA")   # blok metinlerindeki il bağlamı burada nötrlenir
    tanim = [
        ("online-diyet-turleri", "Diyet Türleri: Hangisi Kime Uygun?",
         "Diyet Türleri | Hangi Diyet Kime Uygun? Diyetisyen Anlatıyor",
         "Aralıklı oruç, düşük karbonhidrat, Akdeniz tipi, yüksek protein… Diyet türleri "
         "arasındaki gerçek fark ve hangisinin kime uygun olduğu.",
         "Diyet türleri arasındaki farkı belirleyen şey adları değil, kişinin sağlık durumu ve "
         "sürdürebilirliğidir. Aralıklı oruç, düşük karbonhidratlı düzen, Akdeniz tipi beslenme ve "
         "yüksek proteinli düzen farklı kişilerde farklı sonuç verir.",
         ["diyet_turleri", "diyet_secim_kriteri", "diyet_efsaneleri"],
         [("En hızlı zayıflatan diyet hangisi?",
           "Hızlı kilo kaybı sağlayan kısıtlayıcı düzenler kısa vadede sonuç verse de geri alım "
           "oranı yüksektir. Kalıcı sonuç, sürdürülebilen düzenle elde edilir."),
          ("Karbonhidratı tamamen kesmeli miyim?",
           "Hayır. Bir besin grubunu tamamen çıkarmak eksiklik riski taşır. Yapılan şey genelde "
           "karbonhidratın türünü ve miktarını düzenlemektir."),
          ("Diyet türünü kendim seçebilir miyim?",
           "Seçim yapılabilir, ancak tahlil değerleri ve varsa kronik hastalık durumu "
           "değerlendirilmeden başlanan düzenler beklenen sonucu vermeyebilir.")]),
        ("diyete-nasil-baslanir", "Diyete Nasıl Başlanır?",
         "Diyete Nasıl Başlanır? İlk Hafta İçin Adım Adım Rehber",
         "Diyete başlarken ilk hafta ne yapılmalı? Beslenme kaydı, tahlil kontrolü, öğün "
         "saatleri ve gerçekçi hedef belirleme adım adım anlatılıyor.",
         "Diyete başlarken ilk adım mevcut beslenme düzenini üç gün boyunca değiştirmeden "
         "kaydetmektir. Ardından tahlil değerleri gözden geçirilir, tek bir hedef belirlenir ve "
         "öğün saatleri sabitlenir.",
         ["hazirlik", "diyete_baslama", "ilk_hafta"],
         [("Diyete pazartesi mi başlamalıyım?",
           "Başlangıç gününün sonuca etkisi yoktur. Belirleyici olan planın o günün koşullarına "
           "uygun kurulmuş olmasıdır."),
          ("Diyete başlarken tartılmalı mıyım?",
           "Başlangıç ölçümü referans oluşturur. Ancak takip için haftalık ölçüm yeterlidir; "
           "günlük tartı dalgalanmayı gösterir, değişimi değil."),
          ("Kaç kilo vermeyi hedeflemeliyim?",
           "Hedef kişinin başlangıç durumuna göre belirlenir. Haftalık olarak gerçekçi ve "
           "sürdürülebilir bir aralık, hızlı kayıptan daha iyi sonuç verir.")]),
        ("diyette-sik-yapilan-hatalar", "Diyette Sık Yapılan Hatalar",
         "Diyette Sık Yapılan Hatalar | Süreci Yavaşlatan 6 Alışkanlık",
         "Öğün atlamak, her gün tartılmak, tek besini suçlamak… Diyet sürecini yavaşlatan "
         "yaygın hatalar ve bunların yerine ne yapılması gerektiği.",
         "Diyette en sık yapılan hatalar öğün atlamak, sıvı tüketimini ihmal etmek, her gün "
         "tartılmak, tek bir besini suçlamak ve sonucu çok kısa sürede beklemektir.",
         ["hatalar", "hata_duzeltme", "hata_takip"],
         [("Öğün atlarsam daha hızlı zayıflar mıyım?",
           "Genellikle tersi olur. Atlanan öğün sonraki öğünde porsiyonu büyütür ve günlük toplam "
           "değişmeyebilir."),
          ("Tartı neden her gün farklı gösteriyor?",
           "Günlük ağırlık; sıvı dengesi, tuz tüketimi ve sindirim durumuna göre dalgalanır. "
           "Gerçek değişim haftalık eğilimde görülür."),
          ("Diyeti bir gün bozdum, baştan mı başlamalıyım?",
           "Hayır. Tek bir öğün haftalık düzeni belirlemez. Yapılacak şey baştan başlamak değil, "
           "bir sonraki öğünde plana dönmektir.")]),
    ]
    out = []
    for slug, h1, title, desc, aeo, bloklar, sss in tanim:
        bolumler = []
        for bk in bloklar:
            b, g = DY.DIYET_BLOKLARI[bk](p)
            bolumler.append((b, g))
        out.append(dict(slug=slug, h1=h1, title=title, desc=desc, aeo=aeo,
                        bolumler=bolumler, sss=sss))
    return out


KONULAR = KONULAR + _diyet_konulari()
