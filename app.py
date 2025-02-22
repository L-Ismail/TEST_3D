from flask import Flask, render_template

app = Flask(__name__)

# Exemple de produits
products = [
    {'id': 1, 'name': 'Produit 1', 'description': 'Description du produit 1', 'image': 'image1.jpg'},
    {'id': 2, 'name': 'Produit 2', 'description': 'Description du produit 2', 'image': 'image2.jpg'},
    {'id': 3, 'name': 'Produit 3', 'description': 'Description du produit 3', 'image': 'image3.jpg'},
]

@app.route('/')
def home():
    return render_template('index.html', products=products)

@app.route('/product/<int:product_id>')
def product(product_id):
    product = next((item for item in products if item['id'] == product_id), None)
    return render_template('product.html', product=product)

if __name__ == '__main__':
    app.run(debug=True)