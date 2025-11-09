🖥️ Patient Management Dashboard (Frontend)
This is the desktop application frontend for the Patient Management system, built using PyQt6. It connects to the FastAPI backend to fetch, display, and add patient records.

🚀 Getting Started
Follow these steps to set up and run the desktop dashboard on your machine.

📋 Prerequisites
You need the following installed:

Python 3.x

Backend API Running: The Patient API backend must be running (usually at http://127.0.0.1:8000/) for this frontend to load data and submit new records.

🛠️ Installation
Clone or download this project folder (which contains all the Python and .ui files).

Navigate to the project directory in your terminal.

Install the required Python packages (The requirements file lists PyQt6 and requests):

In Bash-->

pip install -r requirements.txt
▶️ Running the Application
Ensure the Backend API is running in a separate terminal window.

Run the main frontend script (main_ui.py):

In Bash-->
python main_ui.py
The main dashboard window should appear.

If the connection fails, you will see a "Data Load Failure" message box.

📝 Key Features
View Patients: Displays all patient data fetched from the API in a table.

Add New Patient: Clicking the "Add Patient" button (self.pushButton in main_ui.py) opens the AddPatientForm.

Data Submission: The AddPatientForm collects input, validates basic fields (like Age > 0, Phone length, etc.), and sends the data using a POST request to the backend.

Automatic Refresh: After successfully adding a patient, the main table automatically refreshes to show the new data.

🔗 API Connection Details
The application connects to the backend API using the URL defined in main_ui.py:
self.API_BASE_URL = "http://127.0.0.1:8000/api/patients/"