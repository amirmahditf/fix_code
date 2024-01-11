from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
import sqlite3
import json

app = Flask(__name__)


@app.route('/home')
def index():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return render_template('index.html', products=products)
# ... [کدهای قبلی]


@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        stock = request.form.get('stock')
        # در صورتی که توضیحات را اضافه کرده‌اید
        description = request.form.get('description')

        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (name, price, quantity, description) VALUES (?, ?, ?, ?)",
                       (name, price, stock, description))  # اضافه کردن توضیحات
        conn.commit()
        conn.close()

        return redirect(url_for('index'))  # برگرداندن کاربر به صفحه اصلی

    return render_template('add_product.html')  # نمایش صفحه اضافه کردن محصول

# ... [کدهای بقیه]


@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    cart_data = request.cookies.get('cart_data', '{}')
    cart_data = json.loads(cart_data)

    if str(product_id) in cart_data:
        cart_data[str(product_id)]['quantity'] += 1
    else:
        cart_data[str(product_id)] = {'quantity': 1}

    response = make_response(redirect(url_for('cart')))
    response.set_cookie('cart_data', json.dumps(cart_data))
    return response


@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart_data = request.cookies.get('cart_data', '{}')
    cart_data = json.loads(cart_data)

    if str(product_id) in cart_data:
        if cart_data[str(product_id)]['quantity'] > 1:
            cart_data[str(product_id)]['quantity'] -= 1
        else:
            del cart_data[str(product_id)]

    response = make_response(redirect(url_for('cart')))
    response.set_cookie('cart_data', json.dumps(cart_data))
    return response


@app.route('/cart')
def cart():
    cart_data = request.cookies.get('cart_data', '{}')
    cart_data = json.loads(cart_data)

    total_price = 0
    cart_items = {}

    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    for product_id, details in cart_data.items():
        cursor.execute(
            "SELECT name, price FROM products WHERE id=?", (int(product_id),))
        product = cursor.fetchone()

        if product:
            cart_items[product_id] = {
                'name': product[0], 'price': product[1], 'quantity': details['quantity']
            }
            total_price += product[1] * cart_items[product_id]['quantity']

    conn.close()
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)


@app.route('/clear_cart_and_update_inventory', methods=['POST'])
def clear_cart_and_update_inventory():
    cart_data = request.cookies.get('cart_data', '{}')
    cart_data = json.loads(cart_data)

    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    try:
        for product_id, details in cart_data.items():
            cursor.execute("UPDATE products SET quantity = quantity - ? WHERE id=?",
                           (details['quantity'], int(product_id)))

        cursor.execute("DELETE FROM products WHERE quantity <= 0")

        conn.commit()
        conn.close()

        response = make_response(jsonify({'success': True}))
        response.set_cookie('cart_data', '{}')
    except Exception as e:
        print(str(e))
        response = jsonify({'success': False})

    return response


if __name__ == '__main__':
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM products WHERE name='محصول 1' OR name='محصول 2'")
    conn.commit()
    conn.close()

    app.run(debug=True)
