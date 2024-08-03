from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.snackbar import Snackbar
from kivy.clock import Clock
import numpy as np
from kivy.core.window import Window
from kivy.animation import Animation

Window.size = (1000, 600)

KV = '''
ScreenManager:
    LoadingScreen:
    MainScreen:
    InputScreen:

<LoadingScreen>:
    name: 'loading'
    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)
        MDCard:
            orientation: 'vertical'
            size_hint: None, None
            size: dp(300), dp(200)
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            elevation: 10
            padding: dp(20)
            spacing: dp(20)
            MDLabel:
                text: "Eigenvalues & Eigenvectors Calculator"
                halign: 'center'
                font_style: 'H5'
            MDLabel:
                text: "Loading..."
                halign: 'center'
                font_style: 'H6'
            MDProgressBar:
                id: loading_bar
                type: 'indeterminate'

<MainScreen>:
    name: 'main'
    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)
        MDCard:
            orientation: 'vertical'
            size_hint: None, None
            size: dp(400), dp(300)
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            elevation: 10
            padding: dp(20)
            spacing: dp(20)
            MDLabel:
                text: "Eigenvalues & Eigenvectors Calculator"
                halign: 'center'
                font_style: 'H5'
            MDTextField:
                id: matrix_size
                hint_text: "Enter Matrix Size e.g (nxn)"
                size_hint_x: None
                width: '300dp'
                pos_hint: {'center_x': 0.5}
            MDRaisedButton:
                text: "Enter"
                pos_hint: {'center_x': 0.5}
                on_release: app.on_enter_click()

<InputScreen>:
    name: 'input'
    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)
        MDCard:
            orientation: 'vertical'
            size_hint: None, None
            size: dp(600), dp(500)
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            elevation: 10
            padding: dp(20)
            spacing: dp(20)
            MDLabel:
                text: "Enter Matrix Values"
                halign: 'center'
                font_style: 'H5'
            ScrollView:
                MDGridLayout:
                    id: matrix_grid
                    cols: 1
                    adaptive_height: True
            MDRaisedButton:
                text: "Calculate"
                icon: "calculator"
                pos_hint: {'center_x': 0.5}
                on_release: app.calculate_eigen()
            MDBoxLayout:
                orientation: 'horizontal'
                size_hint_y: None
                height: dp(50)
                spacing: dp(10)
                pos_hint: {'center_x': 0.5}
                MDIconButton:
                    icon: "broom"
                    on_release: app.clear_entries()
                MDIconButton:
                    icon: "arrow-left"
                    on_release: app.back_to_main()
'''

class LoadingScreen(Screen):
    pass

class MainScreen(Screen):
    pass

class InputScreen(Screen):
    pass

class EigenApp(MDApp):

    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.primary_hue = "600"
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)

    def on_start(self):
        self.root.current = 'loading'
        Clock.schedule_once(self.show_main_screen, 5)  # Simulate loading for 5 seconds

    def show_main_screen(self, *args):
        self.root.current = 'main'
        self.animate_transition('main')

    def on_enter_click(self):
        size = self.root.get_screen('main').ids.matrix_size.text.strip()
        try:
            rows, cols = map(int, size.split('x'))
            if rows != cols:
                raise ValueError("Matrix must be square.")
            self.create_matrix_entries(rows, cols)
            self.animate_transition('input')
        except ValueError as e:
            self.show_snackbar("Invalid Input", "Please enter a valid matrix size in the format NxN (e.g., 3x3).")

    def create_matrix_entries(self, rows, cols):
        matrix_grid = self.root.get_screen('input').ids.matrix_grid
        matrix_grid.clear_widgets()
        for i in range(rows):
            row_layout = MDGridLayout(cols=cols, size_hint_y=None, height=50)
            for j in range(cols):
                entry = MDTextField(size_hint=(None, None), size=(100, 50), font_size=20)
                row_layout.add_widget(entry)
            matrix_grid.add_widget(row_layout)

    def calculate_eigen(self):
        try:
            matrix_grid = self.root.get_screen('input').ids.matrix_grid
            matrix_entries = [[child for child in row.children] for row in matrix_grid.children]
            matrix = np.array([[float(entry.text) for entry in reversed(row)] for row in matrix_entries])
            eigenvalues, eigenvectors = np.linalg.eig(matrix)
            result_text = f"Eigenvalues:\n{eigenvalues}\n\nEigenvectors:\n{eigenvectors}"
            self.show_result_dialog("Result", result_text)
        except ValueError:
            self.show_snackbar("Invalid Input", "Please enter valid numeric values for the matrix.")
        except Exception as e:
            self.show_snackbar("Error", str(e))

    def clear_entries(self):
        matrix_grid = self.root.get_screen('input').ids.matrix_grid
        for row in matrix_grid.children:
            for entry in row.children:
                entry.text = ""

    def back_to_main(self):
        self.animate_transition('main')

    def show_result_dialog(self, title, text):
        dialog = MDDialog(title=title, text=text, size_hint=(0.8, 1))
        dialog.open()

    def show_snackbar(self, title, text):
        snackbar = Snackbar(text=f"{title}: {text}")
        snackbar.open()

    def animate_transition(self, screen_name):
        screen = self.root.get_screen(screen_name)
        animation = Animation(opacity=0, duration=0)
        animation.bind(on_complete=lambda *args: setattr(screen, 'opacity', 1))
        animation.start(screen)
        self.root.current = screen_name
        Animation(opacity=1, duration=0.5).start(screen)


if __name__ == '__main__':
    EigenApp().run()
