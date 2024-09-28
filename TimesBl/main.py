from PyQt5.QtCore import*
from PyQt5.QtWidgets import*

app = QApplication([])
window = QWidget()
window.setWindowTitle("Smart Notes")
window.resize(800,600)
window.move(0,0)
window.setStyleSheet("background-color : rgb(52, 190, 174): font-size: 15px")




text_editor = QTextEdit()
text_editor.setPlaceholderText("Введіть текст")


list_wiget1 = QListWidget()
list_wiget2 = QListWidget()

text_serther = QLineEdit()
text_serther.setPlaceholderText("Пошук по тексту")

teg_serther = QLineEdit()
teg_serther.setPlaceholderText("Пошук по тегу")

make_note = QPushButton()
make_note.setText("(створити замітку)")

delete_note = QPushButton()
delete_note.setText("(видалити замітку)")

save_note = QPushButton()
save_note.setText("(зберегти замітку)")

searth_for_text = QPushButton()
searth_for_text.setText("(пошук по тексту)")

searth_for_tag = QPushButton()
searth_for_tag.setText("(пошук по тегу)")

add_to_note = QPushButton()
add_to_note.setText("(додати до замітки)")

unpin_to_note = QPushButton()
unpin_to_note.setText("(закріпити до замітки)")

convert_to_txt = QPushButton()
convert_to_txt.setText("(конвертувати в TXT)")

action_theme_btn = QPushButton()
action_theme_btn.setText("(Змінити тему)")


row1 = QHBoxLayout()
row1.addWidget(make_note)
row1.addWidget(delete_note)


row2 = QHBoxLayout()
row2.addWidget(add_to_note)
row2.addWidget(unpin_to_note)



col1 = QVBoxLayout()
col1.addWidget(text_editor)

col2 = QVBoxLayout()
col2.addWidget(QLabel("Список заміток:"))
col2.addWidget(list_wiget1)
col2.addLayout(row1)
col2.addWidget(save_note)

col2.addWidget(QLabel("Список тегів:"))
col2.addWidget(list_wiget2)
col2.addLayout(row2)

layout_note = QVBoxLayout()
layout_note.addLayout(col1)
layout_note.addLayout(col2)

window.setLayout(layout_note)

window.show()
app.exec_()
