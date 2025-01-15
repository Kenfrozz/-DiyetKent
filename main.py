import sys
import gspread
from google.oauth2.service_account import Credentials
from PyQt5.QtWidgets import (
    QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget,
    QPushButton, QMessageBox, QHBoxLayout, QDialog, QLineEdit, QLabel
)
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon


# Google Sheets Yönetimi
class GoogleSheetManager:
    def __init__(self, credentials_file, sheet_name, worksheet_name):
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_file(credentials_file, scopes=scope)
        self.client = gspread.authorize(creds)
        self.sheet = self.client.open(sheet_name).worksheet(worksheet_name)

    def get_data(self):
        return self.sheet.get_all_records()

    def update_row(self, row_index, updated_row):
        # Sütun sayısını dinamik olarak belirle
        num_columns = len(updated_row)
        column_range = chr(64 + num_columns)  # 'A', 'B', 'C', ... 'Z'
        self.sheet.update(range_name=f"A{row_index}:{column_range}{row_index}", values=[updated_row])

    def delete_row(self, row_index):
        self.sheet.delete_rows(row_index)

# Arka Plan İşlemleri
class WorkerThread(QThread):
    data_loaded = pyqtSignal(list)
    row_updated = pyqtSignal()
    row_deleted = pyqtSignal()

    def __init__(self, sheet_manager, task, *args, **kwargs):
        super().__init__()
        self.sheet_manager = sheet_manager
        self.task = task
        self.args = args
        self.kwargs = kwargs

    def run(self):
        if self.task == "load_data":
            data = self.sheet_manager.get_data()
            self.data_loaded.emit(data)
        elif self.task == "update_row":
            self.sheet_manager.update_row(*self.args)
            self.row_updated.emit()
        elif self.task == "delete_row":
            self.sheet_manager.delete_row(*self.args)
            self.row_deleted.emit()

# Ana Arayüz
class MainWindow(QWidget):
    def __init__(self, sheet_manager):
        super().__init__()
        self.sheet_manager = sheet_manager
        self.setWindowTitle("DiyetKent")
        self.setWindowIcon(QIcon("app_icon.ico"))  # Uygulama ikonu ayarlanıyor
        self.resize(800, 600)  # Pencere boyutu ayarlanıyor
        self.layout = QVBoxLayout(self)
        self.table = QTableWidget()
        self.layout.addWidget(self.table)
        self.load_data()

    def load_data(self):
        self.thread = WorkerThread(self.sheet_manager, "load_data")
        self.thread.data_loaded.connect(self.populate_table)
        self.thread.start()

    def populate_table(self, data):
        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(data[0]) + 2)  # +2: Düzenle ve Sil sütunları
        self.table.setHorizontalHeaderLabels(list(data[0].keys()) + ["Düzenle", "Sil"])

        for row_idx, record in enumerate(data, start=2):
            for col_idx, (key, value) in enumerate(record.items()):
                self.table.setItem(row_idx - 2, col_idx, QTableWidgetItem(str(value)))

            edit_button = QPushButton("Düzenle")
            edit_button.clicked.connect(lambda _, r=row_idx: self.edit_row(r))
            self.table.setCellWidget(row_idx - 2, len(record), edit_button)

            delete_button = QPushButton("Sil")
            delete_button.clicked.connect(lambda _, r=row_idx: self.delete_row(r))
            self.table.setCellWidget(row_idx - 2, len(record) + 1, delete_button)

    def edit_row(self, row_index):
        dialog = EditDialog(self.sheet_manager, row_index, self)
        if dialog.exec_():
            self.load_data()

    def delete_row(self, row_index):
        confirm = QMessageBox.question(self, "Onay", "Bu kaydı silmek istediğinize emin misiniz?",
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.thread = WorkerThread(self.sheet_manager, "delete_row", row_index)
            self.thread.row_deleted.connect(self.load_data)
            self.thread.start()

# Düzenleme Diyaloğu
class EditDialog(QDialog):
    def __init__(self, sheet_manager, row_index, parent=None):
        super().__init__(parent)
        self.sheet_manager = sheet_manager
        self.row_index = row_index
        self.setWindowTitle("Düzenle")
        self.layout = QVBoxLayout(self)

        # Mevcut satırdaki verileri al
        data = self.sheet_manager.sheet.row_values(row_index)
        self.inputs = []

        # Giriş alanlarını oluştur
        for index, value in enumerate(data):
            #label = QLabel(f"Sütun {index + 1}")
            input_field = QLineEdit(value)
            #self.layout.addWidget(label)
            self.layout.addWidget(input_field)
            self.inputs.append(input_field)

        # Kaydet butonu
        save_button = QPushButton("Kaydet")
        save_button.clicked.connect(self.save_changes)
        self.layout.addWidget(save_button)

    def save_changes(self):
        # Güncellenen satırı al
        updated_row = [input_field.text() for input_field in self.inputs]
        try:
            # Satırı güncelle
            self.sheet_manager.update_row(self.row_index, updated_row)
            QMessageBox.information(self, "Başarılı", "Başarıyla güncellendi!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Satır güncellenirken bir hata oluştu:\n{e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    sheet_manager = GoogleSheetManager("credentials.json", "DiyetKent", "Kayıtlar")
    window = MainWindow(sheet_manager)
    window.show()
    sys.exit(app.exec_())
