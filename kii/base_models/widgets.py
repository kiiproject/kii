from django import forms


class Markdown(forms.Textarea):

    class Media:

        css = {
            "all": (
                "editor/editor.css", 
                "editor/vendor/icomoon/style.css", 
            )
        }
        js = (
            "editor/editor.js", 
            "editor/marked.js", 
        )