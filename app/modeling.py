import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    r2_score, mean_absolute_error, mean_squared_error
)

class MLEngine:
    def __init__(self, df):
        self.df = df.copy()
        self.le_cat = LabelEncoder()
        self.le_pay = LabelEncoder()
        self.le_status = LabelEncoder()
        self.reg_model = None
        self.clf_model = None
        self.metrics = {}
        self._preprocess()
        self._train_models()

    def _preprocess(self):
        self.df['OrderMonth'] = pd.to_datetime(self.df['OrderDate']).dt.month
        self.df['RevenuePerUnit'] = self.df['TotalAmount'] / self.df['Quantity']
        self.df['CategoryEncoded'] = self.le_cat.fit_transform(self.df['Category'])
        self.df['PaymentEncoded'] = self.le_pay.fit_transform(self.df['PaymentMethod'])
        self.df['StatusEncoded'] = self.le_status.fit_transform(self.df['OrderStatus'])
        self.features = ['Quantity', 'UnitPrice', 'Discount', 'ShippingCost', 'Tax',
                        'CategoryEncoded', 'PaymentEncoded', 'OrderMonth']

    def _train_models(self):
        X = self.df[self.features]
        y_reg = self.df['TotalAmount']
        y_clf = self.df['StatusEncoded']

        X_train, X_test, y_reg_train, y_reg_test, y_clf_train, y_clf_test = train_test_split(
            X, y_reg, y_clf, test_size=0.2, random_state=42
        )

        self.reg_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.reg_model.fit(X_train, y_reg_train)
        y_reg_pred = self.reg_model.predict(X_test)

        self.clf_model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.clf_model.fit(X_train, y_clf_train)
        y_clf_pred = self.clf_model.predict(X_test)

        self.metrics['regression'] = {
            'R2': r2_score(y_reg_test, y_reg_pred),
            'MAE': mean_absolute_error(y_reg_test, y_reg_pred),
            'RMSE': np.sqrt(mean_squared_error(y_reg_test, y_reg_pred))
        }

        self.metrics['classification'] = {
            'Accuracy': accuracy_score(y_clf_test, y_clf_pred),
            'Precision': precision_score(y_clf_test, y_clf_pred, average='weighted', zero_division=0),
            'Recall': recall_score(y_clf_test, y_clf_pred, average='weighted', zero_division=0),
            'F1': f1_score(y_clf_test, y_clf_pred, average='weighted', zero_division=0)
        }

    def get_feature_importance(self):
        importance = pd.DataFrame({
            'feature': self.features,
            'importance': self.reg_model.feature_importances_
        }).sort_values('importance', ascending=False)
        return importance

    def predict_with_confidence(self, input_data):
        reg_pred = self.reg_model.predict(input_data)
        clf_proba = self.clf_model.predict_proba(input_data)
        clf_pred = self.clf_model.predict(input_data)
        return reg_pred, clf_pred, clf_proba
