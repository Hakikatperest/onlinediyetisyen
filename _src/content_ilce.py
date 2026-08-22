# -*- coding: utf-8 -*-
"""İlçe sayfası bölümleri — DİYET nişi.

Önceki sürümde bölümler yaşam düzeni ekseninde kurulmuştu (turizm, vardiya,
kırsal iş...). Bunlar sitenin konusu değil. Yeni eksen doğrudan diyet alt
konuları: öğün düzeni, porsiyon, ara öğün, tatlı isteği, su tüketimi, tartı
takibi, protein, mutfak hazırlığı.

Her ilçe sayfası bu alt konulardan farklı bir çiftini işler; böylece sayfalar
hem konuya sadık kalır hem birbirinin kopyası olmaz.
"""
import turkce as T
from diyet import yazi_linki


def _ad(ilce, il):
    return T.baslik(ilce), T.baslik(il)


def blok_ogun_duzeni(ilce, il, p):
    i, l = _ad(ilce, il)
    return ("Öğün Düzeni: Ne Yediğinden Önce Ne Zaman Yediğin", f"""
<p>Beslenme planında ilk düzenlenen şey genelde menü değil, saat oluyor. Öğünler arası süre
çok uzadığında bir sonraki öğünde porsiyon kendiliğinden büyüyor; çok kısaldığında ise
açlık hissi oluşmadan yeme alışkanlığı yerleşiyor.</p>
<p>{T.bulunma(i)} yaşayan danışanlarda planın ilk haftası çoğunlukla öğün saatlerini
sabitlemeye ayrılıyor. Menü değişikliği ikinci sırada geliyor, çünkü saat oturmadan yapılan
menü değişikliği kalıcı olmuyor.</p>""")


def blok_porsiyon(ilce, il, p):
    i, l = _ad(ilce, il)
    return ("Porsiyon Kontrolü Nasıl Öğrenilir?", f"""
<p>Porsiyon kontrolü tartıyla yemek tartmak demek değil. Pratikte işe yarayan yöntem,
tabak düzenini bir kez doğru kurmak: tabağın yarısı sebze, dörtte biri protein kaynağı,
dörtte biri tahıl.</p>
<p>Bu düzen bir kez oturduğunda ölçüm yapmadan da porsiyon dengesi korunabiliyor.
{T.bulunma(i)} hazırlanan planlarda da hedef, kişinin ölçü aletine bağımlı kalmadan
kendi tabağını kurabilmesi.</p>""")


def blok_ara_ogun(ilce, il, p):
    i, l = _ad(ilce, il)
    return ("Ara Öğün Gerekli mi?", f"""
<p>Ara öğün herkes için zorunlu değil. Belirleyici olan ana öğünler arasındaki sürenin
uzunluğu ve kişinin kan şekeri düzeni. Öğün arası dört saati aşıyorsa ara öğün genelde
işe yarıyor; aşmıyorsa gereksiz kalori ekleyebiliyor.</p>
<p>{T.bulunma(i)} yaşayan danışanlarda ara öğün kararı, günlük akışa bakılarak veriliyor.
{yazi_linki('protein-ihtiyaci', 'Protein ihtiyacının nasıl hesaplandığı')} ara öğün
içeriğini de doğrudan etkiliyor.</p>""")


def blok_tatli(ilce, il, p):
    i, l = _ad(ilce, il)
    return ("Tatlı İsteğiyle Nasıl Baş Edilir?", f"""
<p>Tatlı isteği planın dışında bir kaza değil; planın içinde yeri belirlenmesi gereken bir
durum. Tamamen yasaklandığında istek kaybolmuyor, erteleniyor ve genelde daha büyük bir
porsiyonla geri dönüyor.</p>
<p>Uygulamada işe yarayan yaklaşım, tatlının sıklığını ve porsiyonunu baştan belirlemek.
{T.bulunma(i)} yürütülen görüşmelerde de bu, planın bırakılma oranını düşüren
başlıklardan biri. {yazi_linki('bir-muz-diyeti-bozar-mi', 'Tek bir yiyeceğin diyeti bozup bozmadığını')}
ayrı yazıda ele aldık.</p>""")


def blok_su(ilce, il, p):
    i, l = _ad(ilce, il)
    return ("Su Tüketimi Kilo Verme Sürecini Nasıl Etkiler?", f"""
<p>Susuzluk sıklıkla açlık olarak algılanıyor. Gün içinde yeterli sıvı alınmadığında
ortaya çıkan hâlsizlik ve odaklanma güçlüğü de çoğu zaman öğün ihtiyacıyla karıştırılıyor.</p>
<p>Günlük sıvı hedefi kişiye göre belirleniyor; vücut ağırlığı, hareket düzeyi ve mevsim
etkili. {T.bulunma(i)} hazırlanan planlarda sıvı takibi, ayrı bir görev olarak değil
öğün düzeninin parçası olarak kurgulanıyor.</p>""")


def blok_tarti(ilce, il, p):
    i, l = _ad(ilce, il)
    return ("Tartı Takibi Nasıl Yapılmalı?", f"""
<p>Günlük ağırlık; sıvı dengesi, tuz tüketimi ve sindirim durumuna göre dalgalanır.
Bu yüzden her gün tartılmak gerçek değişimi göstermez, yalnızca gürültüyü gösterir.</p>
<p>Takipte kullanılan yöntem, haftada bir kez aynı gün, sabah aç karnına ve aynı tartıyla
ölçüm yapmak. {T.bulunma(i)} yürütülen takiplerde de değerlendirme tek ölçüme değil,
birkaç haftalık eğilime bakılarak yapılıyor.
{yazi_linki('kilo-veremiyorum', 'Kilo veremediğini düşünenlerde')} çoğu zaman sorun
ölçüm yönteminde çıkıyor.</p>""")


def blok_mutfak_hazirlik(ilce, il, p):
    i, l = _ad(ilce, il)
    return ("Mutfak Hazırlığı: Planı Ayakta Tutan Kısım", f"""
<p>Bir beslenme planının uygulanabilir olması, büyük ölçüde evde ne bulunduğuna bağlı.
Plan doğru olsa bile dolapta uygun seçenek yoksa, o öğün eldeki en hızlı seçenekle
kapatılıyor.</p>
<p>Bu yüzden görüşmelerin bir kısmı alışveriş listesine ve haftalık hazırlığa ayrılıyor.
{T.bulunma(i)} yaşayan danışanlarda da en belirgin fark, planın kendisinden çok
haftalık hazırlığın yapılıp yapılmadığında ortaya çıkıyor.</p>""")


def blok_hedef(ilce, il, p):
    i, l = _ad(ilce, il)
    return ("Gerçekçi Hedef Nasıl Belirlenir?", f"""
<p>Baştan fazla iddialı kurulan hedefler, ilk iki hafta içinde bırakma sebebi oluyor.
Hedefin ölçülebilir, süreye bağlı ve kişinin başlangıç durumuna uygun olması gerekiyor.</p>
<p>{T.bulunma(i)} yapılan ilk görüşmelerde hedef, kilo rakamının yanı sıra alışkanlık
üzerinden de tanımlanıyor: kaç öğün düzenli yeneceği, haftada kaç gün hareket edileceği gibi.
{yazi_linki('surdurulebilir-beslenme-nedir', 'Sürdürülebilir beslenmenin')} temel farkı burada.</p>""")


def blok_ilce_nedir(ilce, il, p):
    i, l = _ad(ilce, il)
    return ("Online Diyetisyen Görüşmesi Ne Sunuyor?", f"""
<p>Online diyetisyen görüşmesi, yüz yüze görüşmenin içeriğini uzaktan yürütür: beslenme
öyküsü alınır, hedef belirlenir, kişiye özel bir öğün planı hazırlanır ve düzenli aralıklarla
takip yapılır. {T.bulunma(i)} yaşayan bir kişi için pratik farkı, bu adımların hiçbirinin
randevu yolculuğu gerektirmemesi.</p>""")


def blok_ilce_surec(ilce, il, p):
    return ("Nasıl Başlıyor?", """
<ol class="steps">
<li><strong>İlk iletişim.</strong> Telefon veya WhatsApp ile uygun saat belirlenir.</li>
<li><strong>Ön görüşme.</strong> Günlük düzen, beslenme alışkanlıkları ve varsa tahliller konuşulur.</li>
<li><strong>Plan.</strong> Kendi mutfağınıza ve öğün saatlerinize göre plan hazırlanır.</li>
<li><strong>Takip.</strong> Düzenli görüşmelerle ilerleme değerlendirilir, plan güncellenir.</li>
</ol>""")


ILCE_BLOKLARI = {
    "ogun_duzeni": blok_ogun_duzeni, "porsiyon": blok_porsiyon, "ara_ogun": blok_ara_ogun,
    "tatli": blok_tatli, "su": blok_su, "tarti": blok_tarti,
    "mutfak_hazirlik": blok_mutfak_hazirlik, "hedef": blok_hedef,
    "nedir": blok_ilce_nedir, "surec": blok_ilce_surec,
}


def ilce_sss(ilce, il, p, tohum):
    i, l = _ad(ilce, il)
    havuz = [
        (f"{i} dışına çıkmadan diyet takibi yapılabilir mi?",
         "Evet. Görüşmeler video üzerinden yapılır; kamerası olan bir telefon veya bilgisayar yeterlidir."),
        (f"{i} için ayrı bir ücret farkı var mı?",
         "Hayır. Ücret; program süresi, görüşme sıklığı ve hizmet kapsamına göre belirlenir, "
         "yaşadığınız ilçeye göre değişmez."),
        ("Diyete başlamadan tahlil yaptırmalı mıyım?",
         "Kan şekeri, tiroit ve demir değerleri planın kurgusunu etkiler. Gerekli görülen "
         "durumlarda hekiminizden tahlil istenmesi önerilir."),
        ("Diyet listesi mi veriliyor, plan mı?",
         "Hazır liste değil, kişiye özel plan hazırlanır. Plan; tahlil değerleri, günlük düzen "
         "ve mutfak alışkanlıklarına göre kurgulanır ve takip görüşmelerinde güncellenir."),
        ("Haftada kaç kilo vermek normal?",
         "Bu kişinin başlangıç durumuna göre değişir; tek bir rakam vermek doğru olmaz. "
         "Hızlı kayıptan çok, kaybın korunabilmesi önemlidir."),
        ("Diyette spor şart mı?",
         "Beslenme düzeni tek başına da değişim sağlar. Hareket eklendiğinde süreç desteklenir "
         "ve kas kaybı riski azalır."),
        ("Öğün atlarsam daha hızlı zayıflar mıyım?",
         "Genellikle tersi olur. Atlanan öğün sonraki öğünde porsiyonu büyütür."),
        ("Diyeti bir gün bozarsam ne olur?",
         "Tek bir öğün haftalık düzeni belirlemez. Yapılacak şey baştan başlamak değil, "
         "bir sonraki öğünde plana dönmektir."),
        (f"{T.bulunma(l)} yüz yüze görüşme seçeneği var mı?",
         ("Adana Seyhan'daki ofiste yüz yüze görüşme mümkündür." if p.get("ofis_ili")
          else f"{T.bulunma(l)} fiziksel bir ofis bulunmuyor; görüşmeler uzaktan yapılıyor.")),
        ("Plan ne sıklıkla güncelleniyor?",
         "Takip görüşmelerinde ilerlemeye, mevsime ve değişen günlük düzene göre güncellenir."),
        ("Ailemle aynı yemeği yiyebilir miyim?",
         "Evet. Plan mümkün olduğunca ortak sofra üzerinden kurulur; fark porsiyonda olur."),
        ("Kilo verme duraklarsa ne yapılıyor?",
         "Duraklama sürecin beklenen aşamasıdır. Beslenme kaydı, uyku ve hareket birlikte "
         "değerlendirilir ve plan güncellenir."),
    ]
    n = len(havuz)
    sira = sorted(range(n), key=lambda k: ((tohum * 2654435761 + k * 2246822519) & 0xFFFFFFFF) ^ (k * 7))
    return [havuz[k] for k in sira[:5]]
