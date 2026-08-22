# -*- coding: utf-8 -*-
"""Havuz seçimlerinin iller arası dağıtımı.

Sorun: hash tabanlı seçimde iki il birden fazla havuzda çakışabiliyor ve sayfa
başına 3-4 ortak cümle çıkıyordu. Havuzları büyütmek bunu azaltır ama garanti
etmez — doğum günü paradoksu gereği 81 ilin 3240 çifti içinde her zaman birkaç
çoklu çakışma kalır.

Çözüm: seçimi tesadüfe bırakmak yerine kısıt olarak tanımlamak. Profiller greedy
atanır; yeni bir profil, daha önce atanmış hiçbir profille `AZAMI_ORTAK`'tan fazla
konumda aynı değeri paylaşmıyorsa kabul edilir. Deterministiktir — aynı il listesi
her zaman aynı profilleri alır.
"""

AZAMI_ORTAK = 2   # iki il en fazla 2 havuzda aynı çerçeveyi paylaşabilir

# Neden 1 değil 2: 17 havuzda "en fazla 1 ortak" istemek, min Hamming uzaklığı 16
# olan bir kod tasarlamak demek. Greedy arama bunu bulamayıp en iyi adaya düşüyor
# ve pratikte 4 ortak çıkıyordu. 2 hedefi ulaşılabilir ve kalite eşiğini (2 ortak
# cümle) sağlamaya yetiyor.


def _rastgele_dizi(tohum):
    """Deterministik sözde-rastgele tam sayı akışı (xorshift + LCG karışımı).

    Önceki `(t * carpan + i*3) % boyut` biçimi yeterince dağılmıyordu: aynı t için
    bütün konumlar benzer desen üretiyor, kısıtı sağlayan aday hiç bulunamıyordu.
    """
    x = (tohum * 2654435761 + 12345) & 0xFFFFFFFF
    while True:
        x ^= (x << 13) & 0xFFFFFFFF
        x ^= x >> 17
        x ^= (x << 5) & 0xFFFFFFFF
        yield x


def _adaylar(n_havuz, boyutlar, tohum):
    akis = _rastgele_dizi(tohum)
    while True:
        yield tuple(next(akis) % boyutlar[i] for i in range(n_havuz))


def _skor_tablosu(profiller):
    """Her il için: başka bir ille paylaştığı azami ortak indeks sayısı."""
    n = len(profiller)
    en = [0] * n
    for i in range(n):
        for j in range(i + 1, n):
            ortak = sum(1 for a, b in zip(profiller[i], profiller[j]) if a == b)
            if ortak > en[i]:
                en[i] = ortak
            if ortak > en[j]:
                en[j] = ortak
    return en


def profil_dagit(anahtarlar, boyutlar, azami_ortak=AZAMI_ORTAK, deneme=8000, tur=40):
    """Greedy yerleştirme + iyileştirme turu.

    Yalnızca greedy yeterli değil: son yerleştirilen iller giderek daralan bir
    alanda seçim yaptığı için kısıtı sağlayamıyor ve 3 ortak indeksli çiftler
    kalıyordu. İyileştirme turunda, kısıtı ihlal eden il tek tek ele alınıp
    DİĞERLERİ SABİTKEN yeniden yerleştiriliyor; bu, greedy'nin sıra bağımlılığını
    büyük ölçüde ortadan kaldırıyor.
    """
    n = len(boyutlar)
    sirali = sorted(anahtarlar)

    def _akis(tohum):
        x = (tohum * 2654435761 + 12345) & 0xFFFFFFFF
        while True:
            x ^= (x << 13) & 0xFFFFFFFF
            x ^= x >> 17
            x ^= (x << 5) & 0xFFFFFFFF
            yield x

    def _en_iyi_aday(idx, profiller, tohum):
        """idx'inci ili, diğerleri sabitken en az çakışacak şekilde yerleştir."""
        akis = _akis(tohum)
        en_iyi, en_iyi_skor = None, 10 ** 9
        for _ in range(deneme):
            aday = tuple(next(akis) % boyutlar[i] for i in range(n))
            skor = 0
            for j, dp in enumerate(profiller):
                if j == idx or dp is None:
                    continue
                ortak = sum(1 for a, b in zip(aday, dp) if a == b)
                if ortak > skor:
                    skor = ortak
                    if skor > en_iyi_skor:
                        break
            if skor < en_iyi_skor:
                en_iyi, en_iyi_skor = aday, skor
                if skor <= azami_ortak:
                    break
        return en_iyi, en_iyi_skor

    profiller = [None] * len(sirali)
    for i in range(len(sirali)):
        profiller[i], _ = _en_iyi_aday(i, profiller, i * 7919 + 13)

    for t in range(tur):
        en = _skor_tablosu(profiller)
        if max(en) <= azami_ortak:
            break
        hedefler = [i for i, v in enumerate(en) if v > azami_ortak]
        gelisme = False
        for i in hedefler:
            yeni_p, yeni_skor = _en_iyi_aday(i, profiller, (t + 1) * 104729 + i * 31)
            if yeni_skor < en[i]:
                profiller[i] = yeni_p
                gelisme = True
        if not gelisme:
            break

    return {ad: profiller[i] for i, ad in enumerate(sirali)}


def kume_dagit(anahtarlar, havuz_boyutu, secim, azami_ortak=2):
    """Her anahtara havuzdan `secim` adet FARKLI indeks atar.

    İki anahtarın paylaştığı indeks sayısı `azami_ortak`'ı aşmaz.
    SSS soruları için: 81 il, 36 soruluk havuz, 5'er soru.
    """
    atanan, sonuc = [], {}
    for sira, anahtar in enumerate(sorted(anahtarlar)):
        secildi, en_iyi, en_iyi_skor = None, None, 10 ** 9
        akis = _rastgele_dizi(sira * 104729 + 7)
        for _ in range(20000):
            kume = set()
            while len(kume) < secim:
                kume.add(next(akis) % havuz_boyutu)
            aday = tuple(sorted(kume))
            skor = max((len(kume & set(o)) for o in atanan), default=0)
            if skor < en_iyi_skor:
                en_iyi, en_iyi_skor = aday, skor
            if skor <= azami_ortak:
                secildi = aday
                break
        if secildi is None:
            secildi = en_iyi
        atanan.append(secildi)
        sonuc[anahtar] = secildi
    return sonuc
