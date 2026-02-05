import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from modeling import MLEngine
from calculator import RevenueIntelligence
from components import (
    render_hero, render_controls, render_impact_dashboard,
    render_model_performance, render_decision_insights, render_roadmap, render_footer
)

st.set_page_config(
    page_title="Data to $$$ | Dr. Data Decision Intelligence",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

@st.cache_data
def load_data():
    return pd.read_csv("data/amazon_sample.csv")

@st.cache_resource
def init_ml(df):
    return MLEngine(df)

def main():
    df = load_data()
    ml_engine = init_ml(df)
    calculator = RevenueIntelligence(df, ml_engine)
    
    render_hero(calculator.baseline, ml_engine.metrics)
    
    discount_cap, optimize_shipping, selected_cats = render_controls(
        df['Category'].unique().tolist()
    )
    
    if selected_cats:
        results = calculator.calculate_scenario(
            discount_cap, optimize_shipping, selected_cats
        )
        if results:
            try:
                render_impact_dashboard(results, ml_engine.metrics)
                render_decision_insights(calculator.get_decision_insights(results))
                render_model_performance(ml_engine)
            except KeyError:
                st.error("No results generated - check category selection")
            except Exception:
                st.error("Something went wrong. Check category selection or try again.")
        else:
            st.error("No results generated - check category selection")
    else:
        st.warning("Select at least one category above to see Machine Learning (ML) predictions")
    
    render_roadmap()
    render_footer()

if __name__ == "__main__":
    main()
