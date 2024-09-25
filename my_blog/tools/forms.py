from django import forms
from .models import Tools


# Regular form
class FileUploadForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    desc = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_file(self):
        file = self.cleaned_data['file']
        ext = file.name.split('.')[-1].lower()
        # if ext not in ["jpg", "pdf", "xlsx", 'exe']:
        #     raise forms.ValidationError("Only jpg, pdf and xlsx exe files are allowed.")
        # return cleaned data is very important.
        return file


# Model form
class FileUploadModelForm(forms.ModelForm):
    class Meta:
        model = Tools
        fields = ('file', 'desc')
        widgets = {
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'desc': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_file(self):
        file = self.cleaned_data['file']
        ext = file.name.split('.')[-1].lower()
        # if ext not in ["jpg", "pdf", "xlsx", 'exe']:
        #     raise forms.ValidationError("Only jpg, pdf and xlsx exe files are allowed.")
        # return cleaned data is very important.
        return file
