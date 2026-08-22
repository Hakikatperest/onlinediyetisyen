# -*- coding: utf-8 -*-
"""Yerel sayfa üreticisi.

Kullanım:
    python3 _src/build.py --iller ADANA MERSİN YALOVA İSTANBUL     # seçili il
    python3 _src/build.py --ornek                                   # 4 pilot il + örnek ilçeler
    python3 _src/build.py --hepsi                                   # 81 il (ONAY GEREKTİRİR)
    python3 _src/build.py --denetim                                 # üretmeden kalite raporu

Her üretim sonunda kalite denetimi çalışır; eşiği aşan sayfa DİSKE YAZILMAZ.
"""
import argparse
import json
import math
import os
import re
import sys
from datetime import date

BURASI = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [BURASI, os.path.join(BURASI, "data")]

import turkce as T                              # noqa: E402
import content as C                             # noqa: E402
import render as R                              # noqa: E402
import quality as Q                             # noqa: E402
from city_context import il_profili             # noqa: E402
from variants import il_varyanti, ilce_varyanti  # noqa: E402

KOK = os.path.dirname(BURASI)
VERI = json.load(open(os.path.join(BURASI, "data", "turkiye.json"), encoding="utf-8"))
SITE = C.SITE
BUGUN = date.today().isoformat()

TR_SLUG = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosucgiosu")


def slug(s):
    s = s.translate(TR_SLUG).lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


# ------------------------------------------------------------ coğrafi komşuluk
def _mesafe(a, b):
    la1, lo1 = math.radians(a["latitude"]), math.radians(a["longitude"])
    la2, lo2 = math.radians(b["latitude"]), math.radians(b["longitude"])
    return 6371 * math.acos(min(1, math.sin(la1) * math.sin(la2) +
                                math.cos(la1) * math.cos(la2) * math.cos(lo2 - lo1)))


def yakin_iller(il, adet=4):
    """Gerçek koordinat mesafesine göre en yakın iller. Rastgele link yok."""
    k = VERI[il]["koordinatlar"]
    d = sorted(((_mesafe(k, v["koordinatlar"]), o) for o, v in VERI.items() if o != il))
    return [o for _, o in d[:adet]]


# ------------------------------------------------------------------ URL / yol
def il_url(il):
    return f"{SITE}/{slug(il)}-online-diyetisyen/"


def ilce_url(il, ilce):
    return f"{SITE}/{slug(il)}/{slug(ilce)}-online-diyetisyen/"


def il_yol(il):
    return os.path.join(KOK, f"{slug(il)}-online-diyetisyen", "index.html")


def ilce_yol(il, ilce):
    return os.path.join(KOK, slug(il), f"{slug(ilce)}-online-diyetisyen", "index.html")


HUB_URL = f"{SITE}/online-diyetisyen/"


# --------------------------------------------------------------- iç linkleme
ANCHOR_HAVUZU = [
    "online diyetisyen", "online diyetisyen hizmeti", "online beslenme danışmanlığı",
    "online diyetisyen desteği", "uzaktan diyetisyen görüşmesi", "online diyet programı",
    "internet üzerinden diyetisyen", "online beslenme desteği",
]


def anchor(tohum, kayma=0):
    return ANCHOR_HAVUZU[(tohum + kayma) % len(ANCHOR_HAVUZU)]


def ana_domain_cumlesi(p, tohum):
    """12. madde: her sayfada ana sayfaya doğal, konumu değişen tek link."""
    a = anchor(tohum)
    kaliplar = [
        f'Görüşme modelinin genel işleyişini <a href="{SITE}/">{a}</a> sayfasında bulabilirsiniz.',
        f'Hizmetin kapsamına dair ayrıntılar <a href="{SITE}/">{a}</a> sayfasında anlatılıyor.',
        f'Takip modelini ve içeriğini merak edenler <a href="{SITE}/">{a}</a> sayfasını inceleyebilir.',
        f'Sürecin bütününe <a href="{SITE}/">{a}</a> sayfasından bakabilirsiniz.',
    ]
    return kaliplar[tohum % len(kaliplar)]


def ilce_listesi_html(il, ilceler, tohum):
    """İlçeleri LİNKSİZ listeler.

    İlçe sayfaları kalite denetiminden geçemediği için üretilmiyor (online hizmette
    ilçe düzeyinde farklılaşacak gerçek bir içerik yok). Onlara link vermek her il
    sayfasında onlarca 404 üretirdi. Liste yine de değerli: okuyucu kendi ilçesini
    görüp kapsam dışında olmadığını anlıyor.
    """
    ic = "".join(f"<span>{i}</span>" for i in sorted(ilceler))
    ad = T.baslik(il)
    giris = [
        f"Görüşmeler uzaktan yapıldığı için {T.tamlayan(ad)} tüm ilçelerinden katılım mümkün:",
        f"{ad} genelinde, ilçe ayrımı olmaksızın tüm bölgelerden görüşme yapılabiliyor:",
        f"Aşağıdaki ilçelerin tamamı dâhil olmak üzere {T.tamlayan(ad)} her yerinden katılınabiliyor:",
    ][tohum % 3]
    return (f'<p>{giris}</p><div class="ilce-grid ilce-liste">{ic}</div>'
            f'<p>Görüşmenin içeriği ilçeye göre değişmiyor; plan kişinin kendi mutfağı ve '
            f'günlük düzeni üzerinden kuruluyor.</p>')


def yayindaki_iller():
    """Yalnızca yerel verisi girilmiş iller yayında sayılır.

    Yakın-il linkleri bu listeye göre süzülür; aksi hâlde henüz üretilmemiş
    il sayfalarına link verilir ve her il sayfası birkaç 404 üretir.
    """
    return [il for il in VERI if il_profili(il)["durum"] == "hazir"]


def yakin_il_html(il, tohum):
    yayinda = set(yayindaki_iller())
    y = [o for o in yakin_iller(il, adet=12) if o in yayinda][:4]
    if not y:
        return ""
    ic = "".join(f'<a href="{il_url(o)}">{T.baslik(o)}</a>' for o in y)
    giris = [
        "Coğrafi olarak yakın illerdeki sayfalar:",
        "Yakın illerin sayfalarına da bakabilirsiniz:",
        "Komşu illerdeki sayfalar:",
    ][tohum % 3]
    return (f'<h2>Yakındaki İllerden Online Diyetisyen Sayfaları</h2>'
            f'<p>{giris}</p><div class="komsu">{ic}</div>')


def cta_html(p, tohum):
    il = T.baslik(p["il"])
    ilDE = T.bulunma(il)
    basliklar = [
        f"{ilDE} Online Diyetisyen Görüşmesi İçin",
        "Görüşme Planlamak İsterseniz",
        f"{il} İçin İlk Adım",
        "Size Uygun Takip Modelini Konuşalım",
    ]
    metinler = [
        f"Uygun görüşme saatini ve size uygun takip modelini konuşmak için telefonla ulaşabilirsiniz.",
        f"Hangi takip modelinin size uyduğunu kısa bir ön görüşmeyle birlikte belirleyebiliriz.",
        f"Beslenme hedefinizi ve mevcut düzeninizi konuşarak başlıyoruz; ilk adım için yazmanız yeterli.",
        f"Sorularınız için telefon veya WhatsApp üzerinden doğrudan iletişime geçebilirsiniz.",
    ]
    return f'''<div class="lok-cta">
<h2>{basliklar[tohum % len(basliklar)]}</h2>
<p>{metinler[(tohum + 2) % len(metinler)]}</p>
<a class="btn btn-lg pulse" href="{C.TEL_HREF}">📞 {C.TEL_GORUNEN}</a>
<a class="btn btn-wa btn-lg" href="{C.WA}" target="_blank" rel="noopener">💬 WhatsApp'tan yaz</a>
</div>'''


# ------------------------------------------------------------ META üreticiler
TITLE_KALIPLARI = [
    "{il} Online Diyetisyen | Online Beslenme Danışmanlığı",
    "{il} Online Diyetisyen — Uzaktan Diyet Desteği",
    "Online Diyetisyen {il} | Video Görüşmeyle Beslenme Takibi",
    "{il} İçin Online Diyetisyen ve Beslenme Planı",
    "{il} Online Diyetisyen | Kişiye Özel Diyet Programı",
]
DESC_KALIPLARI = [
    "{ilDE} online diyetisyen desteği: video görüşme, kişiye özel öğün planı ve düzenli takip. "
    "{dyt} ile uzaktan beslenme danışmanlığı.",
    "{ilDE} yaşayanlar için uzaktan beslenme danışmanlığı. Görüşme nasıl işler, kimler için uygun "
    "ve ücret neye göre değişir — hepsi bu sayfada.",
    "{il} için online diyetisyen rehberi: yerel sofra düzeni, görüşme adımları, online ile yüz yüze "
    "farkı ve sık sorulan sorular.",
    "{ilDE} online diyet ve beslenme takibi. Ulaşım süresi olmadan, kendi mutfağınız üzerinden "
    "kurulan kişiye özel plan.",
]


def il_meta(p, tohum):
    il = T.baslik(p["il"])
    t = TITLE_KALIPLARI[tohum % len(TITLE_KALIPLARI)].format(il=il)
    d = DESC_KALIPLARI[(tohum + 1) % len(DESC_KALIPLARI)].format(
        il=il, ilDE=T.bulunma(il), dyt=C.DYT)
    return t, d


# --------------------------------------------------------------- İL SAYFASI
class VeriEksik(Exception):
    """İl için elle yazılmış yerel bağlam yoksa sayfa üretilmez.

    Bölge varsayılanıyla üretilen sayfa, aynı bölgedeki diğer illerle neredeyse
    aynı olur — yani tam olarak kaçınmaya çalıştığımız şey. Bu illerin sayfası
    city_context.IL_OZEL'e gerçek veri girilene kadar açılmaz.
    """


def il_sayfasi(il, zorla=False):
    p = il_profili(il)
    if p["durum"] != "hazir" and not zorla:
        raise VeriEksik(f"{T.baslik(il)}: city_context.IL_OZEL'de yerel veri yok")
    v = VERI[il]
    plaka, ilceler = v["plaka"], list(v["ilceler"])
    var = il_varyanti(il, plaka, len(ilceler))
    tohum = plaka * 7 + len(ilceler)
    ad = T.baslik(il)
    adDE = T.bulunma(ad)
    url = il_url(il)

    gorseller = R.gorsel_sec(tohum, 2 if len(ilceler) <= 6 else 3)
    hero_gorsel = gorseller[0][0]

    baslik, aciklama = il_meta(p, tohum)
    h1 = f"{ad} Online Diyetisyen"

    kirintilar = [("Ana Sayfa", SITE + "/"),
                  ("Online Diyetisyen", HUB_URL),
                  (h1, url)]

    # ---- gövde: bölüm sırası varyanttan gelir
    parcalar, aeo_cevaplar, sss_listesi = [], [], []
    gorsel_kuyrugu = list(gorseller[1:])

    # Yerel bloklar HER il sayfasında bulunur — varyant yalnızca sıralarını değiştirir.
    # Genel bilgi konu sayfalarına taşındığı için sayfanın gövdesini bunlar taşır.
    ZORUNLU_YEREL = ["mutfak", "iklim", "mesafe"]
    sira = list(var["blok_sirasi"])
    for z in ZORUNLU_YEREL:
        if z not in sira:
            sira.insert(min(len(sira) - 1, sira.index("ilceler") if "ilceler" in sira else 1), z)

    # NOT: Diyet konuları (diyet türleri / diyete başlama / sık hatalar) da lokasyondan
    # bağımsızdır — Adana'da da İstanbul'da da aynıdır. Bu yüzden il sayfasında
    # tekrarlanmaz, konu sayfalarında durur ve buradan link verilir. Aynı ilke:
    # IL_SAYFASINDAN_CIKAN.

    for idx, blok in enumerate(sira):
        if blok == "ilceler":
            parcalar.append(f"<h2>{T.tamlayan(ad)} Hangi İlçelerinden Katılım Var?</h2>"
                            + ilce_listesi_html(il, ilceler, tohum))
            continue
        if blok == "sss":
            sss_listesi = C.sss_sec(p)
            b, g, _ = C.blok_sss(p)
            parcalar.append(f"<h2>{b}</h2>{g}")
            continue
        if blok.startswith("DY:"):
            b, g = DY.DIYET_BLOKLARI[blok[3:]](p)
            parcalar.append(f"<h2>{b}</h2>{g}")
            continue
        if blok in IL_SAYFASINDAN_CIKAN:
            continue
        uretici = C.BLOKLAR.get(blok)
        if not uretici:
            continue
        b, g, aeo = uretici(p)
        parcalar.append((f"<h2>{b}</h2>" if b else "") + g)
        if aeo:
            aeo_cevaplar.append(aeo)
        # görselleri gövdeye dağıt (üst üste gelmesin)
        if gorsel_kuyrugu and idx in (1, 4):
            d, a = gorsel_kuyrugu.pop(0)
            parcalar.append(R.gorsel_html(d, f"{ad} — {a}"))

    parcalar.append(rehber_linkleri_html(p, tohum))
    parcalar.append(f"<p>{ana_domain_cumlesi(p, tohum)}</p>")
    parcalar.append(yakin_il_html(il, tohum))
    parcalar.append(cta_html(p, tohum))
    parcalar.append(f'<p class="guncelleme">Son güncelleme: {BUGUN} · '
                    f'İçerik sorumlusu: {C.DYT}</p>')

    govde = f'''<section class="lok-hero"><div class="wrap">
<span class="rozet">📍 {ad} · Online görüşme</span>
<h1>{h1}</h1>
<p class="sub">{aciklama}</p>
</div></section>
<article class="article"><div class="wrap">
{R.gorsel_html(hero_gorsel, f"{adDE} online diyetisyen desteği — {gorseller[0][1]}", lazy=False)}
{chr(10).join(parcalar)}
</div></article>'''

    schema = R.schema_bloklari(
        url=url, baslik=baslik, aciklama=aciklama, kirintilar=kirintilar,
        sss=sss_listesi, alan_adi=ad, alan_tipi="City",
        guncelleme=BUGUN, ana_gorsel=hero_gorsel)

    html = R.sayfa(url=url, baslik=baslik, aciklama=aciklama, h1=h1,
                   hero_alt=hero_gorsel, kirintilar=kirintilar,
                   govde=govde, schema=schema, guncelleme=BUGUN)
    return dict(tur="il", il=il, url=url, yol=il_yol(il), html=html,
                varyant=var["kod"], aeo=aeo_cevaplar)


# ------------------------------------------------------------- İLÇE SAYFASI
import content_ilce as CI  # noqa: E402
import konular as KON       # noqa: E402
import diyet as DY         # noqa: E402


# Lokasyon-BAĞIMSIZ bilgi il sayfasında tekrarlanmaz; konu sayfalarına gider.
# Duplicate content'i şablon hilesiyle değil, doğru bilgi mimarisiyle çözüyoruz.
IL_SAYFASINDAN_CIKAN = {"nedir", "surec", "ucret", "karsilastirma", "kimler"}


def rehber_linkleri_html(p, tohum):
    ad = T.baslik(p["il"])
    giris = [
        f"{T.bulunma(ad)} yaşayan biri için değişmeyen genel bilgiler ayrı sayfalarda toplandı:",
        "Hizmetin lokasyondan bağımsız tarafını merak ediyorsanız:",
        "Süreç, ücret ve karşılaştırma başlıkları için ayrıntılı rehberler:",
        "Aşağıdaki rehberler bu sayfadaki yerel bilgiyi tamamlıyor:",
    ][tohum % 4]
    ic = "".join(
        f'<a href="{SITE}/{k["slug"]}/">{k["h1"].rstrip("?")}</a>'
        for k in KON.KONULAR
    )
    return f'<h2>Konu Rehberleri</h2><p>{giris}</p><div class="komsu">{ic}</div>'


def _ilce_ozellik(ilce, il):
    """Yalnızca DOĞRULANABİLİR sinyal kullanılır.

    Sayfalar diyet ekseninde kurulduğu için ilçenin kentsel/kırsal/merkez olması
    içeriği belirlemiyor; bu yüzden şu an doğrulanabilir bir ayırt edici özellik yok.
    Persona dağıtımı il düzeyinde yapılır (_il_ici_varyant_dagitimi).
    """
    return None


def _il_ici_varyant_dagitimi(il):
    """Aynı il içinde iki ilçe aynı varyantı ALMAZ (varyant sayısına kadar).

    Önceki hâlinde Seyhan ve Çukurova ikisi de ILC-02'ye düşüyor, aynı personayla
    neredeyse aynı sayfa üretiliyordu (%80 benzerlik). Dağıtım artık il düzeyinde
    yapılıyor: 'Merkez' gibi kesin bilgiler önce sabitlenir, kalanlar sırayla
    farklı varyantlara paylaştırılır.
    """
    from variants import ILCE_VARYANT
    ilceler = sorted(VERI[il]["ilceler"])
    plaka = VERI[il]["plaka"]
    atama, kullanilan = {}, set()
    # 1) kesin bilgiye dayalı atamalar
    for x in ilceler:
        oz = _ilce_ozellik(x, il)
        if oz:
            v = ilce_varyanti(x, il, plaka, oz)
            atama[x] = v
            kullanilan.add(v["kod"])
    # 2) kalanlar: farklı varyantlara sırayla dağıt
    havuz = [v for v in ILCE_VARYANT if v["kod"] not in kullanilan] or list(ILCE_VARYANT)
    kalan = [x for x in ilceler if x not in atama]
    kalan.sort(key=lambda x: (plaka * 31 + sum(ord(c) for c in x)) % 9973)
    for i, x in enumerate(kalan):
        atama[x] = havuz[i % len(havuz)]
    return atama


_VARYANT_ONBELLEK = {}


def ilce_sayfasi(il, ilce):
    p = il_profili(il)
    v = VERI[il]
    plaka = v["plaka"]
    if il not in _VARYANT_ONBELLEK:
        _VARYANT_ONBELLEK[il] = _il_ici_varyant_dagitimi(il)
    var = _VARYANT_ONBELLEK[il][ilce]
    tohum = plaka * 13 + sum(ord(c) for c in ilce) % 97

    i, l = T.baslik(ilce), T.baslik(il)
    url = ilce_url(il, ilce)
    h1 = f"{i} Online Diyetisyen"
    baslik = f"{i} Online Diyetisyen | {l} Online Beslenme Desteği"
    aciklama = (f"{T.bulunma(i)} ({l}) yaşayanlar için online diyetisyen desteği: "
                f"video görüşme, kişiye özel öğün planı ve düzenli takip.")

    kirintilar = [("Ana Sayfa", SITE + "/"),
                  ("Online Diyetisyen", HUB_URL),
                  (f"{l} Online Diyetisyen", il_url(il)),
                  (h1, url)]

    gorseller = R.gorsel_sec(tohum, 1)
    hero = gorseller[0]

    parcalar, sss = [], []

    # İlçe sayfasını il sayfasının kısaltılmışı olmaktan çıkaran iki ek:
    #  (a) ikinci bir persona bloğu — aynı ilçede farklı yaşam düzenleri
    #  (b) ilin yerel sofra bağlamı — ilçenin bağlı olduğu ile özgü, kısa
    from variants import ILCE_VARYANT
    ikinci = ILCE_VARYANT[(ILCE_VARYANT.index(var) + 3 + (tohum % 4)) % len(ILCE_VARYANT)]
    ek_blok = next((b for b in ikinci["blok_sirasi"]
                    if b in CI.ILCE_BLOKLARI and b not in var["blok_sirasi"]), None)

    sira = list(var["blok_sirasi"])
    if ek_blok:
        sira.insert(max(1, len(sira) - 2), ek_blok)

    for blok in sira:
        if blok == "komsu":
            digerleri = [x for x in v["ilceler"] if x != ilce]
            sec = sorted(digerleri, key=lambda x: (tohum + sum(ord(c) for c in x)) % 1009)[:4]
            ic = "".join(f'<a href="{ilce_url(il, x)}">{T.baslik(x)}</a>' for x in sec)
            parcalar.append(
                f'<h2>{T.tamlayan(l)} Diğer İlçeleri</h2>'
                f'<p>{l} genelindeki sayfalara ve diğer ilçelere buradan ulaşabilirsiniz:</p>'
                f'<div class="komsu"><a href="{il_url(il)}"><strong>{l} (il sayfası)</strong></a>{ic}</div>')
            continue
        if blok == "sss":
            sss = CI.ilce_sss(ilce, il, p, tohum)
            ic = "".join(f'<details class="faq"><summary>{s}</summary><div>{c}</div></details>'
                         for s, c in sss)
            parcalar.append(f"<h2>Sık Sorulan Sorular</h2>{ic}")
            continue
        uretici = CI.ILCE_BLOKLARI.get(blok)
        if not uretici:
            continue
        b, g = uretici(ilce, il, p)
        parcalar.append(f"<h2>{b}</h2>{g}")

    if p.get("mutfak"):
        mut = ", ".join(p["mutfak"][:3])
        cerceve = [
            f"Plan hazırlanırken {T.tamlayan(l)} sofrası da hesaba katılıyor: {mut} gibi "
            f"yerel yemekler listeden çıkarılmıyor, ölçüsü ve sıklığı belirleniyor.",
            f"{l} genelinde sofrada sık yer alan {mut} gibi yemekler planın dışında bırakılmıyor; "
            f"haftalık düzen içindeki payı ayarlanıyor.",
            f"{T.bulunma(l)} yaygın olan {mut} gibi seçenekler, porsiyon ve sıklık üzerinden "
            f"planın içine yerleştiriliyor.",
        ][tohum % 3]
        parcalar.append(f'<h2>{T.tamlayan(l)} Sofrası Planın Neresinde?</h2><p>{cerceve} '
                        f'Ayrıntılı anlatım <a href="{il_url(il)}">{l} online diyetisyen</a> '
                        f'sayfasında.</p>')
    parcalar.append(f"<p>{ana_domain_cumlesi(p, tohum)}</p>")
    parcalar.append(cta_html(p, tohum))
    parcalar.append(f'<p class="guncelleme">Son güncelleme: {BUGUN} · İçerik sorumlusu: {C.DYT}</p>')

    govde = f'''<section class="lok-hero"><div class="wrap">
<span class="rozet">📍 {i} · {l} · Online görüşme</span>
<h1>{h1}</h1>
<p class="sub">{aciklama}</p>
</div></section>
<article class="article"><div class="wrap">
{R.gorsel_html(hero[0], f"{T.bulunma(i)} online diyetisyen desteği — {hero[1]}", lazy=False)}
{chr(10).join(parcalar)}
</div></article>'''

    schema = R.schema_bloklari(
        url=url, baslik=baslik, aciklama=aciklama, kirintilar=kirintilar,
        sss=sss, alan_adi=f"{i}, {l}", alan_tipi="AdministrativeArea",
        guncelleme=BUGUN, ana_gorsel=hero[0])

    html = R.sayfa(url=url, baslik=baslik, aciklama=aciklama, h1=h1,
                   hero_alt=hero[0], kirintilar=kirintilar, govde=govde,
                   schema=schema, guncelleme=BUGUN)
    return dict(tur="ilce", il=il, ilce=ilce, url=url, yol=ilce_yol(il, ilce),
                html=html, varyant=var["kod"], aeo=[])


# ------------------------------------------------------------------ DENETİM
def denetle(sayfalar):
    """42. madde denetimi. Sorunlu sayfa yazılmaz."""
    ciftler = [(s["url"], s["html"]) for s in sayfalar]
    rapor, temiz = [], []
    for s in sayfalar:
        r = Q.sayfa_raporu(s["url"], s["html"], ciftler)
        r["sorunlar"] += Q.teknik_seo_kontrol(s["html"], s["url"])
        yasak = Q.yasakli_ifade_kontrol(s["html"])
        if yasak:
            r["sorunlar"].append("yasaklı sağlık ifadesi: " + ", ".join(yasak))
        r["varyant"] = s["varyant"]
        rapor.append(r)
        if not r["sorunlar"]:
            temiz.append(s)
    return rapor, temiz


def yaz(sayfalar):
    for s in sayfalar:
        os.makedirs(os.path.dirname(s["yol"]), exist_ok=True)
        with open(s["yol"], "w", encoding="utf-8") as f:
            f.write(s["html"])
    return len(sayfalar)


def rapor_yazdir(rapor):
    print(f"\n{'sayfa':52}{'varyant':10}{'kelime':>7}{'en yakın':>10}  sorunlar")
    print("─" * 108)
    sorunlu = 0
    for r in sorted(rapor, key=lambda x: -len(x["sorunlar"])):
        kisa = r["yol"].replace(SITE, "")
        d = "✗" if r["sorunlar"] else "✓"
        print(f"{d} {kisa:50}{r['varyant']:10}{r['kelime']:>7}{r['en_yakin_skor']:>9.0%}  "
              f"{'; '.join(r['sorunlar'])[:60] if r['sorunlar'] else ''}")
        sorunlu += bool(r["sorunlar"])
    print("─" * 108)
    en = max((r["en_yakin_skor"] for r in rapor), default=0)
    print(f"{len(rapor)} sayfa · {sorunlu} sorunlu · azami benzerlik %{en*100:.0f} "
          f"(eşik %{Q.ESIK_JACCARD*100:.0f})")
    return sorunlu


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--iller", nargs="*", help="üretilecek iller (BÜYÜK harf)")
    ap.add_argument("--ilceler", nargs="*", help="IL:Ilce biçiminde")
    ap.add_argument("--ornek", action="store_true", help="konu kümeleri + hub + 4 pilot il")
    ap.add_argument("--faz1", action="store_true", help="yalnızca konu kümesi sayfaları")
    ap.add_argument("--hepsi", action="store_true", help="81 il")
    ap.add_argument("--denetim", action="store_true", help="üretme, yalnızca denetle")
    a = ap.parse_args()

    sayfalar = []
    if a.faz1 or a.ornek:
        for k in KON.KONULAR:
            sayfalar.append(konu_sayfasi(k))
    if a.ornek:
        hazir = []
        for il in ("ADANA", "MERSİN", "YALOVA", "İSTANBUL"):
            sayfalar.append(il_sayfasi(il))
            hazir.append(il)
        sayfalar.append(hub_sayfasi(hazir))
    if a.hepsi:
        for il in VERI:
            try:
                sayfalar.append(il_sayfasi(il))
            except VeriEksik:
                pass
    atlanan = []
    for il in (a.iller or []):
        try:
            sayfalar.append(il_sayfasi(il))
        except VeriEksik as e:
            atlanan.append(str(e))
    for x in (a.ilceler or []):
        il, ilce = x.split(":", 1)
        sayfalar.append(ilce_sayfasi(il, ilce))

    if not sayfalar:
        ap.error("üretilecek sayfa seçilmedi (--ornek / --iller / --hepsi)")

    rapor, temiz = denetle(sayfalar)
    sorunlu = rapor_yazdir(rapor)
    if atlanan:
        print(f"\nYerel verisi olmadığı için ATLANAN {len(atlanan)} il:")
        for x in atlanan:
            print("  -", x)
    if a.denetim:
        print("\n(--denetim: hiçbir dosya yazılmadı)")
        return 1 if sorunlu else 0
    n = yaz(temiz)
    print(f"\n{n} sayfa yazıldı, {len(sayfalar) - n} sayfa denetimden geçemedi.")
    return 1 if sorunlu else 0





# --------------------------------------------------------- KONU / HUB SAYFASI
def konu_sayfasi(k):
    url = f"{SITE}/{k['slug']}/"
    kirintilar = [("Ana Sayfa", SITE + "/"),
                  ("Online Diyetisyen", HUB_URL),
                  (k["h1"].rstrip("?"), url)]
    tohum = sum(ord(c) for c in k["slug"])
    gorseller = R.gorsel_sec(tohum, 2)

    parcalar = [f'<div class="ozet"><p><strong>Kısa cevap:</strong> {k["aeo"]}</p></div>']
    for i, (b, g) in enumerate(k["bolumler"]):
        parcalar.append(f"<h2>{b}</h2>{g}")
        if i == 0 and len(gorseller) > 1:
            parcalar.append(R.gorsel_html(gorseller[1][0], f"{k['h1'].rstrip('?')} — {gorseller[1][1]}"))

    ic = "".join(f'<details class="faq"><summary>{s}</summary><div>{c}</div></details>'
                 for s, c in k["sss"])
    parcalar.append(f"<h2>Sık Sorulan Sorular</h2>{ic}")

    digerleri = [x for x in KON.KONULAR if x["slug"] != k["slug"]]
    linkler = "".join(f'<a href="{SITE}/{x["slug"]}/">{x["h1"].rstrip("?")}</a>' for x in digerleri)
    parcalar.append(f'<h2>İlgili Rehberler</h2><div class="komsu">{linkler}'
                    f'<a href="{HUB_URL}">İllere Göre Online Diyetisyen</a></div>')
    parcalar.append(cta_html(dict(il="ADANA"), tohum))
    parcalar.append(f'<p class="guncelleme">Son güncelleme: {BUGUN} · İçerik sorumlusu: {C.DYT}</p>')

    govde = f'''<section class="lok-hero"><div class="wrap">
<h1>{k["h1"]}</h1>
<p class="sub">{k["desc"]}</p>
</div></section>
<article class="article"><div class="wrap">
{R.gorsel_html(gorseller[0][0], f"{k['h1'].rstrip('?')} — {gorseller[0][1]}", lazy=False)}
{chr(10).join(parcalar)}
</div></article>'''

    schema = R.schema_bloklari(url=url, baslik=k["title"], aciklama=k["desc"],
                               kirintilar=kirintilar, sss=k["sss"], alan_adi="Türkiye",
                               alan_tipi="Country", guncelleme=BUGUN,
                               ana_gorsel=gorseller[0][0])
    html = R.sayfa(url=url, baslik=k["title"], aciklama=k["desc"], h1=k["h1"],
                   hero_alt=gorseller[0][0], kirintilar=kirintilar, govde=govde,
                   schema=schema, guncelleme=BUGUN)
    return dict(tur="konu", url=url, yol=os.path.join(KOK, k["slug"], "index.html"),
                html=html, varyant="KONU", aeo=[k["aeo"]])


def hub_sayfasi(hazir_iller):
    """İl sayfalarının üst düğümü. Yalnızca YAYINDA olan illere link verir —
    yayınlanmamış ile link vermek 404 ve orphan sinyali üretir."""
    url = HUB_URL
    baslik = "İllere Göre Online Diyetisyen | Türkiye Geneli"
    desc = ("Türkiye'nin illerine göre online diyetisyen sayfaları. Yerel sofra düzeni, "
            "görüşme akışı ve ilçe bağlantılarıyla birlikte.")
    kirintilar = [("Ana Sayfa", SITE + "/"), ("Online Diyetisyen", url)]
    tohum = 4242
    g = R.gorsel_sec(tohum, 1)[0]

    from regions import IL_BOLGE
    bolgeler = {}
    for il in hazir_iller:
        bolgeler.setdefault(IL_BOLGE[il], []).append(il)

    bloklar = []
    for b in sorted(bolgeler):
        ic = "".join(f'<a href="{il_url(x)}">{T.baslik(x)} Online Diyetisyen</a>'
                     for x in sorted(bolgeler[b]))
        bloklar.append(f"<h3>{b} Bölgesi</h3><div class='ilce-grid'>{ic}</div>")

    konu_linkleri = "".join(f'<a href="{SITE}/{x["slug"]}/">{x["h1"].rstrip("?")}</a>'
                            for x in KON.KONULAR)
    govde = f'''<section class="lok-hero"><div class="wrap">
<h1>İllere Göre Online Diyetisyen</h1>
<p class="sub">{desc}</p>
</div></section>
<article class="article"><div class="wrap">
{R.gorsel_html(g[0], f"Türkiye genelinde online diyetisyen — {g[1]}", lazy=False)}
<div class="ozet"><p><strong>Kısa cevap:</strong> Online diyetisyen görüşmeleri video üzerinden
yapıldığı için Türkiye'nin her ilinden katılım mümkündür. İl sayfaları, o ildeki yerel sofra
düzenine ve günlük yaşam temposuna göre farklılaşan örnekler içerir.</p></div>
<h2>Nereden Başlamalı?</h2>
<p>Diyete başlamayı düşünen çoğu kişi doğrudan "hangi diyet" sorusuyla geliyor. Oysa sıralama
genelde tersi işe yarıyor: önce mevcut düzenin ne olduğu, sonra hedefin ne olacağı, en son
hangi yaklaşımın uygulanacağı. Bir beslenme planının kaç hafta uygulanabildiği, adının ne
olduğundan daha belirleyici.</p>
<p>Aşağıdaki rehberler bu sıralamayı takip ediyor: diyete nasıl başlanacağı, diyet türleri
arasındaki gerçek fark ve süreci en çok yavaşlatan hatalar.</p>
<div class="komsu">{konu_linkleri}</div>
<h2>İl Sayfaları Ne İşe Yarıyor?</h2>
<p>Görüşmeler uzaktan yapıldığı için hizmetin kendisi ile göre değişmiyor. İl sayfalarının
konusu hizmet değil, <strong>sofra</strong>: o ilde yaygın olan yemeklerin bir beslenme planı
içinde nereye oturduğu, mevsim döngüsünün öğün düzenine etkisi ve plana başlarken o ile
özgü pratik ayrıntılar.</p>
<h2>Yerel Sofra Diyetin Neresinde?</h2>
<p>Bir beslenme planının en sık takıldığı yer, kişinin alışkın olduğu sofrayla planın
çelişmesi. Yöresel yemekler listeden çıkarıldığında plan kısa sürede "özel bir dönem"e
dönüşüyor ve o dönem bitince eski düzen geri geliyor.</p>
<p>Uygulamada işe yarayan yaklaşım bunun tersi: yerel yemeği planın içine almak, porsiyonunu
ve haftalık sıklığını belirlemek. Bir ilde bulgur temelli yemekler öne çıkarken bir başkasında
balık ve yeşillik, bir diğerinde ise dışarıda yeme alışkanlığı belirleyici olabiliyor —
plan da buna göre kuruluyor.</p>
<h2>Bölgelere Göre İl Sayfaları</h2>
<p>Şu anda yayında olan il sayfaları aşağıda. Listeye yeni iller, o ile ait yerel bağlam
hazırlandıkça ekleniyor.</p>
{"".join(bloklar)}
{cta_html(dict(il="ADANA"), tohum)}
<p class="guncelleme">Son güncelleme: {BUGUN} · İçerik sorumlusu: {C.DYT}</p>
</div></article>'''
    schema = R.schema_bloklari(url=url, baslik=baslik, aciklama=desc, kirintilar=kirintilar,
                               sss=[], alan_adi="Türkiye", alan_tipi="Country",
                               guncelleme=BUGUN, ana_gorsel=g[0])
    html = R.sayfa(url=url, baslik=baslik, aciklama=desc, h1="İllere Göre Online Diyetisyen",
                   hero_alt=g[0], kirintilar=kirintilar, govde=govde, schema=schema,
                   guncelleme=BUGUN)
    return dict(tur="hub", url=url, yol=os.path.join(KOK, "online-diyetisyen", "index.html"),
                html=html, varyant="HUB", aeo=[])


if __name__ == "__main__":
    sys.exit(main())
