from flask import url_for, current_app
from fidtasks import mail
import os
from PIL import Image
import secrets
from flask_mail import Message


def send_reset_mail(user):
    token = user.get_reset_token()
    msg = Message(subject='Password Reset Request', sender='fidelismcheeloii@gmail.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)} 
If you did not make this request then simply ignore this email and no changes will be made.'''

    mail.send(msg)
    
    
def save_picture(form_picture):
    random_hex = secrets.token_hex(8) #generate random hex
    _, f_ext = os.path.splitext(form_picture.filename) # Get the file extension from the picture passed into the function
    picture_fn = random_hex + f_ext #Combine the random hex and the picture extension to create a new name for the picture
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn) # Point to the exact location of the picture
    #Resizing image using the Pillow module
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn