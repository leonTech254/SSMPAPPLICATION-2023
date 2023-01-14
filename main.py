from kivy.app import App
from kivy.uix.button import Button
from jnius import autoclass

class FingerprintApp(App):
    def build(self):
        self.title = "Fingerprint App"
        self.btn = Button(text="Authenticate", on_press=self.authenticate, font_size=30)
        self.label = Label(text="", font_size=20)
        self.btn.size_hint = (0.5, 0.1)
        self.btn.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.label.pos_hint = {'center_x': 0.5, 'center_y': 0.4}
        return self.btn

    def authenticate(self, *args):
        try:
            FingerprintManager = autoclass('android.hardware.fingerprint.FingerprintManager')
            fingerprint_manager = FingerprintManager.fromContext(getActivity())
            if not fingerprint_manager.isHardwareDetected():
                self.label.text = "No fingerprint sensor found"
                return
            if not fingerprint_manager.hasEnrolledFingerprints():
                self.label.text = "No fingerprints enrolled"
                return
            self.label.text = "Authentication Successful"
        except Exception as e:
            self.label.text = "Authentication Failed"
        Window.add_widget(self.label)

if __name__ == "__main__":
    FingerprintApp().run()
