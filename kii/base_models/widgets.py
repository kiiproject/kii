from django import forms


class Markdown(forms.Textarea):

    def render(self, *args, **kwargs):
        return "<div id='epiceditor'></div>" + super(Markdown, self).render(*args, **kwargs)