from django import forms
from web.models import Category


class ArticleForm(forms.Form):
    """
    文章表单
    """
    title = forms.CharField(min_length=10, max_length=100, initial='',
                            error_messages={
                                'required': '请输入文章标题',
                                'min_length': '标题内容至少10个字符',
                                'max_length': '标题内容最多100个字符'
                            })
    subject = forms.CharField(required=False, max_length=500, initial='',
                              error_messages={
                                  'max_length': '文章主题内容不得超过500个字符'
                              })
    cover = forms.URLField(required=False)
    content = forms.CharField(initial='',
                              error_messages={
                                  'required': '文章内容不能为空'
                              })
    categories = forms.ModelMultipleChoiceField(required=False,
                                                widget=forms.CheckboxSelectMultiple(),
                                                queryset=Category.objects.filter(is_deleted=False)
                                                .order_by('level', 'sort', 'create_time'))
    topping = forms.BooleanField(required=False, initial='')

    def get_title(self):
        return self.cleaned_data['title']

    def get_subject(self):
        return self.cleaned_data['subject']

    def get_cover(self):
        return self.cleaned_data['cover']

    def get_content(self):
        return self.cleaned_data['content']

    def get_categories(self):
        return self.cleaned_data['categories']

    def get_topping(self):
        return self.cleaned_data['topping']
