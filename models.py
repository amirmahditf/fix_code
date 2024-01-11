import sqlite3

# ایجاد یک اتصال به دیتابیس
conn = sqlite3.connect('products.db')
cursor = conn.cursor()

# اضافه کردن 10 محصول جدید به جدول products
products_to_add = [
    ("موبایل اول", 1500000, 50),
    ("موبایل دوم", 1800000, 40),
    ("موبایل سوم", 2000000, 30),
    ("لپ تاپ اول", 3500000, 20),
    ("لپ تاپ دوم", 4000000, 15),
    ("تبلت اول", 1200000, 25),
    ("تبلت دوم", 1300000, 35),
    ("هدفون اول", 500000, 50),
    ("هدفون دوم", 600000, 45),
    ("اسمارت واچ اول", 900000, 10)
]

# اضافه کردن محصولات به جدول با استفاده از دستور SQL
for product in products_to_add:
    cursor.execute(
        "INSERT INTO products (name, price, stock) VALUES (?, ?, ?)", product)

# ذخیره تغییرات و بستن اتصال
conn.commit()
conn.close()
