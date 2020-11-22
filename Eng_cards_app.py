from PyQt5 import QtWidgets,  uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer
import os, sys, random
import pickle

# FUNCTIONS

def tick():
    # edit second (hours, minutes, seconds)
    global sec
    hours = sec // 3600
    minutes = (sec % 3600) // 60
    seconds = (sec % 3600) % 60
    dlg.label_timer.setText(pr_time(hours) + ' : ' + pr_time(minutes) + ' : ' + pr_time(seconds))
    sec += 1

def pr_time (number):
    # edit number for format 00:00:00
    if number < 0:
        number_pr = 00
    elif number < 10:
        number_pr = "0" + str(number)
    else:
        number_pr = str(number)
    return number_pr


def save():
    # save data changes
    file = open(path_program + '\lib' + '\data.pickle', 'wb')
    pickle.dump(dic_words, file)
    file.close()

def count_w_dic():
    # count and write quantity words in dictionary
    dlg.label_w_dic.setText(str(len(dic_words)))

def show_w():
    # random selected and show new word
    global ran_key, counter_w_session, sec
    sec = 0
    try:
        ran_key = random.choice(list(dic_words.keys()))
        dlg.label_word.setText(str(ran_key))
        dlg.label_translate.setText('')
        counter_w_session += 1
    except:
        dlg.label_word.setText('')
        dlg.label_translate.setText('')
    count_session()


def edit_w():
    # edit "rus meaning" (value), for word in dictionary
    if dlg.textEdit_eng.toPlainText() != "" and dlg.textEdit_rus.toPlainText() != "":   # check if there is text in both fields (rus and engl)
        if dlg.textEdit_eng.toPlainText() in dic_words: # check if new word no in dictionary
            dic_words[dlg.textEdit_eng.toPlainText()] = dlg.textEdit_rus.toPlainText()
            dlg.textEdit_eng.setText("")
            dlg.textEdit_rus.setText("")
            save()
        else:
            messag_box("Error", 'This word not in dictionary!', 1)
    else:
        messag_box("Error", 'Both fields must be filled!', 1)

def del_w():
    if dlg.textEdit_eng.toPlainText() != "" :
        if dlg.textEdit_eng.toPlainText() in dic_words:
            messag_box("Delete word", 'Delete word from dictionary?', 2)
        else:
            messag_box("Error", 'This word is not in the dictionary!', 1)
    else:
        messag_box("Error", 'Write English word', 1)

def add_w():
    # add new word in dictionary
    if dlg.textEdit_eng.toPlainText() != "" and dlg.textEdit_rus.toPlainText() != "":
        if dlg.textEdit_eng.toPlainText() not in dic_words:
            dic_words[dlg.textEdit_eng.toPlainText()] = dlg.textEdit_rus.toPlainText()
            dlg.textEdit_eng.setText("")
            dlg.textEdit_rus.setText("")
            count_w_dic()
            save()
        else:
             messag_box("Error",  'This word already in dictionary!', 1)
    else:
        messag_box("Error",  'Both fields must be filled!', 1)

def show_translate():
    global ran_key
    if ran_key != "":
        dlg.label_translate.setText(str(dic_words[ran_key]))
    else:
        pass

def messag_box(title, text, option):
    # constructor for message box
    mes_box = QMessageBox()
    mes_box.setWindowTitle(title)
    mes_box.setText(text)

    if option == 1:
        # Information mes-box
        mes_box.setIcon(QMessageBox.Information)

    elif option == 2:
        # Question mes-box (Yes or No)
        mes_box.setIcon(QMessageBox.Question)
        mes_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        mes_box.setDefaultButton(QMessageBox.Cancel)
        mes_box.buttonClicked.connect(cl_but_mes)
    x = mes_box.exec_()

def cl_but_mes(x):
    # delete word from dictionary
    if x.text() == "OK":
         if dlg.textEdit_eng.toPlainText() ==dlg.label_word.text():
             show_w()
         del dic_words[dlg.textEdit_eng.toPlainText()]
         dlg.textEdit_eng.setText("")
         save()
         count_w_dic()
         messag_box("Good!", 'Word deleted from dictionary!', 1)


def count_session():
    global counter_w_session
    dlg.label_w_session.setText(str(counter_w_session))

# objects for 1 session
counter_w_session = 0
dic_words = {}
ran_key = ''
sec = 0

# SYSTEM ---
path_program = os.path.dirname(os.path.abspath(sys.argv[0]))   # find out the current program address

app = QtWidgets.QApplication([])
# Load GUI (pyQT_Designer)
dlg = uic.loadUi("Eng_dict.ui")

try:
    # open "data.pickle" with dic_name and dic_tag (library) if Not - create (except)
    file = open(path_program + '\lib' + '\data.pickle', 'rb')
    dic_words = pickle.load(file)
except:
    save()


# BUTTONS  ---

dlg.but_show_w.clicked.connect(show_w)
dlg.but_show_translate.clicked.connect(show_translate)
dlg.but_add_w.clicked.connect(add_w)
dlg.but_edit_w.clicked.connect(edit_w)
dlg.but_del_w.clicked.connect(del_w)

# SYSTEM ---
count_w_dic()
show_w()

dlg.show()
timer = QTimer()
timer.timeout.connect(tick)
timer.start(1000)  # start function "start" every 1000 millisecond (1 sec)
app.exec()
