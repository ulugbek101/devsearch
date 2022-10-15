from django.forms import ModelForm
from django import forms
from django.db import models

# from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Project, Review


class ProjectForm(ModelForm):
    # description = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Project
        fields = ['title', 'image', 'description',
                  'demo_link', 'source_link']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        # self.fields['tags'].widget.attrs.update({'class': 'input'})
        for key, value in self.fields.items():
            value.widget.attrs.update({'class': 'input'})


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ('text', )

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({
            'class': 'input input--text',
        })
