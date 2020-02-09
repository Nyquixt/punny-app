from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired, FileField
from wtforms.validators import DataRequired
from wtforms import validators, widgets, StringField, SelectMultipleField

from post.models import Post

class MultiCheckboxField(SelectMultipleField):
    option_widget = widgets.CheckboxInput()
    widget = widgets.ListWidget(prefix_label=False)

class UploadForm(FlaskForm):
    title = StringField('Caption', [
        validators.DataRequired(),
        validators.length(min=1, max=100)
    ])

    tags = MultiCheckboxField('Tags',
        [DataRequired(message='Please select tag')],
        choices=[
            ('general', 'General'),
            ('cs', 'CompSci'),
            ('chemistry', 'Chemistry'),
            ('biology', 'Biology'),
            ('physics', 'Physics'),
            ('maths', 'Maths')
        ])
    
    meme = FileField('Meme', 
        validators=[
            FileRequired(),
            FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Must be JPG, JPEG, PNG or GIF')
        ])

    link = StringField('Link Related to Meme Topic')