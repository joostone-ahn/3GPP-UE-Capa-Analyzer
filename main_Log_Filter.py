import Extract_msg
import RRC
import NAS
import re
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5 import QtGui

msg_type_list =[]
'''
cb.addItem("Select Item")
cb.addItem("1.RRC")
cb.addItem("2.NAS")
cb.addItem("3.UE Capability")
cb.addItem("4.NR Addition Msg")
cb.addItem("5.Custom Input")
'''

type1 = []
type1.append('BCCH-DL-SCH-Message')  # QCT
type1.append('UL-CCCH-Message')  # QCT
type1.append('DL-CCCH-Message')  # QCT
type1.append('DL-DCCH-Message')  # QCT
type1.append('UL-DCCH-Message')  # QCT

type2 =[]
type2.append('lte_emm_msg') #QCT
type2.append('lte_esm_msg') #QCT

type3 = []
type3.append('UE-EUTRA-Capability')
type3.append('UE-NR-Capability')
type3.append('UE-MRDC-Capability')

type4 =[]
# type4.append('valueRRCReconfiguration::=')  # QCT
# type4.append('rrcReconfiguration')  # LSI
type4.append('secondaryCellGroup')

type5 =[]
type5.append('value RadioBearerConfig')  # QCT
# type5.append('RadioBearerConfig')  # LSI

type6 =[] # SIB
type6.append('BCCH-DL-SCH')  # QCT


msg_type_list.append(type1)
msg_type_list.append(type2)
msg_type_list.append(type3)
msg_type_list.append(type4)
msg_type_list.append(type5)
msg_type_list.append(type6)

BoldFont = QtGui.QFont()
BoldFont.setBold(True)

CourierNewFont = QtGui.QFont()
CourierNewFont.setFamily("Courier New")

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.tab_Paste = Paste_tab()
        self.tab_File = File_Tab()
        self.tab_Result = Result_tab()
        # self.tab_About = About_tab()

        self.tabs = QTabWidget()
        self.tabs.addTab(self.tab_File, 'File')
        self.tabs.addTab(self.tab_Paste, 'Paste')
        self.tabs.addTab(self.tab_Result, 'Result')
        # self.tabs.addTab(self.tab_About,'About')

        vbox = QVBoxLayout()
        vbox.addWidget(self.tabs)
        vbox.addWidget(QLabel("Copyright 2022. JUSEOK AHN<ajs3013@lguplus.co.kr> all rights reserved."))


        self.setLayout(vbox)

        self.setWindowTitle('Log filter v.1.3')
        self.setGeometry(110, 50, 1000, 850)
        self.show()


        # 시그널 슬롯 연결
        self.tab_Paste.sig_rst.connect(self.tab_Result.slot_rst)
        self.tab_Paste.sig_nothing.connect(self.tab_Result.slot_nothing)

        self.tab_File.sig_rst.connect(self.tab_Result.slot_rst)
        self.tab_File.sig_nothing.connect(self.tab_Result.slot_nothing)

        # 결과 페이지로 강제 이동
        self.tab_Paste.sig_rst.connect(lambda __:self.tabs.setCurrentIndex(2))
        self.tab_Paste.sig_nothing.connect(lambda __:self.tabs.setCurrentIndex(2))

        self.tab_File.sig_rst.connect(lambda __:self.tabs.setCurrentIndex(2))
        self.tab_File.sig_nothing.connect(lambda __:self.tabs.setCurrentIndex(2))


# class About_tab(QWidget):
#
#     def __init__(self):
#         super().__init__()
#         self.initUI()
#
#     def initUI(self):
#
#         self.TB = QTextBrowser()
#
#         vbox = QVBoxLayout()
#         vbox.addWidget(self.TB)
#         vbox.addStretch()
#
#         TB_content = ""
#         TB_content += "UE Capability Decoder\n"
#         TB_content += "Version : v.1.0\n"
#         TB_content += "Data    : 2020-01-05\n"
#         TB_content += "Contact : ajs3013@lguplus.co.kr\n"
#
#         self.TB.setText(TB_content)
#         self.TB.setFont(CourierNewFont)
#
#         self.setLayout(vbox)



class Paste_tab(QWidget):

    # Signal
    sig_rst = pyqtSignal(list, name ='Result')
    sig_nothing = pyqtSignal(list, name ='Nothing')

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        cb = QComboBox(self)
        cb.addItem("Select Item")
        cb.addItem("1.RRC")
        cb.addItem("2.NAS")
        cb.addItem("3.UE Capa")
        cb.addItem("4.secondaryCellGroup")
        cb.addItem("5.RadioBearerConfig")
        cb.addItem("6.SIB")
        cb.setFixedWidth(150)
        cb.setToolTip("Please select what you want to extract.")

        self.selected = int
        cb.activated[str].connect(self.onActivated)

        msg_all = ''
        self.te = QTextEdit()
        self.te.setAcceptRichText(False)
        self.te.setToolTip('Paste logs that you want to convert and extract')
        self.te.setFixedHeight(500)

        self.msg_all = self.te.toPlainText()

        self.Exe_btn = QPushButton("Execute")
        self.Exe_btn.setFixedWidth(100)
        self.Exe_btn.setCheckable(False)
        self.Exe_btn.setDisabled(True)

        self.Exe_btn.clicked.connect(self.load_msg)

        hbox = QHBoxLayout()
        hbox.addWidget(cb)
        hbox.addWidget(self.Exe_btn)
        hbox.addStretch()

        vbox = QVBoxLayout()
        vbox.addWidget(self.te)
        vbox.addLayout(hbox)
        vbox.addStretch()

        self.setLayout(vbox)

    def onActivated(self, text):
        if text == 'Select Item':
            self.Exe_btn.setDisabled(True)
        else:
            self.selected = int(re.findall("\d",text)[0])-1
            self.Exe_btn.setEnabled(True)

    @pyqtSlot()
    def load_msg(self):
        msg_all_str = self.te.toPlainText()
        msg_all = msg_all_str.split('\n')
        msg, nothing = Extract_msg.extract_msg(msg_all, msg_type_list[self.selected])
        if nothing:
            self.sig_nothing.emit(nothing)
        else:
            rst = []
            if self.selected == 1: # NAS msg
                rst.append(NAS.convert_msg(msg))
                rst.append("QCT")
                rst.append("")
                rst.append("")
            else:
                msg, vendor, debug = RRC.convert_msg(msg)
                rst.append(msg)
                rst.append(vendor)
                rst.append(debug)
                rst.append("")
            self.sig_rst.emit(rst)


class File_Tab(QWidget):

    # Signal
    sig_rst = pyqtSignal(list, name ='Result')
    sig_nothing = pyqtSignal(list, name ='Nothing')

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        cb = QComboBox(self)
        cb.addItem("Select Item")
        cb.addItem("1.RRC")
        cb.addItem("2.NAS")
        cb.addItem("3.UE Capability")
        cb.addItem("4.secondaryCellGroup")
        cb.addItem("5.RadioBearerConfig")
        cb.addItem("6.SIB")
        cb.setFixedWidth(200)
        cb.setToolTip("Please select what you want to extract.")

        self.selected = -1
        cb.activated[str].connect(self.onActivated)

        self.open_btn = QPushButton("Open")
        self.open_btn.setFixedWidth(100)
        self.open_btn.setCheckable(False)
        self.open_btn.setDisabled(True)
        self.open_btn.setToolTip('Open a log file(.txt) that you want to convert and extract')

        hbox = QHBoxLayout()
        hbox.addWidget(cb)
        hbox.addWidget(self.open_btn)
        hbox.addStretch()

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addStretch()

        self.setLayout(vbox)
        self.open_btn.clicked.connect(self.load_msg)

    def onActivated(self, text):
        if text == 'Select Item':
            self.open_btn.setDisabled(True)
        else:
            self.selected = int(re.findall("\d",text)[0])-1
            self.open_btn.setEnabled(True)

    @pyqtSlot()
    def load_msg(self):
        fname = QFileDialog.getOpenFileName(self,'Load file','',"Text files(*.txt)")
        opened_file = '> File : ' + fname[0]
        if fname[0]:
            f = open(fname[0],'rt',encoding='UTF8') #https://m.blog.naver.com/yejoon3117/221058408177
            with f:
                try:
                    msg_all = f.readlines()
                except:
                    print("read fail")
                for n in range(len(msg_all)):
                    msg_all[n] = msg_all[n].replace('\n', '')
        # print(msg_type_list[self.selected])
        msg, nothing = Extract_msg.extract_msg(msg_all, msg_type_list[self.selected])
        # for n in msg:
        #     print(n)

        if nothing:
            self.sig_nothing.emit(nothing)
        else:
            rst = []
            if self.selected == 1: # NAS msg
                rst.append(NAS.convert_msg(msg))
                rst.append("QCT")
                rst.append("")
                rst.append(opened_file)
            else:
                msg, vendor, debug = RRC.convert_msg(msg)
                rst.append(msg)
                rst.append(vendor)
                rst.append(debug)
                rst.append(opened_file)
            self.sig_rst.emit(rst)

class Result_tab(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.LBL_VENDOR = QLabel("Extract & Convert Result")
        self.LBL_FILE = QLabel()

        self.LBL_CONV = QLabel("CONVERTED MSG")
        self.LBL_CONV.setFont(BoldFont)
        self.DSP_CONV = QTextBrowser()
        self.DSP_CONV.setFont(CourierNewFont)
        self.DSP_CONV.setFixedHeight(500)
        self.LBL_DEBUG = QLabel("DEBUG MSG")
        self.LBL_DEBUG.setFont(BoldFont)
        self.DSP_DEBUG = QTextBrowser()
        self.DSP_DEBUG.setFont(CourierNewFont)
        self.DSP_DEBUG.setFixedHeight(100)

        self.btn_save = QPushButton("Save As..")
        self.btn_save.setFixedWidth(100)
        self.LBL_SAVED = QLabel()

        cb = QComboBox(self)
        cb.addItem(".txt")
        cb.addItem(".csv")
        cb.setFixedWidth(50)
        cb.setToolTip("Please select which format you want to save as.")

        self.selected = ".txt"
        cb.activated[str].connect(self.onActivated)

        hbox3 =QHBoxLayout()
        hbox3.addWidget(self.btn_save)
        hbox3.addWidget(cb)
        hbox3.addWidget(self.LBL_SAVED)
        hbox3.addStretch()

        hbox4 = QHBoxLayout()
        hbox4.addWidget(self.LBL_VENDOR)
        hbox4.addWidget(self.LBL_FILE)
        hbox4.addStretch()

        vbox = QVBoxLayout()
        vbox.addLayout(hbox4)
        vbox.addWidget(QLabel())
        vbox.addWidget(self.LBL_CONV)
        vbox.addWidget(self.DSP_CONV)
        vbox.addWidget(QLabel())
        vbox.addWidget(self.LBL_DEBUG)
        vbox.addWidget(self.DSP_DEBUG)
        vbox.addWidget(QLabel())
        vbox.addLayout(hbox3)
        vbox.addWidget(QLabel())
        vbox.addStretch()

        self.setLayout(vbox)
        self.btn_save.clicked.connect(self.save_file)

    def onActivated(self, text):
        self.selected = text

    @pyqtSlot()
    def save_file(self):
        file_contents = "=" * 90 + '\n'
        file_contents += self.LBL_VENDOR.text() +'\n'
        file_contents += "=" * 90 + '\n'
        if self.LBL_FILE.text():
            file_contents += ' ' + self.LBL_FILE.text() +'\n'
            file_contents += "=" * 90 + '\n'*2
        else:
            file_contents += '\n'

        if self.DSP_CONV.toPlainText() != '':
            file_contents += self.format(self.LBL_CONV, self.DSP_CONV)
        if self.DSP_DEBUG.toPlainText() != '':
            file_contents += self.format(self.LBL_DEBUG, self.DSP_DEBUG)

        if self.selected == ".txt":
            save_path = QFileDialog.getSaveFileName(self,'Save file','',"Text files(*.txt)")
            fp = open(save_path[0], "w")
            fp.write(file_contents)
            fp.close()
        elif self.selected == ".csv":
            save_path = QFileDialog.getSaveFileName(self,'Save file','',"CSV files(*.csv)")
            fp = open(save_path[0], "w")
            fp.write(file_contents.replace('\t',','))
            fp.close()
        self.LBL_SAVED.setText(" " + save_path[0])

    def format(self, subject1, subject2):
        contents = "=" * 90 + '\n'
        contents += subject1.text() + '\n'
        contents += "=" * 90 + '\n'
        if subject2 == self.DSP_CONV:
            contents += subject2.toPlainText().replace('  ','\t') + '\n'
        else:
            contents += subject2.toPlainText() + '\n'
        contents += "=" * 90 + '\n'
        contents += "\n"
        return contents

    def init_UI_rst(self):
        self.LBL_VENDOR.setText("Extract & Convert Result")
        self.LBL_FILE.setText("")
        self.LBL_CONV.setText("CONVERTED MSG")
        self.DSP_CONV.setPlainText("")
        self.LBL_DEBUG.setText("DEBUG MSG")
        self.DSP_DEBUG.setPlainText("")
        self.LBL_SAVED.setText("")

    @pyqtSlot(list, name='Nothing')
    def slot_nothing(self, v:list):
        self.init_UI_rst()
        msg_filter(v, self.LBL_DEBUG, self.DSP_DEBUG)

    @pyqtSlot(list, name='DSP RESULT')
    def slot_rst(self, v:list):
        self.init_UI_rst()
        self.LBL_CONV.setText(v[0][0])
        for n in range(1, len(v[0])):
            v[0][n] = v[0][n].replace('\t','  ')
        self.DSP_CONV.setPlainText('\n'.join(v[0][1:]))
        self.LBL_VENDOR.setText("Extract & Convert Result (" + v[1].replace(' ','') + ")")
        msg_filter(v[2], self.LBL_DEBUG, self.DSP_DEBUG)
        if v[3]:
            self.LBL_FILE.setText(v[3])

def msg_filter(v, par1, par2):
    v_filtered = []
    v_lbl = ''
    for n in v:
        if '===' not in n and '---' not in n:
            if 'BAND COMB' in n or 'FEATURESET' in n:
                v_lbl = n
            elif 'DEBUG' in n:
                v_lbl = n + '  > Please send it to "ajs3013@lguplus.co.kr"'
            else:
                v_filtered.append(n)
    v_dsp = '\n'.join(v_filtered)
    if v_dsp:
        if "find nothing from your message" not in v_dsp:
            par1.setText(v_lbl)
    par2.setPlainText(v_dsp)

    return

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())