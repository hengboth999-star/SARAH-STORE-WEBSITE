SARAH STORE WEBSITE STARTER

This ZIP contains a runnable Flask starter website with Khmer customer-facing UI:
- Homepage and four game pages
- Package selection and account-information forms
- SQLite order creation and order list
- Basic admin preview page

IMPORTANT: This is a development starter, NOT a live production store.
No ABA payment, real account lookup, reseller API, automatic delivery, or protected admin login is connected yet. The checkout page clearly labels itself as test mode. Do not accept real customer payments through this starter.

Windows quick start:
1. Extract the ZIP.
2. Open the extracted folder in VS Code.
3. In the VS Code terminal run:
   py -m venv .venv
   .venv\Scripts\activate
   py -m pip install -r requirements.txt
   py app.py
4. Visit http://127.0.0.1:5000

See README_KM.txt for Khmer instructions.
