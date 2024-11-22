from PyQt5.QtWidgets import QDockWidget, QVBoxLayout, QListWidget, QListWidgetItem, QWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class Menu(QDockWidget):
    def __init__(self, parent=None):
        super().__init__("", parent)
        self.setAllowedAreas(Qt.LeftDockWidgetArea)

        # Create a container for the menu
        self.container = QWidget()
        self.layout = QVBoxLayout(self.container)
        self.layout.setContentsMargins(10, 10, 10, 10)

        # Create a list of menu options
        self.menu_list = QListWidget()
        self.menu_list.setFont(QFont("Arial", 10))
        self.menu_list.setStyleSheet("""
            QListWidget {
                background-color: #333333;
                color: white;
                border: none;
            }
            QListWidget::item {
                padding: 10px;
            }
            QListWidget::item:selected {
                background-color: #555555;
            }
        """)
        # Adding items with centered alignment
        items = ["New Model", "Load Model", "User Guide"]
        for item_text in items:
            item = QListWidgetItem(item_text)
            item.setTextAlignment(Qt.AlignCenter)  # Center the text within the item
            self.menu_list.addItem(item)

        self.layout.addWidget(self.menu_list)
        self.menu_list.itemClicked.connect(self.handle_selection)
        self.layout.addWidget(self.menu_list)

        # Set the container widget as the main widget for the dock
        self.setWidget(self.container)

        # Reference to the parent for interaction
        self.parent = parent

    def handle_selection(self, item):
        """Handle selection based on the clicked menu item."""
        selected_option = item.text()
        if selected_option == "New Model":
            self.parent.open_file_dialog()
        elif selected_option == "Load Model":
            self.parent.load_model()
        elif selected_option == "User Guide":
            self.parent.open_user_guide()

