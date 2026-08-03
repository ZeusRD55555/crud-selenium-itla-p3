import re
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from . import db
from .models import Item, User, Admin

main_bp = Blueprint('main', __name__)

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_id'):
            flash('Debe iniciar sesión para acceder a esta página.', 'warning')
            return redirect(url_for('main.login', next=request.path))
        return f(*args, **kwargs)
    return decorated

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('admin_id'):
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.check_password(password):
            session['admin_id'] = admin.id
            session['admin_username'] = admin.username
            next_url = request.args.get('next') or url_for('main.index')
            flash('Sesión iniciada correctamente.', 'success')
            return redirect(next_url)
        flash('Usuario o contraseña incorrectos.', 'danger')
    return render_template('login.html')

@main_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash('Sesión cerrada.', 'info')
    return redirect(url_for('main.login'))

@main_bp.route('/')
@login_required
def index():
    items = Item.query.order_by(Item.created_at.desc()).all()
    return render_template('index.html', items=items)

@main_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description', '')
        new_item = Item(name=name, description=description)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('create.html')

@main_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    item = Item.query.get_or_404(id)
    if request.method == 'POST':
        item.name = request.form['name']
        item.description = request.form.get('description', '')
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('edit.html', item=item)

@main_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('main.index'))

@main_bp.route('/usuarios')
@login_required
def listar_usuarios():
    q = request.args.get('q', '').strip()
    if q:
        usuarios = User.query.filter(User.nombre.contains(q)).all()
    else:
        usuarios = User.query.all()
    return render_template('listar_usuarios.html', usuarios=usuarios, q=q)

@main_bp.route('/usuarios/crear', methods=['GET', 'POST'])
@login_required
def crear_usuario():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        correo = request.form.get('correo', '').strip()
        telefono = request.form.get('telefono', '').strip()

        errores = []
        if not nombre:
            errores.append('El nombre es obligatorio.')
        if not correo:
            errores.append('El correo es obligatorio.')
        elif not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', correo):
            errores.append('El correo no tiene un formato válido.')
        if not telefono:
            errores.append('El teléfono es obligatorio.')
        elif not re.match(r'^\+?[\d\s\-\(\)]{7,20}$', telefono):
            errores.append('El teléfono no tiene un formato válido.')

        if not errores:
            existe = User.query.filter_by(correo=correo).first()
            if existe:
                errores.append('El correo ya está registrado.')

        if errores:
            for e in errores:
                flash(e, 'danger')
            return render_template('crear_usuario.html', nombre=nombre, correo=correo, telefono=telefono)

        nuevo = User(nombre=nombre, correo=correo, telefono=telefono)
        db.session.add(nuevo)
        db.session.commit()
        flash('Usuario creado exitosamente.', 'success')
        return redirect(url_for('main.crear_usuario'))

    return render_template('crear_usuario.html')

@main_bp.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_usuario(id):
    usuario = User.query.get_or_404(id)
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        correo = request.form.get('correo', '').strip()
        telefono = request.form.get('telefono', '').strip()

        errores = []
        if not nombre:
            errores.append('El nombre es obligatorio.')
        if not correo:
            errores.append('El correo es obligatorio.')
        elif not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', correo):
            errores.append('El correo no tiene un formato válido.')
        if not telefono:
            errores.append('El teléfono es obligatorio.')
        elif not re.match(r'^\+?[\d\s\-\(\)]{7,20}$', telefono):
            errores.append('El teléfono no tiene un formato válido.')

        if not errores and correo != usuario.correo:
            existe = User.query.filter_by(correo=correo).first()
            if existe:
                errores.append('El correo ya está registrado por otro usuario.')

        if errores:
            for e in errores:
                flash(e, 'danger')
        else:
            usuario.nombre = nombre
            usuario.correo = correo
            usuario.telefono = telefono
            db.session.commit()
            flash('Usuario actualizado exitosamente.', 'success')
            return redirect(url_for('main.listar_usuarios'))

    return render_template('editar_usuario.html', usuario=usuario)

@main_bp.route('/usuarios/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_usuario(id):
    usuario = User.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuario eliminado exitosamente.', 'success')
    return redirect(url_for('main.listar_usuarios'))
