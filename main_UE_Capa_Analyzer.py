import Extract_msg
import RRC
import RRC_items
import MRDC
import EUTRA
import NR
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5 import QtGui

msg_type_list =[]
# msg_type_list.append('valueUE-EUTRA-Capability::=')  # QCT
msg_type_list.append('UE-EUTRA-Capability')  # LSI/LQMS/Inno
# msg_type_list.append('valueUE-NR-Capability::=')  # QCT
msg_type_list.append('UE-NR-Capability')  # LSI/LQMS/Inno
# msg_type_list.append('valueUE-MRDC-Capability::=')  # QCT
msg_type_list.append('UE-MRDC-Capability')  # LSI/LQMS/Inno

BoldFont = QtGui.QFont()
BoldFont.setBold(True)

CourierNewFont = QtGui.QFont()
CourierNewFont.setFamily("Courier New")

def process (msg):
    debug = []
    msg, rst, debug = RRC.convert_msg(msg)

    # print(rst)
    # for n in msg:
    #     print(n)

    mrdc_rst = []
    msg_mrdc = MRDC.extract_mrdc_msg(msg)
    # for n in msg_mrdc:
    #     print(n)
    if msg_mrdc:
        item_sort = RRC_items.sort_items(msg_mrdc)
        # for n in item_sort:
        #     print(n)
        mrdc_rst, nr_featureset_Id, mrdc_item_max = MRDC.extract_band_combo(item_sort, msg_mrdc, 0)
        # print(mrdc_rst)
    else:
        mrdc_item_max = 0

    eutra_rst = []
    eutra_featureSet = []
    msg_eutra = EUTRA.extract_eutra_msg(msg)
    # for n in msg_eutra:
    #     print(n)

    if msg_eutra:
        item_sort = RRC_items.sort_items(msg_eutra)
        eutra_rst, eutra_featureSet, eutra_item_max = EUTRA.extract_band_combo(item_sort, msg_eutra, mrdc_item_max)
        # print("OK")
        if eutra_item_max > mrdc_item_max:
            mrdc_rst = []
            msg_mrdc = MRDC.extract_mrdc_msg(msg)
            if msg_mrdc:
                item_sort = RRC_items.sort_items(msg_mrdc)
                mrdc_rst, nr_featureset_Id, mrdc_item_max = MRDC.extract_band_combo(item_sort, msg_mrdc, eutra_item_max)



    nr_featureSet = []
    msg_nr = NR.extract_nr_msg(msg)
    if msg_nr:
        item_sort = RRC_items.sort_items(msg_nr)
        nr_featureSet = NR.extract_featureset(item_sort, msg_nr, nr_featureset_Id)

    return eutra_rst, eutra_featureSet, mrdc_rst, nr_featureSet, rst, debug


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
        self.tabs.addTab(self.tab_Paste, '&Paste')
        self.tabs.addTab(self.tab_File, '&File')
        self.tabs.addTab(self.tab_Result, '&Result')
        # self.tabs.addTab(self.tab_About,'About')

        vbox = QVBoxLayout()
        vbox.addWidget(self.tabs)
        vbox.addWidget(QLabel("Copyright 2022. JUSEOK AHN<ajs3013@lguplus.co.kr> all rights reserved."))

        self.setLayout(vbox)

        self.setWindowTitle('UE Capa Decoder v.1.2')
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
#         TB_content += "Version : v.1.1\n"
#         TB_content += "Data    : 2020-01-11\n"
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

        msg_all = ''
        self.te = QTextEdit()
        self.te.setAcceptRichText(False)
        self.te.setToolTip('Paste logs including UE Capa msg.')
        self.te.setFixedHeight(500)


        self.msg_all = self.te.toPlainText()

        self.Exe_btn = QPushButton("Execute")
        self.Exe_btn.setFixedWidth(100)
        self.Exe_btn.setCheckable(False)

        self.Exe_btn.clicked.connect(self.load_msg)

        vbox = QVBoxLayout()
        vbox.addWidget(self.te)
        vbox.addWidget(self.Exe_btn)
        vbox.addStretch()

        self.setLayout(vbox)

    @pyqtSlot()
    def load_msg(self):
        msg_all_str = self.te.toPlainText()
        msg_all = msg_all_str.split('\n')
        msg, nothing = Extract_msg.extract_msg(msg_all, msg_type_list)
        if nothing:
            self.sig_nothing.emit(nothing)
        else:
            rst = []
            eutra_bc, eutra_featureSet, mrdc_bc, nr_featureSet, vendor, debug = process(msg)
            rst.append(eutra_bc)
            rst.append(eutra_featureSet)
            rst.append(mrdc_bc)
            rst.append(nr_featureSet)
            rst.append(vendor)
            rst.append(debug)
            rst.append("") # Opened_file
            self.sig_rst.emit(rst)



class File_Tab(QWidget):

    # Signal
    sig_rst = pyqtSignal(list, name ='Result')
    sig_nothing = pyqtSignal(list, name ='Nothing')

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.open_btn = QPushButton("Open")
        self.open_btn.setFixedWidth(100)
        self.open_btn.setCheckable(False)
        self.open_btn.setToolTip('Open a log file(.txt) including UE Capa msg.')

        vbox = QVBoxLayout()
        vbox.addWidget(self.open_btn)
        vbox.addStretch()

        self.setLayout(vbox)
        self.open_btn.clicked.connect(self.load_msg)

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

        msg, nothing = Extract_msg.extract_msg(msg_all, msg_type_list)
        # for n in msg:
        #     print(n)

        if nothing:
            self.sig_nothing.emit(nothing)
        else:
            rst = []
            eutra_bc, eutra_featureSet, mrdc_bc, nr_featureSet, vendor, debug = process(msg)
            rst.append(eutra_bc)
            rst.append(eutra_featureSet)
            rst.append(mrdc_bc)
            rst.append(nr_featureSet)
            rst.append(vendor)
            rst.append(debug)
            rst.append(opened_file)
            self.sig_rst.emit(rst)

class Result_tab(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.LBL_VENDOR = QLabel("UE Capa Decoding Result")
        self.LBL_FILE = QLabel()

        self.LBL_EUTRA_BC = QLabel("EUTRA BAND COMB")
        self.LBL_EUTRA_BC.setFont(BoldFont)
        self.DSP_EUTRA_BC = QTextBrowser()
        self.DSP_EUTRA_BC.setFont(CourierNewFont)
        self.DSP_EUTRA_BC.setFixedHeight(150)


        self.LBL_MRDC_BC = QLabel("MRDC BAND COMB")
        self.LBL_MRDC_BC.setFont(BoldFont)
        self.DSP_MRDC_BC = QTextBrowser()
        self.DSP_MRDC_BC.setFont(CourierNewFont)
        self.DSP_MRDC_BC.setFixedHeight(150)


        self.LBL_EUTRA_FS = QLabel("EUTRA FEATURESET")
        self.LBL_EUTRA_FS.setFont(BoldFont)
        self.DSP_EUTRA_FS = QTextBrowser()
        self.DSP_EUTRA_FS.setFont(CourierNewFont)
        self.DSP_EUTRA_FS.setFixedHeight(100)

        self.LBL_NR_FS = QLabel("NR FEATURESET")
        self.LBL_NR_FS.setFont(BoldFont)
        self.DSP_NR_FS = QTextBrowser()
        self.DSP_NR_FS.setFont(CourierNewFont)
        self.DSP_NR_FS.setFixedHeight(100)

        self.LBL_DEBUG = QLabel("DEBUG MSG")
        self.LBL_DEBUG.setFont(BoldFont)
        self.DSP_DEBUG = QTextBrowser()
        self.DSP_DEBUG.setFont(CourierNewFont)
        self.DSP_DEBUG.setFixedHeight(100)

        self.btn_save = QPushButton("Save As..")
        self.btn_save.setFixedWidth(100)
        self.LBL_SAVED = QLabel()


        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.LBL_EUTRA_FS)
        hbox1.addWidget(self.LBL_NR_FS)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.DSP_EUTRA_FS)
        hbox2.addWidget(self.DSP_NR_FS)

        hbox3 =QHBoxLayout()
        hbox3.addWidget(self.btn_save)
        hbox3.addWidget(self.LBL_SAVED)

        hbox4 = QHBoxLayout()
        hbox4.addWidget(self.LBL_VENDOR)
        hbox4.addWidget(self.LBL_FILE)
        hbox4.addStretch()

        vbox = QVBoxLayout()
        vbox.addLayout(hbox4)
        vbox.addWidget(QLabel())
        vbox.addWidget(self.LBL_EUTRA_BC)
        vbox.addWidget(self.DSP_EUTRA_BC)
        vbox.addWidget(QLabel())
        vbox.addWidget(self.LBL_MRDC_BC)
        vbox.addWidget(self.DSP_MRDC_BC)
        vbox.addWidget(QLabel())
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addWidget(QLabel())
        vbox.addWidget(self.LBL_DEBUG)
        vbox.addWidget(self.DSP_DEBUG)
        vbox.addWidget(QLabel())
        vbox.addLayout(hbox3)
        vbox.addWidget(QLabel())
        vbox.addStretch()

        self.setLayout(vbox)
        self.btn_save.clicked.connect(self.save_file)

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

        if self.DSP_EUTRA_BC.toPlainText() != '':
            file_contents += self.format(self.LBL_EUTRA_BC, self.DSP_EUTRA_BC)
        if self.DSP_MRDC_BC.toPlainText() != '':
            file_contents += self.format(self.LBL_MRDC_BC, self.DSP_MRDC_BC)
        if self.DSP_EUTRA_FS.toPlainText() != '':
            file_contents += self.format(self.LBL_EUTRA_FS, self.DSP_EUTRA_FS)
        if self.DSP_NR_FS.toPlainText() != '':
            file_contents += self.format(self.LBL_NR_FS, self.DSP_NR_FS)
        if self.DSP_DEBUG.toPlainText() != '':
            file_contents += self.format(self.LBL_DEBUG, self.DSP_DEBUG)

        save_path = QFileDialog.getSaveFileName(self,'Save file','',"Text files(*.txt)")
        fp = open(save_path[0], "w")
        fp.write(file_contents)
        fp.close()
        self.LBL_SAVED.setText(" " + save_path[0])

    def format(self, subject1, subject2):
        contents = "=" * 90 + '\n'
        contents += subject1.text() + '\n'
        contents += "=" * 90 + '\n'
        contents += subject2.toPlainText() + '\n'
        contents += "=" * 90 + '\n'
        contents += "\n"
        return contents

    def init_UI_rst(self):
        self.LBL_VENDOR.setText("UE Capa Decoding Result")
        self.LBL_FILE.setText("")
        self.LBL_EUTRA_BC.setText("EUTRA BAND COMB")
        self.DSP_EUTRA_BC.setPlainText("")
        self.LBL_MRDC_BC.setText("MRDC BAND COMB")
        self.DSP_MRDC_BC.setPlainText("")
        self.LBL_EUTRA_FS.setText("EUTRA FEATURESET")
        self.DSP_EUTRA_FS.setPlainText("")
        self.LBL_NR_FS.setText("NR FEATURESET")
        self.DSP_NR_FS.setPlainText("")
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

        msg_filter(v[0], self.LBL_EUTRA_BC, self.DSP_EUTRA_BC)
        msg_filter(v[1], self.LBL_EUTRA_FS, self.DSP_EUTRA_FS)
        msg_filter(v[2], self.LBL_MRDC_BC, self.DSP_MRDC_BC)
        msg_filter(v[3], self.LBL_NR_FS, self.DSP_NR_FS)
        msg_filter(v[5], self.LBL_DEBUG, self.DSP_DEBUG)

        #VENDOR
        self.LBL_VENDOR.setText("UE Capa Decoding Result (" + v[4].replace(' ','') + ")")

        # Opened file
        if v[6]:
            self.LBL_FILE.setText(v[6])

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