from django import forms


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
    category_ids = forms.CharField(required=False, max_length=200,
                                   error_messages={
                                       'max_length': '文章分类信息过多'
                                   })
    tag_ids = forms.CharField(required=False, max_length=200,
                              error_messages={
                                  'max_length': '文章标签信息过多'
                              })

    def get_title(self):
        return self.cleaned_data['title']

    def get_subject(self):
        return self.cleaned_data['subject']

    def get_cover(self):
        return self.cleaned_data['cover']

    def get_content(self):
        return self.cleaned_data['content']

    def get_category_ids(self):
        return self.cleaned_data['category_ids']

    def get_tag_ids(self):
        return self.cleaned_data['tag_ids']
