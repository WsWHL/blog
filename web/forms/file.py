from django import forms


class fileform(forms.Form):
    """
    上传文件表单
    """
    file = forms.FileField()

    def clean_file(self):
        return self.cleaned_data['file']
