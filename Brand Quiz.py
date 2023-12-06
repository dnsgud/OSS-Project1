import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QPixmap, QImage, QFont
from PyQt5.QtCore import QTimer, Qt
from PIL import Image
import os
import random

class BrandLogoQuiz:
    def __init__(self, logo_directory):
        self.logo_directory = logo_directory
        self.logo_files = [f for f in os.listdir(self.logo_directory) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
        if not self.logo_files:
            print("No valid logo image files found in the directory.")
            sys.exit()

        self.coordinates = (100, 50, 300, 250)
        self.current_logo_file = ""
        self.score = 0
        self.countdown = 5
        self.countdown_timer = QTimer()

        self.app = QApplication(sys.argv)
        self.root = QWidget()
        self.root.setWindowTitle("Brand Logo Quiz")

        self.setup_ui()

    def setup_ui(self):
        self.select_next_logo()

        self.logo_path = os.path.join(self.logo_directory, self.current_logo_file)
        self.logo_image = Image.open(self.logo_path)
        self.cropped_image = self.logo_image.crop(self.coordinates)
        self.q_pixmap = self.pil_to_pixmap(self.cropped_image)

        self.logo_label = QLabel(self.root)
        self.logo_label.setPixmap(self.q_pixmap)

        self.entry = QLineEdit(self.root)
        self.entry.returnPressed.connect(self.check_answer)

        self.submit_button = QPushButton("제출", self.root)
        self.submit_button.clicked.connect(self.check_answer)

        self.result_label = QLabel(self.root)
        self.score_label = QLabel(f"점수: {self.score}", self.root)
        self.countdown_label = QLabel("", self.root)

        # 크기가 큰 폰트로 설정
        font = QFont()
        font.setPointSize(16)  # 원하는 폰트 크기로 조절

        self.result_label.setFont(font)
        self.score_label.setFont(font)
        self.countdown_label.setFont(font)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.entry)
        h_layout.addWidget(self.submit_button)

        v_layout = QVBoxLayout(self.root)
        v_layout.addWidget(self.logo_label)
        v_layout.addLayout(h_layout)
        v_layout.addWidget(self.result_label)
        v_layout.addWidget(self.score_label)
        v_layout.addWidget(self.countdown_label)

        self.root.setLayout(v_layout)

        self.center_window()
        self.root.show()

        self.countdown_timer.timeout.connect(self.update_countdown)
        self.countdown_timer.start(1000)

        sys.exit(self.app.exec_())

    def center_window(self):
        window_width = 400
        window_height = 500
        screen_width = self.app.primaryScreen().geometry().width()
        screen_height = self.app.primaryScreen().geometry().height()

        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        self.root.setGeometry(x_position, y_position, window_width, window_height)

    def select_next_logo(self):
        remaining_logos = [logo for logo in self.logo_files if logo != self.current_logo_file]
        if remaining_logos:
            self.current_logo_file = random.choice(remaining_logos)
        else:
            print("All logos have been used. Restarting from the beginning.")
            self.current_logo_file = random.choice(self.logo_files)

    def pil_to_pixmap(self, image):
        # 이미지의 세로와 가로 길이를 변경
        new_width = 400  # 원하는 가로 길이
        new_height = 300  # 원하는 세로 길이
        image = image.resize((new_width, new_height), Image.LANCZOS)
        image = image.convert("RGBA")
        width, height = image.size
        q_image = QImage(image.tobytes("raw", "RGBA"), width, height, QImage.Format_RGBA8888)
        pixmap = QPixmap.fromImage(q_image)
        return pixmap
