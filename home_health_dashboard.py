from pathlib import Path
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Home Health | Provider Risk Intelligence",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
.stApp{background:#f3f6f9;color:#172b3a}
.block-container{max-width:1480px;padding-top:1rem;padding-bottom:2.5rem}
.hero{background:linear-gradient(135deg,#17324d 0%,#245f78 58%,#2f7f8d 100%);border-radius:18px;padding:24px 30px 22px;margin-bottom:14px;box-shadow:0 8px 24px rgba(23,50,77,.12)}
.hero-title{color:#fff;font-size:30px;line-height:1.15;font-weight:800;margin:0;letter-spacing:-.4px}
.hero-sub{color:rgba(255,255,255,.86);font-size:13px;margin-top:7px}
.hero-meta{color:rgba(255,255,255,.70);font-size:11px;margin-top:12px}
.section{margin:18px 0 8px;color:#17324d;font-size:18px;font-weight:800;letter-spacing:-.15px}
.section-note{color:#718096;font-size:11px;margin:-3px 0 9px}
.kpi-card{background:#fff;border:1px solid #e2e8ef;border-radius:14px;min-height:112px;padding:15px 16px 13px;box-shadow:0 4px 14px rgba(23,50,77,.06)}
.kpi-label{color:#728096;font-size:10px;font-weight:800;text-transform:uppercase;letter-spacing:.7px}
.kpi-value{color:#17324d;font-size:25px;line-height:1.05;font-weight:850;margin-top:9px}
.kpi-sub{color:#8a96a6;font-size:10.5px;margin-top:7px}
.insight{background:#fff;border:1px solid #e2e8ef;border-left:4px solid #2f7188;border-radius:12px;padding:12px 14px;min-height:75px;box-shadow:0 3px 12px rgba(23,50,77,.045)}
.insight-title{color:#17324d;font-size:11px;font-weight:800;text-transform:uppercase;letter-spacing:.45px}
.insight-text{color:#526173;font-size:12px;line-height:1.45;margin-top:5px}
.filter-head{color:#17324d;font-size:12px;font-weight:800;margin-bottom:-2px}
.footer{color:#8793a1;font-size:10px;text-align:center;padding-top:18px}
div[data-testid="stExpander"]{background:#fff;border:1px solid #e2e8ef;border-radius:12px}
div[data-testid="stVerticalBlock"] > div{gap:.55rem}
</style>
""", unsafe_allow_html=True)

BASE = Path(__file__).resolve().parent
DATA_CANDIDATES = [
    BASE / "home_health_dashboard_final_100k.csv",
    BASE / "home_health_dashboard_analysis_100k.csv",
    BASE / "home_health_dashboard_ready_100k.csv",
]
DATA_FILE = next((p for p in DATA_CANDIDATES if p.exists()), None)

if DATA_FILE is None:
    st.error(
        "Final dashboard CSV not found. Put "
        "'home_health_dashboard_final_100k.csv' in the same folder as "
        "'home_health_dashboard.py'."
    )
    st.stop()

@st.cache_data(show_spinner="Loading 100K provider records...")
def load_data(path):
    data = pd.read_csv(path)
    numeric_cols = [
        "total_episodes_non_lupa",
        "distinct_beneficiaries_non_lupa",
        "average_number_of_total_visits_per_episode_non_lupa",
        "average_number_of_skilled_nursing_visits_per_episode_non_lupa",
        "average_number_of_pt_visits_per_episode_non_lupa",
        "average_number_of_ot_visits_per_episode_non_lupa",
        "average_number_of_st_visits_per_episode_non_lupa",
        "average_number_of_home_health_aide_visits_per_episode_non_lupa",
        "average_number_of_medical_social_visits_per_episode_non_lupa",
        "total_hha_charge_amount_non_lupa",
        "total_hha_medicare_payment_amount_non_lupa",
        "total_hha_medicare_standard_payment_amount_non_lupa",
        "outlier_payments_as_a_percent_of_medicare_payment_amount_non_lupa",
        "total_lupa_episodes",
        "total_hha_medicare_payment_amount_for_lupas",
        "average_age",
        "average_hcc_score",
        "risk_score",
        "payment_gap",
        "payment_to_charge_pct",
        "medicare_payment_per_episode",
        "lupa_episode_rate_pct",
        "beneficiaries_per_episode",
        "high_risk_flag",
    ]
    for col in numeric_cols:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors="coerce")
    if "risk_class" in data.columns:
        data["risk_class"] = data["risk_class"].astype(str)
    return data

df = load_data(str(DATA_FILE))

def fmt_num(x):
    if pd.isna(x):
        return "0"
    x = float(x)
    if abs(x) >= 1_000_000_000:
        return f"{x/1_000_000_000:.1f}B"
    if abs(x) >= 1_000_000:
        return f"{x/1_000_000:.1f}M"
    if abs(x) >= 1_000:
        return f"{x/1_000:.1f}K"
    return f"{x:,.0f}"

def fmt_money(x):
    if pd.isna(x):
        return "$0"
    x = float(x)
    sign = "-" if x < 0 else ""
    x = abs(x)
    if x >= 1_000_000_000:
        return f"{sign}${x/1_000_000_000:.1f}B"
    if x >= 1_000_000:
        return f"{sign}${x/1_000_000:.1f}M"
    if x >= 1_000:
        return f"{sign}${x/1_000:.1f}K"
    return f"{sign}${x:,.0f}"

def fmt_pct(x, decimals=1):
    if pd.isna(x):
        return "0%"
    return f"{float(x):.{decimals}f}%"

def make_fig(fig, height=350, title=None):
    fig.update_layout(
        title=title,
        height=height,
        margin=dict(l=10, r=20, t=52, b=12),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family="Arial, sans-serif", color="#304154", size=11),
        title_font=dict(size=15, color="#17324d"),
        hoverlabel=dict(bgcolor="white", font_size=11),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.01,
            xanchor="right",
            x=1,
            font=dict(size=10),
        ),
    )
    fig.update_xaxes(gridcolor="#edf1f5", zeroline=False)
    fig.update_yaxes(gridcolor="#edf1f5", zeroline=False)
    return fig

RISK_ORDER = ["Low", "Medium", "High"]
RISK_COLORS = {"Low": "#4D8F73", "Medium": "#D39A32", "High": "#C84B4B"}

st.markdown(
    f"""
    <div class="hero">
        <div class="hero-title">🏥 Home Health Provider Risk Intelligence</div>
        <div class="hero-sub">
            Executive view of provider activity, financial performance,
            utilization patterns and risk indicators
        </div>
        <div class="hero-meta">
            Step-22 dashboard dataset • {len(df):,} provider records • 62 analytical fields
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="filter-head">FILTERS</div>', unsafe_allow_html=True)
with st.container(border=True):
    c1, c2, c3, c4 = st.columns([0.9, 0.9, 1.0, 2.1])
    with c1:
        st.markdown("**Risk**")
        risk_filter = st.selectbox(
            "Risk class", ["All"] + RISK_ORDER, label_visibility="collapsed"
        )
    with c2:
        st.markdown("**Geography — State**")
        state_values = sorted(df["state"].dropna().astype(str).unique())
        state_filter = st.selectbox(
            "State", ["All"] + state_values, label_visibility="collapsed"
        )
    state_df = df if state_filter == "All" else df[df["state"].astype(str) == state_filter]
    with c3:
        st.markdown("**Geography — City**")
        city_values = sorted(state_df["city"].dropna().astype(str).unique())
        city_filter = st.selectbox(
            "City", ["All"] + city_values, label_visibility="collapsed"
        )
    with c4:
        st.markdown("**Provider — Agency**")
        agency_search = st.text_input(
            "Agency", placeholder="Search agency name…", label_visibility="collapsed"
        )

f = df.copy()
if risk_filter != "All":
    f = f[f["risk_class"] == risk_filter]
if state_filter != "All":
    f = f[f["state"].astype(str) == state_filter]
if city_filter != "All":
    f = f[f["city"].astype(str) == city_filter]
if agency_search.strip():
    term = agency_search.strip().upper()
    f = f[f["agency_name"].astype(str).str.upper().str.contains(term, na=False)]

if f.empty:
    st.warning("No provider records match the selected filters.")
    st.stop()

providers = f["provider_id"].nunique()
agencies = f["agency_name"].nunique()
episodes = f["total_episodes_non_lupa"].sum()
beneficiaries = f["distinct_beneficiaries_non_lupa"].sum()
payment = f["total_hha_medicare_payment_amount_non_lupa"].sum()
charges = f["total_hha_charge_amount_non_lupa"].sum()
high_risk = (f["risk_class"] == "High").sum()
avg_risk = f["risk_score"].mean()
payment_per_episode = payment / max(episodes, 1)
high_risk_payment = f.loc[
    f["risk_class"] == "High",
    "total_hha_medicare_payment_amount_non_lupa",
].sum()
high_risk_payment_share = high_risk_payment / max(payment, 1) * 100

st.markdown('<div class="section">Executive Snapshot</div>', unsafe_allow_html=True)
st.markdown(
    f'<div class="section-note">Current view: {len(f):,} provider records after filters</div>',
    unsafe_allow_html=True,
)

kpis = [
    ("Providers", fmt_num(providers), "Unique provider records"),
    ("Agencies", fmt_num(agencies), "Organizations represented"),
    ("Episodes", fmt_num(episodes), "Non-LUPA episodes"),
    ("Beneficiaries", fmt_num(beneficiaries), "Distinct beneficiaries"),
    ("Medicare Payments", fmt_money(payment), "Total non-LUPA payment"),
    ("High-Risk Providers", fmt_num(high_risk), f"{high_risk/len(f)*100:.1f}% of current view"),
]
kcols = st.columns(6)
for col, (label, value, sub) in zip(kcols, kpis):
    with col:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
                <div class="kpi-sub">{sub}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown('<div class="section">What Management Should Notice</div>', unsafe_allow_html=True)

state_payment = (
    f.groupby("state", as_index=False)["total_hha_medicare_payment_amount_non_lupa"]
    .sum()
    .sort_values("total_hha_medicare_payment_amount_non_lupa", ascending=False)
)
top_state = state_payment.iloc[0]["state"] if len(state_payment) else "N/A"
top_state_payment = (
    state_payment.iloc[0]["total_hha_medicare_payment_amount_non_lupa"]
    if len(state_payment) else 0
)
ratio_median = f["payment_to_charge_pct"].median()
i1, i2, i3 = st.columns(3)
with i1:
    st.markdown(
        f'<div class="insight"><div class="insight-title">Risk exposure</div>'
        f'<div class="insight-text">High-risk providers represent '
        f'<b>{high_risk_payment_share:.1f}%</b> of Medicare payments in the current view.</div></div>',
        unsafe_allow_html=True,
    )
with i2:
    st.markdown(
        f'<div class="insight"><div class="insight-title">Geographic concentration</div>'
        f'<div class="insight-text"><b>{top_state}</b> is the largest payment market '
        f'with <b>{fmt_money(top_state_payment)}</b> in Medicare payments.</div></div>',
        unsafe_allow_html=True,
    )
with i3:
    st.markdown(
        f'<div class="insight"><div class="insight-title">Unit economics</div>'
        f'<div class="insight-text">Medicare payment averages <b>{fmt_money(payment_per_episode)}</b> '
        f'per non-LUPA episode; median payment-to-charge is <b>{fmt_pct(ratio_median)}</b>.</div></div>',
        unsafe_allow_html=True,
    )

st.markdown('<div class="section">Risk Intelligence</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-note">Where is risk concentrated, and how does risk relate to provider activity?</div>',
    unsafe_allow_html=True,
)

r1, r2 = st.columns([1, 1.15])
with r1:
    risk_summary = (
        f.groupby("risk_class")
        .agg(
            Providers=("provider_id", "nunique"),
            Medicare_Payment=("total_hha_medicare_payment_amount_non_lupa", "sum"),
        )
        .reindex(RISK_ORDER)
        .fillna(0)
        .reset_index()
    )
    fig = px.bar(
        risk_summary,
        x="Providers",
        y="risk_class",
        orientation="h",
        color="risk_class",
        text="Providers",
        color_discrete_map=RISK_COLORS,
        category_orders={"risk_class": RISK_ORDER},
        hover_data={"Providers": ":,", "Medicare_Payment": ":$,.0f"},
    )
    fig.update_traces(texttemplate="%{text:,}", textposition="outside")
    fig.update_layout(showlegend=False)
    make_fig(fig, 355, "Provider Risk Class")
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

with r2:
    fig = px.histogram(
        f,
        x="risk_score",
        color="risk_class",
        nbins=32,
        opacity=0.78,
        color_discrete_map=RISK_COLORS,
        category_orders={"risk_class": RISK_ORDER},
    )
    fig.add_vline(
        x=avg_risk,
        line_dash="dash",
        line_color="#17324d",
        annotation_text=f"Average {avg_risk:.3f}",
        annotation_position="top right",
    )
    fig.update_layout(bargap=0.04)
    make_fig(fig, 355, "Risk Score Distribution")
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

fig = px.bar(
    risk_summary,
    x="risk_class",
    y="Medicare_Payment",
    color="risk_class",
    text="Medicare_Payment",
    color_discrete_map=RISK_COLORS,
    category_orders={"risk_class": RISK_ORDER},
)
fig.update_traces(texttemplate="%{y:$,.3s}", textposition="outside")
fig.update_layout(showlegend=False)
make_fig(fig, 330, "Medicare Payment Exposure by Risk Class")
st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

st.markdown('<div class="section">Financial Performance</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-note">Compare payment concentration and identify unusual payment-to-charge behavior.</div>',
    unsafe_allow_html=True,
)

p1, p2 = st.columns([1.25, 1])
with p1:
    state_pay = (
        f.groupby("state", as_index=False)
        .agg(
            Medicare_Payment=("total_hha_medicare_payment_amount_non_lupa", "sum"),
            Episodes=("total_episodes_non_lupa", "sum"),
        )
        .sort_values("Medicare_Payment", ascending=False)
        .head(12)
    )
    state_pay["Label"] = state_pay["Medicare_Payment"].map(fmt_money)
    fig = px.bar(
        state_pay.sort_values("Medicare_Payment"),
        x="Medicare_Payment",
        y="state",
        orientation="h",
        text="Label",
        color="Medicare_Payment",
        color_continuous_scale=["#b8d1dc", "#245b78"],
        hover_data={"Episodes": ":,"},
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(coloraxis_showscale=False)
    make_fig(fig, 395, "Top States by Medicare Payment")
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

with p2:
    ratio = f["payment_to_charge_pct"].clip(0, 300)
    fig = go.Figure()
    fig.add_trace(
        go.Box(
            x=ratio,
            name="Providers",
            boxmean=True,
            marker=dict(color="#2f7188"),
            line=dict(color="#2f7188"),
            fillcolor="rgba(47,113,136,0.12)",
        )
    )
    fig.add_vline(
        x=ratio.median(),
        line_dash="dash",
        line_color="#C84B4B",
        annotation_text=f"Median {ratio.median():.1f}%",
        annotation_position="top",
    )
    make_fig(fig, 395, "Payment-to-Charge Ratio — Distribution")
    fig.update_layout(xaxis_title="Payment-to-Charge (%)", yaxis_title="", showlegend=False)
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

gap = f["payment_gap"]
gap_q = gap.clip(gap.quantile(0.01), gap.quantile(0.99))
fig = px.histogram(x=gap_q, nbins=35, color_discrete_sequence=["#557f91"])
fig.add_vline(
    x=gap.median(),
    line_dash="dash",
    line_color="#C84B4B",
    annotation_text=f"Median {fmt_money(gap.median())}",
)
make_fig(fig, 320, "Payment Gap Distribution — Charges minus Medicare Payment")
fig.update_layout(xaxis_title="Payment Gap", yaxis_title="Providers")
st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

st.markdown('<div class="section">Operations & Utilization</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-note">Understand provider scale, beneficiary load and visit intensity.</div>',
    unsafe_allow_html=True,
)

o1, o2 = st.columns(2)
with o1:
    qcols = [
        "distinct_beneficiaries_non_lupa",
        "total_episodes_non_lupa",
        "risk_score",
        "risk_class",
        "agency_name",
        "state",
    ]
    q = f[qcols].dropna().sample(min(len(f), 7000), random_state=42)
    fig = px.scatter(
        q,
        x="distinct_beneficiaries_non_lupa",
        y="total_episodes_non_lupa",
        color="risk_class",
        color_discrete_map=RISK_COLORS,
        category_orders={"risk_class": RISK_ORDER},
        hover_data=["agency_name", "state", "risk_score"],
        opacity=0.60,
    )
    make_fig(fig, 390, "Provider Scale — Episodes vs Beneficiaries")
    fig.update_layout(xaxis_title="Distinct Beneficiaries", yaxis_title="Non-LUPA Episodes")
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

with o2:
    q = f[["risk_score", "lupa_episode_rate_pct", "risk_class"]].dropna().sample(
        min(len(f), 7000), random_state=42
    )
    fig = px.scatter(
        q,
        x="risk_score",
        y="lupa_episode_rate_pct",
        color="risk_class",
        color_discrete_map=RISK_COLORS,
        category_orders={"risk_class": RISK_ORDER},
        opacity=0.60,
    )
    make_fig(fig, 390, "Risk Score vs LUPA Episode Rate")
    fig.update_layout(xaxis_title="Risk Score", yaxis_title="LUPA Episode Rate (%)")
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

visit_cols = {
    "average_number_of_skilled_nursing_visits_per_episode_non_lupa": "Skilled Nursing",
    "average_number_of_pt_visits_per_episode_non_lupa": "Physical Therapy",
    "average_number_of_ot_visits_per_episode_non_lupa": "Occupational Therapy",
    "average_number_of_st_visits_per_episode_non_lupa": "Speech Therapy",
    "average_number_of_home_health_aide_visits_per_episode_non_lupa": "Home Health Aide",
    "average_number_of_medical_social_visits_per_episode_non_lupa": "Medical Social",
}
available_visit = [c for c in visit_cols if c in f.columns]
if available_visit:
    visit_avg = f[available_visit].mean().sort_values(ascending=False).rename(index=visit_cols).reset_index()
    visit_avg.columns = ["Visit Type", "Average Visits"]
    fig = px.bar(
        visit_avg,
        x="Average Visits",
        y="Visit Type",
        orientation="h",
        text="Average Visits",
    )
    fig.update_traces(texttemplate="%{text:.1f}", textposition="outside")
    make_fig(fig, 350, "Average Visits per Non-LUPA Episode")
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

st.markdown('<div class="section">Beneficiary & Clinical Profile</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-note">Population characteristics and condition prevalence available in the dataset.</div>',
    unsafe_allow_html=True,
)

c1, c2 = st.columns([1, 1.25])
with c1:
    demographic = {
        "male_beneficiaries": "Male",
        "female_beneficiaries": "Female",
        "nondual_beneficiaries": "Non-Dual",
        "dua_beneficiaries": "Dual",
    }
    available_demo = [c for c in demographic if c in f.columns]
    if available_demo:
        demo = f[available_demo].sum().rename(index=demographic).reset_index()
        demo.columns = ["Group", "Beneficiaries"]
        fig = px.bar(
            demo.sort_values("Beneficiaries"),
            x="Beneficiaries",
            y="Group",
            orientation="h",
            text="Beneficiaries",
        )
        fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
        make_fig(fig, 350, "Beneficiary Composition")
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

with c2:
    clinical_map = {
        "percent_of_beneficiaries_with_atrial_fibrillation": "Atrial Fibrillation",
        "percent_of_beneficiaries_with_alzheimers": "Alzheimer's",
        "percent_of_beneficiaries_with_asthma": "Asthma",
        "percent_of_beneficiaries_with_cancer": "Cancer",
        "percent_of_beneficiaries_with_chf": "CHF",
        "percent_of_beneficiaries_with_chronic_kidney_disease": "Chronic Kidney Disease",
        "percent_of_beneficiaries_with_copd": "COPD",
        "percent_of_beneficiaries_with_depression": "Depression",
        "percent_of_beneficiaries_with_diabetes": "Diabetes",
        "percent_of_beneficiaries_with_hyperlipidemia": "Hyperlipidemia",
        "percent_of_beneficiaries_with_ihd": "IHD",
        "percent_of_beneficiaries_with_osteoporosis": "Osteoporosis",
        "percent_of_beneficiaries_with_ra_oa": "RA / OA",
        "percent_of_beneficiaries_with_schizophrenia": "Schizophrenia",
        "percent_of_beneficiaries_with_stroke": "Stroke",
    }
    available_clinical = [c for c in clinical_map if c in f.columns]
    if available_clinical:
        clinical = f[available_clinical].mean().sort_values(ascending=False).rename(index=clinical_map).reset_index()
        clinical.columns = ["Condition", "Average %"]
        fig = px.bar(
            clinical.sort_values("Average %"),
            x="Average %",
            y="Condition",
            orientation="h",
            text="Average %",
        )
        fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        make_fig(fig, 430, "Average Beneficiary Condition Prevalence")
        fig.update_layout(xaxis_title="Average beneficiary share (%)", showlegend=False)
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

age = f["average_age"].mean()
hcc = f["average_hcc_score"].mean()
lupa_avg = f["lupa_episode_rate_pct"].mean()
a1, a2, a3 = st.columns(3)
a1.metric("Average Age", f"{age:.1f}")
a2.metric("Average HCC Score", f"{hcc:.2f}")
a3.metric("Average LUPA Rate", fmt_pct(lupa_avg))

st.markdown('<div class="section">High-Risk Provider Watchlist</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-note">Prioritize review of providers with the highest model-generated risk scores. Risk is an analytical flag, not a finding of fraud.</div>',
    unsafe_allow_html=True,
)

watch_cols = [
    "provider_id",
    "agency_name",
    "city",
    "state",
    "total_episodes_non_lupa",
    "distinct_beneficiaries_non_lupa",
    "total_hha_medicare_payment_amount_non_lupa",
    "payment_to_charge_pct",
    "lupa_episode_rate_pct",
    "risk_score",
    "risk_class",
]
watch_cols = [c for c in watch_cols if c in f.columns]
watch = f.sort_values("risk_score", ascending=False)[watch_cols].head(15).copy()

watch.rename(
    columns={
        "provider_id": "Provider ID",
        "agency_name": "Agency",
        "city": "City",
        "state": "State",
        "total_episodes_non_lupa": "Episodes",
        "distinct_beneficiaries_non_lupa": "Beneficiaries",
        "total_hha_medicare_payment_amount_non_lupa": "Medicare Payment",
        "payment_to_charge_pct": "Pay / Charge %",
        "lupa_episode_rate_pct": "LUPA Rate %",
        "risk_score": "Risk Score",
        "risk_class": "Risk Class",
    },
    inplace=True,
)

watch["Medicare Payment"] = watch["Medicare Payment"].map(fmt_money)
watch["Pay / Charge %"] = watch["Pay / Charge %"].map(lambda x: f"{x:.1f}%")
watch["LUPA Rate %"] = watch["LUPA Rate %"].map(lambda x: f"{x:.1f}%")
watch["Risk Score"] = watch["Risk Score"].round(3)

st.dataframe(
    watch,
    width="stretch",
    hide_index=True,
    height=455,
    column_config={
        "Provider ID": st.column_config.TextColumn("Provider ID"),
        "Episodes": st.column_config.NumberColumn("Episodes", format="%,d"),
        "Beneficiaries": st.column_config.NumberColumn("Beneficiaries", format="%,d"),
        "Risk Score": st.column_config.NumberColumn("Risk Score", format="%.3f"),
    },
)

with st.expander("How to read this dashboard"):
    st.markdown(
        """
        **Risk:** `risk_score` and `risk_class` are the project's analytical risk indicators.
        High risk means the provider is prioritized for review; it does not by itself establish fraud.

        **Financial:** Payment-to-charge and payment gap highlight payment relationships
        that deserve investigation. Extreme values should be reviewed together with provider
        volume and utilization rather than interpreted in isolation.

        **Operations:** Episodes, beneficiaries, visits and LUPA rate describe provider
        activity and utilization intensity.

        **Clinical:** Condition percentages and HCC score describe the beneficiary profile
        available in the final dataset. They are descriptive context, not causal explanations
        for provider risk.
        """
    )

st.markdown(
    f'<div class="footer">Home Health Provider Risk & Financial Analytics • '
    f'Final Step-22 dataset • {len(df):,} provider records • Current view: {len(f):,} records</div>',
    unsafe_allow_html=True,
)
