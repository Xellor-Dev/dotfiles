import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTextEdit,
    QPushButton,
    QComboBox,
    QDesktopWidget,
)
from PyQt5.QtGui import QColor, QPalette
from deep_translator import GoogleTranslator
from langdetect import detect, LangDetectException


class TranslatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Window title
        self.setWindowTitle("Translator with Auto-Detect")
        self.resize(800, 600)  # Set window size
        self.center_window()  # Center the window on the screen
        self.setStyleSheet("background-color: #1e1e2e; color: #cdd6f4;")

        # Create the main layout
        layout = QVBoxLayout()

        # Input text field
        self.input_text = QTextEdit(self)
        self.input_text.textChanged.connect(self.auto_detect_language)  # Auto-detect language
        self.input_text.setStyleSheet("""
            QTextEdit {
                background-color: #313244;
                color: #cdd6f4;
                border: 1px solid #45475a;
                padding: 8px;
                font-size: 16px;
                font-family: Arial, sans-serif;
            }
        """)
        layout.addWidget(QLabel("Enter text to translate:", self))
        layout.addWidget(self.input_text)

        # Language selection dropdowns
        language_layout = QHBoxLayout()
        self.source_lang = QComboBox()
        self.target_lang = QComboBox()

        languages = {
            "English": "en",
            "Polish": "pl",
            "Russian": "ru",
            "Ukrainian": "uk",
        }

        self.languages = languages
        self.source_lang.addItems(languages.keys())
        self.target_lang.addItems(languages.keys())

        self.source_lang.setStyleSheet("background-color: #45475a; color: #cdd6f4;")
        self.target_lang.setStyleSheet("background-color: #45475a; color: #cdd6f4;")

        language_layout.addWidget(QLabel("From:", self))
        language_layout.addWidget(self.source_lang)
        language_layout.addWidget(QLabel("To:", self))
        language_layout.addWidget(self.target_lang)

        layout.addLayout(language_layout)

        # Translate button
        self.translate_button = QPushButton("Translate", self)
        self.translate_button.setStyleSheet("""
            QPushButton {
                background-color: #89b4fa;
                color: #1e1e2e;
                border: none;
                padding: 10px;
                font-size: 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #74c7ec;
            }
            QPushButton:pressed {
                background-color: #94e2d5;
            }
        """)
        self.translate_button.clicked.connect(self.translate_text)
        layout.addWidget(self.translate_button)

        # Output text field
        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(True)
        self.output_text.setStyleSheet("""
            QTextEdit {
                background-color: #313244;
                color: #cdd6f4;
                border: 1px solid #45475a;
                padding: 8px;
                font-size: 16px;
                font-family: Arial, sans-serif;
            }
        """)
        layout.addWidget(QLabel("Translated text:", self))
        layout.addWidget(self.output_text)

        self.setLayout(layout)

    def center_window(self):
        # Center the window on the current screen
        screen_geometry = QDesktopWidget().availableGeometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())

    def auto_detect_language(self):
        # Automatically detect the language of the input text
        text = self.input_text.toPlainText()
        if not text.strip():
            return  # Do nothing if the input is empty

        try:
            detected_lang = detect(text)
            lang_key = next(
                (key for key, value in self.languages.items() if value == detected_lang), None
            )
            if lang_key:
                index = list(self.languages.keys()).index(lang_key)
                self.source_lang.setCurrentIndex(index)  # Set the detected language
        except LangDetectException:
            pass  # If language cannot be detected, do nothing

    def translate_text(self):
        # Get input text and selected languages
        text = self.input_text.toPlainText()
        source = self.source_lang.currentText()
        target = self.target_lang.currentText()

        # Language codes
        language_codes = {
            "English": "en",
            "Polish": "pl",
            "Russian": "ru",
            "Ukrainian": "uk",
        }

        source_code = language_codes[source]
        target_code = language_codes[target]

        try:
            # Use GoogleTranslator to perform translation
            translation = GoogleTranslator(source=source_code, target=target_code).translate(text)
            self.output_text.setText(translation)
        except Exception as e:
            self.output_text.setText(f"Error during translation: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TranslatorApp()

    # Apply dark theme from Catppuccin Mocha colors
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#1e1e2e"))
    palette.setColor(QPalette.WindowText, QColor("#cdd6f4"))
    palette.setColor(QPalette.Base, QColor("#313244"))
    palette.setColor(QPalette.Text, QColor("#cdd6f4"))
    palette.setColor(QPalette.Button, QColor("#89b4fa"))
    palette.setColor(QPalette.ButtonText, QColor("#1e1e2e"))
    app.setPalette(palette)

    window.show()
    sys.exit(app.exec_())
