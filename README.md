# A to Z Enterprises — Website

Mobile accessories shop + repair service website.
Built with Flask + MySQL, Black & Gold premium design.

---

## Setup Steps

### 1. Install Python packages
```bash
pip install -r requirements.txt
```

### 2. Create the MySQL database
```bash
mysql -u root -p < schema.sql
```
This creates the `atoz_enterprises` database with tables + sample data.

### 3. Set your MySQL password in app.py
Open `app.py`, find `DB_CONFIG` near the top, and set your password:
```python
"password": "",  # <-- put your MySQL password here
```

### 4. Create your admin login
```bash
flask --app app.py create-admin
```
Type a username and password when prompted.

### 5. Run the website
```bash
python app.py
```
Open browser: http://localhost:5000
Admin panel: http://localhost:5000/admin/login

---

## Project Structure

```
atoz-website/
├── app.py                    Flask backend (all routes)
├── schema.sql                MySQL database + sample data
├── requirements.txt
├── templates/
│   ├── base.html             shared header/footer/nav
│   ├── index.html            homepage
│   ├── products.html         shop with category filter
│   ├── repairs.html          repair services
│   ├── reviews.html          reviews + submission form
│   ├── contact.html          contact + map
│   └── admin/
│       ├── login.html
│       ├── base.html         admin sidebar layout
│       ├── dashboard.html
│       ├── products.html     add/edit/delete products
│       ├── repairs.html      manage repair services
│       ├── reviews.html      approve/delete reviews
│       └── enquiries.html    view customer messages
└── static/
    ├── css/style.css         Black & Gold design
    └── js/main.js
```

## Shop Details (to change: edit SHOP_INFO in app.py)
- Phone 1: 8838519294
- Phone 2: 8248398049
- Email: seshasundharamoorthi2005@gmail.com
- Address: Muthayammal Engg College Opp, Kakaveri, Rasipuram, Namakkal
- Hours: Morning 8:00 AM - Night 10:00 PM
