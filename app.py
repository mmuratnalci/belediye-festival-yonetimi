import streamlit as st


st.set_page_config(
    page_title="Belediye Festival Yönetimi Simülatörü",
    page_icon="🎪",
    layout="wide",
)

FESTIVAL_COSTS = {
    "Müzik": {
        "Program ve teknik": 100_000,
        "Alan ve altyapı": 45_000,
        "Güvenlik ve temizlik": 30_000,
        "Günlük ziyaretçi": 2_800,
    },
    "Gastronomi": {
        "Program ve teknik": 65_000,
        "Alan ve altyapı": 50_000,
        "Güvenlik ve temizlik": 30_000,
        "Günlük ziyaretçi": 3_200,
    },
    "Kültür-sanat": {
        "Program ve teknik": 70_000,
        "Alan ve altyapı": 35_000,
        "Güvenlik ve temizlik": 25_000,
        "Günlük ziyaretçi": 1_900,
    },
}

PROMOTION_OPTIONS = {
    "Belediye kanalları": {"cost": 15_000, "reach": 1.0, "score": 15},
    "Yerel medya": {"cost": 35_000, "reach": 1.15, "score": 20},
    "Çok kanallı tanıtım": {"cost": 60_000, "reach": 1.3, "score": 25},
}

SUSTAINABILITY_MEASURES = {
    "Atık ayrıştırma ve yeniden kullanılabilir servis": 12.5,
    "Toplu taşıma ve bisiklet erişimini teşvik etme": 12.5,
    "Enerji tasarrufu veya yenilenebilir enerji kullanımı": 12.5,
    "Yerel tedarikçi ve mevsimlik ürünleri tercih etme": 12.5,
}


def format_tl(amount):
    return f"{amount:,.0f}".replace(",", ".") + " TL"


st.markdown(
    """
    <style>
    .stApp { background: #f3f5f0; color: #202b27; }
    [data-testid="stSidebar"] { background: #e5ebe3; }
    h1, h2, h3 { font-family: Georgia, 'Times New Roman', serif; color: #173e33; }
    h1 { font-size: 2.35rem; }
    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #dce4da;
        border-top: 3px solid #33745d;
        padding: 1rem;
        border-radius: 5px;
    }
    [data-testid="stMetricValue"] { color: #173e33; }
    .caption { color: #53635b; }
    @media (max-width: 640px) {
        h1 { font-size: 1.8rem; }
        [data-testid="stMetric"] { padding: 0.7rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Belediye Festival Yönetimi Simülatörü")
st.caption("Festival planınızı tahmini bütçe, ziyaret ve organizasyon puanıyla değerlendirin.")
st.info(
    "Bu simülatördeki bütün maliyet ve katılım tahminleri eğitim amaçlı ve varsayımsaldır. "
    "Gerçek piyasa fiyatlarını veya etkinlik sonuçlarını temsil etmez."
)

with st.sidebar:
    st.header("Festival planı")
    festival_type = st.selectbox("Festival türü", list(FESTIVAL_COSTS))
    budget = st.slider(
        "Toplam bütçe",
        min_value=200_000,
        max_value=1_000_000,
        value=500_000,
        step=25_000,
        format="%d TL",
    )
    duration = st.slider("Süre (gün)", min_value=1, max_value=3, value=2, step=1)
    promotion = st.selectbox("Tanıtım yöntemi", list(PROMOTION_OPTIONS))
    sustainability_measures = st.multiselect(
        "Sürdürülebilirlik uygulamaları",
        list(SUSTAINABILITY_MEASURES),
        help="Planda uygulamayı taahhüt ettiğiniz çevre dostu önlemleri seçin.",
    )

festival = FESTIVAL_COSTS[festival_type]
promotion_data = PROMOTION_OPTIONS[promotion]
expenses = {
    "İzin ve koordinasyon": 35_000,
    "Program ve teknik": festival["Program ve teknik"] * duration,
    "Alan ve altyapı": festival["Alan ve altyapı"] * duration,
    "Güvenlik ve temizlik": festival["Güvenlik ve temizlik"] * duration,
    "Tanıtım": promotion_data["cost"],
}
total_cost = sum(expenses.values())
remaining_budget = budget - total_cost
estimated_visitors = round(festival["Günlük ziyaretçi"] * duration * promotion_data["reach"])

budget_score = 50 * min(1, budget / total_cost)
duration_score = {1: 15, 2: 12, 3: 9}[duration]
reserve_score = 10 if remaining_budget >= budget * 0.1 else 5 if remaining_budget > 0 else 0
success_score = round(min(100, budget_score + promotion_data["score"] + duration_score + reserve_score))

sustainability_action_score = sum(
    SUSTAINABILITY_MEASURES[measure] for measure in sustainability_measures
)
sustainability_visitor_penalty = min(20, round(estimated_visitors / 250))
sustainability_duration_penalty = (duration - 1) * 3
sustainability_score = round(
    max(
        0,
        min(
            100,
            50
            + sustainability_action_score
            - sustainability_visitor_penalty
            - sustainability_duration_penalty,
        ),
    )
)

st.subheader("Plan özeti")
metric_columns = st.columns(5)
metric_columns[0].metric("Tahmini gider", format_tl(total_cost))
metric_columns[1].metric("Kalan bütçe", format_tl(remaining_budget))
metric_columns[2].metric("Tahmini ziyaret", f"{estimated_visitors:,}".replace(",", "."))
metric_columns[3].metric("Organizasyon puanı", f"{success_score}/100")
metric_columns[4].metric("Sürdürülebilirlik puanı", f"{sustainability_score}/100")

if remaining_budget < 0:
    st.error(f"Tahmini gider bütçeyi {format_tl(abs(remaining_budget))} aşıyor.")
else:
    st.success("Tahmini gider belirlediğiniz bütçenin içinde.")

st.subheader("Sürdürülebilirlik değerlendirmesi")
st.info(
    f"**Puan açıklaması:** 50 temel puana seçilen her uygulama için 12,5 puan eklenir. "
    f"Tahmini ziyaretçi sayısı için (her 250 ziyaretçide 1 puan, en çok 20) "
    f"ve ilk günü aşan her festival günü için 3 puan düşülür. Bu planda "
    f"{len(sustainability_measures)} uygulamadan {sustainability_action_score:g} puan kazanıldı; "
    f"ziyaretçi baskısı {sustainability_visitor_penalty}, süre etkisi "
    f"{sustainability_duration_penalty} puan düşürdü. "
    "Puan, çevresel planlama göstergesidir; ölçülmüş karbon ayak izi veya çevresel etki hesabı değildir."
)
unselected_measures = [
    measure for measure in SUSTAINABILITY_MEASURES if measure not in sustainability_measures
]
if unselected_measures:
    st.caption("Puanı geliştirmek için değerlendirilebilecek uygulamalar: " + "; ".join(unselected_measures))
else:
    st.caption("Listelenen tüm sürdürülebilirlik uygulamaları seçildi.")

left_column, right_column = st.columns([1.15, 0.85], gap="large")
with left_column:
    st.subheader("Gider dağılımı")
    chart_data = {
        "Gider kalemi": list(expenses),
        "Tahmini tutar (TL)": list(expenses.values()),
    }
    st.bar_chart(chart_data, x="Gider kalemi", y="Tahmini tutar (TL)", horizontal=True)
    st.caption("Günlük operasyon giderleri festival gün sayısıyla çarpılır; koordinasyon ve tanıtım sabit varsayılır.")

with right_column:
    st.subheader("Hesaplama kuralları")
    st.markdown(
        f"""
        - **Gider:** 35.000 TL koordinasyon + türün günlük giderleri × {duration} gün + tanıtım gideri.
        - **Ziyaret:** türün günlük ziyaretçi varsayımı × gün sayısı × tanıtım katsayısı ({promotion_data['reach']:.2f}).
        - **Puan:** bütçe yeterliliği (50), tanıtım (15–25), süre (9–15) ve bütçe rezervi (0–10) bileşenlerinin toplamı; en çok 100.
        - **Sürdürülebilirlik:** 50 temel puan + seçilen uygulamalar (her biri 12,5) − ziyaretçi baskısı (250 ziyaretçide 1, en çok 20) − ilk günden sonraki her gün için 3 puan; 0–100 aralığına sınırlandırılır.
        - **Kalan bütçe:** seçilen bütçe − tahmini gider. Eksi değer bütçe aşımını gösterir.
        """
    )

st.subheader("Gider kalemleri")
for expense_name, amount in expenses.items():
    st.write(f"**{expense_name}:** {format_tl(amount)}")

report_lines = [
    "BELEDİYE FESTİVAL YÖNETİMİ SİMÜLATÖRÜ - TAHMİN RAPORU",
    "=" * 58,
    f"Festival türü: {festival_type}",
    f"Süre: {duration} gün",
    f"Tanıtım yöntemi: {promotion}",
    f"Ayrılan bütçe: {format_tl(budget)}",
    "",
    "TAHMİNİ GİDERLER",
]
report_lines.extend(f"- {name}: {format_tl(amount)}" for name, amount in expenses.items())
report_lines.extend(
    [
        f"Toplam tahmini gider: {format_tl(total_cost)}",
        f"Kalan bütçe: {format_tl(remaining_budget)}",
        f"Tahmini ziyaret: {estimated_visitors:,}".replace(",", "."),
        f"Organizasyon başarı puanı: {success_score}/100",
        f"Sürdürülebilirlik puanı: {sustainability_score}/100",
        "Sürdürülebilirlik uygulamaları: "
        + (", ".join(sustainability_measures) if sustainability_measures else "Seçilmedi"),
        "",
        "SÜRDÜRÜLEBİLİRLİK PUANI AÇIKLAMASI",
        "50 temel puana seçilen her uygulama için 12,5 puan eklenir.",
        f"Ziyaretçi baskısı: {sustainability_visitor_penalty} puan; ilk günü aşan süre etkisi: {sustainability_duration_penalty} puan.",
        "Puan, çevresel planlama göstergesidir; ölçülmüş karbon ayak izi veya çevresel etki hesabı değildir.",
        "",
        "HESAPLAMA NOTU",
        "Günlük operasyon giderleri gün sayısıyla çarpılır; koordinasyon ve tanıtım sabit gider kabul edilir.",
        f"Ziyaret tahmini günlük tür varsayımı x gün sayısı x {promotion_data['reach']:.2f} tanıtım katsayısıdır.",
        "Başarı puanı bütçe yeterliliği, tanıtım, süre ve bütçe rezervi bileşenlerinden hesaplanır.",
        "",
        "UYARI: Bu rapordaki bütün maliyet, katılım ve puan tahminleri eğitim amaçlı ve varsayımsaldır.",
        "Gerçek piyasa fiyatlarını veya etkinlik sonuçlarını temsil etmez.",
    ]
)
st.download_button(
    "Türkçe TXT raporunu indir",
    data="\n".join(report_lines).encode("utf-8"),
    file_name="festival_tahmin_raporu.txt",
    mime="text/plain; charset=utf-8",
    use_container_width=True,
)