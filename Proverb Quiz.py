import json
import os
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget, QPushButton, \
    QStackedWidget, QHBoxLayout, QMessageBox, QDialog
from PyQt5.QtGui import QPixmap, QFont, QImage
from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import sys
import linecache



class ProverbQuiz(QMainWindow):
    def __init__(self, parent, time_limit):
        super(ProverbQuiz, self).__init__(parent)
         # 초기화
        self.total_score = 0
        self.best_score = self.load_highest_score()
        self.time_limit = time_limit
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.remaining_time = self.time_limit
        # UI 요소 생성
        self.label = QLabel("", self)
        self.label.setGeometry(10, 70, 400, 50)
        self.label.setAlignment(Qt.AlignTop)

        self.result_label = QLabel("", self)
        self.result_label.setGeometry(10, 170, 400, 50)
        self.result_label.setAlignment(Qt.AlignTop)
        self.result_label.setStyleSheet(
            f"font-size: 20px; color: #FF595E; margin-bottom: 10px;"
        )

          self.setStyleSheet(
            "background-color: #F9F6F2;"
        )

        self.entry = QLineEdit(self)
        self.entry.setGeometry(10, 130, 300, 30)
        self.entry.returnPressed.connect(self.check_answer)

        self.total_score_label = QLabel(f"현재 점수: {self.total_score}", self)
        self.best_score_label = QLabel(f"최고 점수: {self.best_score}", self)

        self.retry_button = QPushButton("다시하기", self)
        self.retry_button.clicked.connect(self.retry_game)

        self.main_button = QPushButton("메인화면", self)
        self.main_button.clicked.connect(self.show_main_menu)

        self.retry_button.hide()
        self.main_button.hide()

        self.time_label = QLabel(f'남은 시간: {self.remaining_time}초', self)

        self.setup_styles()

        self.used_proverbs = set()
                layout = QVBoxLayout()
        layout.addWidget(self.total_score_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.best_score_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.label, alignment=Qt.AlignCenter)
        layout.addWidget(self.time_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.entry, alignment=Qt.AlignCenter)
        layout.addWidget(self.result_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.retry_button, alignment=Qt.AlignCenter)
        layout.addWidget(self.main_button, alignment=Qt.AlignCenter)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
        self.generate_quiz()

    def center_on_screen(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

    def setup_styles(self):
        # QLabel
        font_size = 50
        label_style = (
            f"font-size: {font_size}px; color: #2E86AB; background-color: #F9EBB2;"
            " padding: 20px; border-radius: 10px; margin-bottom: 20px; border: 2px solid #2E86AB;"
        )

        self.score_label.setStyleSheet(label_style)
        self.best_score_label.setStyleSheet(label_style)
        self.label.setStyleSheet(label_style)
        self.time_label.setStyleSheet(label_style)

        # QLineEdit
        font_size = 70
        self.entry.setStyleSheet(
            f"font-size: {font_size}px; padding: 10px; border: 2px solid #2E86AB; border-radius: 10px; margin-bottom: 20px;"
        )

        # QPushButton
        font_size = 24
        self.button.setStyleSheet(
            f"font-size: {font_size}px; padding: 10px; background-color: #FF595E; color: #FFF; "
            "border: 2px solid #FF595E; border-radius: 10px;"
        )

    def generate_quiz(self):
        self.remaining_time = self.time_limit
        while True:
            proverb = self.get_random_proverb()
            if proverb not in self.used_proverbs:
                break

        self.used_proverbs.add(proverb)

        self.quiz, self.answer = self.create_quiz(proverb)
        self.quiz = self.quiz.replace("'", "")
        self.label.setText(f"속담을 완성하세요: {self.quiz}")
        self.entry.clear()

        self.timer.start(1000)

    def get_random_proverb(self):
        no = random.randint(1, 100)
        return linecache.getline('saying.txt', no).strip()

    def create_quiz(self, saying):
        words = saying.split()
        index_to_hide = random.randint(0, len(words) - 2)
        hidden_word1 = words[index_to_hide]
        hidden_word2 = words[index_to_hide + 1]
        words[index_to_hide] = '□' * len(hidden_word1)
        words[index_to_hide + 1] = '□' * len(hidden_word2)
        return " ".join(words), f"{hidden_word1} {hidden_word2}"

    def check_answer(self):
        user_input = self.entry.text().strip()
        self.timer.stop()

        if user_input == self.answer:
            self.total_score += 1
            if self.total_score > self.best_score:
                self.best_score = self.total_score
                self.best_score_label.setText(f"최고 점수: {self.best_score}")
            QMessageBox.information(self, "정답", "정답입니다!")
        else:
            retry = QMessageBox.question(self, "틀림", f"틀렸습니다. 정답은 '{self.answer}'입니다.\n다시 시도하시겠습니까?",
                                         QMessageBox.Yes | QMessageBox.No)
            if retry == QMessageBox.No:
                self.close()
            else:
                self.total_score = 0

        self.score_label.setText(f"현재 점수: {self.total_score}")
        self.generate_quiz()

    def update_time(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.time_label.setText(f"남은 시간: {self.remaining_time}초")
            self.label.setText(f"속담을 완성하세요: {self.quiz}")
        elif self.remaining_time == 0:
            self.remaining_time = -1
            self.timer.stop()

            retry = QMessageBox.question(self, "시간 초과", "제한 시간이 초과되었습니다.\n다시 시도하시겠습니까?",
                                         QMessageBox.Yes | QMessageBox.No)
            if retry == QMessageBox.Yes:
                self.total_score = 0
                self.generate_quiz()
            else:
                self.close()
        else:
            self.generate_quiz()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuizApp()
    window.showMaximized()  # 전체 화면으로 표시
    sys.exit(app.exec_())
