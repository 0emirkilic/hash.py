import sys
import hashlib
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox


class HashVerifier(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Dosya Hash Doğrulayıcı')
        self.file_path = ''
        self.file_hash = ''
        self.hash_type = 'md5'

        self.file_label = QLabel('Dosya Seçin:')
        self.file_textbox = QLineEdit()
        self.file_button = QPushButton('Dosya Seç')
        self.file_button.clicked.connect(self.get_file)

        self.hash_label = QLabel('Hash Değeri:')
        self.hash_textbox = QLineEdit()
        self.hash_button = QPushButton('Doğrula')
        self.hash_button.clicked.connect(self.verify_hash)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.file_label)
        self.layout.addWidget(self.file_textbox)
        self.layout.addWidget(self.file_button)
        self.layout.addWidget(self.hash_label)
        self.layout.addWidget(self.hash_textbox)
        self.layout.addWidget(self.hash_button)

        self.setLayout(self.layout)
        self.show()

    def get_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.file_path, _ = QFileDialog.getOpenFileName(self, "Dosya Seç", "", "Tüm Dosyalar (*);;Metin Dosyaları (*.txt);;Resim Dosyaları (*.jpg *.png *.jpeg *.gif)", options=options)
        self.file_textbox.setText(self.file_path)

        if self.file_path:
            self.file_hash = self.calculate_hash(self.file_path, self.hash_type)

    def verify_hash(self):
        if not self.file_hash:
            QMessageBox.warning(self, 'Hata', 'Lütfen önce bir dosya seçin.')
            return

        user_hash = self.hash_textbox.text()
        if not user_hash:
            QMessageBox.warning(self, 'Hata', 'Lütfen bir hash değeri girin.')
            return

        if user_hash == self.file_hash:
            QMessageBox.information(self, 'Doğrulama Başarılı', 'Dosya doğrulandı.')
        else:
            QMessageBox.warning(self, 'Doğrulama Başarısız', 'Dosya doğrulanamadı.')

    def calculate_hash(self, file_path, hash_type):
        hasher = getattr(hashlib, hash_type)()
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(8192)
                if not data:
                    break
                hasher.update(data)
        return hasher.hexdigest()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = HashVerifier()
    sys.exit(app.exec_())
