import sys
from PyQt6.QtWidgets import QApplication,QWidget,QTableWidgetItem,QMessageBox,QDialog,QHeaderView
from PyQt6.uic import loadUi
from add_patient_form import AddPatientForm
import os
import requests

class DashboardApp(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("main_ui.ui", self) 
        self.setWindowTitle("Patient Management Dashboard")
        self.API_BASE_URL = "http://127.0.0.1:8000/api/patients/"
        self.pushButton.clicked.connect(self.open_new_patient_form)
        self.load_patient_data()
        # patient_name_column_index = 0
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

    def load_patient_data(self):
        try:
            # 1. Fetch data from the API
            response = requests.get(self.API_BASE_URL)
            response.raise_for_status() # Check for 4xx/5xx status codes
            data = response.json() 
            patients = data.get('patients', []) 
            if not isinstance(patients, list):
                QMessageBox.warning(self, "Data Format Warning", "API response missing 'patients' list.")
                self.tableWidget.setRowCount(0)
                return
            self.patient_count = len(patients)
            self.label_patient_count.setText(f"Total Patients: {self.patient_count}") 
            self.tableWidget.setRowCount(self.patient_count)


            for row, patient in enumerate(patients):
                if not isinstance(patient, dict): continue
                self.tableWidget.setItem(row, 0, QTableWidgetItem(str(patient.get('name', 'N/A'))))
                self.tableWidget.setItem(row, 1, QTableWidgetItem(str(patient.get('age', 'N/A'))))
                self.tableWidget.setItem(row, 2, QTableWidgetItem(str(patient.get('phone', 'N/A'))))
                self.tableWidget.setItem(row, 3, QTableWidgetItem(str(patient.get('registration_date', 'N/A')).split('T')[0]))
                self.tableWidget.setItem(row, 4, QTableWidgetItem(f"{patient.get('billed_amount', 0.0):.2f}"))
                self.tableWidget.setItem(row, 5, QTableWidgetItem(f"{patient.get('outstanding_amount', 0.0):.2f}"))

        except Exception as e:
            QMessageBox.critical(self, "Data Load Failure", "An error occurred while loading data. Check console for details.")
            print(f"DEBUG: Load data failed due to: {e}") 
            self.tableWidget.setRowCount(0)



    def open_new_patient_form(self):
        self.add_form = AddPatientForm(self)     
        if self.add_form.exec() == QDialog.DialogCode.Accepted:
            self.load_patient_data()

# --- Application Entry Point ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DashboardApp()
    window.show()
    sys.exit(app.exec())