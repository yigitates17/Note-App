from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from .models import Note, User, UpdateForm
from . import db
from datetime import datetime

views = Blueprint('views', __name__)


@views.route('/')
def home():
    select_all = db.session.query(User, Note).filter(Note.user_id == User.id).order_by(Note.date.desc()).all()
    return render_template('home.html', user=current_user, all_notes=select_all)


@views.route('/view_notes')
@login_required
def notes():
    return render_template('notes.html', user=current_user)


@views.route('/add_notes', methods=['POST', 'GET'])
@login_required
def add_notes():
    if request.method == 'POST':
        title = request.form.get('title')
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', "warning")
            return render_template('add_notes.html', user=current_user)
        else:
            new_note = Note(data=note, title=title, user_id=current_user.id, date=datetime.now())
            db.session.add(new_note)
            db.session.commit()
            flash("Note is added!", "success")
            return redirect(url_for('views.notes'))

    return render_template('add_notes.html', user=current_user)


@views.route('/delete_note/<string:delete_id>', methods=['POST', 'GET'])
@login_required
def delete_note(delete_id):
    delete = Note.query.filter_by(id=delete_id).first()
    db.session.delete(delete)
    db.session.commit()
    flash(f"The note {delete.title} has been deleted.", "success")
    return redirect(url_for('views.notes'))


@views.route('/edit_note/<string:edit_id>', methods=['POST', 'GET'])
@login_required
def edit_note(edit_id):
    select_note = db.session.query(User, Note).filter(Note.id == edit_id, User.id == Note.user_id).first()

    if request.method == "GET":
        if select_note:
            if select_note[0].id == select_note[1].user_id:
                edit_form = UpdateForm()
                edit_form.title.data = select_note[1].title
                edit_form.content.data = select_note[1].data
                return render_template('edit_note.html', user=current_user, form=edit_form)
            else:
                flash("You don't have permission to perform this.", "danger")
                return redirect(url_for('views.home'))
        else:
            flash("There is no note available in this page.", "danger")
            return redirect(url_for('views.home'))
    else:
        update_note = UpdateForm(request.form)
        new_title = update_note.title.data
        new_content = update_note.content.data
        db.session.query(Note).filter(edit_id == Note.id).update({Note.title: new_title}, synchronize_session=False)
        db.session.query(Note).filter(edit_id == Note.id).update({Note.data: new_content}, synchronize_session=False)
        db.session.query(Note).filter(edit_id == Note.id).update({Note.date: datetime.now()}, synchronize_session=False)
        db.session.commit()
        flash("Your note has been updated.", "success")
        return redirect(url_for('views.notes'))


@views.route('/notes/<string:note_id>', methods=['POST', 'GET'])
@login_required
def note_pages(note_id):
    # selected = Note.query.filter_by(id=note_id).first()
    select_all = db.session.query(Note).filter(Note.id == note_id).first()
    return render_template('note_page.html', user=current_user, the_note=select_all, note_id=note_id)
    pass
