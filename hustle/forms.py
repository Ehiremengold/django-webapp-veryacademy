from .models import Hustle, Comment, Skill
from django import forms
from mptt.forms import TreeNodeChoiceField


class HustleForm(forms.ModelForm):

    class Meta:
        model = Hustle
        fields = ['hustle_name', 'content', 'category', "travel_availability"]


class HustleFullForm(HustleForm):
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True,
                                                                   "accept": "image/*, video/*"}), required=False)

    class Meta(HustleForm.Meta):
        fields = HustleForm.Meta.fields + ['files']


class CommentForm(forms.ModelForm):
    parent = TreeNodeChoiceField(queryset=Comment.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['parent'].widget.attrs.update({'class': "d-none"})
        self.fields['parent'].label = ''
        self.fields['parent'].required = False

    comment = forms.CharField(label="", widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "text here", "rows": "1", "cols": "50"}))

    class Meta:
        model = Comment
        fields = ("parent", "comment",)


class SkillForm(forms.ModelForm):
    skill = forms.CharField(label="", widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "text here", "rows": "1", "cols": "50"}))

    class Meta:
        model = Skill
        fields = ("skill",)


