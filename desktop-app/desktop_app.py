import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QFileDialog, QListWidget,
    QMessageBox, QFrame
)
from PyQt5.QtCore import Qt
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt

API = "http://127.0.0.1:8000/api"


# ================= AUTH WINDOW =================
class AuthWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Parameter Visualizer")
        self.setFixedSize(400, 420)

        self.mode = "login"

        layout = QVBoxLayout()

        title = QLabel(" Chemical Equipment Visualizer")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:18px;font-weight:bold;")

        self.subtitle = QLabel("Login to continue")
        self.subtitle.setAlignment(Qt.AlignCenter)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.action_btn = QPushButton("Login")
        self.switch_btn = QPushButton("Switch to Signup")

        self.action_btn.clicked.connect(self.submit)
        self.switch_btn.clicked.connect(self.switch_mode)

        layout.addWidget(title)
        layout.addWidget(self.subtitle)
        layout.addSpacing(20)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.action_btn)
        layout.addWidget(self.switch_btn)

        self.setLayout(layout)

    def switch_mode(self):
        if self.mode == "login":
            self.mode = "signup"
            self.subtitle.setText("Create a new account")
            self.action_btn.setText("Signup")
            self.switch_btn.setText("Switch to Login")
        else:
            self.mode = "login"
            self.subtitle.setText("Login to continue")
            self.action_btn.setText("Login")
            self.switch_btn.setText("Switch to Signup")

    def submit(self):
        username = self.username_input.text()
        password = self.password_input.text()

        endpoint = "/login/" if self.mode == "login" else "/register/"

        try:
            res = requests.post(API + endpoint, json={
                "username": username,
                "password": password
            })
            data = res.json()

            if res.status_code != 200:
                raise Exception(data.get("error", "Authentication failed"))

            self.close()
            self.dashboard = DashboardWindow(data["token"], username)
            self.dashboard.show()

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


# ================= DASHBOARD =================
class DashboardWindow(QWidget):
    def __init__(self, token, username):
        super().__init__()
        self.token = token
        self.username = username
        self.headers = {"Authorization": f"Token {token}"}
        self.current_dataset_id = None

        self.setWindowTitle("Dashboard")
        self.resize(1100, 700)

        main_layout = QHBoxLayout()

        # -------- SIDEBAR --------
        sidebar = QVBoxLayout()
        sidebar_frame = QFrame()
        sidebar_frame.setFixedWidth(220)
        sidebar_frame.setStyleSheet("background:#0f172a;color:white;")

        logo = QLabel(" CEPV")
        logo.setAlignment(Qt.AlignCenter)
        logo.setStyleSheet("font-size:18px;font-weight:bold;")

        history_label = QLabel("Dataset History")
        history_label.setStyleSheet("font-weight:bold;")

        self.history_list = QListWidget()
        self.history_list.itemClicked.connect(self.load_history_summary)

        logout_btn = QPushButton(" Logout")
        logout_btn.clicked.connect(self.logout)

        sidebar.addWidget(logo)
        sidebar.addSpacing(20)
        sidebar.addWidget(history_label)
        sidebar.addWidget(self.history_list)
        sidebar.addStretch()
        sidebar.addWidget(logout_btn)

        sidebar_frame.setLayout(sidebar)

        # -------- MAIN CONTENT --------
        content = QVBoxLayout()

        welcome = QLabel(f" Welcome back, {username}")
        welcome.setStyleSheet("font-size:20px;font-weight:bold;")

        upload_btn = QPushButton(" Upload CSV")
        upload_btn.clicked.connect(self.upload_csv)

        self.summary_label = QLabel("Upload a CSV file to begin analysis")
        self.summary_label.setStyleSheet("margin-top:10px;")

        avg_chart_btn = QPushButton(" Average Parameters")
        avg_chart_btn.clicked.connect(self.show_avg_chart)

        type_chart_btn = QPushButton(" Type Distribution")
        type_chart_btn.clicked.connect(self.show_type_chart)

        pdf_btn = QPushButton(" Download PDF Report")
        pdf_btn.clicked.connect(self.download_pdf)

        content.addWidget(welcome)
        content.addWidget(upload_btn)
        content.addWidget(self.summary_label)
        content.addWidget(avg_chart_btn)
        content.addWidget(type_chart_btn)
        content.addWidget(pdf_btn)
        content.addStretch()

        main_layout.addWidget(sidebar_frame)
        main_layout.addLayout(content)

        self.setLayout(main_layout)
        self.load_history()

    # -------- UTIL --------
    def toast(self, msg):
        QMessageBox.information(self, "Info", msg)

    def logout(self):
        self.close()
        self.auth = AuthWindow()
        self.auth.show()

    # -------- CSV UPLOAD --------
    def upload_csv(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Upload CSV", "", "CSV Files (*.csv)"
        )
        if not path:
            return

        with open(path, "rb") as f:
            res = requests.post(
                API + "/upload/",
                headers=self.headers,
                files={"file": f}
            )

        if res.status_code == 200:
            self.toast("Dataset uploaded successfully")
            self.load_history()
        else:
            self.toast("Invalid CSV file")

    # -------- HISTORY --------
    def load_history(self):
        res = requests.get(API + "/history/", headers=self.headers)
        data = res.json()

        self.history_list.clear()
        for d in data:
            self.history_list.addItem(f"{d['id']} - {d['name']}")

    def load_history_summary(self, item):
        dataset_id = int(item.text().split(" - ")[0])
        self.current_dataset_id = dataset_id

        res = requests.get(
            f"{API}/summary/{dataset_id}/",
            headers=self.headers
        )
        summary = res.json()
        stats = summary["statistics"]

        text = (
            "📊 Dataset Summary\n\n"
            f"Total Records: {summary['total_count']}\n\n"
            f"Flowrate → Avg: {stats['flowrate']['avg']} | "
            f"Min: {stats['flowrate']['min']} | "
            f"Max: {stats['flowrate']['max']}\n\n"
            f"Pressure → Avg: {stats['pressure']['avg']} | "
            f"Min: {stats['pressure']['min']} | "
            f"Max: {stats['pressure']['max']}\n\n"
            f"Temperature → Avg: {stats['temperature']['avg']} | "
            f"Min: {stats['temperature']['min']} | "
            f"Max: {stats['temperature']['max']}"
        )

        self.summary_label.setText(text)

    # -------- CHARTS --------
    def show_type_chart(self):
        if not self.current_dataset_id:
            self.toast("Select a dataset first")
            return

        res = requests.get(
            f"{API}/summary/{self.current_dataset_id}/",
            headers=self.headers
        )
        s = res.json()

        plt.figure()
        plt.pie(
            s["type_distribution"].values(),
            labels=s["type_distribution"].keys(),
            autopct="%1.1f%%",
            startangle=140
        )
        plt.title("Equipment Type Distribution")
        plt.axis("equal")
        plt.show()


    def show_avg_chart(self):
        if not self.current_dataset_id:
            self.toast("Select a dataset first")
            return

        res = requests.get(
            f"{API}/summary/{self.current_dataset_id}/",
            headers=self.headers
        )
        s = res.json()

        plt.figure()
        plt.bar(
            ["Flowrate", "Pressure", "Temperature"],
            [
                s["statistics"]["flowrate"]["avg"],
                s["statistics"]["pressure"]["avg"],
                s["statistics"]["temperature"]["avg"],
            ],
            color=["#2563eb", "#16a34a", "#dc2626"]
        )
        plt.title("Average Equipment Parameters")
        plt.ylabel("Value")
        plt.grid(axis="y", alpha=0.3)
        plt.show()

    # -------- PDF --------
    def download_pdf(self):
        if not self.current_dataset_id:
            self.toast("Select a dataset first")
            return

        res = requests.get(
            f"{API}/report/{self.current_dataset_id}/",
            headers=self.headers
        )

        with open("dataset_report.pdf", "wb") as f:
            f.write(res.content)

        self.toast("PDF downloaded")


# ================= RUN APP =================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = AuthWindow()
    win.show()
    sys.exit(app.exec_())
