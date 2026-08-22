# -*- coding: utf-8 -*-
"""Diyet nişine ait içerik blokları.

Sayfaların zenginleşme ekseni budur: yaşam düzeni/turizm/vardiya gibi konu dışı
başlıklar değil, doğrudan DİYET konuları — diyet türleri, diyete nasıl başlanır,
kilo verme süreci, öğün düzeni, sık yapılan hatalar.

Sitedeki mevcut blog yazılarına iç link buradan verilir; böylece yeni sayfalar
mevcut içerikle tek bir konu ağı oluşturur.
"""
import turkce as T
from content import SITE, _tohum

# Mevcut yazılar — iç link hedefleri (hepsi yayında, sitemap'te var)
YAZILAR = {
    "aralikli-oruc": "aralıklı oruç (16:8) gerçekten zayıflatır mı",
    "insulin-direnci-nedir": "insülin direncinde beslenme",
    "kilo-veremiyorum": "diyet yaptığı hâlde kilo veremeyenler",
    "protein-ihtiyaci": "günlük protein ihtiyacı",
    "surdurulebilir-beslenme-nedir": "sürdürülebilir beslenme nedir",
    "surdurulebilir-beslenmenin-10-altin-kurali": "sürdürülebilir beslenmenin 10 kuralı",
    "ultra-islenmis-gidalar": "ultra işlenmiş gıdalar",
    "zayiflama-igneleri": "zayıflama iğneleri",
    "bir-muz-diyeti-bozar-mi": "bir muz diyeti bozar mı",
    "online-diyet-nedir": "online diyet nedir",
    "lipodem-nedir": "lipödem ve beslenme",
}


def yazi_linki(slug, metin=None):
    return f'<a href="{SITE}/blog/{slug}/">{metin or YAZILAR[slug]}</a>'


# --------------------------------------------------------------- DİYET TÜRLERİ
def blok_diyet_turleri(p):
    t = _tohum(p)
    baslik = [
        "Hangi Diyet Türü Kime Uygun?",
        "Diyet Türleri Arasındaki Fark Ne?",
        "Popüler Diyet Türlerine Diyetisyen Gözüyle Bakış",
        "Diyet Türü Seçerken Nelere Bakılır?",
    ][t % 4]
    giris = [
        "Danışanların en sık sorduğu soru hangi diyetin en iyi olduğu. Kısa cevap: "
        "kişiye uyan ve uzun süre sürdürülebilen diyet.",
        "Bir diyetin işe yarayıp yaramadığını belirleyen şey adı değil, kişinin onu ne kadar "
        "süre uygulayabildiği.",
        "İnternette dolaşan diyet listelerinin çoğu aynı prensibin farklı isimlerle "
        "paketlenmiş hâli. Farkı yaratan, kişiye uygun olup olmadığı.",
        "Diyet türü seçimi bir moda meselesi değil; kişinin sağlık durumu, günlük düzeni ve "
        "mutfak alışkanlıkları belirleyici.",
    ][(t + 1) % 4]
    return baslik, f"""
<p>{giris}</p>
<div class="tablo-kaydir"><table class="cmp">
<thead><tr><th>Yaklaşım</th><th>Temel mantığı</th><th>Kimde dikkat gerekir</th></tr></thead>
<tbody>
<tr><td>Dengeli beslenme düzeni</td><td>Öğün dağılımı ve porsiyon kontrolü; besin grubu çıkarılmaz</td><td>Genel olarak en geniş uygulama alanı</td></tr>
<tr><td>Aralıklı oruç</td><td>Yeme penceresinin daraltılması</td><td>Kan şekeri düzensizliği, ilaç kullanımı, gebelik</td></tr>
<tr><td>Düşük karbonhidratlı düzen</td><td>Karbonhidrat payının azaltılması</td><td>Böbrek hastalığı, yoğun spor yapanlar</td></tr>
<tr><td>Akdeniz tipi beslenme</td><td>Zeytinyağı, sebze, baklagil ve balık ağırlıklı sofra</td><td>Porsiyon kontrolü atlanırsa hedefe ulaşılmaz</td></tr>
<tr><td>Yüksek proteinli düzen</td><td>Protein payının artırılması</td><td>Böbrek fonksiyon bozukluğu olanlar</td></tr>
</tbody></table></div>
<p>Bu yaklaşımların hiçbiri herkes için doğru ya da yanlış değil. Görüşmelerde seçim,
kişinin tahlil değerleri ve günlük düzeni üzerinden yapılıyor.
{yazi_linki('aralikli-oruc', 'Aralıklı orucun gerçekten zayıflatıp zayıflatmadığını')} ve
{yazi_linki('protein-ihtiyaci', 'günlük protein ihtiyacının nasıl hesaplandığını')}
ayrı yazılarda ele aldık.</p>
<p class="note"><strong>Not:</strong> Bir besin grubunu tamamen çıkaran diyetler, kısa vadede
hızlı sonuç verse de uzun süre uygulandığında eksiklik riski taşır. Böyle bir düzene geçmeden
önce diyetisyen ve gerekli durumlarda hekim değerlendirmesi önerilir.</p>"""


# ------------------------------------------------------- DİYETE NASIL BAŞLANIR
def blok_diyete_baslama(p):
    t = _tohum(p)
    baslik = [
        "Diyete Nasıl Başlanır?",
        "İlk Hafta: Diyete Başlarken Ne Yapılmalı?",
        "Diyete Başlamanın Doğru Sırası",
        "Diyete Başlarken Atılacak İlk Adımlar",
    ][t % 4]
    return baslik, f"""
<ol class="steps">
<li><strong>Mevcut düzeni yaz.</strong> Üç gün boyunca ne yediğinizi değiştirmeden kaydedin.
Planın başlangıç noktası burasıdır.</li>
<li><strong>Tahlil değerlerini gözden geçir.</strong> Kan şekeri, tiroit ve demir değerleri
sürecin nasıl kurgulanacağını etkiler.</li>
<li><strong>Tek bir hedef belirle.</strong> Aynı anda beş şeyi değiştirmek yerine bir alışkanlıkla
başlamak, kalıcılığı artırır.</li>
<li><strong>Öğün saatlerini sabitle.</strong> Ne yendiğinden önce ne zaman yendiği düzene girer.</li>
<li><strong>Yasak listesi yerine ölçü kur.</strong> Sevdiğiniz yemekleri planın dışına atmak,
bırakma sebebinin ta kendisi.</li>
<li><strong>Takip aralığını belirle.</strong> Değişimi ölçmeden sürdürmek, ilk zorlukta
bırakmaya yol açar.</li>
</ol>
<p>İlk görüşmelerde en sık karşılaştığımız durum, kişinin daha önce
birkaç kez başlayıp bırakmış olması. Bunun sebebi çoğu zaman irade değil, baştan fazla
iddialı kurulmuş bir plan.
{yazi_linki('kilo-veremiyorum', 'Diyet yaptığı hâlde kilo veremeyenlerde ne olduğunu')}
ayrıntılı yazdık.</p>"""


# ------------------------------------------------------- SIK YAPILAN HATALAR
def blok_hatalar(p):
    t = _tohum(p)
    baslik = [
        "Diyette Sık Yapılan Hatalar",
        "Süreci Yavaşlatan Yaygın Hatalar",
        "Diyette En Çok Nerede Takılıyoruz?",
        "Planı Bozan Yaygın Alışkanlıklar",
    ][t % 4]
    return baslik, f"""
<ul class="chk">
<li><strong>Öğün atlamak.</strong> Atlanan öğün, sonraki öğünde porsiyonu büyütür.</li>
<li><strong>Sıvıyı unutmak.</strong> Susuzluk sıklıkla açlık olarak algılanır.</li>
<li><strong>Her gün tartılmak.</strong> Günlük dalgalanma gerçek değişimi gizler; haftalık
ölçüm eğilimi gösterir.</li>
<li><strong>Tek bir besini suçlamak.</strong> Sonucu belirleyen tek bir yiyecek değil,
haftalık toplam düzendir. {yazi_linki('bir-muz-diyeti-bozar-mi', 'Bir muzun diyeti bozup bozmadığını')}
ayrı yazıda ele aldık.</li>
<li><strong>Hazır ürünlere “diyet” etiketiyle güvenmek.</strong>
{yazi_linki('ultra-islenmis-gidalar', 'Ultra işlenmiş gıdaların')} etiketi çoğu zaman içeriğini anlatmaz.</li>
<li><strong>Sonucu çok kısa sürede beklemek.</strong> Hızlı verilen kilo, çoğunlukla hızlı geri alınır.</li>
</ul>
<p>Görüşmelerde bu başlıklar tek tek ele alınıyor ve plan, kişinin hangi
noktada takıldığına göre güncelleniyor.</p>"""


DIYET_BLOKLARI = {
    "diyet_turleri": blok_diyet_turleri,
    "diyete_baslama": blok_diyete_baslama,
    "hatalar": blok_hatalar,
}


# ---------------------------------------------------- Konu sayfası ek bölümleri
# Bu bloklar YALNIZCA konu sayfalarında kullanılır (lokasyondan bağımsız),
# bu yüzden tekrar riski yok ve serbestçe uzayabilirler.

def blok_diyet_secim_kriteri(p=None):
    return ("Diyet Seçerken Bakılması Gereken 4 Ölçüt", f"""
<ol class="steps">
<li><strong>Sürdürülebilirlik.</strong> Altı ay uygulayamayacağınız bir düzen, altı hafta
sonunda bıraktığınızda başladığınız yere döndürür.</li>
<li><strong>Sağlık durumu.</strong> Kan şekeri düzensizliği, tiroit sorunu, böbrek hastalığı
veya ilaç kullanımı seçimi doğrudan sınırlar.</li>
<li><strong>Mutfak gerçeği.</strong> Hazırlaması saatler süren veya bulunması zor besinlere
dayanan plan, ilk yoğun haftada uygulanamaz hâle gelir.</li>
<li><strong>Besin çeşitliliği.</strong> Bir besin grubunu tamamen dışlayan düzenler uzun
vadede eksiklik riski taşır.</li>
</ol>
<p>Bu dört ölçüt birlikte değerlendirildiğinde, çoğu kişide "en iyi diyet" sorusunun cevabı
popüler bir isim değil, kişinin mevcut düzenine yapılan birkaç hedefli düzenleme oluyor.
{yazi_linki('surdurulebilir-beslenme-nedir', 'Sürdürülebilir beslenmenin ne anlama geldiğini')}
ayrı bir yazıda ele aldık.</p>""")


def blok_diyet_efsaneleri(p=None):
    return ("Diyet Türleri Hakkında Yaygın Yanlışlar", f"""
<ul class="chk">
<li><strong>“Akşam 18.00'den sonra yemek kilo yaptırır.”</strong> Belirleyici olan saat değil,
gün içindeki toplam alım ve öğün dağılımı.</li>
<li><strong>“Yağ yemek yağlandırır.”</strong> Sağlıklı yağ kaynakları planın gerekli parçasıdır;
mesele miktarda.</li>
<li><strong>“Detoks programları vücudu temizler.”</strong> Karaciğer ve böbrek bu işi zaten yapar.
Kısa süreli sıvı ağırlıklı programlarda kaybedilen çoğunlukla sıvıdır.</li>
<li><strong>“Glutensiz beslenmek zayıflatır.”</strong> Çölyak veya gluten duyarlılığı yoksa
tek başına zayıflatıcı etkisi yoktur.</li>
<li><strong>“Zayıflama iğnesi diyeti gereksiz kılar.”</strong>
{yazi_linki('zayiflama-igneleri', 'Zayıflama iğnelerini')} ayrı bir yazıda ele aldık;
beslenme düzeni kurulmadan kullanılan hiçbir yöntem kalıcı olmuyor.</li>
</ul>""")


def blok_ilk_hafta(p=None):
    return ("İlk İki Hafta Nasıl Geçiyor?", f"""
<p>İlk hafta genellikle ölçüm ve gözlem haftasıdır: mevcut düzen kaydedilir, öğün saatleri
sabitlenir ve büyük değişiklikler yapılmaz. Bu, çoğu kişinin atladığı ama süreci en çok
etkileyen aşama.</p>
<p>İkinci haftada plan devreye girer. Bu noktada beklenen şey mükemmel uygulama değil,
düzenin oturması. Danışanlarda ilk iki haftada sık görülen üç durum var: aşırı hızlı kilo
kaybı beklentisi, tek bir bozulmadan sonra pes etme eğilimi ve tartıya günlük bakma
alışkanlığı. Üçü de takip görüşmesinde ele alınıyor.</p>
<p class="note"><strong>Not:</strong> Halsizlik, baş dönmesi veya olağandışı belirtiler
ortaya çıkarsa plan beklemeden gözden geçirilmelidir. Kronik hastalığı olan veya düzenli
ilaç kullanan kişilerde süreç hekim değerlendirmesiyle birlikte yürütülür.</p>""")


def blok_hazirlik(p=None):
    return ("Diyete Başlamadan Önce Hazırlanacak Üç Şey", f"""
<ul class="chk">
<li><strong>Üç günlük beslenme kaydı.</strong> Değiştirmeden, olduğu gibi. Planın başlangıç
noktası bu kayıt.</li>
<li><strong>Güncel tahlil sonuçları.</strong> Varsa son altı aya ait sonuçlar; yoksa gerekli
görülen durumlarda istenebilir.</li>
<li><strong>Gerçekçi bir zaman aralığı.</strong> Yoğun bir sınav veya taşınma haftasında
başlamak, planın ilk günden aksamasına yol açıyor.</li>
</ul>
<p>{yazi_linki('online-diyet-nedir', 'Online diyetin nasıl işlediğini')} merak edenler için
ayrı bir yazı var.</p>""")


def blok_hata_duzeltme(p=None):
    return ("Hata Yaptığınızı Fark Ettiğinizde Ne Yapmalı?", f"""
<p>Diyette bir öğünün veya bir günün plan dışına çıkması, sürecin başarısızlığı değil.
Asıl belirleyici olan, bundan sonra ne yapıldığı. Yaygın hata, bozulan günü telafi etmek
için ertesi gün öğün atlamak veya aşırı kısıtlamaya gitmek — bu, çoğunlukla yeni bir
bozulma döngüsü başlatıyor.</p>
<p>İşe yarayan yaklaşım basit: telafi yok, bir sonraki öğünde plana dönüş var. Haftalık
düzen içinde bir öğünün ağırlığı, çoğu kişinin sandığından çok daha küçük.</p>""")


def blok_hata_takip(p=None):
    return ("Bu Hatalar Takipte Nasıl Yakalanıyor?", f"""
<p>Yukarıdaki hataların çoğu, kişi farkında olmadan sürüyor. Beslenme kaydı tutulduğunda
ise kalıp birkaç hafta içinde görünür hâle geliyor: hangi öğünün atlandığı, hangi saatte
atıştırma olduğu, sıvı tüketiminin nerede düştüğü.</p>
<p>Takip görüşmelerinin bir kısmı tam olarak bunun için ayrılıyor — plandaki maddeleri
tekrarlamak için değil, kaydın gösterdiği kalıbı birlikte okumak için.
{yazi_linki('surdurulebilir-beslenmenin-10-altin-kurali', 'Sürdürülebilir beslenmenin 10 kuralını')}
da bu çerçevede derledik.</p>""")


DIYET_BLOKLARI.update({
    "diyet_secim_kriteri": blok_diyet_secim_kriteri,
    "diyet_efsaneleri": blok_diyet_efsaneleri,
    "ilk_hafta": blok_ilk_hafta,
    "hazirlik": blok_hazirlik,
    "hata_duzeltme": blok_hata_duzeltme,
    "hata_takip": blok_hata_takip,
})
