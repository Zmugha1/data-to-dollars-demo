import pandas as pd
import numpy as np

class RevenueIntelligence:
    def __init__(self, df, ml_engine):
        self.df = df
        self.ml = ml_engine
        self.baseline = {
            'revenue': df['TotalAmount'].sum(),
            'orders': len(df),
            'avg_order_value': df['TotalAmount'].mean(),
            'cancellation_rate': len(df[df['OrderStatus'] == 'Cancelled']) / len(df)
        }

    def calculate_scenario(self, discount_cap, optimize_shipping, selected_categories):
        filtered = self.df[self.df['Category'].isin(selected_categories)].copy()

        if len(filtered) == 0:
            return None

        current_discount_avg = filtered['Discount'].mean()
        discount_savings = 0

        if current_discount_avg > discount_cap:
            excess_discount = current_discount_avg - discount_cap
            discount_savings = excess_discount * filtered['TotalAmount'].sum() * 0.3

        shipping_savings = 0
        if optimize_shipping:
            high_shipping = filtered[filtered['ShippingCost'] > 8]
            shipping_savings = len(high_shipping) * 4.50 * 12

        X_filtered = filtered[self.ml.features]
        _, status_pred, proba = self.ml.predict_with_confidence(X_filtered)

        high_risk_mask = (status_pred == 1) | (proba.max(axis=1) < 0.7)
        high_risk_count = high_risk_mask.sum()
        prevention_value = high_risk_count * filtered['TotalAmount'].mean() * 0.6

        total_annual_impact = (discount_savings + shipping_savings + prevention_value) * 12

        return {
            'annual_savings': total_annual_impact,
            'discount_recovery': discount_savings * 12,
            'shipping_savings': shipping_savings * 12,
            'risk_prevention': prevention_value * 12,
            'high_risk_orders': int(high_risk_count),
            'model_confidence': self.ml.metrics['classification']['Precision'],
            'roi_percentage': (total_annual_impact / self.baseline['revenue']) * 100
        }

    def get_decision_insights(self, scenario_results):
        insights = []

        if scenario_results['discount_recovery'] > 50000:
            insights.append({
                'type': 'High Impact',
                'icon': '🎯',
                'title': 'Discount Cap Strategy',
                'text': f"With {self.ml.metrics['regression']['R2']:.1%} prediction accuracy, capping discounts recovers ${scenario_results['discount_recovery']:,.0f} annually",
                'action': 'Implement dynamic pricing'
            })

        if scenario_results['high_risk_orders'] > 100:
            insights.append({
                'type': 'Risk Alert',
                'icon': '⚠️',
                'title': f"{scenario_results['high_risk_orders']} Orders At Risk",
                'text': f"Model precision ({self.ml.metrics['classification']['Precision']:.1%}) identifies cancellations before they happen",
                'action': 'Trigger retention protocol'
            })

        return insights
