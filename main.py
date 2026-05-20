import os
import sys
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QInputDialog, QListWidgetItem, QMainWindow
#maybe add timer 

class TaskNode:
    def __init__(self, activity, time, note):
        self.activity = activity
        self.time = time
        self.note = note
        self.next = None


class NovaTreeScheduler(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "scheduler.ui"), self)

        self.front = None
        self.rear = None

        self.btn_add.setText("Add")
        self.btn_delete.setText("Delete")

        self.btn_add.clicked.connect(self.add_activity)
        self.btn_delete.clicked.connect(self.delete_activity)

        self.taskList.setStyleSheet(
            """
            QListWidget {
                background: #0f172a;
                border: none;
                padding: 10px;
                color: white;
                font-size: 14px;
            }
            QListWidget::item {
                background: #111827;
                border: 1px solid #334155;
                border-radius: 12px;
                padding: 10px 12px;
                margin-bottom: 8px;
            }
            QListWidget::item:selected {
                background: #1d4ed8;
                border-color: #60a5fa;
            }
            """
        )

    def inputs(self, title, label):
        text, ok = QInputDialog.getText(self, title, label)
        if ok and text.strip():
            return text.strip()
        return None  

    def add_activity(self):
        
        activity = self.inputs("New Activity", "Activity name:")
        

        time = self.inputs("Activity Time", "Time:")
        

        note = self.inputs("Activity Note", "Note:")
        

        node = TaskNode(activity, time, note)
        if self.front is None:
            self.front = self.rear = node
        else:
            self.rear.next = node
            self.rear = node

        self.refresh_task_list()

    def delete_activity(self):
        if self.front is None:
            return

        if self.front.next is None:
            self.front = None
            self.rear = None
            self.refresh_task_list()
            return

        prev = None
        curr = self.front
        while curr.next is not None:
            prev = curr
            curr = curr.next

        prev.next = None
        self.rear = prev
        self.refresh_task_list()

    def refresh_task_list(self):
        self.taskList.clear()
        curr = self.front
        while curr is not None:
            self.taskList.addItem(
                QListWidgetItem(f"{curr.activity}   |   Time: {curr.time}   |   Note: {curr.note}")
            )
            curr = curr.next


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NovaTreeScheduler()
    window.show()
    sys.exit(app.exec())