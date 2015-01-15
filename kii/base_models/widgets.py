from django import forms


class Markdown(forms.Textarea):

    class Media:

        css = {
            "all": (
                "default/editor/editor.css", 
                "default/editor/vendor/icomoon/style.css", 
            )
        }
        js = (
            "default/editor/editor.js", 
            "default/editor/marked.js", 
        )