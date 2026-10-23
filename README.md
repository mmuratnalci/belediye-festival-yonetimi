# Belediye Festival Yönetimi Simülatörü

Festival türü, bütçe, süre ve tanıtım seçimine göre varsayımsal giderleri, kalan bütçeyi, ziyaretçi tahminini, organizasyon ve sürdürülebilirlik puanlarını gösteren Türkçe Streamlit uygulaması.

## Çalıştırma

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

Streamlit'in verdiği yerel adresi tarayıcıda açın (genellikle `http://localhost:8501`).

## Hesaplama varsayımları

- Giderler; 35.000 TL sabit koordinasyon gideri, festival türüne göre günlük program/teknik, alan/altyapı ve güvenlik/temizlik giderleri ile sabit tanıtım giderinin toplamıdır.
- Günlük gider varsayımları müzik için 175.000 TL, gastronomi için 145.000 TL ve kültür-sanat için 130.000 TL'dir.
- Günlük ziyaretçi varsayımları sırasıyla 2.800, 3.200 ve 1.900'dür. Tanıtım katsayıları belediye kanalları için 1, yerel medya için 1,15, çok kanallı tanıtım için 1,3'tür.
- Başarı puanı; bütçe yeterliliği (en çok 50), tanıtım (15/20/25), süre (15/12/9) ve kalan bütçe rezervi (10/5/0) puanlarının toplamıdır; sonuç 100 ile sınırlandırılır.
- Sürdürülebilirlik puanı 50 temel puandan başlar; atık ayrıştırma/yeniden kullanılabilir servis, toplu taşıma/bisiklet erişimi, enerji tasarrufu/yenilenebilir enerji ve yerel tedarik uygulamalarının her biri 12,5 puan ekler. Tahmini ziyaretçi sayısı her 250 kişi için 1 puan (en çok 20), ilk günü aşan her festival günü ise 3 puan düşürür. Sonuç 0–100 aralığında tutulur.

**Tüm gider, ziyaretçi ve puan tahminleri eğitim amaçlı ve varsayımsaldır; sürdürülebilirlik puanı ölçülmüş karbon ayak izi veya çevresel etki hesabı değildir. Gerçek teklif veya sonuç değildir.**