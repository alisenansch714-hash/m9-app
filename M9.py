import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.button import Button
from kivy.uix.label import Label


class FileHider(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        self.status = Label(
            text="اختر ملفًا ثم اضغط إخفاء أو إظهار",
            size_hint=(1, 0.1)
        )

        self.filechooser = FileChooserListView(
            path="/storage/emulated/0"
        )

        self.hide_btn = Button(
            text="إخفاء الملف",
            size_hint=(1, 0.1)
        )
        self.hide_btn.bind(on_press=self.hide_file)

        self.show_btn = Button(
            text="إظهار الملف",
            size_hint=(1, 0.1)
        )
        self.show_btn.bind(on_press=self.show_file)

        self.add_widget(self.status)
        self.add_widget(self.filechooser)
        self.add_widget(self.hide_btn)
        self.add_widget(self.show_btn)

    def hide_file(self, instance):
        try:
            if not self.filechooser.selection:
                self.status.text = "اختر ملفًا أولًا"
                return

            filepath = self.filechooser.selection[0]
            dirname = os.path.dirname(filepath)
            filename = os.path.basename(filepath)

            if filename.startswith("."):
                self.status.text = "الملف مخفي بالفعل"
                return

            hidden_path = os.path.join(dirname, "." + filename)

            os.rename(filepath, hidden_path)

            self.status.text = "تم إخفاء الملف بنجاح"

        except Exception as e:
            self.status.text = f"خطأ: {e}"

    def show_file(self, instance):
        try:
            if not self.filechooser.selection:
                self.status.text = "اختر ملفًا أولًا"
                return

            filepath = self.filechooser.selection[0]
            dirname = os.path.dirname(filepath)
            filename = os.path.basename(filepath)

            if not filename.startswith("."):
                self.status.text = "الملف غير مخفي"
                return

            visible_path = os.path.join(dirname, filename[1:])

            os.rename(filepath, visible_path)

            self.status.text = "تم إظهار الملف"

        except Exception as e:
            self.status.text = f"خطأ: {e}"


class FileHiderApp(App):
    def build(self):
        return FileHider()


if __name__ == "__main__":
    FileHiderApp().run()
