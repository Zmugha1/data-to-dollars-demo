import pandas as pd
import numpy as np
from pathlib import Path

np.random.seed(42)
n = 5000

categories = ['Electronics', 'Home & Kitchen', 'Books', 'Clothing', 'Sports']
payment_methods = ['Credit Card', 'Debit Card', 'Amazon Pay', 'Cash on Delivery']
statuses = ['Delivered', 'Cancelled', 'Returned', 'Pending']
countries = ['United States', 'India', 'UK', 'Canada', 'Germany']

data = {
    'OrderID': [f'ORD{i:07d}' for i in range(1, n+1)],
    'OrderDate': pd.date_range('2023-01-01', periods=n, freq='h').tolist(),
    'Category': np.random.choice(categories, n),
    'Quantity': np.random.randint(1, 6, n),
    'UnitPrice': np.round(np.random.uniform(5, 600, n), 2),
    'Discount': np.round(np.random.uniform(0, 0.30, n), 2),
    'ShippingCost': np.round(np.random.uniform(0, 20, n), 2),
    'Tax': np.round(np.random.uniform(0, 50, n), 2),
    'PaymentMethod': np.random.choice(payment_methods, n),
    'OrderStatus': np.random.choice(statuses, n, p=[0.75, 0.15, 0.05, 0.05]),
    'Country': np.random.choice(countries, n)
}

df = pd.DataFrame(data)
df['TotalAmount'] = (df['UnitPrice'] * df['Quantity'] * (1 - df['Discount'])) + df['Tax'] + df['ShippingCost']

# Write to data/ folder (same parent as this script when run from project root or from data/)
out_dir = Path(__file__).resolve().parent
out_path = out_dir / 'amazon_sample.csv'
df.to_csv(out_path, index=False)
print(f"Generated {n} rows at {out_path}")
