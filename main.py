from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.garden.fingerprint import Fingerprint

class FingerprintApp(App):
    def build(self):
        self.finger = Fingerprint()
        self.finger.start()
        self.title = "Fingerprint App"
        self.btn = Button(text="Authenticate", on_press=self.authenticate, font_size=30)
        self.label = Label(text="", font_size=20)
        self.btn.size_hint = (0.5, 0.1)
        self.btn.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.label.pos_hint = {'center_x': 0.5, 'center_y': 0.4}
        return self.btn

    def authenticate(self, *args):
        if self.finger.is_available():
            self.finger.authenticate()
            self.label.text = "Authentication Successful"
        else:
            self.label.text = "Fingerprint scanner not available"
        Window.add_widget(self.label)

if __name__ == "__main__":
    FingerprintApp().run()
