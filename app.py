# ...

from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

productos = [
    {'id': 1, 'nombre': 'Producto 1', 'precio': 10.0},
    {'id': 2, 'nombre': 'Producto 2', 'precio': 20.0},
    {'id': 3, 'nombre': 'Producto 3', 'precio': 30.0},
]

@app.route('/')
def index():
    carrito = session.get('carrito', [])
    total = sum(producto['precio'] for producto in carrito)
    return render_template('index.html', productos=productos, carrito=carrito, total=total)

@app.route('/agregar/<int:producto_id>')
def agregar_producto(producto_id):
    if 'carrito' not in session:
        session['carrito'] = []
    producto = next((p for p in productos if p['id'] == producto_id), None)
    if producto:
        session['carrito'].append(producto)
    return redirect(url_for('index'))

@app.route('/eliminar/<int:producto_id>')
def eliminar_producto(producto_id):
    if 'carrito' in session:
        session['carrito'] = [p for p in session['carrito'] if p['id'] != producto_id]
    return redirect(url_for('index'))

@app.route('/vaciar_carrito')
def vaciar_carrito():
    session.pop('carrito', None)
    return redirect(url_for('index'))

# Nueva ruta y función para la interfaz de administración
@app.route('/admin')
def admin():
    return render_template('admin.html', productos=productos)

# Nueva ruta y función para agregar productos desde el formulario
@app.route('/admin/agregar_producto', methods=['POST'])
def agregar_producto_admin():
    nombre = request.form.get('nombre')
    precio = float(request.form.get('precio'))
    
    nuevo_producto = {
        'id': len(productos) + 1,
        'nombre': nombre,
        'precio': precio,
    }
    
    productos.append(nuevo_producto)
    
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)
