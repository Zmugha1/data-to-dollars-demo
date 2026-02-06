# Project spec: Data to $$$ Revenue Leak Detector

---

## 1. Business context

### The $387K Leak (Real Scenario)

We analyzed **5,000 synthetic Amazon-style transactions** using our Revenue Leak Detector. Here is what the models found:

- **R² = 0.9992** — **Regression Engine:** Predicts order values with **$3.88 average error**.
- **94.3%** — **Classification Engine:** Identifies cancellation risk before orders fail.

**The leaks discovered**

- **Discount overkill:** 23% of orders had greater than 20% discounts despite high conversion probability.
- **Shipping waste:** Expedited shipping on low-margin orders eroding profit.
- **Cancellation blindness:** 15% of orders showed pre-purchase cancellation signals that were ignored.

**The fix**

By capping discounts at 15% for high-confidence orders and optimizing shipping logistics, the model projects **$387,000 annual recovery** on a **$2.4M revenue base**.

---

Many businesses lose money without realizing it: too much discount on products that get cancelled, high shipping costs that could be reduced, and orders that look fine today but end up cancelled tomorrow. This app is a **demo** that shows how you can use your order data (and simple analytics) to:

- See where money might be “leaking” (e.g. excess discounts, expensive shipping).
- Spot orders that are **at risk** of being cancelled before they cancel.
- Get **rough dollar estimates** of how much you could save or protect if you act (e.g. cap discounts, fix shipping, or follow up on risky orders).

The demo uses **fake, sample data** only—no real customer or order data is used or uploaded. It is for learning and showing the idea, not for making real business decisions.

---

## 2. What “ROI” and “savings” mean in this app

- **ROI** here means: *if you change the way you run things (e.g. limit discounts, improve shipping, prevent some cancellations), how much money could you save or keep?*
- **Savings** in the app are **estimates**, not guarantees. They answer: *“Roughly how much could we save per year if we did these things?”*

The app shows three kinds of “savings”:

1. **Discount recovery** — Money you keep by not giving more than a certain level of discount (e.g. cap at 15%).
2. **Shipping savings** — Money you save by improving or reducing high shipping costs (e.g. on orders where shipping is over $8).
3. **Risk prevention** — Money you *don’t lose* by preventing some cancellations (e.g. by contacting at-risk customers or not over-discounting products that cancel a lot).

The **total annual savings** you see is the app’s estimate of: *discount recovery + shipping savings + risk prevention* over one year.

---

## 3. How the app works (in plain language)

1. The app loads **sample order data** (thousands of fake orders with categories, prices, discounts, shipping, and whether they were delivered or cancelled).
2. It **learns patterns** from that data (e.g. “high discount + certain categories = more cancellations”).
3. **You choose** what to test: discount cap (e.g. 0.15 = 15%), whether to “optimize” high shipping, and which **categories** to look at (e.g. Clothing, Sports).
4. The app **simulates** what would happen with those choices and shows:
   - How much you might **save** (discount + shipping + risk prevention).
   - How many orders are **at risk** of cancellation and the dollar value of “saving” some of them.

Nothing in the app changes your real business; it only shows **what-if** numbers on sample data.

---

## 4. How to use the demo (step-by-step)

Follow these steps on the live app. No login or upload is required.

### Step 1: Open the app

- Open the app in your browser (e.g. the Streamlit Cloud link you were given).
- Wait for the page to load. You will see a dark blue header with the title **“Data to $$$ Revenue Leak Detector”** and a short line about Dr. Data Decision Intelligence.

### Step 2: Understand the summary at the top

Right under the title, the app shows **baseline numbers** for the sample data:

- **Baseline Revenue** — Total sales in the sample (e.g. about $3.9M).
- **Orders** — Number of orders (e.g. 5,000).
- **Avg Order Value** — Average amount per order (e.g. about $793).
- **Cancellation Rate** — Share of orders that were cancelled (e.g. 14.3%).
- **Model R²** — How well the app’s model fits the data (you can ignore this; it’s just a quality check).

These numbers describe the **sample data**, not your real business.

### Step 3: Use “Scenario controls”

Scroll to the section called **“Scenario controls.”** You will see three things:

1. **Discount cap (e.g. 0.15 = 15 pct)**  
   - This is a **slider**.  
   - It means: *“What if we don’t allow the average discount to go above this?”*  
   - Example: **0.15** = 15%. You can move the slider (e.g. 0.10 = 10%, 0.20 = 20%) and see how the savings change.

2. **Optimize high shipping**  
   - This is a **checkbox**.  
   - If you **check** it, the app assumes you improve or reduce cost for orders with high shipping (e.g. over $8) and shows “shipping savings.”  
   - If you **uncheck** it, the app does not add shipping savings.

3. **Categories to analyze**  
   - This is a **multi-select** list (e.g. Clothing, Sports, Electronics, Books, Home & Kitchen).  
   - **You must pick at least one category.** The app only calculates savings and risk for the categories you select.  
   - Example: Select “Clothing” and “Sports” to see numbers for those two only.

### Step 4: Read the “Impact dashboard”

After you choose at least one category, the app shows an **“Impact dashboard”** with four numbers:

1. **Annual savings (est.)**  
   - This is the **total** amount the app estimates you could save in one year (discount + shipping + risk prevention) for the selected categories.  
   - This is the **main “saved amount”** to look at.

2. **Discount recovery**  
   - The part of that total that comes from **capping discounts** at the level you set.

3. **Shipping savings**  
   - The part that comes from **optimizing high shipping** (only if you checked that box).

4. **Risk prevention**  
   - The part that comes from **preventing some cancellations** (e.g. by acting on at-risk orders).  
   - Below or near this you may see something like **“X orders”** — that is the **number of orders at risk**. The **risk prevention** dollar amount is the value of “saving” those orders.

So:

- **Saved amount** = **Annual savings (est.)** (and the three lines show the breakdown).  
- **At-risk** = the **number of orders** the app flags as likely to cancel, and **Risk prevention** is the dollar value of those orders you could “save” by preventing cancellations.

### Step 5: Read “Decision insights” (if any)

If the numbers are big enough, the app may show short **“Decision insights”** such as:

- “Discount cap is high impact” — meaning capping discount could save a lot.
- “X orders at risk” — meaning the app sees many orders that might cancel; you could focus retention or support there.

These are simple, text-only tips based on the same numbers.

### Step 6: Optional — “Model performance” and “7-step roadmap”

- **Model performance** shows technical quality of the app’s internal model (e.g. R², accuracy). You can skip this if you only care about the dollar numbers.
- **7-step roadmap** is a high-level list of how you’d take this kind of analysis from demo to real use (data, models, rules, monitoring). It’s for context, not something you “do” inside the demo.

### Step 7: Try different settings

- Change the **discount cap** (e.g. 0.10 vs 0.20) and see how **Annual savings** and **Discount recovery** change.  
- Turn **“Optimize high shipping”** on and off and see how **Shipping savings** and **Annual savings** change.  
- Change **categories** (e.g. add Electronics, remove Sports) and see how all the numbers update.

This way you get a feel for **which levers** (discount, shipping, category) affect the **saved amount** and **at-risk amount** most.

---

## 5. Quick reference: what each number means

| What you see            | Meaning in plain language |
|-------------------------|---------------------------|
| **Baseline Revenue**    | Total sales in the sample data. |
| **Orders**              | Number of orders in the sample. |
| **Avg Order Value**     | Average $ per order. |
| **Cancellation Rate**   | Share of orders that were cancelled (e.g. 14.3%). |
| **Annual savings (est.)** | **Total saved amount** per year (discount + shipping + risk prevention) for your scenario. |
| **Discount recovery**   | Part of savings from capping discount. |
| **Shipping savings**     | Part of savings from optimizing high shipping. |
| **Risk prevention**     | Dollar value of “saving” at-risk orders (part of total savings). |
| **High risk orders**     | **At-risk amount** in count: how many orders the app thinks might cancel. |
| **Risk prevention ($)**  | **At-risk amount** in dollars: value of those orders you could keep by preventing cancellations. |

---

## 6. Important disclaimers

- The app uses **synthetic (fake) data** only. No real business data is used or stored.
- All **savings and ROI** numbers are **estimates** for the sample data and the scenario you set. They are not guarantees for your real business.
- This is a **demo** to explain the idea and how to use the interface. Real decisions should use your own data and proper analysis.

---

## 7. Brand and voice

- **Name:** Data to $$$ Revenue Leak Detector (Dr. Data Decision Intelligence).  
- **Voice:** Professional, credible, no fluff.  
- **Colors:** Cream (#FFF8E7), Navy (#2C3E50), Teal (#4ECDC4), Coral (#FF6B6B).

---

*Last updated: project spec for GitHub repo and how-to instructions for layman audience.*
