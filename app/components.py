"""
Data to $$$ Revenue Leak Detector — UI components.
Brand: Cream #FFF8E7, Navy #2C3E50, Teal #4ECDC4, Coral #FF6B6B
"""
import streamlit as st


def render_hero(baseline, metrics):
    rev = baseline["revenue"]
    orders = baseline["orders"]
    aov = baseline["avg_order_value"]
    cancel_pct = baseline["cancellation_rate"] * 100
    r2_pct = metrics["regression"]["R2"] * 100
    html = (
        "<div style=\"background:#2C3E50;border-radius:16px;padding:32px 40px;margin-bottom:24px;color:#FFF8E7;\">"
        "<h1 style=\"margin:0 0 8px 0;font-size:2rem;font-weight:700;color:#FFF8E7;\">"
        "Data to $$$ Revenue Leak Detector</h1>"
        "<p style=\"margin:0 0 24px 0;opacity:0.9;font-size:1.05rem;\">"
        "Dr. Data Decision Intelligence — ML-powered revenue impact and risk detection</p>"
        "<div style=\"display:flex;flex-wrap:wrap;gap:24px;\">"
        "<div><span style=\"color:#4ECDC4;font-weight:600;\">Baseline Revenue</span>"
        "<div style=\"font-size:1.5rem;font-weight:700;\">${:,.0f}</div></div>"
        "<div><span style=\"color:#4ECDC4;font-weight:600;\">Orders</span>"
        "<div style=\"font-size:1.5rem;font-weight:700;\">{:,.0f}</div></div>"
        "<div><span style=\"color:#4ECDC4;font-weight:600;\">Avg Order Value</span>"
        "<div style=\"font-size:1.5rem;font-weight:700;\">${:,.2f}</div></div>"
        "<div><span style=\"color:#4ECDC4;font-weight:600;\">Cancellation Rate</span>"
        "<div style=\"font-size:1.5rem;font-weight:700;\">{:.1f} pct</div></div>"
        "<div><span style=\"color:#4ECDC4;font-weight:600;\">Model R2</span>"
        "<div style=\"font-size:1.5rem;font-weight:700;\">{:.2f} pct</div></div>"
        "</div></div>"
    ).format(rev, orders, aov, cancel_pct, r2_pct)
    st.markdown(html, unsafe_allow_html=True)


def render_controls(category_list):
    st.subheader("Scenario controls")
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        discount_cap = st.slider(
            "Discount cap (e.g. 0.15 = 15 pct)",
            min_value=0.0,
            max_value=0.30,
            value=0.15,
            step=0.01,
            format="%.2f",
            help="Cap average discount for selected categories",
        )
    with col2:
        optimize_shipping = st.checkbox(
            "Optimize high shipping",
            value=True,
            help="Apply shipping optimization for orders with cost > $8",
        )
    with col3:
        selected_cats = st.multiselect(
            "Categories to analyze",
            options=category_list,
            default=category_list[:2] if len(category_list) >= 2 else category_list,
            help="Select one or more categories",
        )
    return discount_cap, optimize_shipping, selected_cats


def render_impact_dashboard(results, metrics):
    st.markdown("---")
    st.subheader("Impact dashboard")
    r = results
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            "Annual savings (est.)",
            "${:,.0f}".format(r["annual_savings"]),
            "{:.1f} pct of baseline".format(r["roi_percentage"]),
        )
    with col2:
        st.metric("Discount recovery", "${:,.0f}".format(r["discount_recovery"]), "From cap")
    with col3:
        st.metric("Shipping savings", "${:,.0f}".format(r["shipping_savings"]), "Optimization")
    with col4:
        st.metric("Risk prevention", "${:,.0f}".format(r["risk_prevention"]), "{} orders".format(r["high_risk_orders"]))

    conf_pct = r["model_confidence"] * 100
    r2_pct = metrics["regression"]["R2"] * 100
    f1_pct = metrics["classification"]["F1"] * 100
    st.write("**Model confidence (precision):** {:.1f} pct — Estimates based on Random Forest regression (R2 {:.2f} pct) and classification (F1 {:.2f} pct).".format(conf_pct, r2_pct, f1_pct))


def render_model_performance(ml_engine):
    st.markdown("---")
    st.subheader("Model performance")
    reg = ml_engine.metrics["regression"]
    clf = ml_engine.metrics["classification"]
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Regression (revenue prediction)**")
        st.write("R2: {:.3f} | MAE: ${:.2f} | RMSE: ${:.2f}".format(reg["R2"], reg["MAE"], reg["RMSE"]))
    with c2:
        st.markdown("**Classification (order status)**")
        st.write("Accuracy: {:.2f} pct | Precision: {:.2f} pct | Recall: {:.2f} pct | F1: {:.2f} pct".format(
            clf["Accuracy"] * 100, clf["Precision"] * 100, clf["Recall"] * 100, clf["F1"] * 100
        ))

    importance = ml_engine.get_feature_importance()
    st.markdown("**Feature importance (revenue model)**")
    st.dataframe(importance, use_container_width=True, hide_index=True)


def render_decision_insights(insights):
    if not insights:
        return
    st.markdown("---")
    st.subheader("Decision insights")
    for item in insights:
        icon = item.get("icon", "")
        title = item.get("title", "")
        text = item.get("text", "")
        action = item.get("action", "")
        st.write("**{} {}**".format(icon, title))
        st.write(text)
        st.write("→ " + action)


def render_roadmap():
    st.markdown("---")
    st.subheader("7-step roadmap to production")
    steps = [
        ("1", "Data pipeline", "Ingest and validate order data (batch or stream)."),
        ("2", "Feature store", "Compute and store features for ML (discount, shipping, category, etc.)."),
        ("3", "Model training", "Train and version regression + classification models (e.g. Random Forest)."),
        ("4", "Inference API", "Serve predictions (revenue, cancellation risk) via API or job."),
        ("5", "Business rules", "Apply discount cap and shipping rules based on predictions."),
        ("6", "Monitoring", "Track model drift, accuracy, and business KPIs."),
        ("7", "Feedback loop", "Use outcomes (actual revenue, cancellations) to retrain models."),
    ]
    for num, title, desc in steps:
        st.write("**{} {}** — {}".format(num, title, desc))


def render_footer():
    st.markdown("---")
    st.write("**Data to $$$** — Dr. Data Decision Intelligence. Demo uses synthetic data only.")
