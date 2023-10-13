from flask import render_template, request, redirect, flash, session 
from flask_app import app
from flask_app.models.appointment import Appointment

@app.route('/post_appointment', methods=['POST', 'GET'])
def post_appointment():
    if request.method == 'POST':
        nombre = request.form.get('nombreTarea') 
        fecha = request.form.get('fechaTarea')   
        estado = request.form.get('estadoTarea') 
        
        if not nombre or not fecha or not estado:
            flash('Por favor, complete todos los campos.', 'error')
            return redirect('/post_appointment')
        
        data = {
            'task': nombre,
            'date': fecha,
            'status': estado,
            'users_id': 1 
        }
        appointment = Appointment.save(data)
        
        flash('Tarea creada con éxito.', 'success')
        return redirect('/dashboard')  
    else:
        return render_template('create_tarea.html')

@app.route("/delete/appointment/<int:appointment_id>")
def delete_appointment(appointment_id):

    Appointment.destroy(appointment_id)
    return redirect("/dashboard")

@app.route('/edit_appointment/<int:appointment_id>', methods=['GET', 'POST'])
def edit_appointment(appointment_id):
    if 'user_id' not in session:
        return redirect('/logout')

    user_id = session['user_id']

    appointment = Appointment.get_by_id(appointment_id)

    if appointment.user_id != user_id:
        flash("No tienes permiso para editar esta cita")
        return redirect('/dashboard')

    if request.method == 'POST':
        new_task = request.form['new_task']
        new_date = request.form['new_date']
        new_status = request.form['new_status']

        data = {
            'task': new_task,
            'date': new_date,
            'status': new_status,
            'id': appointment_id
        }
        Appointment.update(data)

        flash("Cita editada con éxito")
        return redirect('/dashboard')

    return render_template("edit_tarea.html", appointment=appointment)