from PyQt5.QtWidgets import QApplication
import sys
import json
from ui1 import Ui_MainWindow

class NotesApp(Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.notes = {}
        self.load_notes()
        self.setup_connections()
        self.list_notes.addItems(self.notes)
    
    def load_notes(self):
        try:
            with open('note_data.json', 'r', encoding='utf-8') as file:
                self.notes = json.load(file)
        except FileNotFoundError:
            self.notes = {}
    
    def save_notes(self):
        with open('note_data.json', 'w', encoding='utf-8') as file:
            json.dump(self.notes, file)
    
    def show_note(self):
        key = self.listWidget.selectedItems()[0].text()
        self.text_field.setText(self.notes[key]['текст'])
        self.tags_list.clear()
        self.tags_list.addItems(self.notes[key]['теги'])
    
    def add_note(self):
        note_name, ok = self.get_input('Додати замітку', 'Назва замітки')
        if ok and note_name:
            self.notes[note_name] = {'текст': "", 'теги': []}
            self.notes_list.addItem(note_name)
            self.save_notes()
    
    def save_note(self):
        if self.notes_list.selectedItems():
            key = self.notes_list.selectedItems()[0].text()
            self.notes[key]['текст'] = self.text_field.toPlainText()
            self.save_notes()
    
    def del_note(self):
        if self.notes_list.selectedItems():
            key = self.notes_list.selectedItems()[0].text()
            del self.notes[key]
            self.notes_list.clear()
            self.tags_list.clear()
            self.text_field.clear()
            self.notes_list.addItems(self.notes)
            self.save_notes()
    
    def add_tag(self):
        if self.notes_list.selectedItems():
            key = self.notes_list.selectedItems()[0].text()
            tag = self.tag_field.text()
            if tag not in self.notes[key]['теги']:
                self.notes[key]['теги'].append(tag)
                self.tags_list.addItem(tag)
                self.tag_field.clear()
                self.save_notes()
    
    def del_tag(self):
        if self.notes_list.selectedItems() and self.tags_list.selectedItems():
            key = self.notes_list.selectedItems()[0].text()
            tag = self.tags_list.selectedItems()[0].text()
            self.notes[key]['теги'].remove(tag)
            self.tags_list.clear()
            self.tags_list.addItems(self.notes[key]['теги'])
            self.save_notes()
    
    def setup_connections(self):
        self.notes_list.itemClicked.connect(self.show_note)
        self.create_note_button.clicked.connect(self.add_note)
        self.save_note_button.clicked.connect(self.save_note)
        self.delete_note_button.clicked.connect(self.del_note)
        self.add_tag_button.clicked.connect(self.add_tag)
        self.delete_tag_button.clicked.connect(self.del_tag)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NotesApp()
    window.show()
    sys.exit(app.exec_())