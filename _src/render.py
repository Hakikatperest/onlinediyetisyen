# -*- coding: utf-8 -*-
"""HTML kabuğu, schema ve görsel yerleşimi.

ŞEMA KARARI — önemli:
Bu sayfalarda LocalBusiness / MedicalClinic şeması KULLANILMAZ (Adana hariç).
Sebebi: o illerde fiziksel bir işletme yok. 81 ile MedicalClinic kopyalamak,
Google'a var olmayan 81 şube bildirmek anlamına gelir; bu doğrudan sahte
yerel işletme sinyalidir ve manuel işlem riski taşır.
Bunun yerine `Service` + `areaServed` kullanılır — "bu hizmet o ile veriliyor"
demenin doğru ve dürüst yolu budur.
"""
import json
import turkce as T
from content import SITE, DYT, TEL_HREF, TEL_GORUNEN, WA

# 1280x720 — CLS önlemek için sabit oran
GORSELLER = [
    ("online-diyetisyen1.webp", "video görüşmeyle yürütülen online diyetisyen danışmanlığı"),
    ("en-iyi-online-diyetisyen.webp", "kişiye özel beslenme planı hazırlanan online diyetisyen görüşmesi"),
    ("online-diyetisyen-tugba-seker.webp", f"{DYT} — beslenme ve diyet uzmanı"),
    ("online-diyetisyen-iletisim.webp", "online diyetisyen randevusu için iletişim"),
    ("online-diyetisyen-numarasi.webp", "online diyetisyen görüşme hattı"),
]


def _karistir(tohum, i):
    """32-bit karıştırma. Düz çarpım kullanılamaz: küçük i değerlerinde çarpım
    monoton arttığı için modulo hiç devreye girmez ve her tohum aynı sırayı verir."""
    x = (tohum * 2654435761 + i * 2246822519) & 0xFFFFFFFF
    x ^= (x >> 15)
    x = (x * 2246822519) & 0xFFFFFFFF
    x ^= (x >> 13)
    return x


def gorsel_sec(tohum, adet):
    """Sayfaya deterministik ama farklı görsel kümesi atar (1-4 arası)."""
    n = len(GORSELLER)
    sira = sorted(range(n), key=lambda i: _karistir(tohum, i))
    return [GORSELLER[i] for i in sira[:max(1, min(adet, n))]]


def gorsel_html(dosya, alt, baslik_alti=None, lazy=True, aranabilir=True):
    """Görseli tel: bağlantısına sarar — görsele tıklayan arama başlatır.

    aria-label ekran okuyucuya eylemi bildirir: görsel dekoratif değil,
    tıklanınca arama başlatan bir bağlantı.
    """
    cap = f"<figcaption>{baslik_alti}</figcaption>" if baslik_alti else ""
    yukleme = 'loading="lazy" decoding="async"' if lazy else 'fetchpriority="high" decoding="async"'
    img = (f'<img src="{SITE}/images/{dosya}" alt="{alt}" '
           f'width="1280" height="720" {yukleme}>')
    if aranabilir:
        img = (f'<a class="gorsel-ara" href="{TEL_HREF}" '
               f'aria-label="Telefonla ara: {TEL_GORUNEN}">{img}'
               f'<span class="ara-rozet">📞 Hemen ara</span></a>')
    return f'<figure class="lok-gorsel">{img}{cap}</figure>'


# --------------------------------------------------------------------- SCHEMA
def schema_bloklari(*, url, baslik, aciklama, kirintilar, sss, alan_adi, alan_tipi,
                    guncelleme, ana_gorsel):
    """kirintilar: [(ad, url), ...] | sss: [(soru, cevap), ...]"""
    g = [{
        "@context": "https://schema.org", "@type": "WebPage",
        "@id": url + "#webpage", "url": url, "name": baslik, "description": aciklama,
        "inLanguage": "tr-TR", "dateModified": guncelleme,
        "isPartOf": {"@type": "WebSite", "@id": SITE + "/#website",
                     "name": "Online Diyetisyen", "url": SITE + "/"},
        "primaryImageOfPage": {"@type": "ImageObject", "url": f"{SITE}/images/{ana_gorsel}",
                               "width": 1280, "height": 720},
        "about": {"@id": SITE + "/#hizmet"},
        # Sayfanın sorumlusu — gerçek, doğrulanabilir kişi
        "reviewedBy": {"@id": SITE + "/#tugba"},
    }, {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": ad, "item": u}
            for i, (ad, u) in enumerate(kirintilar)
        ],
    }, {
        # Hizmetin kendisi — areaServed ile lokasyon bağı DÜRÜST biçimde kurulur
        "@context": "https://schema.org", "@type": "Service",
        "@id": url + "#service",
        "serviceType": "Online diyetisyen ve beslenme danışmanlığı",
        "name": baslik,
        "provider": {"@id": SITE + "/#tugba"},
        "areaServed": {"@type": alan_tipi, "name": alan_adi,
                       "containedInPlace": {"@type": "Country", "name": "Türkiye"}},
        "availableChannel": {
            "@type": "ServiceChannel",
            "serviceUrl": SITE + "/#iletisim",
            "servicePhone": {"@type": "ContactPoint", "telephone": "+90 507 036 18 59"},
            "serviceLocation": {"@type": "VirtualLocation", "url": SITE + "/#iletisim"},
        },
    }, {
        "@context": "https://schema.org", "@type": "Person",
        "@id": SITE + "/#tugba", "name": "Tuğba Şeker Ağaç", "jobTitle": "Diyetisyen",
        "url": SITE + "/",
        "alumniOf": {"@type": "CollegeOrUniversity", "name": "Erciyes Üniversitesi",
                     "department": "Sağlık Bilimleri Fakültesi Beslenme ve Diyetetik Bölümü"},
        "knowsAbout": ["beslenme danışmanlığı", "kilo yönetimi", "insülin direncinde beslenme",
                       "PCOS beslenmesi", "sporcu beslenmesi"],
    }]
    if sss:
        g.append({
            "@context": "https://schema.org", "@type": "FAQPage",
            "@id": url + "#faq",
            "mainEntity": [
                {"@type": "Question", "name": s,
                 "acceptedAnswer": {"@type": "Answer", "text": c}}
                for s, c in sss
            ],
        })
    return "\n".join(
        '<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False) + "</script>"
        for x in g
    )


# --------------------------------------------------------------------- KABUK
HEADER = f'''<header class="nav" id="nav">
  <div class="wrap nav-inner">
    <a href="/" class="logo" aria-label="Online Diyetisyen - {DYT}">
      <img class="logo-img" src="{SITE}/images/online-diyetisyen-logo.png" alt="Online Diyetisyen - {DYT}" width="1024" height="304">
    </a>
    <nav class="menu" id="menu">
      <a href="/#hizmetler">Hizmetler</a>
      <a href="/#nasil">Nasıl Çalışır</a>
      <a href="/#fiyatlar">Fiyatlar</a>
      <a href="/#hakkinda">Hakkında</a>
      <a href="/blog/">Blog</a>
      <a href="/#iletisim">İletişim</a>
    </nav>
    <div class="nav-cta"><button class="burger" id="burger" aria-label="Menü"><span></span><span></span><span></span></button></div>
  </div>
</header>'''

WA_METIN = "https://wa.me/905070361859?text=Merhaba%2C%20online%20diyet%20hakk%C4%B1nda%20bilgi%20almak%20istiyorum."

# Ana sayfadaki sağ alt sabit butonlarla birebir aynı işaretleme.
# .wa-float / .call-float stilleri assets/local.css içinde zaten mevcut.
FLOAT_BUTONLAR = f'''<a class="call-float pulse-blue" href="{TEL_HREF}" aria-label="Telefonla Ara">
  <svg viewBox="0 0 24 24" fill="currentColor"><path d="M20.01 15.38c-1.23 0-2.42-.2-3.53-.56-.35-.12-.74-.03-1.01.24l-1.57 1.97c-2.83-1.35-5.48-3.9-6.89-6.83l1.95-1.66c.27-.28.35-.67.24-1.02-.37-1.11-.56-2.3-.56-3.53 0-.54-.45-.99-.99-.99H4.19C3.65 3 3 3.24 3 3.99 3 13.28 10.73 21 20.01 21c.71 0 .99-.63.99-1.18v-3.45c0-.54-.45-.99-.99-.99z"/></svg>
</a>
<a class="wa-float pulse" href="{WA_METIN}" target="_blank" rel="noopener" aria-label="WhatsApp">
  <svg viewBox="0 0 32 32" fill="currentColor"><path d="M16 .5C7.4.5.5 7.4.5 16c0 2.8.7 5.4 2 7.7L.5 31.5l8-2.1c2.2 1.2 4.8 1.9 7.5 1.9 8.6 0 15.5-6.9 15.5-15.5S24.6.5 16 .5zm0 28.2c-2.4 0-4.7-.6-6.7-1.8l-.5-.3-4.7 1.2 1.3-4.6-.3-.5a12.6 12.6 0 0 1-1.9-6.7C3 8.8 8.8 3 16 3s13 5.8 13 13-5.8 12.7-13 12.7zm7.1-9.5c-.4-.2-2.3-1.1-2.6-1.3-.3-.1-.6-.2-.8.2-.2.4-.9 1.3-1.2 1.5-.2.2-.4.3-.8.1-.4-.2-1.6-.6-3.1-1.9-1.1-1-1.9-2.3-2.1-2.7-.2-.4 0-.6.2-.8.2-.2.4-.4.5-.7.2-.2.2-.4.4-.7.1-.3 0-.5 0-.7-.1-.2-.8-2-1.1-2.7-.3-.7-.6-.6-.8-.6h-.7c-.2 0-.6.1-.9.5-.3.4-1.2 1.2-1.2 2.9s1.2 3.4 1.4 3.6c.2.2 2.4 3.7 5.9 5.2.8.4 1.5.6 2 .7.8.3 1.6.2 2.2.1.7-.1 2.3-.9 2.6-1.8.3-.9.3-1.6.2-1.8-.1-.1-.3-.2-.7-.4z"/></svg>
</a>'''


# Hero altındaki eylem butonları — ana sayfadaki .hero-cta ile aynı sınıflar.
HERO_CTA = f'''<div class="hero-cta lok-hero-cta">
  <a class="btn btn-wa btn-lg pulse" href="{WA_METIN}" target="_blank" rel="noopener">💬 Ücretsiz Ön Görüşme</a>
  <a class="btn btn-ghost btn-lg" href="{TEL_HREF}">📞 {TEL_GORUNEN}</a>
</div>'''


FOOTER = f'''<footer class="site">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-brand">
        <a href="/" class="logo" style="color:#fff"><span class="mark">🥗</span><span style="color:#fff">Online Diyetisyen<small style="color:#9bc0aa">{DYT}</small></span></a>
        <p>Türkiye'nin her ilinden, evinizden çıkmadan kişiye özel online diyet ve beslenme danışmanlığı.</p>
      </div>
      <div>
        <h4>Hızlı Menü</h4>
        <a href="/#hizmetler">Hizmetler</a>
        <a href="/#nasil">Nasıl Çalışır</a>
        <a href="/#fiyatlar">Fiyatlar</a>
        <a href="/blog/">Blog</a>
        <a href="/online-diyetisyen/">İllere Göre Online Diyetisyen</a>
      </div>
      <div>
        <h4>İletişim</h4>
        <a href="{TEL_HREF}">📞 {TEL_GORUNEN}</a>
        <a href="{WA}" target="_blank" rel="noopener">💬 WhatsApp</a>
        <a href="/#iletisim">📍 Adana &amp; Online</a>
      </div>
    </div>
    <div class="foot-bottom">
      <span>© <span id="yil">2026</span> Online Diyetisyen — {DYT}. Tüm hakları saklıdır.</span>
      <span>www.onlinediyetisyen.online</span>
    </div>
  </div>
</footer>
<script>
document.getElementById('yil').textContent=new Date().getFullYear();
var b=document.getElementById('burger'),m=document.getElementById('menu');
if(b&&m)b.addEventListener('click',function(){{m.classList.toggle('acik');}});
addEventListener('scroll',function(){{document.getElementById('nav').classList.toggle('scrolled',scrollY>10);}});
</script>'''


def kirinti_html(kirintilar):
    ic = ' <span class="sep">›</span> '.join(
        (f'<a href="{u}">{ad}</a>' if i < len(kirintilar) - 1 else f"<span>{ad}</span>")
        for i, (ad, u) in enumerate(kirintilar)
    )
    return f'<nav class="crumb" aria-label="Sayfa yolu"><div class="wrap">{ic}</div></nav>'


def sayfa(*, url, baslik, aciklama, h1, hero_alt, kirintilar, govde, schema, guncelleme):
    return f'''<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script async src="https://www.web4medya.com/w4t.js" data-key="w4-7ng86yxtkw3b3u1a"></script>
<title>{baslik}</title>
<meta name="description" content="{aciklama}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="author" content="{DYT}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:title" content="{baslik}">
<meta property="og:description" content="{aciklama}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/images/{hero_alt}">
<meta property="og:locale" content="tr_TR">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#1f7a4d">
<link rel="icon" href="{SITE}/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{SITE}/assets/local.css">
{schema}
</head>
<body>
{HEADER}
{kirinti_html(kirintilar)}
<main>
{govde}
</main>
{FOOTER}
{FLOAT_BUTONLAR}
</body>
</html>'''
