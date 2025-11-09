from PyQt6.QtWidgets import QDialog,QMessageBox
from PyQt6.QtGui import QIntValidator, QDoubleValidator, QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression
from PyQt6.uic import loadUi
import requests

class AddPatientForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("add_patient_form.ui", self)
        self.setWindowTitle("Add New Patient")
        self.parent_dashboard = parent # Store the main dashboard instance
        self.buttonBox.accepted.connect(self.save_patient_data)
        self.buttonBox.rejected.connect(self.reject)

        #validators
        name_regex = QRegularExpression("^[a-zA-Z\\s]*$")
        name_validator = QRegularExpressionValidator(name_regex, self.lineEdit_name)
        self.lineEdit_name.setValidator(name_validator)
        age_validator = QIntValidator(0, 999, self.lineEdit_age)
        self.lineEdit_age.setValidator(age_validator)
        phone_regex = QRegularExpression("^[0-9]{10}$")
        phone_validator = QRegularExpressionValidator(phone_regex, self.lineEdit_phone)
        self.lineEdit_phone.setValidator(phone_validator)
        self.lineEdit_phone.setMaxLength(10)
        amount_validator = QDoubleValidator(0.00, 999999.99, 2, self)
        self.lineEdit_billedamt.setValidator(amount_validator)
        self.lineEdit_outstandingamt.setValidator(amount_validator)

    def save_patient_data(self):
        new_patient_data = {
            'name': self.lineEdit_name.text(), 
            'age': int(self.lineEdit_age.text() or 0),
            'phone': self.lineEdit_phone.text(),
            'registration_date': self.dateTimeEdit.dateTime().toString("yyyy-MM-ddTHH:mm:ss"), 
            'billed_amount': float(self.lineEdit_billedamt.text() or 0.0),
            'outstanding_amount': float(self.lineEdit_outstandingamt.text() or 0.0)
        }
        
        # 2. Send Data to API
        try:
            response = requests.post(self.parent_dashboard.API_BASE_URL, json=new_patient_data)
            response.raise_for_status()
            QMessageBox.information(self, "Success", "Patient added successfully!")
            self.accept()
        except ValueError:
        # Catches input errors (user typed 'abc' in the Age field, etc.)
            QMessageBox.warning(self, "Input Error", "Please ensure all number fields (Age, Billed, Outstanding) are valid.")
            self.reject()
        
        except requests.exceptions.HTTPError as e:
            # Catches all API validation and server errors (400s and 500s)
            error_detail = "API Rejected Data."
            try:
                # Try to get the detailed JSON error from FastAPI (like the 422 validation details)
                error_detail = e.response.json().get('detail', e.response.text)
            except Exception:
                # If the response isn't JSON, just use the status code and reason
                error_detail = f"HTTP Error {e.response.status_code}: {e.response.reason}"
                
                QMessageBox.critical(self, "Submission Failed", f"Data could not be saved. Reason: {error_detail}")
            self.reject() 

        except Exception as e:
            # Catches everything else (network, variable typos, etc.)
            QMessageBox.critical(self, "Fatal Error", f"An unexpected system error occurred: {e}")
            self.reject()


