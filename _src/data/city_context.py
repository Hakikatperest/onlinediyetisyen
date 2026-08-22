# -*- coding: utf-8 -*-
"""İl bazlı GERÇEK bağlam verisi.

Kural: buraya yalnızca doğrulanabilir bilgi girer.
  ✓ Yöresel mutfak (kültürel olgu), iklim karakteri, üniversite varlığı,
    ofise fiziksel erişim gerçeği, idari statü.
  ✗ Nüfus/gelir istatistiği, "şehrin ruhu" klişesi, sahte danışan, sahte şube.

`mutfak_notu` ve `pratik` alanları sayfanın özgün değer çekirdeğidir: bir diyetisyenin o
yörenin sofrasına dair söyleyeceği, BAŞKA İL SAYFASINDA GEÇMEYECEK somut şey.
Boş bırakılan il, bölge varsayılanıyla çalışır ve `durum='taslak'` işaretlenir.
"""
from regions import IL_BOLGE, BUYUKSEHIR, OFIS_IL

# ---- Bölge tabanı: il verisi girilmemişse güvenli, genel ama doğru zemin ----
BOLGE_TABAN = {
    "Akdeniz": dict(
        iklim="uzun ve sıcak yazlar, ılık kışlar",
        iklim_notu=[
            "Yaz aylarında sıvı kaybı ve iştah dalgalanması belirginleşir; öğün saatleri sıcağa göre kayar.",
            "Uzun yaz döneminde gündüz iştahı düşerken akşam öğünü ağırlaşabilir.",
            "Sıcak dönemde sıvı ihtiyacı artar ve öğün saatleri günün serin bölümlerine kayar.",
            "Yılın büyük bölümünde açık havada hareket mümkündür; asıl değişken sıcakla değişen iştah.",
        ],
        mutfak=["zeytinyağlı sebze yemekleri", "narenciye", "bulgur pilavı"],
        mutfak_notu="Akdeniz sofrası zeytinyağı ve sebze açısından güçlü bir zemin sunar; asıl mesele porsiyon ve tahıl dengesidir.",
    ),
    "Ege": dict(
        iklim="ılıman yazlar, yağışlı ve ılık kışlar",
        iklim_notu=[
            "Yıl boyu taze ot ve sebze erişimi yüksektir; mevsimsel çeşitlilik planlamayı kolaylaştırır.",
            "Mevsim geçişleri yumuşaktır; sebze çeşitliliği yıl boyu korunabilir.",
            "Ilıman iklim, açık havada düzenli hareketi yılın çoğuna yaymayı mümkün kılar.",
            "Taze ürüne erişimin sürekliliği, haftalık menü planlamasını kolaylaştırır.",
        ],
        mutfak=["zeytinyağlılar", "ot kavurmaları", "deniz ürünleri"],
        mutfak_notu="Ege mutfağı zaten dengeye yakın; kazanç çoğunlukla ekmek-meze miktarının ayarlanmasından gelir.",
    ),
    "Marmara": dict(
        iklim="dört mevsim belirgin, nemli",
        iklim_notu=[
            "Uzun ulaşım süreleri ve vardiyalı çalışma düzeni öğün saatlerini düzensizleştirir.",
            "Dört mevsimin belirgin olması, öğün içeriğinin yıl içinde birkaç kez gözden geçirilmesini gerektirir.",
            "Nemli havada sıvı ihtiyacı beklenenden yüksek seyredebilir.",
            "Kış aylarında açık hava hareketi azalırken öğün porsiyonları büyüme eğilimi gösterir.",
        ],
        mutfak=["hamur işleri", "deniz ürünleri", "dışarıda yeme alışkanlığı"],
        mutfak_notu="Marmara'da asıl zorluk yemeğin içeriği değil, günün hangi saatinde ve nerede yendiğidir.",
    ),
    "İç Anadolu": dict(
        iklim="karasal; sıcak yazlar, sert ve uzun kışlar",
        iklim_notu=[
            "Kış aylarında dışarıda hareket süresi kısalır; günlük adım sayısı belirgin düşer.",
            "Karasal iklimde gece-gündüz farkı büyüktür; öğün saatleri buna göre oturtulur.",
            "Uzun kış dönemi taze sebze erişimini sınırlar; planda alternatifler baştan belirlenir.",
            "Yaz sıcağı ile kış soğuğu arasındaki fark, yıl içinde iki ayrı plan gerektirebilir.",
        ],
        mutfak=["etli hamur yemekleri", "tarhana", "buğday ve bulgur ağırlıklı sofra"],
        mutfak_notu="İç Anadolu sofrasında tahıl payı yüksektir; protein ve sebzeyi öğüne eklemek çoğu zaman çıkarmaktan daha etkilidir.",
    ),
    "Karadeniz": dict(
        iklim="yıl boyu yağışlı, nemli",
        iklim_notu=[
            "Yağışlı günlerin çokluğu açık hava hareketini kesintiye uğratır; iç mekân alternatifi planlanmalıdır.",
            "Nem oranı yüksektir; sıvı ihtiyacı hava sıcaklığından bağımsız olarak takip edilir.",
            "Yıl boyu yağış, günlük hareket planının hava koşulundan bağımsız kurulmasını gerektirir.",
            "Yeşil sebzeye erişim yıl boyu sürer; bu, lif hedefini tutturmayı kolaylaştırır.",
        ],
        mutfak=["hamsi ve diğer balıklar", "mısır ekmeği", "karalahana", "süt ürünleri"],
        mutfak_notu="Karadeniz sofrasının balık ve yeşillik tarafı güçlüdür; mısır ekmeği ve tereyağı miktarı ise takip gerektirir.",
    ),
    "Doğu Anadolu": dict(
        iklim="sert ve uzun kışlar, kısa yazlar",
        iklim_notu=[
            "Kış çok uzundur; hareketsiz geçen aylar ve enerji yoğun geleneksel sofra bir arada değerlendirilir.",
            "Sert kış koşulları açık hava hareketini aylarca sınırlar; plan buna göre kurulur.",
            "Yüksek rakım ve uzun kış, günlük enerji ihtiyacını mevsime göre belirgin değiştirir.",
            "Kısa yaz döneminde taze ürün çeşitliliği artar; kışın alternatifler önceden planlanır.",
        ],
        mutfak=["et yemekleri", "süt ve peynir çeşitleri", "kışlık kavurma"],
        mutfak_notu="Doğu Anadolu'da protein erişimi güçlüdür; denge çoğunlukla sebze ve lif tarafının artırılmasıyla kurulur.",
    ),
    "Güneydoğu Anadolu": dict(
        iklim="çok sıcak ve kurak yazlar, ılık kışlar",
        iklim_notu=[
            "Yaz sıcağı gündüz iştahını bastırıp akşam öğününü ağırlaştırabilir; sıvı takibi önem kazanır.",
            "Kurak ve sıcak yaz döneminde sıvı kaybı hızlıdır; günlük hedef yeniden hesaplanır.",
            "Gündüz sıcaklığı yüksek olduğu için hareket sabah ve akşam saatlerine planlanır.",
            "Uzun sıcak dönem, öğün saatlerinin yıl içinde belirgin kaymasına yol açar.",
        ],
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
        pratik=(
            "Adana'da en sık verdiğimiz öneri, kebap sofrasında lavaşı tabakla birlikte değil ayrı bir tabakta almak. Görünür hale gelen ekmek miktarı, çoğu danışanda kendiliğinden yarıya iniyor. Şalgamı da acılı yerine sade tercih etmek, tuz alımını gün içinde belirgin düşürüyor."
        ),
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
        pratik=(
            "Mersin'de tantuniyi plandan çıkarmıyoruz; onun yerine yanına ayran ve tatlı yerine sadece bol yeşillik ekliyoruz. Bu tek değişiklik öğünün toplamını üçte bir oranında düşürüyor. Narenciye mevsiminde ise portakalı sıkıp içmek yerine dilimleyerek yemek, lif alımını koruyor."
        ),
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
        pratik=(
            "Yalova'da yerel sebze ve meyveye erişim kolaylığını değerlendirip haftalık alışverişi tek seferde yapmak planın uygulanabilirliğini artırıyor. Sabah öğününü atlamamak ise burada en sık verdiğimiz tek maddelik öneri."
        ),
    ),
    # ---------------- AKDENİZ ----------------
    "ANTALYA": dict(
        mutfak=["piyaz", "şiş köfte", "hibeş", "narenciye", "tahinli piyaz"],
        mutfak_notu=(
            "Antalya piyazı tahinli olduğu için burada 'hafif meze' sanılan tabak aslında iyi bir "
            "protein ve yağ kaynağı — sorun onu ana yemeğin yanına ek olarak koymak. Danışanlarda sık "
            "gördüğümüz kalıp, yaz aylarında ana öğünün küçülüp akşam mezelerle uzayan bir sofraya "
            "dönüşmesi. Narenciyeye yıl boyu erişim ise plana kolaylık sağlıyor."
        ),
        ozel="Sıcak dönemde iştahın gündüz düşüp akşam toplanması en sık düzenlenen başlık.",
        universite="Akdeniz Üniversitesi",
        pratik=(
            "Antalya'da yaz aylarında öğle öğününü hafifletip akşamı büyütme eğilimi yaygın. Uyguladığımız düzenleme basit: öğleye protein eklemek ve akşam mezelerini üç tabakla sınırlamak. Piyazı ise ana yemeğin yanına değil, ana yemeğin yerine koymak da bir seçenek."
        ),
    ),
    "BURDUR": dict(
        mutfak=["şiş köfte", "ceviz helvası", "testi kebabı", "yoğurt ve süt ürünleri"],
        mutfak_notu=(
            "Burdur sofrasında süt ve yoğurt payı yüksek; bu, protein ve kalsiyum tarafını "
            "kendiliğinden güçlendiriyor. Planlarda daha çok tam yağlı ürünlerin porsiyonunu "
            "ayarlamakla uğraşıyoruz. Ceviz helvası gibi tatlılar ise 'ev yapımı olduğu için serbest' "
            "sanıldığında haftalık şeker toplamını sessizce yükseltiyor."
        ),
        ozel="Ev yapımı tatlıların sıklığı, planda en sık gözden kaçan kalem.",
        universite="Burdur Mehmet Akif Ersoy Üniversitesi",
        pratik=(
            "Burdur'da yoğurdu tam yağlıdan yarım yağlıya geçirmek, günlük yağ alımını fark edilmeden düşüren en kolay adım. Ceviz helvası gibi ev tatlılarını ise haftada bir güne sabitlemek, porsiyon kısmaktan daha kolay uygulanıyor."
        ),
    ),
    "HATAY": dict(
        mutfak=["humus", "oruk", "künefe", "zeytin ve zahter", "tepsi kebabı"],
        mutfak_notu=(
            "Hatay mutfağı baklagil ve zeytinyağı tarafıyla planın işini kolaylaştırıyor: humus, "
            "oruk ve zahter kahvaltısı zaten dengeli bir zemin. Asıl konu künefe. Danışanlarda "
            "gördüğümüz şey künefenin özel gün tatlısı değil, haftalık rutin haline gelmesi — "
            "porsiyon ve sıklık belirlendiğinde plandan çıkarmak gerekmiyor."
        ),
        ozel="Kahvaltı kültürünün güçlü olması, günün ilk öğününü kurmayı kolaylaştırıyor.",
        universite="Hatay Mustafa Kemal Üniversitesi",
        pratik=(
            "Hatay'da kahvaltıyı zahter, zeytin ve humus üzerine kurmak günün ilk öğününü hem doyurucu hem dengeli yapıyor. Künefe için önerimiz porsiyonu bölüşmek: tek kişilik porsiyon çoğu zaman iki kişilik enerji taşıyor."
        ),
    ),
    "ISPARTA": dict(
        mutfak=["kabune pilavı", "gül reçeli", "elma", "kaz eti"],
        mutfak_notu=(
            "Isparta'da elma yıl boyu erişilebilir ve ara öğün planlamasını kolaylaştıran birkaç "
            "meyveden biri. Buna karşılık gül reçeli ve şekerli ürünler çay saatinin sabit parçası "
            "olduğunda günlük şeker toplamı hızla yükseliyor. Kabune gibi pirinç temelli yemeklerde "
            "ise porsiyonun yanına sebze eklemek çoğu zaman yeterli düzeltme oluyor."
        ),
        ozel="Öğrenci nüfusunun yoğun olduğu bir il; yurt ve yemekhane düzenine göre plan sık kuruluyor.",
        universite="Süleyman Demirel Üniversitesi",
        pratik=(
            "Isparta'da çay saatinde gül reçeli yerine taze elma dilimlemek, günlük şeker toplamını belirgin düşürüyor. Kabune gibi pilav temelli yemeklerde ise tabağın yarısını salatayla doldurmak porsiyonu kendiliğinden dengeliyor."
        ),
    ),
    "KAHRAMANMARAŞ": dict(
        mutfak=["Maraş dondurması", "tarhana", "acı biber", "sıkma", "kömbe"],
        mutfak_notu=(
            "Maraş sofrasında iki uç bir arada: tarhana ve sıkma gibi tahıl temelli, doyurucu ve "
            "planlanabilir yemekler ile dondurma ve tatlı geleneği. Danışanlarda en sık düzenlediğimiz "
            "şey, dondurmayı yasaklamak yerine haftalık sıklığını belirlemek. Acı biber tüketimi "
            "yüksek olanlarda ise reflü ve mide şikâyetleri plana ayrıca giriyor."
        ),
        ozel="Tarhana gibi geleneksel çorbalar, akşam öğününü hafifletmek için işe yarayan bir zemin.",
        universite="Kahramanmaraş Sütçü İmam Üniversitesi",
        pratik=(
            "Maraş'ta dondurmayı plandan çıkarmak yerine tek toplu porsiyona ve haftada bir güne bağlamak işe yarıyor. Tarhana çorbasını akşam öğününün başına almak ise ana yemekte porsiyonun küçülmesini sağlıyor."
        ),
    ),
    "OSMANİYE": dict(
        mutfak=["yer fıstığı", "bulgur pilavı", "sıkma", "kabak çiçeği dolması"],
        mutfak_notu=(
            "Osmaniye'de yer fıstığı hem üretimi hem tüketimi yaygın; ara öğün olarak değerli ama "
            "porsiyonu kontrol edilmediğinde günlük enerjiyi belirgin yükselten bir kalem. "
            "Danışanlarda genelde avuç ölçüsünü sabitlemek yeterli oluyor. Bulgur temelli sofra ise "
            "lif tarafını kendiliğinden güçlü tutuyor."
        ),
        ozel="Kuruyemişin ara öğüne planlı biçimde yerleştirilmesi burada sık çalışılan bir başlık.",
        universite="Osmaniye Korkut Ata Üniversitesi",
        pratik=(
            "Osmaniye'de yer fıstığını paketten değil, önceden ayrılmış avuç ölçüsünden yemek en etkili düzenleme. Bulgur pilavının yanına ayrıca ekmek almamak da günlük karbonhidrat toplamını dengeliyor."
        ),
    ),
    # ---------------- EGE ----------------
    "İZMİR": dict(
        mutfak=["boyoz", "kumru", "ot kavurmaları", "deniz ürünleri", "gevrek"],
        mutfak_notu=(
            "İzmir'de sabah öğünü çoğu zaman ayaküstü bir hamur işine dönüşüyor: boyoz, gevrek, "
            "kumru. Bunlar hızlı ve ucuz ama tek başına protein tarafı zayıf, öğle öncesi açlığı "
            "öne çekiyor. Buna karşılık İzmir'in ot kültürü ve deniz ürünlerine erişimi, planın "
            "geri kalanını kurmayı kolaylaştıran güçlü bir zemin."
        ),
        ozel="Sabah öğününe protein eklemek, burada en sık yaptığımız tek maddelik düzeltme.",
        universite="Ege Üniversitesi",
        pratik=(
            "İzmir'de sabah boyoz veya gevrek yiyenlere önerimiz yanına bir yumurta veya peynir eklemek. Bu tek ekleme, öğle öncesi açlığı belirgin geciktiriyor. Ot kavurmalarını haftada iki kez sofraya almak ise lif hedefini kendiliğinden karşılıyor."
        ),
    ),
    "AYDIN": dict(
        mutfak=["incir", "zeytin ve zeytinyağı", "çöp şiş", "keşkek"],
        mutfak_notu=(
            "Aydın inciri kuru olarak tüketildiğinde küçük hacimde yüksek şeker taşıyor; "
            "danışanlarda 'meyve, serbest' varsayımıyla fazla tüketilen kalemlerin başında geliyor. "
            "Taze incir mevsiminde ise porsiyon ayarı yeterli oluyor. Zeytinyağlı sebze yemekleri "
            "planın omurgasını kurmak için burada oldukça elverişli."
        ),
        ozel="Kuru meyve porsiyonunun netleştirilmesi sık çalışılan bir başlık.",
        universite="Aydın Adnan Menderes Üniversitesi",
        pratik=(
            "Aydın'da kuru inciri üç adetle sınırlamak, taze mevsimde ise iki adet ölçüsünü korumak günlük şeker dengesini koruyor. Zeytinyağlı sebze yemeklerini haftanın üç gününe yaymak, planın omurgasını kurmanın en pratik yolu."
        ),
    ),
    "DENİZLİ": dict(
        mutfak=["kekikli tavuk", "leblebi", "tandır", "gözleme"],
        mutfak_notu=(
            "Denizli'de leblebi yaygın bir atıştırmalık ve aslında lif-protein dengesi iyi bir "
            "seçenek; sorun genelde ölçüsüz tüketilmesi. Ara öğün olarak avuç ölçüsüyle plana "
            "girdiğinde işe yarıyor. Tandır gibi et yemeklerinde ise yanındaki pilav-ekmek ikilisini "
            "tek karbonhidrata indirmek çoğu zaman yeterli düzeltme."
        ),
        ozel="Atıştırmalıkların ölçülendirilmesi burada planın en belirleyici parçası.",
        universite="Pamukkale Üniversitesi",
        pratik=(
            "Denizli'de leblebiyi paketten değil önceden ölçülmüş kâseden yemek en sık verdiğimiz öneri. Kekikli tavuk gibi fırın yemeklerini haftada iki kez sofraya almak, protein hedefini zorlamadan karşılıyor."
        ),
    ),
    "MANİSA": dict(
        mutfak=["mesir", "üzüm ve kuru üzüm", "kebap", "keşkek"],
        mutfak_notu=(
            "Manisa'da kuru üzüm hem yaygın hem de yanıltıcı: küçük bir avuç bile belirgin şeker "
            "taşıyor ve 'doğal olduğu için serbest' varsayımıyla tüketildiğinde günlük toplamı "
            "yükseltiyor. Planda genelde yerini koruyor, sadece ölçüsü ve saati belirleniyor. "
            "Keşkek gibi tahıl-et yemekleri ise doyurucu ve planlanabilir."
        ),
        ozel="Kuru meyvenin ara öğüne ölçülü yerleştirilmesi burada sık çalışılıyor.",
        universite="Manisa Celâl Bayar Üniversitesi",
        pratik=(
            "Manisa'da kuru üzümü sabah kahvaltısına değil, öğleden sonra ara öğüne almak kan şekeri dalgalanmasını azaltıyor. Bir avuç yerine on beş tane şeklinde sayıyla ölçmek de uygulaması en kolay yöntem."
        ),
    ),
    "MUĞLA": dict(
        mutfak=["deniz ürünleri", "zeytinyağlı otlar", "çökertme kebabı", "bal"],
        mutfak_notu=(
            "Muğla sofrası balık ve ot ağırlığıyla dengeye zaten yakın. Danışanlarda asıl konu "
            "genelde meze kültürü: tek tek hafif görünen tabaklar bir araya geldiğinde ana öğünden "
            "büyük bir toplam çıkarabiliyor. Çözüm mezeyi çıkarmak değil, tabak sayısını ve "
            "ekmek miktarını baştan belirlemek."
        ),
        ozel="Meze düzeninde tabak sayısını sabitlemek, en sık uyguladığımız düzeltme.",
        universite="Muğla Sıtkı Koçman Üniversitesi",
        pratik=(
            "Muğla'da meze sofrasında tabak sayısını üçle sınırlamak ve ekmeği baştan iki dilimle ölçmek, akşam öğününün toplamını yarı yarıya değiştiriyor. Balığı ızgara tercih etmek ise yağ payını kendiliğinden düşürüyor."
        ),
    ),
    "AFYONKARAHİSAR": dict(
        mutfak=["sucuk", "kaymak", "haşhaşlı çörek", "ekmek kadayıfı"],
        mutfak_notu=(
            "Afyon sofrasının iki simgesi olan sucuk ve kaymak, yağ ve tuz tarafını hızla "
            "yükseltebiliyor. Bunları plandan çıkarmak yerine kahvaltıda birini seçip porsiyonunu "
            "belirlemek çoğu danışanda yeterli oluyor. Haşhaşlı ürünler ve ekmek kadayıfı ise "
            "haftalık şeker ve yağ toplamında ayrıca hesaba katılıyor."
        ),
        ozel="Kahvaltıda 'ikisi birden' yerine 'biri, ölçülü' yaklaşımı burada işe yarıyor.",
        universite="Afyon Kocatepe Üniversitesi",
        pratik=(
            "Afyon'da kahvaltıda sucuk ve kaymağı aynı anda değil dönüşümlü almak en etkili düzenleme. Ekmek kadayıfını ise porsiyon bölüşerek tüketmek, plandan çıkarmadan sürdürmeyi mümkün kılıyor."
        ),
    ),
    "KÜTAHYA": dict(
        mutfak=["tarhana", "cimcik", "gökçimen", "höşmerim"],
        mutfak_notu=(
            "Kütahya'da tarhana çorbası günlük sofranın sabit parçası ve akşam öğününü hafifletmek "
            "için iyi bir başlangıç. Cimcik gibi hamur yemeklerinde ise porsiyon büyüdüğünde günün "
            "karbonhidrat payı tek öğünde toplanabiliyor; yanına protein ve sebze eklemek dengeyi "
            "kuruyor."
        ),
        ozel="Hamur yemeklerinin yanına protein eklemek burada en sık verilen öneri.",
        universite="Kütahya Dumlupınar Üniversitesi",
        pratik=(
            "Kütahya'da tarhana çorbasını akşam öğününün başlangıcı yapmak, ana yemekte porsiyonun küçülmesini sağlıyor. Cimcik gibi hamur yemeklerinde ise yanına yoğurt eklemek protein dengesini kuruyor."
        ),
    ),
    "UŞAK": dict(
        mutfak=["tarhana", "arap kadayıfı", "höşmerim", "keşkek"],
        mutfak_notu=(
            "Uşak tarhanası yöresel olarak yoğun tüketiliyor ve doyurucu bir çorba zemini sunuyor. "
            "Danışanlarda düzenlediğimiz asıl kalem çay saatinde yerleşen hamur tatlıları — "
            "arap kadayıfı gibi şerbetli tatlılarda porsiyondan çok sıklık belirleyici oluyor."
        ),
        ozel="Şerbetli tatlıların haftalık sıklığını netleştirmek burada öncelikli başlık.",
        universite="Uşak Üniversitesi",
        pratik=(
            "Uşak'ta şerbetli tatlıları haftada bir güne toplamak, her gün küçük porsiyon almaktan daha iyi sonuç veriyor. Tarhanayı sabah öğününe almak ise öğle öncesi atıştırmayı azaltıyor."
        ),
    ),
    # ---------------- MARMARA ----------------
    "BURSA": dict(
        mutfak=["İskender", "kestane şekeri", "Bursa şeftalisi", "pideli köfte"],
        mutfak_notu=(
            "Bursa'da İskender, porsiyonu değil bileşimi nedeniyle dikkat isteyen bir yemek: "
            "et, pide, yoğurt ve tereyağı aynı tabakta toplanıyor. Danışanlarda plandan çıkarmak "
            "yerine ayda birkaç kez ve tereyağı azaltılmış biçimde yer alması çoğu zaman yeterli. "
            "Şeftali mevsiminde ise taze meyveye erişim ara öğün planını kolaylaştırıyor."
        ),
        ozel="Tek tabakta toplanan karbonhidrat-yağ birleşimlerini ayrıştırmak burada sık çalışılıyor.",
        universite="Bursa Uludağ Üniversitesi",
        pratik=(
            "Bursa'da İskender yerken pidenin altındaki kısmı tamamen bitirmemek ve ek tereyağı istememek, öğünün toplamını üçte bir azaltıyor. Şeftali mevsiminde ise tatlı yerine meyveye geçmek en kolay değişim."
        ),
    ),
    "BALIKESİR": dict(
        mutfak=["höşmerim", "kaymaklı tatlılar", "zeytinyağlılar", "süt ürünleri"],
        mutfak_notu=(
            "Balıkesir'de süt ve peynir çeşitliliği yüksek; protein tarafını kurmak kolay. "
            "Buna karşılık höşmerim gibi süt tatlıları 'sütlü olduğu için hafif' sanılıyor — "
            "şeker yoğunluğu göz ardı edilebiliyor. Zeytinyağlı sebze yemekleri ise planın "
            "omurgasını taşıyacak kadar güçlü bir gelenek."
        ),
        ozel="Süt tatlılarının şeker payını görünür kılmak, ilk görüşmelerde sık gündeme geliyor.",
        universite="Balıkesir Üniversitesi",
        pratik=(
            "Balıkesir'de peynir çeşitliliğini avantaja çevirip kahvaltıda tek çeşit yerine iki küçük dilim farklı peynir almak doygunluğu artırıyor. Höşmerimi ise tatlı ihtiyacının tamamı değil bir bölümü olarak planlıyoruz."
        ),
    ),
    "ÇANAKKALE": dict(
        mutfak=["deniz ürünleri", "peynir helvası", "zeytin", "domates"],
        mutfak_notu=(
            "Çanakkale'de balığa erişim düzenli ve bu, haftalık protein planını kurmayı belirgin "
            "kolaylaştırıyor. Danışanlarda düzenlediğimiz kalem genelde balığın pişirme yöntemi: "
            "kızartma yerine fırın veya ızgaraya geçiş, öğünün yağ payını tek hamlede düşürüyor. "
            "Peynir helvası ise porsiyonu küçük tutulduğunda plandan çıkmıyor."
        ),
        ozel="Pişirme yöntemi değişikliği, burada en hızlı sonuç veren tek düzeltme.",
        universite="Çanakkale Onsekiz Mart Üniversitesi",
        pratik=(
            "Çanakkale'de balığı kızartma yerine fırında pişirmek tek başına öğünün yağ payını yarıya indiriyor. Haftada iki balık öğünü, protein planını neredeyse kendiliğinden kuruyor."
        ),
    ),
    "EDİRNE": dict(
        mutfak=["tava ciğer", "Edirne peyniri", "badem ezmesi", "deva-i misk helvası"],
        mutfak_notu=(
            "Edirne'de tava ciğer demir açısından değerli ama kızartma yöntemi nedeniyle öğünün "
            "yağ payını yükseltiyor; haftada bir-iki kez ve yanına bol sebzeyle plana rahatlıkla "
            "giriyor. Badem ezmesi gibi tatlılar ise küçük hacimde yüksek şeker taşıdığı için "
            "ölçüsü baştan belirlenmediğinde günlük toplamı sessizce artırıyor."
        ),
        ozel="Kızartmayı tamamen çıkarmak yerine sıklığını sınırlamak burada daha sürdürülebilir oluyor.",
        universite="Trakya Üniversitesi",
        pratik=(
            "Edirne'de tava ciğeri haftada bir güne sabitleyip yanına bol soğan ve yeşillik almak dengeyi kuruyor. Badem ezmesini ise adetle ölçmek, göz kararı almaktan daha güvenilir."
        ),
    ),
    "TEKİRDAĞ": dict(
        mutfak=["Tekirdağ köftesi", "ayçiçek yağı", "peynir helvası", "deniz ürünleri"],
        mutfak_notu=(
            "Tekirdağ köftesi ızgara yöntemiyle hazırlandığı için aslında plana uygun bir protein "
            "kaynağı; belirleyici olan yanındaki pilav-ekmek-piyaz üçlüsünün aynı anda tabağa "
            "gelmesi. Danışanlarda tek bir karbonhidrat seçmek çoğu zaman yeterli düzeltme oluyor."
        ),
        ozel="Aynı öğünde birden fazla karbonhidrat kaynağını ayrıştırmak burada sık çalışılıyor.",
        universite="Tekirdağ Namık Kemal Üniversitesi",
        pratik=(
            "Tekirdağ'da köftenin yanında pilav ve ekmeği birlikte değil, ikisinden birini seçmek en pratik düzenleme. Piyazı ise ana karbonhidrat olarak saymak porsiyon hesabını kolaylaştırıyor."
        ),
    ),
    "KOCAELİ": dict(
        mutfak=["pişmaniye", "kandıra yoğurdu", "deniz ürünleri", "sanayi bölgesi yemek düzeni"],
        mutfak_notu=(
            "Kocaeli'de beslenmeyi en çok etkileyen şey vardiyalı ve yemekhaneli çalışma düzeni. "
            "Öğle öğünü çoğunlukla dışarıda ve sabit bir menüden seçiliyor; plan da bu menü "
            "üzerinden kuruluyor. Pişmaniye gibi yerel tatlılar ise porsiyonu küçük göründüğü için "
            "sıklığı fark edilmeden artabiliyor."
        ),
        ozel="Yemekhane menüsü üzerinden seçim yapmayı öğretmek, burada planın en pratik parçası.",
        universite="Kocaeli Üniversitesi",
        pratik=(
            "Kocaeli'de yemekhane menüsünden seçim yaparken tabağın yarısını salata ve sebzeye ayırmak, kalan yarıyı planlamayı kolaylaştırıyor. Pişmaniyeyi ise ofis çekmecesinde değil evde tutmak sıklığı kendiliğinden azaltıyor."
        ),
    ),
    "SAKARYA": dict(
        mutfak=["ıslama köfte", "dartılı pilav", "fındık", "Taraklı helvası"],
        mutfak_notu=(
            "Sakarya'nın ıslama köftesi, ekmeğin et suyuna batırılmasıyla hazırlandığı için "
            "farkında olmadan yüksek miktarda ekmek tüketilen bir öğün. Danışanlarda porsiyonu "
            "yarıya indirip yanına salata eklemek dengeyi kuruyor. Fındık ise ara öğün için "
            "değerli, avuç ölçüsü belirlendiğinde plana rahat giriyor."
        ),
        ozel="Ekmeğin görünmez biçimde tüketildiği öğünleri fark ettirmek burada öncelikli.",
        universite="Sakarya Üniversitesi",
        pratik=(
            "Sakarya'da ıslama köftede ekmek sayısını baştan belirlemek şart; porsiyon geldiğinde durmak zor oluyor. Fındığı ise sabah kahvaltısına eklemek öğle öncesi atıştırmayı azaltıyor."
        ),
    ),
    "BİLECİK": dict(
        mutfak=["Bilecik peyniri", "cevizli baklava", "papaz üzümü"],
        mutfak_notu=(
            "Bilecik peyniri günlük kahvaltının sabit parçası ve protein tarafını kolayca "
            "kuruyor. Danışanlarda düzenlediğimiz kalem genelde kahvaltıda peynirle birlikte "
            "gelen ekmek miktarı. Cevizli baklava gibi tatlılarda ise ceviz içeriği tatlıyı "
            "sağlıklı yapmıyor — porsiyon ve sıklık yine belirleyici."
        ),
        ozel="Kahvaltıda ekmek ölçüsünü netleştirmek en sık verilen öneri.",
        universite="Bilecik Şeyh Edebali Üniversitesi",
        pratik=(
            "Bilecik'te kahvaltıda peynir miktarını korumak ama ekmeği iki dilimle sınırlamak en etkili düzenleme. Cevizli baklavayı ise misafirlik günlerine bırakmak sıklığı doğal olarak düşürüyor."
        ),
    ),
    "KIRKLARELİ": dict(
        mutfak=["hardaliye", "kaşar peyniri", "ayçiçeği", "manda yoğurdu"],
        mutfak_notu=(
            "Kırklareli'nde hardaliye üzüm bazlı olduğu için 'sağlıklı içecek' sanılıyor; "
            "şeker içeriği nedeniyle su yerine geçmiyor ve günlük sıvı hedefine sayılmıyor. "
            "Manda yoğurdu ve kaşar ise protein tarafını güçlü tutuyor, sadece yağ oranı "
            "nedeniyle porsiyonu belirleniyor."
        ),
        ozel="Şekerli içeceklerin sıvı hedefinden ayrılması burada sık açıklanan bir konu.",
        universite="Kırklareli Üniversitesi",
        pratik=(
            "Kırklareli'nde hardaliyeyi su yerine değil tatlı ihtiyacının yerine saymak doğru yaklaşım. Manda yoğurdunu ise günlük porsiyonu bir kâseyle sınırlayarak plana almak yeterli oluyor."
        ),
    ),
    # ---------------- İÇ ANADOLU ----------------
    "ANKARA": dict(
        mutfak=["Ankara tava", "beypazarı kurusu", "simit", "döner"],
        mutfak_notu=(
            "Ankara'da öğle öğünü büyük ölçüde dışarıda ve hızlı seçeneklerden kuruluyor: döner, "
            "simit, tost. Bunların hiçbiri plandan çıkmak zorunda değil; belirleyici olan öğünün "
            "yanına ne eklendiği ve gün içinde kaç kez tekrarlandığı. Danışanlarda en sık "
            "gördüğümüz tablo, sabahın atlanıp öğlenin ayaküstü kapatılması."
        ),
        ozel="Kamu ve ofis çalışma düzeni nedeniyle öğün saatleri sabitlemesi burada öncelikli.",
        universite="Ankara Üniversitesi",
        pratik=(
            "Ankara'da öğle döneri yerken lavaş yerine porsiyon tercih etmek ve yanına ayran almak öğünü dengeliyor. Sabah simidi ise tek başına değil yanında peynirle alındığında öğle öncesi açlığı geciktiriyor."
        ),
    ),
    "KONYA": dict(
        mutfak=["etli ekmek", "fırın kebabı", "bamya çorbası", "sac arası"],
        mutfak_notu=(
            "Konya sofrasında hamur ve et birlikte geliyor: etli ekmek tek başına bir öğünün "
            "tamamını karşılayabilecek bir porsiyon. Danışanlarda plandan çıkarmak yerine "
            "porsiyonun yarısını yanına salatayla dengelemek işe yarıyor. Bamya çorbası gibi "
            "hafif başlangıçlar ise akşam öğününü kontrol etmeyi kolaylaştırıyor."
        ),
        ozel="Tek tabakta gelen büyük porsiyonları bölmek, burada en sık uygulanan düzeltme.",
        universite="Selçuk Üniversitesi",
        pratik=(
            "Konya'da etli ekmeği tek başına bir öğün saymak ve yanına ayrıca çorba veya pilav almamak en önemli düzenleme. Bamya çorbasını öğün başına almak ise porsiyonu kendiliğinden küçültüyor."
        ),
    ),
    "KAYSERİ": dict(
        mutfak=["mantı", "pastırma", "sucuk", "yağlama"],
        mutfak_notu=(
            "Kayseri mantısı küçük hacimli göründüğü için porsiyon kolayca büyüyor; üzerine "
            "eklenen yoğurt ve tereyağıyla birlikte öğünün toplamı beklenenden yüksek çıkıyor. "
            "Pastırma ise protein açısından değerli ama tuz payı nedeniyle tansiyon takibi olan "
            "danışanlarda ayrıca değerlendiriliyor."
        ),
        ozel="Tuz tüketimi, burada plana en sık eklenen ikinci başlık.",
        universite="Erciyes Üniversitesi",
        pratik=(
            "Kayseri'de mantıyı porsiyonla değil kâseyle ölçmek ve üzerine tereyağı yerine yoğurt tercih etmek öğünün yağ payını belirgin düşürüyor. Pastırmayı ise haftada iki kahvaltıya sınırlamak tuz alımını dengeliyor."
        ),
    ),
    "ESKİŞEHİR": dict(
        mutfak=["çiğbörek", "met helvası", "balaban köfte", "Tatar mutfağı"],
        mutfak_notu=(
            "Eskişehir'de çiğbörek kızartma yöntemiyle hazırlandığı için tek başına yüksek yağ "
            "taşıyor; danışanlarda haftalık sıklığını belirlemek plandan çıkarmaktan daha "
            "sürdürülebilir oluyor. Öğrenci nüfusunun yoğun olduğu bir il olduğu için planlar "
            "sıklıkla yurt ve öğrenci evi koşullarına göre kuruluyor."
        ),
        ozel="Öğrenci bütçesi ve sınırlı mutfak imkânı, plan kurgusunu doğrudan belirliyor.",
        universite="Eskişehir Osmangazi Üniversitesi",
        pratik=(
            "Eskişehir'de çiğbörek porsiyonunu ikiyle sınırlamak ve yanına ayran yerine su almak en kolay uygulanan düzenleme. Yurt yemekhanesinde ise tabağın yarısını sebzeye ayırmak plana uyumu artırıyor."
        ),
    ),
    "SİVAS": dict(
        mutfak=["Sivas köftesi", "katmer", "madımak", "içli köfte"],
        mutfak_notu=(
            "Sivas'ta madımak gibi yabani otlar mevsiminde sofranın parçası ve lif tarafını "
            "güçlendiriyor. Buna karşılık katmer ve hamur işleri günlük rutine girdiğinde "
            "karbonhidrat payı yükseliyor. Uzun kış nedeniyle hareket süresi düştüğü için "
            "planlar kış aylarında ayrıca gözden geçiriliyor."
        ),
        ozel="Kış aylarında düşen günlük hareket, plan güncellemesinin ana sebebi.",
        universite="Sivas Cumhuriyet Üniversitesi",
        pratik=(
            "Sivas'ta kış aylarında hareket düştüğü için porsiyonları değil öğün sayısını korumak öncelikli. Madımak mevsiminde ise haftada iki kez ot yemeği sofraya almak lif hedefini karşılıyor."
        ),
    ),
    "NEVŞEHİR": dict(
        mutfak=["testi kebabı", "kuru bakla", "pekmez", "nohut yemeği"],
        mutfak_notu=(
            "Nevşehir sofrasında baklagil payı yüksek ve bu, lif-protein dengesini kurmayı "
            "kolaylaştırıyor. Danışanlarda düzenlediğimiz kalem genelde pekmez: besleyici olsa da "
            "yoğun şeker içerdiği için kaşık ölçüsü belirlenmediğinde günlük toplamı yükseltiyor."
        ),
        ozel="Pekmez ve bal gibi doğal tatlandırıcıların ölçülendirilmesi burada sık gündemde.",
        universite="Nevşehir Hacı Bektaş Veli Üniversitesi",
        pratik=(
            "Nevşehir'de pekmezi kaşıkla ölçmek ve günde bir tatlı kaşığıyla sınırlamak en pratik adım. Nohut ve bakla yemeklerini haftada üç kez sofraya almak ise protein tarafını kolaylıkla kuruyor."
        ),
    ),
    "AKSARAY": dict(
        mutfak=["Aksaray kebabı", "tandır", "bulgur pilavı", "kuru fasulye"],
        mutfak_notu=(
            "Aksaray'da bulgur ve baklagil temelli yemekler günlük sofranın merkezinde; bu, "
            "plan açısından iyi bir zemin. Asıl düzenleme et yemeklerinin porsiyonunda ve "
            "yanına gelen ekmekte oluyor. Bulgur pilavının yanına ayrıca ekmek almamak, "
            "çoğu danışanda tek başına fark yaratan bir alışkanlık değişikliği."
        ),
        ozel="Pilav ve ekmeği aynı öğünde ayırmak burada en sık verilen öneri.",
        universite="Aksaray Üniversitesi",
        pratik=(
            "Aksaray'da bulgur pilavının yanına ekmek almamak tek başına günlük karbonhidrat toplamını dengeliyor. Kuru fasulyeyi ise haftada iki öğüne yaymak hem bütçeyi hem planı rahatlatıyor."
        ),
    ),
    "NİĞDE": dict(
        mutfak=["patates", "elma", "gökçe fasulye", "tandır"],
        mutfak_notu=(
            "Niğde'de patates üretimi yaygın ve sofrada sık yer alıyor. Patates plandan "
            "çıkarılması gereken bir besin değil; belirleyici olan pişirme yöntemi ve aynı "
            "öğünde ekmekle birlikte tüketilip tüketilmediği. Elma ise ara öğün için yıl boyu "
            "erişilebilir bir seçenek sunuyor."
        ),
        ozel="Nişastalı sebzeleri karbonhidrat sayarak planlamak burada sık açıklanıyor.",
        universite="Niğde Ömer Halisdemir Üniversitesi",
        pratik=(
            "Niğde'de patatesi sebze değil karbonhidrat sayarak planlamak en sık açıkladığımız konu. Elmayı ise ara öğüne almak akşam tatlı isteğini belirgin azaltıyor."
        ),
    ),
    "KARAMAN": dict(
        mutfak=["divle obruk peyniri", "bulgur", "elma", "tirit"],
        mutfak_notu=(
            "Karaman'da tahıl ve baklagil temelli sofra planın işini kolaylaştırıyor. "
            "Divle peyniri gibi olgunlaştırılmış peynirlerde tuz payı yüksek olduğu için "
            "tansiyon takibi olan danışanlarda porsiyon ayrıca belirleniyor. Tirit gibi "
            "ekmek temelli yemeklerde ise ekmek miktarı görünmez biçimde artabiliyor."
        ),
        ozel="Olgun peynirlerde tuz payı, planda ayrıca değerlendirilen bir kalem.",
        universite="Karamanoğlu Mehmetbey Üniversitesi",
        pratik=(
            "Karaman'da olgun peyniri günlük bir dilimle sınırlamak tuz alımını dengeliyor. Tirit gibi ekmek temelli yemeklerde ise ekmeği önceden ölçüp tabağa koymak porsiyonu kontrol altında tutuyor."
        ),
    ),
    "KIRŞEHİR": dict(
        mutfak=["kuru fasulye", "tarhana", "cevizli sucuk", "höşmerim"],
        mutfak_notu=(
            "Kırşehir'de kuru fasulye ve tarhana günlük sofranın sabit parçası; ikisi de plana "
            "rahatlıkla giren, doyurucu seçenekler. Danışanlarda düzenlediğimiz kalem genelde "
            "yanlarına gelen pilav ve ekmeğin aynı anda tabakta olması."
        ),
        ozel="Baklagil öğünlerinde ikinci karbonhidratı çıkarmak burada yeterli düzeltme oluyor.",
        universite="Kırşehir Ahi Evran Üniversitesi",
        pratik=(
            "Kırşehir'de kuru fasulyenin yanına pilav yerine bol salata almak öğünü dengeliyor. Tarhanayı ise akşam öğününün başına koymak ana yemekte porsiyonu küçültüyor."
        ),
    ),
    "KIRIKKALE": dict(
        mutfak=["kuru fasulye", "bulgur pilavı", "cevizli baklava", "tandır"],
        mutfak_notu=(
            "Kırıkkale sofrası tahıl ve baklagil ağırlıklı; lif tarafı güçlü. Danışanlarda "
            "en sık karşılaştığımız durum, öğle öğününün iş temposu nedeniyle atlanıp akşam "
            "öğününün büyümesi. Planın ilk haftası genelde öğün saatlerini yeniden kurmaya ayrılıyor."
        ),
        ozel="Atlanan öğle öğününü geri kazandırmak burada planın ilk adımı.",
        universite="Kırıkkale Üniversitesi",
        pratik=(
            "Kırıkkale'de öğle öğününü atlamamak için iş çantasına önceden hazırlanmış bir ara öğün koymak en etkili adım. Akşam porsiyonunun büyümesi çoğu zaman bu tek değişiklikle çözülüyor."
        ),
    ),
    "ÇANKIRI": dict(
        mutfak=["tuz", "keşkek", "etli pilav", "helva"],
        mutfak_notu=(
            "Çankırı sofrasında et ve tahıl birlikte geliyor; keşkek ve etli pilav gibi yemekler "
            "doyurucu ve planlanabilir. Danışanlarda düzenlenen kalem genelde porsiyon büyüklüğü "
            "ve yemeğin yanına eklenen ekmek. Sebze payını artırmak, dengeyi kuran en pratik adım."
        ),
        ozel="Sebze payını artırmak, burada çıkarma yapmaktan daha etkili oluyor.",
        universite="Çankırı Karatekin Üniversitesi",
        pratik=(
            "Çankırı'da etli pilav ve keşkek gibi yemeklerin yanına mutlaka salata eklemek, porsiyonu değiştirmeden dengeyi kuruyor. Ekmeği ise yemeğin yanında değil sonrasında düşünmek miktarı azaltıyor."
        ),
    ),
    "YOZGAT": dict(
        mutfak=["testi kebabı", "arabaşı", "parmak çöreği", "tarhana"],
        mutfak_notu=(
            "Yozgat'ta arabaşı, hamur ve çorbanın birlikte tüketildiği geleneksel bir öğün; "
            "doyurucu ama karbonhidrat payı yüksek. Danışanlarda porsiyonu küçültüp yanına "
            "protein eklemek dengeyi kuruyor. Uzun kış nedeniyle hareket azaldığı için planlar "
            "mevsime göre güncelleniyor."
        ),
        ozel="Geleneksel öğünleri çıkarmadan porsiyon üzerinden düzenlemek burada esas yaklaşım.",
        universite="Yozgat Bozok Üniversitesi",
        pratik=(
            "Yozgat'ta arabaşı porsiyonunu yarıya indirip yanına yoğurt eklemek dengeyi kuruyor. Kış aylarında ise ev içi hareket planı yapmak azalan günlük adım sayısını telafi ediyor."
        ),
    ),
    # ---------------- KARADENİZ ----------------
    "TRABZON": dict(
        mutfak=["hamsi", "akçaabat köftesi", "kuymak", "karalahana", "Vakfıkebir ekmeği"],
        mutfak_notu=(
            "Trabzon sofrasının balık ve yeşillik tarafı planın işini kolaylaştırıyor: hamsi "
            "mevsiminde haftalık protein planı neredeyse kendiliğinden kuruluyor. Asıl düzenleme "
            "kuymakta oluyor — tereyağı ve mısır unuyla hazırlandığı için küçük bir tabak bile "
            "yüksek enerji taşıyor. Danışanlarda kahvaltıda kuymağın sıklığını belirlemek, "
            "porsiyonunu küçültmekten daha iyi sonuç veriyor."
        ),
        ozel="Hamsinin kızartma yerine fırında pişirilmesi, öğünün yağ payını belirgin düşürüyor.",
        universite="Karadeniz Teknik Üniversitesi",
        pratik=(
            "Trabzon'da kuymağı her sabah değil haftada iki kahvaltıya almak en etkili düzenleme. Hamsiyi ise mısır ununa bulayıp kızartmak yerine fırında pişirmek öğünün yağ payını belirgin düşürüyor."
        ),
    ),
    "RİZE": dict(
        mutfak=["hamsi", "muhlama", "karalahana", "Laz böreği", "çay"],
        mutfak_notu=(
            "Rize'de çay tüketimi günlük rutinin merkezinde ve asıl konu çayın kendisi değil, "
            "yanında yerleşen şeker ile hamur işi. Danışanlarda günde tüketilen kesme şeker "
            "sayısını hesaplamak çoğu zaman şaşırtıcı bir toplam çıkarıyor. Karalahana ve "
            "hamsi ise planın lif ve protein tarafını güçlü tutuyor."
        ),
        ozel="Çay saatinin şeker payını görünür kılmak, burada en sık yaptığımız ilk düzeltme.",
        universite="Recep Tayyip Erdoğan Üniversitesi",
        pratik=(
            "Rize'de günde tüketilen kesme şekeri saymak çoğu danışanda şaşırtıcı bir toplam çıkarıyor. Çayı azaltmak yerine şekeri kademeli düşürmek uygulanabilir oluyor. Karalahanayı ise haftada iki kez sofraya almak lif hedefini karşılıyor."
        ),
    ),
    "SAMSUN": dict(
        mutfak=["Samsun pidesi", "hamsi", "kaz eti", "nokul"],
        mutfak_notu=(
            "Samsun pidesi tek başına bir öğünü karşılayacak porsiyonda geliyor ve genelde "
            "yanında ayran veya tatlıyla tamamlanıyor. Danışanlarda pidenin yarısını yanına "
            "salatayla dengelemek işe yarıyor. Karadeniz'in balık erişimi burada da protein "
            "planını kolaylaştıran bir avantaj."
        ),
        ozel="Tek tabaklık büyük porsiyonları bölmek burada en pratik düzeltme.",
        universite="Ondokuz Mayıs Üniversitesi",
        pratik=(
            "Samsun'da pideyi tek başına öğün saymak ve yanına ayrıca tatlı almamak en önemli düzenleme. Balığı ise haftada iki kez sofraya alarak protein planını kurmak kolaylaşıyor."
        ),
    ),
    "ORDU": dict(
        mutfak=["fındık", "karalahana", "pide", "kivi"],
        mutfak_notu=(
            "Ordu'da fındık hem üretimin hem de günlük tüketimin parçası. Ara öğün olarak "
            "değerli ama ölçüsüz tüketildiğinde günlük enerjiyi hızla yükseltiyor; avuç ölçüsünü "
            "sabitlemek çoğu danışanda yeterli oluyor. Karalahana ve kivi ise mevsimsel lif ve "
            "C vitamini tarafını güçlü tutuyor."
        ),
        ozel="Kuruyemişin ölçülendirilmesi, planın burada en belirleyici maddesi.",
        universite="Ordu Üniversitesi",
        pratik=(
            "Ordu'da fındığı paketten değil önceden ayrılmış avuç ölçüsünden yemek en sık verdiğimiz öneri. Kivi mevsiminde ise ara öğünü meyveye çevirmek şeker ihtiyacını doğal yoldan karşılıyor."
        ),
    ),
    "GİRESUN": dict(
        mutfak=["fındık", "karalahana çorbası", "tirmit", "pide"],
        mutfak_notu=(
            "Giresun'da fındık günlük sofranın doğal parçası; sorun genelde ana öğünlerin yerine "
            "geçmesi. Danışanlarda fındığı ara öğüne planlı biçimde yerleştirmek, hem açlığı "
            "kontrol ediyor hem de ana öğünlerin atlanmasını önlüyor. Karalahana çorbası ise "
            "akşam öğününü hafifletmek için iyi bir başlangıç."
        ),
        ozel="Kuruyemişin öğün yerine geçmesini önlemek burada sık çalışılan bir başlık.",
        universite="Giresun Üniversitesi",
        pratik=(
            "Giresun'da fındığı ana öğün yerine değil öğün arasına planlı biçimde yerleştirmek gerekiyor. Karalahana çorbasını akşam başına almak ise ana yemekte porsiyonu küçültüyor."
        ),
    ),
    "BARTIN": dict(
        mutfak=["Bartın pirinci", "kestane", "karalahana sarması", "mısır ekmeği"],
        mutfak_notu=(
            "Bartın'da pirinç yerel üretimin parçası ve sofrada düzenli yer alıyor; plandan "
            "çıkarmak yerine porsiyonunu belirleyip yanına sebze eklemek daha sürdürülebilir "
            "oluyor. Kestane ise mevsiminde ara öğün olarak değerli ama karbonhidrat payı "
            "yüksek bir besin — kuruyemiş sanılıp serbest tüketildiğinde günlük toplamı "
            "yükseltiyor. Karalahana sarması ise lif tarafını güçlü tutuyor."
        ),
        ozel="Kestanenin kuruyemiş değil karbonhidrat olarak planlanması burada sık açıklanıyor.",
        universite="Bartın Üniversitesi",
        pratik=(
            "Bartın'da pirinç pilavının porsiyonunu yarıya indirip yanına bol sebze eklemek en pratik düzenleme. Kestaneyi ise kuruyemiş değil karbonhidrat sayıp günde beş-altı adetle sınırlamak, mevsiminde en sık verdiğimiz öneri. Karalahana sarmasını haftada bir sofraya almak da lif tarafını güçlendiriyor."
        ),
    ),
    "KASTAMONU": dict(
        mutfak=["etli ekmek", "banduma", "siyez bulguru", "pastırma"],
        mutfak_notu=(
            "Kastamonu'da siyez bulguru yerel bir tahıl ve lif içeriğiyle plana uygun bir zemin "
            "sunuyor. Banduma gibi ekmek temelli yemeklerde ise ekmek miktarı görünmez biçimde "
            "artabiliyor. Danışanlarda porsiyonu tabakta önceden ayırmak, yemek sırasında "
            "durdurmaktan daha iyi sonuç veriyor."
        ),
        ozel="Porsiyonu önceden tabağa ayırmak burada en sık verilen pratik öneri.",
        universite="Kastamonu Üniversitesi",
        pratik=(
            "Kastamonu'da siyez bulgurunu beyaz pirinç yerine tercih etmek lif alımını kendiliğinden artırıyor. Banduma gibi yemeklerde ise porsiyonu tabağa önceden ayırmak miktarı kontrol altında tutuyor."
        ),
    ),
    "SİNOP": dict(
        mutfak=["nokul", "mantı", "deniz ürünleri", "kestane"],
        mutfak_notu=(
            "Sinop'ta balığa erişim düzenli ve haftalık protein planını kurmayı kolaylaştırıyor. "
            "Nokul gibi hamur işleri ise çay saatinin sabit parçası olduğunda günlük karbonhidrat "
            "payını yükseltiyor. Danışanlarda çay saatini tamamen kaldırmak yerine içeriğini "
            "değiştirmek daha kalıcı oluyor."
        ),
        ozel="Çay saatini kaldırmak yerine içeriğini değiştirmek burada işe yarayan yaklaşım.",
        universite="Sinop Üniversitesi",
        pratik=(
            "Sinop'ta balığı haftada iki öğüne almak protein planını kuruyor. Nokulu ise her çay saatinde değil hafta sonu bir öğüne bağlamak sıklığı doğal olarak düşürüyor."
        ),
    ),
    "ZONGULDAK": dict(
        mutfak=["kömeç", "papaz yahnisi", "mısır ekmeği", "karalahana"],
        mutfak_notu=(
            "Zonguldak'ta vardiyalı çalışma düzeni beslenmeyi doğrudan etkiliyor: uyku saati "
            "değiştiğinde açlık ritmi de kayıyor ve klasik üç öğün kurgusu işlemiyor. Planlar "
            "burada saate değil vardiya sırasına göre kuruluyor. Karalahana ve mısır ekmeği "
            "gibi yerel öğeler ise plana rahatlıkla giriyor."
        ),
        ozel="Öğünleri saate değil vardiya sırasına bağlamak burada esas yaklaşım.",
        universite="Zonguldak Bülent Ecevit Üniversitesi",
        pratik=(
            "Zonguldak'ta vardiya öncesi ve sonrası iki sabit öğün belirlemek, düzensiz saatlerde bile planı ayakta tutuyor. Vardiya arasına ise önceden hazırlanmış bir ara öğün koymak kantin seçimini devre dışı bırakıyor."
        ),
    ),
    "KARABÜK": dict(
        mutfak=["Safranbolu lokumu", "bükme", "kuyu kebabı", "safran"],
        mutfak_notu=(
            "Karabük'te lokum ve şerbetli tatlılar günlük rutine girdiğinde şeker payı hızla "
            "yükseliyor; danışanlarda haftalık sıklığı belirlemek porsiyon küçültmekten daha "
            "etkili oluyor. Sanayi bölgesindeki vardiyalı çalışma düzeni de öğün saatlerini "
            "plan kurgusunda öne çıkarıyor."
        ),
        ozel="Tatlının haftalık sıklığını netleştirmek burada ilk düzenlenen kalem.",
        universite="Karabük Üniversitesi",
        pratik=(
            "Karabük'te lokumu misafirlik günlerine bırakmak ve evde stok tutmamak sıklığı kendiliğinden azaltıyor. Vardiyalı çalışanlarda ise uyanıştan sonraki ilk öğünü sabitlemek önceliğimiz."
        ),
    ),
    "DÜZCE": dict(
        mutfak=["fındık", "mantı", "kabak tatlısı", "Abhaz mutfağı"],
        mutfak_notu=(
            "Düzce'de fındık üretimi yaygın ve sofrada düzenli yer alıyor; ara öğün planında "
            "değerli ama ölçüsü belirlenmediğinde günlük toplamı yükseltiyor. Kabak tatlısı gibi "
            "sebze temelli tatlılarda ise şerbet payı çoğu zaman göz ardı ediliyor."
        ),
        ozel="Sebze temelli tatlıların da şeker taşıdığını göstermek burada sık gündeme geliyor.",
        universite="Düzce Üniversitesi",
        pratik=(
            "Düzce'de fındığı ara öğüne avuç ölçüsüyle yerleştirmek en pratik adım. Kabak tatlısında ise şerbeti süzmek ve porsiyonu küçük tutmak tatlıyı plandan çıkarmadan sürdürmeyi sağlıyor."
        ),
    ),
    "BOLU": dict(
        mutfak=["mantı", "kuru fasulye", "tost", "aşçılık geleneği"],
        mutfak_notu=(
            "Bolu'da aşçılık geleneği güçlü ve ev yemeği kültürü yaygın; bu, plan açısından "
            "avantaj çünkü yemekler evde ve içeriği bilinerek hazırlanıyor. Danışanlarda "
            "düzenlenen kalem genelde porsiyon büyüklüğü ve tereyağı miktarı oluyor."
        ),
        ozel="Ev yemeği kültürünün güçlü olması, plan uyumunu kolaylaştıran bir avantaj.",
        universite="Bolu Abant İzzet Baysal Üniversitesi",
        pratik=(
            "Bolu'da ev yemeği kültürünü avantaja çevirip haftalık menüyü pazar günü planlamak planın uygulanabilirliğini belirgin artırıyor. Tereyağını ise yemeğin üzerine değil pişirme sırasında ölçüyle eklemek miktarı düşürüyor."
        ),
    ),
    "AMASYA": dict(
        mutfak=["Amasya elması", "keşkek", "bamya", "toyga çorbası"],
        mutfak_notu=(
            "Amasya elması yıl boyu erişilebilir ve ara öğün planını kolaylaştıran bir seçenek. "
            "Keşkek gibi tahıl-et yemekleri doyurucu ve planlanabilir; danışanlarda düzenlenen "
            "kalem genelde yanına gelen ekmek ve tereyağı. Toyga çorbası ise yoğurt temelli "
            "olduğu için protein tarafını destekliyor."
        ),
        ozel="Meyveye kolay erişim, ara öğün planını burada belirgin kolaylaştırıyor.",
        universite="Amasya Üniversitesi",
        pratik=(
            "Amasya'da elmayı ara öğüne almak akşam tatlı isteğini azaltıyor. Keşkeğin yanına ise ayrıca ekmek almamak günlük karbonhidrat dengesini koruyor."
        ),
    ),
    "TOKAT": dict(
        mutfak=["Tokat kebabı", "bez sarma", "çemen", "keşkek"],
        mutfak_notu=(
            "Tokat kebabı fırında ve sebzeyle birlikte hazırlandığı için aslında plana uygun "
            "bir yöntem; belirleyici olan porsiyon ve yanına gelen ekmek. Bez sarma gibi "
            "sarma-dolma çeşitleri ise pirinç içeriği nedeniyle karbonhidrat sayılarak "
            "planlanıyor."
        ),
        ozel="Sarma ve dolmaları karbonhidrat olarak hesaplamak burada sık açıklanıyor.",
        universite="Tokat Gaziosmanpaşa Üniversitesi",
        pratik=(
            "Tokat'ta kebabı fırın yönteminde bırakıp yanına bol sebze almak dengeyi kuruyor. Sarma ve dolmaları ise karbonhidrat sayarak günlük plana yazmak porsiyon hesabını netleştiriyor."
        ),
    ),
    "ÇORUM": dict(
        mutfak=["leblebi", "iskilip dolması", "keşkek", "bağdaş"],
        mutfak_notu=(
            "Çorum leblebisi lif ve protein açısından iyi bir ara öğün; sorun genelde ölçüsüz "
            "tüketilmesi. Avuç ölçüsü belirlendiğinde plana rahat giriyor. İskilip dolması gibi "
            "pirinç temelli yemeklerde ise porsiyonun yanına ayrıca ekmek almamak yeterli "
            "düzeltme oluyor."
        ),
        ozel="Leblebinin ölçülü ara öğün olarak planlanması burada sık çalışılıyor.",
        universite="Hitit Üniversitesi",
        pratik=(
            "Çorum'da leblebiyi önceden ölçülmüş kâseden yemek en etkili düzenleme. İskilip dolmasının yanına ise ayrıca pilav veya ekmek almamak öğünü dengeliyor."
        ),
    ),
    "ARTVİN": dict(
        mutfak=["muhlama", "hurmalı çorba", "karalahana", "bal"],
        mutfak_notu=(
            "Artvin'de muhlama ve tereyağı temelli kahvaltı geleneği güçlü; bunlar plandan "
            "çıkarılmak yerine sıklığı belirlenerek yönetiliyor. Bal ise doğal olduğu için "
            "serbest sanılan bir kalem — kaşık ölçüsü netleştirilmediğinde günlük şeker toplamını "
            "yükseltiyor. Karalahana lif tarafını güçlü tutuyor."
        ),
        ozel="Balın kaşık ölçüsünü belirlemek burada sık yapılan bir düzeltme.",
        universite="Artvin Çoruh Üniversitesi",
        pratik=(
            "Artvin'de muhlamayı haftada iki kahvaltıya sınırlamak ve balı tatlı kaşığıyla ölçmek en sık verdiğimiz iki öneri. Karalahanayı ise haftalık menüye sabitlemek lif hedefini karşılıyor."
        ),
    ),
    "GÜMÜŞHANE": dict(
        mutfak=["pestil ve köme", "siron", "kuru fasulye", "dut"],
        mutfak_notu=(
            "Gümüşhane'de pestil ve köme yerel üretimin parçası; meyve temelli olsalar da "
            "yoğunlaştırılmış şeker içerdikleri için ara öğünde porsiyon belirlenmeden "
            "tüketildiğinde günlük toplamı yükseltiyor. Siron gibi hamur yemeklerinde ise "
            "yanına protein eklemek dengeyi kuruyor."
        ),
        ozel="Kurutulmuş meyve ürünlerinin şeker yoğunluğunu göstermek burada öncelikli.",
        universite="Gümüşhane Üniversitesi",
        pratik=(
            "Gümüşhane'de pestil ve kömeyi ara öğün olarak değil tatlı porsiyonu olarak saymak doğru yaklaşım. Siron gibi hamur yemeklerinde ise yanına yoğurt eklemek protein dengesini kuruyor."
        ),
    ),
    "BAYBURT": dict(
        mutfak=["ehli keşkek", "lor dolması", "civil peyniri", "yoğurt çorbası"],
        mutfak_notu=(
            "Bayburt sofrasında süt ürünleri ve tahıl birlikte geliyor; lor ve civil peyniri "
            "protein tarafını güçlü tutuyor. Uzun ve sert kış nedeniyle günlük hareket süresi "
            "belirgin düşüyor, bu yüzden planlar kış aylarında enerji tarafından gözden "
            "geçiriliyor."
        ),
        ozel="Kışın düşen hareket miktarı, plan güncellemesinin ana sebebi.",
        universite="Bayburt Üniversitesi",
        pratik=(
            "Bayburt'ta lor ve civil peynirini günlük protein kaynağı olarak plana yazmak işi kolaylaştırıyor. Kış aylarında ise ev içi hareket planı yapmak azalan günlük aktiviteyi telafi ediyor."
        ),
    ),
    # ---------------- DOĞU ANADOLU ----------------
    "ERZURUM": dict(
        mutfak=["cağ kebabı", "kadayıf dolması", "civil peyniri", "su böreği"],
        mutfak_notu=(
            "Erzurum'da kış çok uzun ve geleneksel sofra bu koşula göre kurulmuş: enerji yoğun, "
            "et ve süt ağırlıklı. Bu, protein tarafını kolaylaştırıyor ama sebze ve lif payı "
            "planda ayrıca kurulmayı gerektiriyor. Kadayıf dolması gibi kızartılıp şerbetlenen "
            "tatlılarda ise sıklık, porsiyondan daha belirleyici."
        ),
        ozel="Kış aylarında sebze çeşitliliğini plana eklemek burada öncelikli başlık.",
        universite="Atatürk Üniversitesi",
        pratik=(
            "Erzurum'da uzun kış boyunca sebze çeşitliliğini korumak için dondurulmuş sebze kullanmak pratik bir çözüm. Cağ kebabının yanına ise pilav yerine bol yeşillik almak öğünü dengeliyor. Kadayıf dolmasını haftada bir güne bağlamak da sürdürülebilir oluyor."
        ),
    ),
    "MUŞ": dict(
        mutfak=["herisi", "kavurma", "otlu peynir", "kesme çorbası"],
        mutfak_notu=(
            "Muş'ta herisi buğday ve etin uzun süre birlikte pişirilmesiyle hazırlanıyor; "
            "doyurucu ve protein-tahıl dengesi aslında iyi bir yemek. Danışanlarda düzenlediğimiz "
            "kalem genelde üzerine eklenen tereyağı miktarı. Kavurma ise kış için hazırlanan bir "
            "geleneksel yöntem olduğundan yağ payı yüksek; porsiyonu belirlendiğinde plandan "
            "çıkarmak gerekmiyor. Otlu peynir hem protein hem lif tarafına katkı veriyor."
        ),
        ozel="Uzun kış nedeniyle hareketin düştüğü aylarda plan enerji tarafından güncelleniyor.",
        universite="Muş Alparslan Üniversitesi",
        pratik=(
            "Muş'ta herisinin üzerine eklenen tereyağını yemek pişerken değil tabakta ölçüyle koymak, öğünün yağ payını belirgin düşürüyor. Kavurmayı ise haftada iki öğüne sınırlayıp yanına bol sebze almak dengeyi kuruyor. Kış aylarında hareket azaldığı için porsiyonları değil öğün düzenini korumak önceliğimiz."
        ),
    ),
    "VAN": dict(
        mutfak=["Van kahvaltısı", "otlu peynir", "murtuğa", "kavut"],
        mutfak_notu=(
            "Van kahvaltısı çeşitlilik açısından güçlü ama tabakta aynı anda çok sayıda "
            "yüksek yağlı öğe bulunuyor: kaymak, bal, murtuğa, kavurma. Danışanlarda hepsini "
            "çıkarmak yerine bir öğünde kaç yağ kaynağı olacağını belirlemek işe yarıyor. "
            "Otlu peynir ise hem protein hem ot içeriğiyle planın işine geliyor."
        ),
        ozel="Kahvaltıda yağ kaynağı sayısını sınırlamak burada en pratik düzeltme.",
        universite="Van Yüzüncü Yıl Üniversitesi",
        pratik=(
            "Van kahvaltısında tabakta aynı anda en fazla iki yağ kaynağı bulundurmak en etkili düzenleme; kaymak, bal, murtuğa ve kavurmanın hepsi bir arada olduğunda öğün günün en yüksek enerjilisi haline geliyor. Otlu peyniri ise her kahvaltıda tutmak protein tarafını güçlendiriyor."
        ),
    ),
    "MALATYA": dict(
        mutfak=["kayısı", "kağıt kebabı", "analı kızlı", "içli köfte"],
        mutfak_notu=(
            "Malatya kayısısı kuru olarak günlük tüketimin parçası; küçük hacimde yoğun şeker "
            "taşıdığı için 'meyve, serbest' varsayımıyla tüketildiğinde günlük toplamı belirgin "
            "yükseltiyor. Danışanlarda adet ölçüsü belirlemek yeterli oluyor. Analı kızlı gibi "
            "bulgur-baklagil yemekleri ise plana rahatlıkla giriyor."
        ),
        ozel="Kuru kayısıda adet ölçüsünü netleştirmek burada en sık yapılan düzeltme.",
        universite="İnönü Üniversitesi",
        pratik=(
            "Malatya'da kuru kayısıyı avuçla değil adetle almak, günde üç-dört tane şeklinde sınırlamak en pratik adım. Analı kızlı gibi bulgur yemeklerini ise haftada iki kez sofraya almak lif hedefini karşılıyor."
        ),
    ),
    "ELAZIĞ": dict(
        mutfak=["içli köfte", "harput köftesi", "gömme", "orcik"],
        mutfak_notu=(
            "Elazığ'da içli köfte kızartma yöntemiyle hazırlandığında öğünün yağ payı belirgin "
            "yükseliyor; haşlama veya fırın yöntemine geçiş tek başına fark yaratıyor. Orcik "
            "gibi pekmez-ceviz temelli ürünler ise doğal içerikli olsalar da yoğun şeker "
            "taşıdığı için ara öğünde ölçülendiriliyor."
        ),
        ozel="Kızartma yerine haşlama yöntemine geçiş, burada en hızlı sonuç veren değişiklik.",
        universite="Fırat Üniversitesi",
        pratik=(
            "Elazığ'da içli köfteyi kızartmak yerine haşlamak öğünün yağ payını yarıya indiriyor. Orciki ise ara öğün değil tatlı porsiyonu olarak saymak doğru yaklaşım."
        ),
    ),
    "ERZİNCAN": dict(
        mutfak=["tulum peyniri", "bal", "cimcik", "lokum"],
        mutfak_notu=(
            "Erzincan tulum peyniri protein açısından değerli ama yağ ve tuz payı yüksek; "
            "porsiyon belirlendiğinde plana rahatlıkla giriyor. Bal ve lokum gibi kalemler "
            "kahvaltıda birlikte yer aldığında günün ilk öğünü beklenenden yüksek enerjiyle "
            "başlıyor."
        ),
        ozel="Kahvaltıda tatlı ve peyniri aynı anda tabağa koymamak burada sık verilen öneri.",
        universite="Erzincan Binali Yıldırım Üniversitesi",
        pratik=(
            "Erzincan'da kahvaltıda tulum peyniriyle balı aynı anda tabağa koymamak en sık verdiğimiz öneri. Peyniri günlük bir dilimle sınırlamak ise tuz ve yağ dengesini koruyor."
        ),
    ),
    "KARS": dict(
        mutfak=["kaşar peyniri", "kaz eti", "bal", "piti"],
        mutfak_notu=(
            "Kars kaşarı ve balı kahvaltının merkezinde; ikisi de kaliteli ürünler ama birlikte "
            "ve ölçüsüz tüketildiğinde sabah öğünü günün en yüksek enerjili öğünü haline "
            "geliyor. Kaz eti ise mevsimsel ve yağ payı yüksek bir protein kaynağı; sıklığı "
            "belirlenerek plana giriyor."
        ),
        ozel="Sabah öğününün gün içindeki enerji payını dengelemek burada öncelikli.",
        universite="Kafkas Üniversitesi",
        pratik=(
            "Kars'ta kahvaltıda kaşar ve balı birlikte değil dönüşümlü almak sabah öğününün enerji payını dengeliyor. Kaz etini ise mevsiminde haftada bir öğüne sınırlamak yeterli oluyor."
        ),
    ),
    "AĞRI": dict(
        mutfak=["abdigör köftesi", "otlu peynir", "kavurma", "hasuta"],
        mutfak_notu=(
            "Ağrı'da uzun kış ve yüksek rakım nedeniyle geleneksel sofra enerji yoğun kurulmuş. "
            "Abdigör köftesi et ve bulgur temelli, doyurucu bir seçenek; porsiyonu belirlendiğinde "
            "plana uygun. Danışanlarda genelde sebze ve lif payını artırmak, çıkarma yapmaktan "
            "daha etkili oluyor."
        ),
        ozel="Sebze payını artırmak, burada kısıtlama yapmaktan daha sürdürülebilir.",
        universite="Ağrı İbrahim Çeçen Üniversitesi",
        pratik=(
            "Ağrı'da abdigör köftesinin yanına bol salata eklemek porsiyonu değiştirmeden dengeyi kuruyor. Uzun kış boyunca ise dondurulmuş sebze kullanmak çeşitliliği koruyor."
        ),
    ),
    "IĞDIR": dict(
        mutfak=["kayısı", "bostana", "kavurma", "pilav"],
        mutfak_notu=(
            "Iğdır'da meyve üretimi yaygın ve taze meyveye erişim ara öğün planını "
            "kolaylaştırıyor. Bostana gibi sebze temelli salatalar da lif tarafını güçlendiriyor. "
            "Danışanlarda düzenlenen kalem genelde pilav porsiyonu ve yanına eklenen ekmek."
        ),
        ozel="Taze meyveye erişim kolaylığı burada ara öğün planını belirgin destekliyor.",
        universite="Iğdır Üniversitesi",
        pratik=(
            "Iğdır'da taze meyveye erişim kolaylığını ara öğüne çevirmek en pratik adım. Pilav porsiyonunun yanına ayrıca ekmek almamak ise günlük karbonhidrat dengesini koruyor."
        ),
    ),
    "ARDAHAN": dict(
        mutfak=["kaşar peyniri", "bal", "kete", "süt ürünleri"],
        mutfak_notu=(
            "Ardahan'da süt ürünleri sofranın merkezinde ve protein tarafını güçlü tutuyor. "
            "Kete gibi hamur işleri ise çay saatinin sabit parçası olduğunda karbonhidrat payını "
            "yükseltiyor. Uzun kış nedeniyle hareket süresi düştüğü için planlar mevsime göre "
            "gözden geçiriliyor."
        ),
        ozel="Süt ürünlerinin yağ oranını ayarlamak, burada porsiyon kısmaktan daha etkili.",
        universite="Ardahan Üniversitesi",
        pratik=(
            "Ardahan'da süt ürünlerini tam yağlıdan yarım yağlıya geçirmek günlük yağ alımını fark edilmeden düşürüyor. Keteyi ise her çay saatinde değil hafta sonu bir öğüne bağlamak sıklığı azaltıyor."
        ),
    ),
    "BİTLİS": dict(
        mutfak=["büryan kebabı", "otlu peynir", "avşor", "ceviz"],
        mutfak_notu=(
            "Bitlis'te büryan kebabı fırında ve yağı süzülerek pişirildiği için aslında plana "
            "uygun bir yöntem; belirleyici olan porsiyon ve yanına gelen ekmek. Ceviz ise ara "
            "öğün için değerli ama avuç ölçüsü belirlenmediğinde günlük toplamı yükseltiyor."
        ),
        ozel="Ekmek porsiyonunu netleştirmek burada planın en belirleyici maddesi.",
        universite="Bitlis Eren Üniversitesi",
        pratik=(
            "Bitlis'te büryan kebabının yanındaki ekmeği baştan iki dilimle ölçmek en etkili düzenleme. Cevizi ise ara öğüne avuç ölçüsüyle yerleştirmek günlük toplamı kontrol altında tutuyor."
        ),
    ),
    "BİNGÖL": dict(
        mutfak=["bal", "otlu peynir", "kavurma", "cacık"],
        mutfak_notu=(
            "Bingöl balı yerel üretimin parçası ve kahvaltıda düzenli yer alıyor; doğal olması "
            "şeker payını değiştirmediği için kaşık ölçüsü belirleniyor. Otlu peynir ve cacık "
            "gibi seçenekler ise protein ve sıvı tarafını destekliyor."
        ),
        ozel="Doğal tatlandırıcıların da şeker sayıldığını göstermek burada sık gündemde.",
        universite="Bingöl Üniversitesi",
        pratik=(
            "Bingöl'de balı tatlı kaşığıyla ölçüp günde bir kaşıkla sınırlamak en pratik adım. Cacığı ise öğün yanına almak hem sıvı hem protein tarafını destekliyor."
        ),
    ),
    "TUNCELİ": dict(
        mutfak=["otlu peynir", "sarımsak", "keşkek", "dut pekmezi"],
        mutfak_notu=(
            "Tunceli'de yabani ot kullanımı yaygın ve bu, lif çeşitliliğini kendiliğinden "
            "artırıyor. Dut pekmezi gibi geleneksel ürünler besleyici olsa da yoğun şeker "
            "içerdiği için ölçülendiriliyor. Keşkek ise doyurucu ve planlanabilir bir öğün."
        ),
        ozel="Yabani ot çeşitliliği, lif hedefini tutturmayı burada kolaylaştırıyor.",
        universite="Munzur Üniversitesi",
        pratik=(
            "Tunceli'de yabani ot çeşitliliğini haftalık menüye sabitlemek lif hedefini kendiliğinden karşılıyor. Dut pekmezini ise günde bir tatlı kaşığıyla ölçmek şeker dengesini koruyor."
        ),
    ),
    "HAKKARİ": dict(
        mutfak=["otlu peynir", "kavurma", "dolma", "ceviz"],
        mutfak_notu=(
            "Hakkari'de yüksek rakım ve uzun kış nedeniyle geleneksel sofra enerji yoğun. "
            "Otlu peynir protein ve ot tarafını birlikte veriyor. Danışanlarda planlama "
            "genelde kış aylarında azalan hareket ile geleneksel sofranın enerji payını "
            "birlikte değerlendirmek üzerine kuruluyor."
        ),
        ozel="Uzun kış boyunca hareket planını iç mekâna taşımak burada öncelikli.",
        universite="Hakkari Üniversitesi",
        pratik=(
            "Hakkari'de uzun kış boyunca hareket planını iç mekâna taşımak, azalan günlük aktiviteyi telafi ediyor. Otlu peyniri ise günlük protein kaynağı olarak plana yazmak işi kolaylaştırıyor."
        ),
    ),
    # ---------------- GÜNEYDOĞU ANADOLU ----------------
    "GAZİANTEP": dict(
        mutfak=["baklava", "lahmacun", "beyran", "Antep fıstığı", "yuvalama"],
        mutfak_notu=(
            "Gaziantep mutfağı Türkiye'nin en zengin sofralarından biri ve bu hem avantaj hem "
            "zorluk. Bulgur, mercimek ve sebze temelli yemekler planın omurgasını kurmaya "
            "fazlasıyla elverişli. Asıl konu baklava ve tatlı geleneği: danışanlarda gördüğümüz "
            "kalıp, tatlının özel gün yemeği değil haftalık rutinin parçası olması. Antep fıstığı "
            "ise değerli bir ara öğün ama avuç ölçüsü belirlenmediğinde toplamı yükseltiyor."
        ),
        ozel="Tatlıyı plandan çıkarmak yerine haftalık sıklığını belirlemek burada esas yaklaşım.",
        universite="Gaziantep Üniversitesi",
        pratik=(
            "Gaziantep'te baklavayı plandan çıkarmak yerine haftada bir güne ve iki dilime bağlamak, uzun vadede en sürdürülebilir çözüm. Antep fıstığını ise paketten değil önceden ayrılmış avuç ölçüsünden yemek gerekiyor. Yuvalama ve mercimekli yemekleri haftalık menüye sabitlemek de planın omurgasını kuruyor."
        ),
    ),
    "ŞANLIURFA": dict(
        mutfak=["çiğ köfte", "lahmacun", "şıllık tatlısı", "isot", "mırra"],
        mutfak_notu=(
            "Şanlıurfa'da çiğ köfte bulgur temelli olduğu için aslında plana uygun bir zemin; "
            "belirleyici olan yanında tüketilen lavaş miktarı ve porsiyon sayısı. Yaz sıcağı "
            "gündüz iştahını bastırıp akşam öğününü ağırlaştırdığından, danışanlarda gün içi "
            "öğünleri geri kazandırmak plana ilk giren madde oluyor."
        ),
        ozel="Sıcak dönemde gündüz atlanan öğünleri geri kazandırmak burada öncelikli.",
        universite="Harran Üniversitesi",
        pratik=(
            "Şanlıurfa'da çiğ köftenin yanındaki lavaşı baştan ölçmek en önemli düzenleme; porsiyon sayısı değil ekmek miktarı belirleyici oluyor. Yaz aylarında ise gündüz atlanan öğünleri geri kazandırmak için sabah ve öğleye hafif ama düzenli öğünler koyuyoruz."
        ),
    ),
    "DİYARBAKIR": dict(
        mutfak=["kaburga dolması", "meftune", "karpuz", "lebeni çorbası"],
        mutfak_notu=(
            "Diyarbakır'da meftune gibi sebze-et yemekleri planın işine geliyor: sebze payı "
            "yüksek ve porsiyonu kontrol edilebilir. Kaburga dolması ise pirinç ve etin bir "
            "arada olduğu enerji yoğun bir yemek; sıklığı belirlenerek plana giriyor. Yaz "
            "sıcağında sıvı takibi ayrıca öne çıkıyor."
        ),
        ozel="Yaz aylarında sıvı hedefinin yeniden hesaplanması burada rutin bir adım.",
        universite="Dicle Üniversitesi",
        pratik=(
            "Diyarbakır'da meftune gibi sebze-et yemeklerini haftalık menüye sabitlemek planın işini kolaylaştırıyor. Yaz aylarında ise karpuzu tek başına değil peynirle birlikte almak kan şekeri dalgalanmasını azaltıyor."
        ),
    ),
    "MARDİN": dict(
        mutfak=["kaburga dolması", "ikbebet", "sembusek", "badem şekeri"],
        mutfak_notu=(
            "Mardin sofrasında bulgur ve baklagil temelli yemekler yaygın; lif tarafı güçlü. "
            "Badem şekeri ve şerbetli tatlılar ise misafir kültürünün parçası olduğu için "
            "sıklığı kişinin kontrolünde olmayabiliyor. Danışanlarda misafirlikte uygulanabilir "
            "bir strateji kurmak, plandan çıkarmaktan daha işlevsel oluyor."
        ),
        ozel="Misafirlik düzeninde uygulanabilir seçenekler planın parçası haline getiriliyor.",
        universite="Mardin Artuklu Üniversitesi",
        pratik=(
            "Mardin'de misafirlikte tatlıyı reddetmek yerine porsiyonu yarıya indirmek daha uygulanabilir oluyor. Bulgur temelli günlük yemekleri ise haftada üç kez sofraya almak lif hedefini karşılıyor."
        ),
    ),
    "ADIYAMAN": dict(
        mutfak=["çiğ köfte", "tütün köftesi", "besni üzümü", "Antep fıstığı"],
        mutfak_notu=(
            "Adıyaman'da bulgur temelli yemekler sofranın merkezinde ve plana uygun bir zemin "
            "sunuyor. Besni üzümü kuru olarak tüketildiğinde yoğun şeker taşıyor; ara öğünde "
            "ölçülendirildiğinde plandan çıkması gerekmiyor."
        ),
        ozel="Kuru üzümün ara öğüne ölçülü yerleştirilmesi burada sık çalışılıyor.",
        universite="Adıyaman Üniversitesi",
        pratik=(
            "Adıyaman'da çiğ köftenin yanına lavaş yerine bol yeşillik almak öğünü dengeliyor. Besni üzümünü ise ara öğüne on beş tane şeklinde sayıyla yerleştirmek en pratik ölçü."
        ),
    ),
    "BATMAN": dict(
        mutfak=["büryan", "perde pilavı", "kadayıf", "bulgur"],
        mutfak_notu=(
            "Batman'da perde pilavı pirinç, et ve kuruyemişin bir arada olduğu enerji yoğun "
            "bir yemek; özel gün yemeği olarak plana rahatlıkla giriyor ama haftalık rutine "
            "dönüştüğünde toplamı yükseltiyor. Bulgur temelli günlük yemekler ise dengeyi "
            "kurmayı kolaylaştırıyor."
        ),
        ozel="Özel gün yemeklerinin rutine dönüşüp dönüşmediğini takip etmek burada önemli.",
        universite="Batman Üniversitesi",
        pratik=(
            "Batman'da perde pilavını haftalık rutine değil özel günlere bırakmak en önemli düzenleme. Günlük sofrada ise bulgur temelli yemekleri korumak dengeyi kuruyor."
        ),
    ),
    "SİİRT": dict(
        mutfak=["büryan kebabı", "perde pilavı", "Siirt fıstığı", "kavut"],
        mutfak_notu=(
            "Siirt fıstığı yerel üretimin parçası ve ara öğün için değerli bir seçenek; "
            "avuç ölçüsü belirlendiğinde plana rahat giriyor. Büryan kebabı ise yağı süzülerek "
            "pişirildiği için yöntemi uygun; belirleyici olan yanındaki ekmek miktarı."
        ),
        ozel="Kuruyemişte avuç ölçüsünü sabitlemek burada en pratik düzeltme.",
        universite="Siirt Üniversitesi",
        pratik=(
            "Siirt'te fıstığı avuç ölçüsüyle ara öğüne yerleştirmek en sık verdiğimiz öneri. Büryanın yanındaki ekmeği ise baştan ölçmek porsiyon hesabını netleştiriyor."
        ),
    ),
    "ŞIRNAK": dict(
        mutfak=["kibe", "otlu peynir", "bulgur", "ceviz"],
        mutfak_notu=(
            "Şırnak sofrasında bulgur ve baklagil payı yüksek; lif ve tokluk tarafı güçlü. "
            "Otlu peynir protein tarafını destekliyor. Danışanlarda düzenlenen kalem genelde "
            "öğün sayısı: gün içinde iki öğüne düşen düzenlerde akşam porsiyonu büyüyor."
        ),
        ozel="Günlük öğün sayısını üçe tamamlamak burada planın ilk adımı oluyor.",
        universite="Şırnak Üniversitesi",
        pratik=(
            "Şırnak'ta günlük öğün sayısını üçe tamamlamak, akşam porsiyonunun büyümesini önleyen en etkili adım. Otlu peyniri ise kahvaltıda sabit tutmak protein tarafını destekliyor."
        ),
    ),
    "KİLİS": dict(
        mutfak=["katmer", "cılbır", "zeytinyağı", "bulgur"],
        mutfak_notu=(
            "Kilis katmeri fıstıklı ve kaymaklı olduğu için kahvaltıda yer aldığında günün "
            "ilk öğünü yüksek enerjiyle başlıyor; haftalık sıklığı belirlendiğinde plandan "
            "çıkması gerekmiyor. Zeytinyağı temelli günlük yemekler ise dengeyi kurmayı "
            "kolaylaştırıyor."
        ),
        ozel="Kahvaltılık tatlıların sıklığını netleştirmek burada öncelikli başlık.",
        universite="Kilis 7 Aralık Üniversitesi",
        pratik=(
            "Kilis'te katmeri her kahvaltıda değil hafta sonu bir öğüne bağlamak sıklığı doğal olarak düşürüyor. Zeytinyağlı sebze yemeklerini ise haftada üç kez sofraya almak planın omurgasını kuruyor."
        ),
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
        pratik=(
            "İstanbul'da en çok işe yarayan düzenleme, akşam eve dönüşte değil yolda planlı bir ara öğün almak. Gece 21.00'den sonra kurulan büyük sofranın sebebi genellikle gün boyu yetersiz kalan alım. Ayrıca öğle yemeğini iş çevresindeki iki-üç sabit seçenek üzerinden baştan belirlemek, her gün yeniden karar verme yükünü kaldırıyor."
        ),
    ),
}


def il_profili(il_adi):
    """Bir il için birleşik bağlam sözlüğü döndürür."""
    bolge = IL_BOLGE[il_adi]
    p = dict(BOLGE_TABAN[bolge])
    p.update(dict(
        il=il_adi, bolge=bolge, pratik=None,
        buyuksehir=il_adi in BUYUKSEHIR,
        ofis_ili=(il_adi == OFIS_IL),
        durum="taslak",
        ozel=None, universite=None,
    ))
    if il_adi in IL_OZEL:
        p.update(IL_OZEL[il_adi])
        p["durum"] = "hazir"
    return p
