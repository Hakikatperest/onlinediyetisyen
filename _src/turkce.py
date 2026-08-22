# -*- coding: utf-8 -*-
"""Türkçe dil yardımcıları.

İki gerçek hata için var:
1) Python'un .title()/.lower() metodu Türkçe "İ" harfini bozar:
   "MERSİN".title() -> "Mersi̇n"  (i + birleşen nokta)
2) Ek uyumu: "Mersin'dan" değil "Mersin'den"; "Sivas'da" değil "Sivas'ta".

Yer adı çekimi yanlış olan bir metin, okuyucuya anında makine üretimi hissi
verir — bu sistemin en çok kaçınması gereken şey.
"""

_BUYUK = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"
_KUCUK = "abcçdefgğhıijklmnoöprsştuüvyz"
_ALT = str.maketrans(_BUYUK, _KUCUK)
_UST = str.maketrans(_KUCUK, _BUYUK)

SESLI = "aeıioöuü"
KALIN = "aıou"
SERT = "fstkçşhp"          # sert ünsüzler → ek sertleşir (-de -> -te)

# Ek almadan önce yazımı değişen / geleneksel kullanımı farklı olan yer adları
ISTISNA = {
    "Kocaeli":    dict(de="Kocaeli'nde", den="Kocaeli'nden", e="Kocaeli'ne"),
    "Kırklareli": dict(de="Kırklareli'nde", den="Kırklareli'nden", e="Kırklareli'ne"),
    "Tunceli":    dict(de="Tunceli'nde", den="Tunceli'nden", e="Tunceli'ne"),
}


def kucult(s):
    return s.translate(_ALT)


def buyult(s):
    return s.translate(_UST)


def baslik(s):
    """Türkçeye uygun başlık biçimi: 'MERSİN' -> 'Mersin', 'IĞDIR' -> 'Iğdır'."""
    out = []
    for kelime in s.split(" "):
        if not kelime:
            out.append(kelime)
            continue
        out.append(buyult(kelime[0]) + kucult(kelime[1:]))
    return " ".join(out)


def _son_sesli(s):
    for ch in reversed(kucult(s)):
        if ch in SESLI:
            return ch
    return "a"


def _son_harf(s):
    k = kucult(s).rstrip("'")
    return k[-1] if k else "a"


def bulunma(ad):
    """-de / -da / -te / -ta  →  'Adana'da', 'Mersin'de', 'Sivas'ta'"""
    if ad in ISTISNA:
        return ISTISNA[ad]["de"]
    ek = "da" if _son_sesli(ad) in KALIN else "de"
    if _son_harf(ad) in SERT:
        ek = "ta" if ek == "da" else "te"
    return f"{ad}'{ek}"


def ayrilma(ad):
    """-den / -dan / -ten / -tan  →  'Adana'dan', 'Mersin'den', 'Sivas'tan'"""
    if ad in ISTISNA:
        return ISTISNA[ad]["den"]
    ek = "dan" if _son_sesli(ad) in KALIN else "den"
    if _son_harf(ad) in SERT:
        ek = "tan" if ek == "dan" else "ten"
    return f"{ad}'{ek}"


def yonelme(ad):
    """-e / -a / -ye / -ya  →  'Adana'ya', 'Mersin'e', 'Bolu'ya'"""
    if ad in ISTISNA:
        return ISTISNA[ad]["e"]
    ek = "a" if _son_sesli(ad) in KALIN else "e"
    if _son_harf(ad) in SESLI:
        ek = "y" + ek
    return f"{ad}'{ek}"


def tamlayan(ad):
    """-nın / -nin / -ın / -in  →  'Adana'nın', 'Mersin'in', 'Bolu'nun'"""
    sesli = _son_sesli(ad)
    ek = {"a": "ın", "ı": "ın", "o": "un", "u": "un",
          "e": "in", "i": "in", "ö": "ün", "ü": "ün"}[sesli]
    if _son_harf(ad) in SESLI:
        ek = "n" + ek
    return f"{ad}'{ek}"
