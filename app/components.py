"""
Data to $$$ Revenue Leak Detector — UI components.
Brand: Cream #FFF8E7, Navy #2C3E50, Teal #4ECDC4, Coral #FF6B6B
"""
import streamlit as st


def render_hero(baseline, metrics):
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, #2C3E50 0%, #1a252f 100%);
            border-radius: 16px;
            padding: 32px 40px;
            margin-bottom: 24px;
            color: #FFF8E7;
            box-shadow: 0 8px 32px rgba(0,0,0,0.12);
        ">
            <h1 style="margin: 0 0 8px 0; font-size: 2rem; font-weight: 700; color: #FFF8E7;">
                💰 Data to $$$ Revenue Leak Detector
            </h1>
            <p style="margin: 0 0 24px 0; opacity: 0.9; font-size: 1.05rem;">
                Dr. Data Decision Intelligence — ML-powered revenue impact and risk detection
            </p>
            <div style="display: flex; flex-wrap: wrap; gap: 24px;">
                <div>
                    <span style="color: #4ECDC4; font-weight: 600;">Baseline Revenue</span>
                    <div style="font-size: 1.5rem; font-weight: 700;">${:,.0f}</div>
                </div>
                <div>
                    <span style="color: #4ECDC4; font-weight: 600;">Orders</span>
                    <div style="font-size: 1.5rem; font-weight: 700;">{:,.0f}</div>
                </div>
                <div>
                    <span style="color: #4ECDC4; font-weight: 600;">Avg Order Value</span>
                    <div style="font-size: 1.5rem; font-weight: 700;">${:,.2f}</div>
                </div>
                <div>
                    <span style="color: #4ECDC4; font-weight: 600;">Cancellation Rate</span>
                    <div style="font-size: 1.5rem; font-weight: 700;">{:.1%}</div>
                </div>
                <div>
                    <span style="color: #4ECDC4; font-weight: 600;">Model R²</span>
                    <div style="font-size: 1.5rem; font-weight: 700;">{:.2%}</div>
                </div>
            </div>
        </div>
        """.format(
            baseline['revenue'],
            baseline['orders'],
            baseline['avg_order_value'],
            baseline['cancellation_rate'],
            metrics['regression']['R2']
        ),
        unsafe_allow_html=True,
    )


def render_controls(category_list):
    st.subheader("Scenario controls")
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        discount_cap = st.slider(
            "Discount cap (%)",
            min_value=0.0,
            max_value=0.30,
            value=0.15,
            step=0.01,
            format="%.0%%",
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
            f"${r['annual_savings']:,.0f}",
            f"{r['roi_percentage']:.1f}% of baseline",
        )
    with col2:
        st.metric("Discount recovery", f"${r['discount_recovery']:,.0f}", "From cap")
    with col3:
        st.metric("Shipping savings", f"${r['shipping_savings']:,.0f}", "Optimization")
    with col4:
        st.metric("Risk prevention", f"${r['risk_prevention']:,.0f}", f"{r['high_risk_orders']} orders")

    st.markdown(
        """
        <div style="
            background: #FFFFFF;
            border: 1px solid #E0E0E0;
            border-radius: 12px;
            padding: 16px 20px;
            margin-top: 16px;
            color: #2C3E50;
        ">
            <strong style="color: #4ECDC4;">Model confidence (precision):</strong> {:.1%} — 
            Estimates based on Random Forest regression (R² {:.2%}) and classification (F1 {:.2%}).
        </div>
        """.format(
            r['model_confidence'],
            metrics['regression']['R2'],
            metrics['classification']['F1'],
        ),
        unsafe_allow_html=True,
    )


def render_model_performance(ml_engine):
    st.markdown("---")
    st.subheader("Model performance")
    reg = ml_engine.metrics['regression']
    clf = ml_engine.metrics['classification']
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Regression (revenue prediction)**")
        st.write(f"R²: {reg['R2']:.3f} | MAE: ${reg['MAE']:.2f} | RMSE: ${reg['RMSE']:.2f}")
    with c2:
        st.markdown("**Classification (order status)**")
        st.write(f"Accuracy: {clf['Accuracy']:.2%} | Precision: {clf['Precision']:.2%} | Recall: {clf['Recall']:.2%} | F1: {clf['F1']:.2%}")

    importance = ml_engine.get_feature_importance()
    st.markdown("**Feature importance (revenue model)**")
    st.dataframe(importance, use_container_width=True, hide_index=True)


def render_decision_insights(insights):
    if not insights:
        return
    st.markdown("---")
    st.subheader("Decision insights")
    for item in insights:
        st.markdown(
            """
            <div style="
                background: #FFFFFF;
                border-left: 4px solid #4ECDC4;
                border-radius: 8px;
                padding: 16px 20px;
                margin-bottom: 12px;
                color: #2C3E50;
                box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            ">
                <span style="font-size: 1.25rem;">{icon}</span>
                <strong style="color: #2C3E50;">{title}</strong>
                <p style="margin: 8px 0 0 0; opacity: 0.9;">{text}</p>
                <p style="margin: 8px 0 0 0; color: #4ECDC4; font-weight: 600;">→ {action}</p>
            </div>
            """.format(
                icon=item.get('icon', '📌'),
                title=item.get('title', ''),
                text=item.get('text', ''),
                action=item.get('action', ''),
            ),
            unsafe_allow_html=True,
        )


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
        st.markdown(
            """
            <div style="
                display: flex;
                align-items: flex-start;
                gap: 12px;
                margin-bottom: 12px;
                padding: 12px 16px;
                background: #FFFFFF;
                border-radius: 10px;
                border: 1px solid #E8E8E8;
                color: #2C3E50;
            ">
                <span style="
                    background: #4ECDC4;
                    color: #2C3E50;
                    width: 28px;
                    height: 28px;
                    border-radius: 50%;
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    font-weight: 700;
                    flex-shrink: 0;
                ">{num}</span>
                <div>
                    <strong>{title}</strong>
                    <p style="margin: 4px 0 0 0; opacity: 0.85; font-size: 0.95rem;">{desc}</p>
                </div>
            </div>
            """.format(num=num, title=title, desc=desc),
            unsafe_allow_html=True,
        )


def render_footer():
    st.markdown("---")
    st.markdown(
        """
        <div style="
            text-align: center;
            padding: 24px 16px;
            color: #2C3E50;
            opacity: 0.8;
            font-size: 0.9rem;
        ">
            <strong>Data to $$$</strong> — Dr. Data Decision Intelligence. 
            Demo uses synthetic data only. 
            Colors: Cream (#FFF8E7), Navy (#2C3E50), Teal (#4ECDC4), Coral (#FF6B6B).
        </div>
        """,
        unsafe_allow_html=True,
    )
