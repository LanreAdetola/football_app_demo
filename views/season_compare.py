import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_shooting_data, apply_dark_theme, ACCENT_BLUE, ACCENT_ORANGE

st.title("Season Comparison: 24/25 vs 25/26")
st.caption("Compare team shooting performance across both seasons.")

df24 = load_shooting_data("24")
df25 = load_shooting_data("25")

# Only compare teams present in both seasons
common_squads = set(df24["Squad"]) & set(df25["Squad"])
df24 = df24[df24["Squad"].isin(common_squads)].copy()
df25 = df25[df25["Squad"].isin(common_squads)].copy()

df24["Season"] = "24/25"
df25["Season"] = "25/26"

metric = st.selectbox(
    "Compare metric",
    ["Gls", "Sh", "SoT", "Sh/90", "SoT/90", "G/Sh", "G/SoT"],
    format_func=lambda m: {
        "Gls": "Goals", "Sh": "Total Shots", "SoT": "Shots on Target",
        "Sh/90": "Shots per 90", "SoT/90": "Shots on Target per 90",
        "G/Sh": "Goals per Shot", "G/SoT": "Goals per Shot on Target",
    }.get(m, m),
)

combined = pd.concat([
    df24[["Squad", metric, "Season"]],
    df25[["Squad", metric, "Season"]],
])
combined = combined.sort_values(by=metric, ascending=False)

fig = px.bar(
    combined, x="Squad", y=metric, color="Season", barmode="group",
    color_discrete_map={"24/25": ACCENT_BLUE, "25/26": ACCENT_ORANGE},
    title=f"Season Comparison: {metric}",
)
apply_dark_theme(fig)
st.plotly_chart(fig, use_container_width=True)

# Delta table
st.markdown("---")
st.subheader("Change Between Seasons")

merged = df24[["Squad", metric]].merge(
    df25[["Squad", metric]], on="Squad", suffixes=(" 24/25", " 25/26")
)
col_24 = f"{metric} 24/25"
col_25 = f"{metric} 25/26"
merged["Change"] = merged[col_25] - merged[col_24]
merged = merged.sort_values(by="Change", ascending=False)

st.dataframe(
    merged.style.format({col_24: "{:.2f}", col_25: "{:.2f}", "Change": "{:+.2f}"}),
    use_container_width=True,
)
