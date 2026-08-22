# -*- coding: utf-8 -*-
"""İçerik kalite kontrol ve duplicate önleme motoru.

Kullanıcının 30. ve 42. maddelerindeki kontrolleri ÖLÇÜLEBİLİR hale getirir.
"Bence farklı görünüyor" yerine sayı üretir; eşiği aşan sayfa yayınlanmaz.

Ölçütler
--------
jaccard5   : 5-kelimelik shingle kümeleri üzerinden benzerlik (0..1)
ortak_cumle: iki sayfada birebir aynı geçen cümle sayısı
sablon_orani: sayfanın kaçta kaçı tüm sayfalarda ortak bloklardan oluşuyor
"""
import re
import unicodedata
from collections import Counter

# Yayın eşikleri — aşan sayfa build sırasında REDDEDİLİR
ESIK_JACCARD = 0.40        # iki sayfa arası azami shingle benzerliği
ESIK_ORTAK_CUMLE = 2       # iki sayfada birebir aynı geçebilecek azami cümle
ESIK_SABLON_ORANI = 0.55   # sayfanın azami "ortak blok" payı
ESIK_ORTAK_SSS = 2         # iki sayfada ortak olabilecek azami SSS sorusu
ASGARI_OZGUN_KELIME = 220  # sayfaya özel (o sayfada ilk kez geçen) asgari kelime


def _metin(html, sadece_main=True):
    """HTML'den okunabilir düz metin çıkarır.

    `sadece_main`: header/footer her sayfada aynıdır — bunlar duplicate ölçümüne
    girerse her sayfa yapay olarak benzer görünür. Ölçüm <main> içeriğiyle yapılır;
    <main> yoksa tüm belgeye düşülür.
    """
    if sadece_main:
        m = re.search(r"(?is)<main[^>]*>(.*?)</main>", html)
        if m:
            html = m.group(1)
        # Sayfa mobilyası: her sayfada bulunması GEREKEN, içerik sayılmayan öğeler.
        # (Güncelleme/sorumlu satırı E-E-A-T için zorunlu; duplicate ölçümüne girmemeli.)
        html = re.sub(r'(?is)<p class="guncelleme">.*?</p>', " ", html)
        # SSS ayrı ölçülür: standart bir soruya standart cevap vermek kopya değildir,
        # ama aynı soru setinin sayfalar arası tekrarı da sınırsız olmamalı → ortak_sss()
        html = re.sub(r"(?is)<details class=\"faq\">.*?</details>", " ", html)
    s = re.sub(r"(?is)<(script|style|svg)[^>]*>.*?</\1>", " ", html)
    s = re.sub(r"(?s)<!--.*?-->", " ", s)
    s = re.sub(r"(?s)<[^>]+>", " ", s)
    s = re.sub(r"&[a-z]+;|&#\d+;", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def _normal(s):
    s = unicodedata.normalize("NFKC", s).lower()
    s = s.replace("i̇", "i")
    return re.sub(r"[^\wçğıöşü ]+", " ", s, flags=re.UNICODE)


def kelimeler(html):
    return _normal(_metin(html)).split()


def cumleler(html):
    return [c.strip() for c in re.split(r"(?<=[.!?])\s+", _metin(html)) if len(c.strip()) > 40]


def shingles(html, n=5):
    k = kelimeler(html)
    return {" ".join(k[i:i + n]) for i in range(max(0, len(k) - n + 1))}


def jaccard(a_html, b_html, n=5):
    a, b = shingles(a_html, n), shingles(b_html, n)
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def ortak_cumleler(a_html, b_html):
    return set(cumleler(a_html)) & set(cumleler(b_html))


def sss_sorulari(html):
    return set(re.findall(r"(?is)<summary>(.*?)</summary>", html))


def ortak_sss(a_html, b_html):
    return sss_sorulari(a_html) & sss_sorulari(b_html)


def sayfa_raporu(yol, html, digerleri):
    """Tek sayfa için tam kalite raporu. digerleri: [(yol, html), ...]"""
    kl = kelimeler(html)
    r = dict(yol=yol, kelime=len(kl), sorunlar=[], en_yakin=None, en_yakin_skor=0.0)

    if len(kl) < 300:
        r["sorunlar"].append(f"ince içerik: {len(kl)} kelime")

    for d_yol, d_html in digerleri:
        if d_yol == yol:
            continue
        j = jaccard(html, d_html)
        if j > r["en_yakin_skor"]:
            r["en_yakin_skor"], r["en_yakin"] = j, d_yol
        if j > ESIK_JACCARD:
            r["sorunlar"].append(f"benzerlik {j:.0%} > %{ESIK_JACCARD:.0%} → {d_yol}")
        os_ = ortak_sss(html, d_html)
        if len(os_) > ESIK_ORTAK_SSS:
            r["sorunlar"].append(f"{len(os_)} ortak SSS sorusu → {d_yol}")
        ortak = ortak_cumleler(html, d_html)
        if len(ortak) > ESIK_ORTAK_CUMLE:
            ornek = sorted(ortak, key=len, reverse=True)[0][:70]
            r["sorunlar"].append(f"{len(ortak)} ortak cümle → {d_yol} (örn: “{ornek}…”)")
    return r


def ozgun_kelime_sayisi(html, digerleri):
    """Bu sayfada geçip diğer hiçbir sayfada geçmeyen kelime adedi."""
    k = set(kelimeler(html))
    for _, d_html in digerleri:
        k -= set(kelimeler(d_html))
    return len(k)


def teknik_seo_kontrol(html, url):
    """42. maddedeki teknik denetim — her sayfada zorunlu."""
    p = []
    if html.count("<h1") != 1:
        p.append(f"H1 sayısı {html.count('<h1')} (1 olmalı)")
    if 'rel="canonical"' not in html:
        p.append("canonical yok")
    else:
        m = re.search(r'rel="canonical"\s+href="([^"]+)"', html) or \
            re.search(r'href="([^"]+)"\s+rel="canonical"', html)
        if m and m.group(1).rstrip("/") != url.rstrip("/"):
            p.append(f"canonical uyuşmuyor: {m.group(1)}")
    if not re.search(r'<meta name="description" content="(.{70,165})"', html):
        p.append("description yok veya 70-165 karakter dışında")
    t = re.search(r"<title>(.*?)</title>", html, re.S)
    if not t:
        p.append("title yok")
    elif not (25 <= len(t.group(1)) <= 65):
        p.append(f"title uzunluğu {len(t.group(1))} (25-65 olmalı)")
    if "BreadcrumbList" not in html:
        p.append("breadcrumb schema yok")
    if 'noindex' in html:
        p.append("noindex bulundu")
    if not re.search(r'<img[^>]+alt="[^"]{5,}"', html):
        p.append("anlamlı alt metinli görsel yok")
    return p


def yasakli_ifade_kontrol(html):
    """18. madde — sağlık içeriği güvenliği. Kesin iddia/garanti avı."""
    metin = _normal(_metin(html))
    yasak = [
        "kesin kilo", "garanti kilo", "kesin sonuç", "tedavi eder", "iyileştirir",
        "hastalığı geçirir", "tamamen geçer", "herkes için uygundur", "yan etkisi yoktur",
        "mucize", "kesinlikle zayıflar", "ilaçsız tedavi", "şifa",
    ]
    return [y for y in yasak if y in metin]
