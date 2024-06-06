from collections import namedtuple

from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import QMessageBox, QWidget, QLabel, QComboBox, \
    QLineEdit, QGridLayout, QTabWidget, \
    QMainWindow, QPushButton, QApplication, QInputDialog, QTableWidget, QTableWidgetItem

import well_data

from work_py.alone_oreration import well_volume
from main import MyWindow
from work_py.change_fluid import TabPage_SO_swab, Change_fluid_Window

from work_py.alone_oreration import privyazkaNKT, need_h2s
from .rationingKRS import descentNKT_norm, liftingNKT_norm, well_volume_norm



class TabPage_SO_swab(QWidget):
    def __init__(self, tableWidget):
        from .acid_paker import CheckableComboBox
        super().__init__()
        self.validator_int = QIntValidator(0, 8000)
        self.validator_float = QDoubleValidator(0.87, 1.65, 2)
        self.swab_true_label_type = QLabel("компоновка", self)
        self.swab_true_edit_type = QComboBox(self)
        self.tableWidget = tableWidget
        paker_layout_list = ['двухпакерная', 'однопакерная',
                                        'воронка', 'пакер с заглушкой', 'Опрессовка снижением уровня на шаблоне',
                                        'Опрессовка снижением уровня на пакере с заглушкой']
        self.swab_true_edit_type.addItems(paker_layout_list)

        self.swab_true_edit_type.setCurrentIndex(3)

        self.depth_gauge_label = QLabel("глубинные манометры", self)
        self.depthGaugeCombo = QComboBox(self)
        self.depthGaugeCombo.addItems(['Нет', 'Да'])

        self.diametr_paker_labelType = QLabel("Диаметр пакера", self)
        self.diametr_paker_edit = QLineEdit(self)

        self.pakerLabel = QLabel("глубина пакера", self)
        self.pakerEdit = QLineEdit(self)
        self.pakerEdit.setValidator(self.validator_int)


        if (well_data.perforation_sole - 40) < well_data.current_bottom:
            self.pakerEdit.setText(f"{int(well_data.perforation_sole - 40)}")
        else:
            self.pakerEdit.setText(f"{int(well_data.current_bottom - 40)}")

        self.paker2Label = QLabel("глубина вверхнего пакера", self)
        self.paker2Edit = QLineEdit(self)
        self.paker2Edit.setValidator(self.validator_int)
        if (well_data.perforation_sole - 40) < well_data.current_bottom:
            self.paker2Edit.setText(f"{int(well_data.perforation_sole - 40)}")
        else:
            self.pakerEdit.setText(f"{int(well_data.current_bottom - 40)}")

        self.khovst_label = QLabel("Длина хвостовики", self)
        self.khvostEdit = QLineEdit(self)
        self.khvostEdit.setValidator(self.validator_int)
        self.khvostEdit.setText(str(10))
        self.khvostEdit.setClearButtonEnabled(True)

        plast_work = ['']
        plast_work.extend(well_data.plast_work)

        self.plast_label = QLabel("Выбор пласта", self)
        self.plast_combo = CheckableComboBox(self)
        self.plast_combo.combo_box.addItems(plast_work)
        self.plast_combo.combo_box.currentTextChanged.connect(self.update_plast_edit)

        self.swabTypeLabel = QLabel("задача при освоении", self)
        self.swabTypeCombo = QComboBox(self)
        self.swabTypeCombo.addItems(['Задача №2.1.13', 'Задача №2.1.16', 'Задача №2.1.11', 'ГРР'
                                     'своя задача'])
        self.swabTypeCombo.setCurrentIndex(well_data.swabTypeComboIndex)
        self.swabTypeCombo.setProperty('value', 'Задача №2.1.16')

        self.swab_volumeEditLabel = QLabel("объем освоения", self)
        self.swab_volumeEdit = QLineEdit(self)
        self.swab_volumeEdit.setValidator(self.validator_int)
        self.swab_volumeEdit.setText('20')

        self.need_change_zgs_label = QLabel('Необходимо ли менять ЖГС', self)
        self.need_change_zgs_combo = QComboBox(self)
        self.need_change_zgs_combo.addItems(['Нет', 'Да'])

        self.fluid_new_label = QLabel('удельный вес ЖГС', self)
        self.fluid_new_edit = QLineEdit(self)
        self.fluid_new_edit.setValidator(self.validator_float)
        self.pressuar_new_label = QLabel('Ожидаемое давление', self)
        self.pressuar_new_edit = QLineEdit(self)
        self.pressuar_new_edit.setValidator(self.validator_int)

        if len(well_data.plast_project) == 0:
            self.plast_new_label = QLabel('индекс нового пласта', self)
            self.plast_new_combo = QComboBox(self)
            self.plast_new_combo.addItems(well_data.plast_project)
        else:
            self.plast_new_label = QLabel('индекс нового пласта', self)
            self.plast_new_combo = QLineEdit(self)

        self.swab_true_edit_type.currentTextChanged.connect(self.swabTrueEdit_select)

        self.grid = QGridLayout(self)
        self.grid.addWidget(self.swab_true_label_type, 0, 0)
        self.grid.addWidget(self.swab_true_edit_type, 1, 0)
        self.grid.addWidget(self.plast_label, 0, 1)
        self.grid.addWidget(self.plast_combo, 1, 1)
        self.grid.addWidget(self.diametr_paker_labelType, 0, 2)
        self.grid.addWidget(self.diametr_paker_edit, 1, 2)
        self.grid.addWidget(self.khovst_label, 0, 3)
        self.grid.addWidget(self.khvostEdit, 1, 3)
        self.grid.addWidget(self.pakerLabel, 0, 4)
        self.grid.addWidget(self.pakerEdit, 1, 4)
        self.grid.addWidget(self.paker2Label, 0, 5)
        self.grid.addWidget(self.paker2Edit, 1, 5)

        self.grid.addWidget(self.swabTypeLabel, 6, 1)
        self.grid.addWidget(self.swabTypeCombo, 7, 1)

        self.grid.addWidget(self.swab_volumeEditLabel, 6, 2)
        self.grid.addWidget(self.swab_volumeEdit, 7, 2)
        self.grid.addWidget(self.depth_gauge_label, 6, 3)
        self.grid.addWidget(self.depthGaugeCombo, 7, 3)

        self.grid.addWidget(self.need_change_zgs_label, 9, 1)
        self.grid.addWidget(self.need_change_zgs_combo, 10, 1)
        self.diametr_paker_edit.setText('122')
        # self.grid.addWidget(self.plast_new_label, 9, 3)
        # self.grid.addWidget(self.plast_new_combo, 10, 3)
        #
        # self.grid.addWidget(self.fluid_new_label, 9, 4)
        # self.grid.addWidget( self.fluid_new_edit, 10, 4)
        #
        # self.grid.addWidget(self.pressuar_new_label, 9, 5)
        # self.grid.addWidget(self.pressuar_new_edit, 10, 5)
        self.need_change_zgs_combo.currentTextChanged.connect(self.update_change_fluid)

        if all(well_data.dict_perforation[plast]['отрайбировано'] for plast in list(well_data.dict_perforation.keys())):
            self.swab_true_edit_type.setCurrentIndex(0)
        else:
            self.swab_true_edit_type.setCurrentIndex(1)
        self.pakerEdit.textChanged.connect(self.update_paker_edit)
        self.paker2Edit.textChanged.connect(self.update_paker_edit)
        self.pakerEdit.textChanged.connect(self.update_paker_diametr)

    def update_change_fluid(self, index):
        if index == 'Да':
            if len(well_data.plast_project) != 0:
                self.plast_new_combo = QComboBox(self)
                self.plast_new_combo.addItems(well_data.plast_project)
                plast = self.plast_new_combo.currentText()
            else:
                self.plast_new_combo = QLineEdit(self)
                plast = self.plast_new_combo.text()

            cat_h2s_list_plan = list(map(int, [well_data.dict_category[plast]['по сероводороду'].category for plast in
                                               well_data.plast_project if well_data.dict_category.get(plast) and
                                               well_data.dict_category[plast]['отключение'] == 'планируемый']))

            if len(cat_h2s_list_plan) != 0:
                self.pressuar_new_edit.setText(f'{well_data.dict_category[plast]["по давлению"].data_pressuar}')
            self.grid.addWidget(self.plast_new_label, 9, 2)
            self.grid.addWidget(self.plast_new_combo, 10, 2)

            self.grid.addWidget(self.fluid_new_label, 9, 3)
            self.grid.addWidget(self.fluid_new_edit, 10, 3)

            self.grid.addWidget(self.pressuar_new_label, 9, 4)
            self.grid.addWidget(self.pressuar_new_edit, 10, 4)
        else:

            self.plast_new_label.setParent(None)
            self.plast_new_combo.setParent(None)
            self.fluid_new_label.setParent(None)
            self.fluid_new_edit.setParent(None)
            self.pressuar_new_label.setParent(None)
            self.pressuar_new_edit.setParent(None)

    def update_paker_edit(self):
        dict_perforation = well_data.dict_perforation
        rows = self.tableWidget.rowCount()
        plasts = well_data.texts
        # print(plasts)
        roof_plast = well_data.current_bottom
        sole_plast = 0
        for plast in well_data.plast_work:
            for plast_sel in plasts:
                if plast_sel == plast:
                    if roof_plast >= dict_perforation[plast]['кровля']:
                        roof_plast = dict_perforation[plast]['кровля']
                    if sole_plast <= dict_perforation[plast]['подошва']:
                        sole_plast = dict_perforation[plast]['подошва']

        paker_depth = self.pakerEdit.text()
        if self.swab_true_edit_type.currentText() in ['однопакерная', 'однопакерная, упорный', 'пакер с заглушкой']:
            if paker_depth != '':
                self.khvostEdit.setText(str(10))


            if rows == 0:
                if paker_depth != '' and self.khvostEdit.text() != '':
                    self.distance_between_packers_voronka = int(self.khvostEdit.text()) - int(self.pakerEdit.text())
            else:
                self.khvostEdit.setEnabled(False)
                if self.khvostEdit != '':
                    self.khvostEdit.setText(f'{int(paker_depth) - self.distance_between_packers_voronka}')
                self.khvostEdit.setEnabled(False)
        elif self.swab_true_edit_type.currentText() in ['двухпакерная', 'двухпакерная, упорные']:
            if rows == 0:
                if paker_depth != '':
                    self.khvostEdit.setText(f'{10}')

                    if self.swab_true_edit_type.currentText() == 'двухпакерная, упорные':
                        self.khvostEdit.setText(str(int(well_data.current_bottom - int(paker_depth))))

                if self.pakerEdit.text() != '' and self.paker2Edit.text() != '':
                    self.distance_between_packers = abs(int(self.pakerEdit.text()) - int(self.paker2Edit.text()))

                    print(f' расстояние между пакерами {self.distance_between_packers}')
            else:
                self.khvostEdit.setEnabled(False)
                self.paker2Edit.setEnabled(False)
                if self.pakerEdit.text() != '':
                    self.paker2Edit.setText(f'{int(self.pakerEdit.text()) - self.distance_between_packers}')


        elif self.swab_true_edit_type.currentText() in ['воронка']:
            self.khvostEdit.setText(f'{sole_plast}')

    def update_paker_diametr(self):
        from .opressovka import TabPage_SO
        paker_depth = self.pakerEdit.text()
        if paker_depth:
            paker_diametr = int(TabPage_SO.paker_diametr_select(self, paker_depth))
            self.diametr_paker_edit.setText(str(int(paker_diametr)))

    def swabTrueEdit_select(self):


        if self.swab_true_edit_type.currentText() == 'однопакерная':
            paker_layout_list_tab = ["Пласт", "хвост", "пакер", "вид освоения", "объем освоения"]
            self.pakerLabel.setText('Глубина пакера')
            self.grid.addWidget(self.plast_label, 0, 1)
            self.grid.addWidget(self.plast_combo, 1, 1)
            self.grid.addWidget(self.khovst_label, 0, 3)
            self.grid.addWidget(self.khvostEdit, 1, 3)
            self.paker2Label.setParent(None)
            self.paker2Edit.setParent(None)
            self.grid.addWidget(self.pakerLabel, 0, 4)
            self.grid.addWidget(self.pakerEdit, 1, 4)
            self.grid.addWidget(self.diametr_paker_labelType, 0, 2)
            self.grid.addWidget(self.diametr_paker_edit, 1, 2)

            self.plast_new_label.setParent(None)
            self.plast_new_combo.setParent(None)
            self.fluid_new_label.setParent(None)
            self.fluid_new_edit.setParent(None)
            self.pressuar_new_label.setParent(None)
            self.pressuar_new_edit.setParent(None)

        elif self.swab_true_edit_type.currentText() == 'двухпакерная':
            self.pakerLabel.setText('Глубина нижнего пакера')
            self.grid.addWidget(self.khovst_label, 0, 3)
            self.grid.addWidget(self.khvostEdit, 1, 3)
            self.grid.addWidget(self.pakerLabel, 0, 4)
            self.grid.addWidget(self.plast_label, 0, 1)
            self.grid.addWidget(self.plast_combo, 1, 1)
            self.grid.addWidget(self.pakerEdit, 1, 4)
            self.grid.addWidget(self.paker2Label, 0, 5)
            self.grid.addWidget(self.paker2Edit, 1, 5)
            self.grid.addWidget(self.diametr_paker_labelType, 0, 2)
            self.grid.addWidget(self.diametr_paker_edit, 1, 2)
            self.plast_new_label.setParent(None)
            self.plast_new_combo.setParent(None)
            self.fluid_new_label.setParent(None)
            self.fluid_new_edit.setParent(None)
            self.pressuar_new_label.setParent(None)
            self.pressuar_new_edit.setParent(None)
            paker_layout_list_tab = ["Пласт", "хвост", "пакер", "2-й пакер", "вид освоения", "объем освоения"]

        elif self.swab_true_edit_type.currentText() == 'воронка':

            self.pakerLabel.setText('Глубина воронки')
            self.khovst_label.setParent(None)
            self.khvostEdit.setParent(None)
            self.paker2Label.setParent(None)
            self.paker2Edit.setParent(None)
            self.diametr_paker_labelType.setParent(None)
            self.diametr_paker_edit.setParent(None)

            self.fluid_new_label.setParent(None)
            self.fluid_new_edit.setParent(None)
            self.pressuar_new_label.setParent(None)
            self.pressuar_new_edit.setParent(None)
            paker_layout_list_tab = ["Пласт", "воронка", "вид освоения", "объем освоения"]

        elif self.swab_true_edit_type.currentText() == 'пакер с заглушкой':
            self.swabTypeLabel.setParent(None)
            self.swabTypeCombo.setParent(None)
            self.swab_volumeEdit.setParent(None)

            self.khovst_label.setParent(None)
            self.khvostEdit.setParent(None)
            self.pakerLabel.setParent(None)
            self.pakerEdit.setParent(None)
            self.plast_new_label.setParent(None)
            self.plast_new_combo.setParent(None)
            self.fluid_new_label.setParent(None)
            self.fluid_new_edit.setParent(None)
            self.pressuar_new_label.setParent(None)
            self.pressuar_new_edit.setParent(None)
            self.diametr_paker_labelType.setParent(None)
            self.diametr_paker_edit.setParent(None)
            self.pakerLabel.setText('Глубина пакера')
            self.paker2Label.setText('Глубина понижения')
            self.paker2Edit.setText(f'{well_data.current_bottom - 250}')
            self.grid.addWidget(self.paker2Label, 0, 5)
            self.grid.addWidget(self.paker2Edit, 1, 5)

            self.grid.addWidget(self.khovst_label, 0, 3)
            self.grid.addWidget(self.khvostEdit, 1, 3)
            self.grid.addWidget(self.pakerLabel, 0, 4)
            self.grid.addWidget(self.pakerEdit, 1, 4)
            self.grid.addWidget(self.diametr_paker_labelType, 0, 2)
            self.grid.addWidget(self.diametr_paker_edit, 1, 2)
            self.paker2Label.setParent(None)
            self.paker2Edit.setParent(None)
            paker_layout_list_tab = ["Пласт", "хвост", "пакер", "вид освоения", "объем освоения"]
        elif self.swab_true_edit_type.currentText() == 'Опрессовка снижением уровня на шаблоне':
            self.depth_gauge_label.setParent(None)
            self.depthGaugeCombo.setParent(None)
            self.swab_volumeEditLabel.setParent(None)
            self.swabTypeLabel.setParent(None)
            self.swabTypeCombo.setParent(None)
            self.swab_volumeEdit.setParent(None)
            self.plast_label.setParent(None)
            self.plast_combo.setParent(None)
            self.khovst_label.setParent(None)
            self.khvostEdit.setParent(None)
            self.pakerLabel.setParent(None)
            self.pakerEdit.setParent(None)
            self.diametr_paker_labelType.setParent(None)
            self.diametr_paker_edit.setParent(None)
            self.paker2Label.setText('Глубина Понижения уровня')
            self.paker2Edit.setText(f'{well_data.current_bottom - 250}')
            self.grid.addWidget(self.paker2Label, 0, 5)
            self.grid.addWidget(self.paker2Edit, 1, 5)

            self.need_change_zgs_label = QLabel('Необходимо ли менять ЖГС', self)
            self.need_change_zgs_combo = QComboBox(self)
            self.need_change_zgs_combo.addItems(['Нет', 'Да'])

            if len(well_data.plast_work) == 0:
                self.need_change_zgs_combo.setCurrentIndex(1)

            if len(well_data.plast_project) == 0:
                self.plast_new_label = QLabel('индекс нового пласта', self)
                self.plast_new_combo = QComboBox(self)
                self.plast_new_combo.addItems(well_data.plast_project)
            else:
                self.plast_new_label = QLabel('индекс нового пласта', self)
                self.plast_new_combo = QLineEdit(self)

            self.fluid_new_label = QLabel('удельный вес ЖГС', self)
            self.fluid_new_edit = QLineEdit(self)

            self.pressuar_new_label = QLabel('Ожидаемое давление', self)
            self.pressuar_new_edit = QLineEdit(self)
            paker_layout_list_tab = ["забой", "глубина понижения", "вид освоения"]


        elif self.swab_true_edit_type.currentText() == 'Опрессовка снижением уровня на пакере с заглушкой':
            self.paker2Label.setText('Глубина Понижения уровня')
            self.paker2Edit.setText(f'{well_data.current_bottom - 250}')
            self.grid.addWidget(self.khovst_label, 0, 3)
            self.grid.addWidget(self.khvostEdit, 1, 3)
            self.grid.addWidget(self.pakerLabel, 0, 4)
            self.grid.addWidget(self.pakerEdit, 1, 4)
            self.grid.addWidget(self.diametr_paker_labelType, 0, 2)
            self.grid.addWidget(self.diametr_paker_edit, 1, 2)
            paker_layout_list_tab = ["забой", "хвост", "посадка пакера", "глубина понижения"]
        self.tableWidget.setHorizontalHeaderLabels([])
        self.tableWidget.setHorizontalHeaderLabels(paker_layout_list_tab)
    def update_plast_edit(self):

        dict_perforation = well_data.dict_perforation
        plasts = well_data.texts
        # print(f'пласты {plasts, len(well_data.texts), len(plasts), well_data.texts}')
        roof_plast = well_data.current_bottom
        sole_plast = 0

        for plast in well_data.plast_work:
            for plast_sel in plasts:
                if plast_sel == plast:

                    if roof_plast >= dict_perforation[plast]['кровля']:
                        roof_plast = dict_perforation[plast]['кровля']
                    if sole_plast <= dict_perforation[plast]['подошва']:
                        sole_plast = dict_perforation[plast]['подошва']

        if self.swab_true_edit_type.currentText() in ['однопакерная', 'воронка',
                                                      'Опрессовка снижением уровня на шаблоне']:
            paker_depth = int(roof_plast - 40)
            self.pakerEdit.setText(f"{paker_depth}")
            self.paker2Edit.setText(str(int(paker_depth - 30)))

        else:
            paker_depth = int(sole_plast + 10)
            self.pakerEdit.setText(f"{paker_depth}")
            self.paker2Edit.setText(str(int(roof_plast - 10)))





class TabWidget(QTabWidget):
    def __init__(self, tableWidget):
        super().__init__()
        self.addTab(TabPage_SO_swab(tableWidget), 'Свабирование')


class Swab_Window(QMainWindow):
    def __init__(self, ins_ind, table_widget, parent=None):
        super(QMainWindow, self).__init__(parent)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.table_widget = table_widget

        self.ins_ind = ins_ind

        self.dict_nkt = {}
        self.table_widget = table_widget
        self.tableWidget = QTableWidget(0, 8)
        self.tabWidget = TabWidget(self.tableWidget)



        self.buttonAdd = QPushButton('Добавить данные в план работ')
        self.buttonAdd.clicked.connect(self.add_work)
        self.buttonDel = QPushButton('Удалить записи из таблице')
        self.buttonDel.clicked.connect(self.del_row_table)
        self.buttonadd_work = QPushButton('Добавить в план работ')
        self.buttonadd_work.clicked.connect(self.add_work, Qt.QueuedConnection)
        self.buttonAddString = QPushButton('Добавить освоение')
        self.buttonAddString.clicked.connect(self.addString)

        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonAddString, 2, 0)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.tableWidget, 1, 0, 1, 2)

        vbox.addWidget(self.buttonDel, 2, 1)
        vbox.addWidget(self.buttonadd_work, 3, 0, 1, 0)

    def addString(self):
        from work_py.acid_paker import AcidPakerWindow

        swab_true_edit_type = self.tabWidget.currentWidget().swab_true_edit_type.currentText()
        plast_combo = self.tabWidget.currentWidget().plast_combo.combo_box.currentText()
        swabTypeCombo = self.tabWidget.currentWidget().swabTypeCombo.currentText()
        swab_list = ['Задача №2.1.13', 'Задача №2.1.16', 'Задача №2.1.11', 'ГРР'
                                                               'своя задача']

        swab_edit_combo = QComboBox(self)
        swab_edit_combo.addItems(swab_list)
        swab_edit_combo.setCurrentIndex(swab_list.index(swabTypeCombo))

        swab_volume_edit = int(float(self.tabWidget.currentWidget().swab_volumeEdit.text().replace(',', '.')))


        if (not plast_combo or not swab_volume_edit) and swab_true_edit_type in ['однопакерная', 'пакер с заглушкой',
                                                                                 'воронка', 'двухпакерная']:
            msg = QMessageBox.information(self, 'Внимание', 'Заполните данные по объему')
            return

        self.tableWidget.setSortingEnabled(False)
        rows = self.tableWidget.rowCount()

        if swab_true_edit_type in ['однопакерная', 'пакер с заглушкой']:
            if rows != 0:
                mes = QMessageBox.warning(self, 'ОШИБКА', 'НЕЛЬЗЯ на одной и тоже компоновки освоивать повторно')
                return
            paker_khost = AcidPakerWindow.if_None(self, self.tabWidget.currentWidget().khvostEdit.text())
            paker_depth = AcidPakerWindow.if_None(self, self.tabWidget.currentWidget().pakerEdit.text())

            if well_data.current_bottom < float(paker_khost + paker_depth) or \
                    0 < paker_khost + paker_depth < well_data.current_bottom is False:
                msg = QMessageBox.information(self, 'Внимание',
                                              f'Компоновка ниже {paker_khost + paker_depth}м текущего забоя '
                                              f'{well_data.current_bottom}м')
                return
            if MyWindow.check_true_depth_template(self, paker_depth) is False:
                return
            if MyWindow.true_set_Paker(self, paker_depth) is False:
                return
            if MyWindow.check_depth_in_skm_interval(self, paker_depth) is False:
                return

            self.tableWidget.insertRow(rows)
            self.tableWidget.setItem(rows, 0, QTableWidgetItem(plast_combo))
            self.tableWidget.setItem(rows, 1, QTableWidgetItem(str(paker_khost)))
            self.tableWidget.setItem(rows, 2, QTableWidgetItem(str(paker_depth)))
            self.tableWidget.setCellWidget(rows, 3, swab_edit_combo)
            self.tableWidget.setItem(rows, 4, QTableWidgetItem(str(swab_volume_edit)))


        elif swab_true_edit_type in ['двухпакерная']:
            paker_khost = AcidPakerWindow.if_None(self, self.tabWidget.currentWidget().khvostEdit.text())
            paker_depth = AcidPakerWindow.if_None(self, self.tabWidget.currentWidget().pakerEdit.text())
            paker2_depth = AcidPakerWindow.if_None(self, self.tabWidget.currentWidget().paker2Edit.text())
            if MyWindow.check_true_depth_template(self, paker_depth) is False:
                return
            if MyWindow.true_set_Paker(self, paker_depth) is False:
                return
            if MyWindow.check_depth_in_skm_interval(self, paker_depth) is False:
                return
            if MyWindow.check_true_depth_template(self, paker2_depth) is False:
                return
            if MyWindow.true_set_Paker(self, paker2_depth) is False:
                return
            if MyWindow.check_depth_in_skm_interval(self, paker2_depth) is False:
                return

            if well_data.current_bottom < float(paker_khost + paker2_depth):
                msg = QMessageBox.information(self, 'Внимание',
                                              f'Компоновка ниже {paker_khost + paker_depth}м текущего забоя '
                                              f'{well_data.current_bottom}м')
                return
            self.tableWidget.insertRow(rows)
            self.tableWidget.setItem(rows, 0, QTableWidgetItem(plast_combo))
            self.tableWidget.setItem(rows, 1, QTableWidgetItem(str(paker_khost)))
            self.tableWidget.setItem(rows, 2, QTableWidgetItem(str(paker_depth)))
            self.tableWidget.setItem(rows, 3, QTableWidgetItem(str(paker2_depth)))
            self.tableWidget.setCellWidget(rows, 4, swab_edit_combo)
            self.tableWidget.setItem(rows, 5, QTableWidgetItem(str(swab_volume_edit)))

        elif swab_true_edit_type in ['воронка']:
            if rows != 0:
                mes = QMessageBox.warning(self, 'ОШИБКА', 'НЕЛЬЗЯ на одной и тоже компоновки освоивать повторно')
                return
            paker_khost = self.tabWidget.currentWidget().khvostEdit.text()

            self.tableWidget.insertRow(rows)
            self.tableWidget.setItem(rows, 0, QTableWidgetItem(plast_combo))
            self.tableWidget.setItem(rows, 1, QTableWidgetItem(str(paker_khost)))
            self.tableWidget.setCellWidget(rows, 2, swab_edit_combo)
            self.tableWidget.setItem(rows, 3, QTableWidgetItem(str(swab_volume_edit)))

        elif swab_true_edit_type in ['Опрессовка снижением уровня на шаблоне']:
            if rows != 0:
                mes = QMessageBox.warning(self, 'ОШИБКА', 'НЕЛЬЗЯ на одной и тоже компоновки освоивать повторно')
                return
            paker_opy = self.tabWidget.currentWidget().paker2Edit.text()
            if paker_opy != '':
                paker_opy = int(float(str(paker_opy).replace(',', '.')))

            self.tableWidget.insertRow(rows)
            self.tableWidget.setItem(rows, 0, QTableWidgetItem(str(well_data.current_bottom)))
            self.tableWidget.setItem(rows, 1, QTableWidgetItem(str(paker_opy)))

        elif swab_true_edit_type in ['Опрессовка снижением уровня на пакере с заглушкой']:
            paker_depth = AcidPakerWindow.if_None(self, self.tabWidget.currentWidget().pakerEdit.text())
            paker_khost = AcidPakerWindow.if_None(self, self.tabWidget.currentWidget().khvostEdit.text())
            if rows != 0:
                mes = QMessageBox.warning(self, 'ОШИБКА', 'НЕЛЬЗЯ на одной и тоже компоновки освоивать повторно')
            paker_opy = self.tabWidget.currentWidget().paker2Edit.text()
            if paker_opy != '':
                paker_opy = int(float(str(paker_opy).replace(',', '.')))

            self.tableWidget.insertRow(rows)
            self.tableWidget.setItem(rows, 0, QTableWidgetItem(str(well_data.current_bottom)))
            self.tableWidget.setItem(rows, 1, QTableWidgetItem(str(paker_khost)))
            self.tableWidget.setItem(rows, 2, QTableWidgetItem(str(paker_depth)))
            self.tableWidget.setItem(rows, 3, QTableWidgetItem(str(paker_opy)))


    def del_row_table(self):
        row = self.tableWidget.currentRow()
        if row == -1:
            msg = QMessageBox.information(self, 'Внимание', 'Выберите строку для удаления')
            return
        self.tableWidget.removeRow(row)

    def add_work(self):

        diametr_paker = int(float(self.tabWidget.currentWidget().diametr_paker_edit.text()))
        swab_true_edit_type = self.tabWidget.currentWidget().swab_true_edit_type.currentText()
        need_change_zgs_combo = self.tabWidget.currentWidget().need_change_zgs_combo.currentText()
        depthGaugeCombo = self.tabWidget.currentWidget().depthGaugeCombo.currentText()

        rows = self.tableWidget.rowCount()
        if need_change_zgs_combo == 'Да':
            if len(well_data.plast_project) != 0:
                plast_new_combo = self.tabWidget.currentWidget().plast_new_combo.currentText()
            else:
                plast_new_combo = self.tabWidget.currentWidget().plast_new_combo.text()

            fluid_new_edit = self.tabWidget.currentWidget().fluid_new_edit.text()
            if fluid_new_edit != '':
                fluid_new_edit = float(fluid_new_edit.replace(',', '.'))
            pressuar_new_edit = self.tabWidget.currentWidget().pressuar_new_edit.text()

            if pressuar_new_edit != '':
                pressuar_new_edit = int(float(pressuar_new_edit.replace(',', '.')))
        else:
            plast_new_combo = ''
            fluid_new_edit = ''
            pressuar_new_edit = ''
        if (plast_new_combo == '' or fluid_new_edit == '' or pressuar_new_edit == '') and \
                need_change_zgs_combo == 'Да':
            mes = QMessageBox.critical(self, 'Ошибка', 'Введены не все параметры')
            return

        for row in range(rows):
            if swab_true_edit_type in ['двухпакерная', 'двухпакерная, упорные']:
                plast_combo = self.tableWidget.item(row, 0).text()
                if row == 0:
                    paker_khost = int(float(self.tableWidget.item(row, 1).text()))
                    if paker_khost < 0:
                        mes = QMessageBox.warning(self, "ВНИМАНИЕ", 'Не корректная компоновка')
                        return
                    well_data.paker_khost = paker_khost
                else:
                    paker_khost = well_data.paker_khost

                paker_depth = int(float(self.tableWidget.item(row, 2).text()))
                paker2_depth = int(float(self.tableWidget.item(row, 3).text()))
                swabTypeCombo = self.tableWidget.cellWidget(row, 4).currentText()
                swab_volumeEdit = int(float(self.tableWidget.item(row, 2).text()))
                if row == 0:
                    work_list = self.swabbing_with_2paker(diametr_paker, paker_depth, paker2_depth, paker_khost,
                                                          plast_combo, swabTypeCombo, swab_volumeEdit, depthGaugeCombo,
                                                          need_change_zgs_combo,
                                                          plast_new_combo, fluid_new_edit, pressuar_new_edit)
                elif rows == row + 1:
                    work_list = work_list[:-1]
                    work_list.extend(self.swabbing_with_2paker(diametr_paker, paker_depth, paker2_depth, paker_khost,
                                                          plast_combo, swabTypeCombo, swab_volumeEdit, depthGaugeCombo,
                                                          need_change_zgs_combo,
                                                          plast_new_combo, fluid_new_edit, pressuar_new_edit)[1:])
                else:
                    work_list = work_list[:-1]
                    work_list.extend(self.swabbing_with_2paker(diametr_paker, paker_depth, paker2_depth, paker_khost,
                                                          plast_combo, swabTypeCombo, swab_volumeEdit, depthGaugeCombo,
                                                          need_change_zgs_combo,
                                                          plast_new_combo, fluid_new_edit, pressuar_new_edit)[1:9])

            elif swab_true_edit_type in ['однопакерная']:
                plast_combo = self.tableWidget.item(row, 0).text()


                if rows == row + 1:
                    paker_khost = int(float(self.tableWidget.item(row, 1).text()))
                    if paker_khost < 0:
                        mes = QMessageBox.warning(self, "ВНИМАНИЕ", 'Не корректная компоновка')
                        return
                    well_data.paker_khost = paker_khost
                else:
                    paker_khost = well_data.paker_khost

                paker_depth = int(float(self.tableWidget.item(row, 2).text()))
                swabTypeCombo = self.tableWidget.cellWidget(row, 3).currentText()
                swab_volumeEdit = int(float(self.tableWidget.item(row, 4).text()))
                if rows == 1:
                    work_list = self.swabbing_with_paker(diametr_paker, paker_depth, paker_khost, plast_combo,
                                                         swabTypeCombo, swab_volumeEdit, depthGaugeCombo,
                                                         need_change_zgs_combo,
                                                         plast_new_combo, fluid_new_edit, pressuar_new_edit)
                elif row == 0:
                    work_list.extend(self.swabbing_with_paker(diametr_paker, paker_depth, paker_khost, plast_combo,
                                                     swabTypeCombo, swab_volumeEdit, depthGaugeCombo, need_change_zgs_combo,
                                                     plast_new_combo, fluid_new_edit, pressuar_new_edit)[:9:-1])
                elif row == len(rows):
                    work_list.extend(self.swabbing_with_2paker(diametr_paker, paker_depth, paker2_depth, paker_khost,
                                                               plast_combo, swabTypeCombo, swab_volumeEdit,
                                                               depthGaugeCombo,
                                                               need_change_zgs_combo,
                                                               plast_new_combo, fluid_new_edit,
                                                               pressuar_new_edit)[1:9:-1])

            elif swab_true_edit_type == 'воронка':
                plast_combo = self.tableWidget.item(row, 0).text()

                paker_depth = int(float(self.tableWidget.item(row, 1).text()))
                swabTypeCombo = self.tableWidget.cellWidget(row, 2).currentText()
                swab_volumeEdit = int(float(self.tableWidget.item(row, 3).text()))

                work_list = self.swabbing_with_voronka(paker_depth, plast_combo, swabTypeCombo,
                                                       swab_volumeEdit, depthGaugeCombo, need_change_zgs_combo,
                                                 plast_new_combo, fluid_new_edit, pressuar_new_edit)

            elif swab_true_edit_type == 'пакер с заглушкой':
                plast_combo = self.tableWidget.item(row, 0).text()
                if row == 0:
                    paker_khost = int(float(self.tableWidget.item(row, 1).text()))
                    if paker_khost < 0:
                        mes = QMessageBox.warning(self, "ВНИМАНИЕ", 'Не корректная компоновка')
                        return
                    well_data.paker_khost = paker_khost
                else:
                    paker_khost = well_data.paker_khost

                paker_depth = int(float(self.tableWidget.item(row, 2).text()))
                swabTypeCombo = self.tableWidget.cellWidget(row, 3).currentText()
                swab_volumeEdit = int(float(self.tableWidget.item(row, 4).text()))

                work_list = self.swabbing_with_paker_stub(diametr_paker, paker_depth, paker_khost, plast_combo,
                                                     swabTypeCombo, swab_volumeEdit, depthGaugeCombo, need_change_zgs_combo,
                                                    plast_new_combo, fluid_new_edit, pressuar_new_edit)
            elif swab_true_edit_type == 'Опрессовка снижением уровня на шаблоне':
                paker2_depth = int(float(self.tableWidget.item(row, 1).text()))
                work_list = self.swabbing_opy(paker2_depth, fluid_new_edit, need_change_zgs_combo,
                                              plast_new_combo, pressuar_new_edit)
            elif swab_true_edit_type == 'Опрессовка снижением уровня на пакере с заглушкой':
                paker2_depth = int(float(self.tableWidget.item(row, 3).text()))
                paker_khost = int(float(self.tableWidget.item(row, 1).text()))
                paker_depth = int(float(self.tableWidget.item(row, 2).text()))
                work_list = self.swabbing_opy_with_paker(diametr_paker, paker_khost, paker_depth, paker2_depth)

        MyWindow.populate_row(self, self.ins_ind, work_list, self.table_widget)
        well_data.pause = False
        self.close()

    def swabbing_opy_with_paker(self, diametr_paker, paker_khost, paker_depth, depth_opy):
        if MyWindow.check_true_depth_template(self, paker_depth) is False:
            return
        if MyWindow.true_set_Paker(self, paker_depth) is False:
            return
        if MyWindow.check_depth_in_skm_interval(self, paker_depth) is False:
            return
        need_change_zgs_combo = str(self.tabWidget.currentWidget().need_change_zgs_combo.currentText())
        if need_change_zgs_combo == 'Да':
            if len(well_data.plast_project) != 0:
                plast_new_combo = self.tabWidget.currentWidget().plast_new_combo.currentText()
            else:
                plast_new_combo = self.tabWidget.currentWidget().plast_new_combo.text()
            fluid_new_edit = int(float(self.tabWidget.currentWidget().fluid_new_edit.text()))
            pressuar_new_edit = int(float(self.tabWidget.currentWidget().pressuar_new_edit.text()))

        nkt_diam = ''.join(['73' if well_data.column_diametr._value > 110 or (
                well_data.column_diametr._value > 110 and well_data.column_additional is True \
                and well_data.head_column_additional._value < depth_opy is True) else '60'])

        if well_data.column_additional is False or (well_data.column_additional is True and \
                                                   paker_depth < well_data.head_column_additional._value and
                                                   well_data.head_column_additional._value > 800) or \
                (well_data.column_additional_diametr._value < 110 and
                 paker_depth > well_data.head_column_additional._value):
            paker_select = f'заглушка +  НКТ{nkt_diam} {paker_khost}м + пакер ' \
                           f'ПРО-ЯМО-{diametr_paker}мм (либо аналог) ' \
                           f'для ЭК {well_data.column_diametr._value}мм х {well_data.column_wall_thickness._value}мм +' \
                           f' щелевой фильтр НКТ 10м'
            paker_short = f'заглушка  + НКТ{nkt_diam} {paker_khost}м + пакер ПРО-ЯМО-{diametr_paker}мм + ' \
                          f'щелевой фильтр НКТ 10м + репер'

            dict_nkt = {int(nkt_diam): paker_depth + paker_khost}
        elif well_data.column_additional is True and well_data.column_additional_diametr._value < 110 and \
                paker_depth > well_data.head_column_additional._value:
            paker_select = f'заглушка + НКТ{60}мм {paker_khost}м + пакер ПРО-ЯМО-' \
                           f'{diametr_paker}мм (либо аналог) ' \
                           f'для ЭК {well_data.column_additional_diametr._value}мм х' \
                           f' {well_data.column_additional_wall_thickness._value}мм + щелевой фильтр + НКТ60мм 10м '
            paker_short = f'заглушка+ НКТ{60}мм {paker_khost}м + пакер ПРО-ЯМО-{diametr_paker}мм  + щелевой фильтр + ' \
                          f'НКТ60мм 10м '
            dict_nkt = {int(nkt_diam): well_data.head_column_additional._value, 60:
                int(paker_depth - well_data.head_column_additional._value)}
        elif well_data.column_additional is True and well_data.column_additional_diametr._value > 110 \
                and paker_depth > well_data.head_column_additional._value:
            paker_select = f'заглушка + НКТ{well_data.nkt_diam}мм со' \
                           f' снятыми фасками {paker_khost}м + ' \
                           f'пакер ПРО-ЯМО-{diametr_paker}мм (либо аналог) ' \
                           f'для ЭК {well_data.column_additional_diametr._value}мм х ' \
                           f'{well_data.column_additional_wall_thickness._value}мм' \
                           f' + щелевой фильтр + НКТ{well_data.nkt_diam}мм со снятыми фасками 10м'
            paker_short = f'заглушка + НКТ{well_data.nkt_diam}мм со снятыми фасками {paker_khost}м + ' \
                          f'пакер ПРО-ЯМО-{diametr_paker}мм + щелевой фильтр + НКТ{well_data.nkt_diam}мм ' \
                          f'со снятыми фасками 10м'
            dict_nkt = {int(nkt_diam): paker_depth + paker_khost}
        elif nkt_diam == 60:
            dict_nkt = {60: paker_depth + paker_khost}

        paker_list = [
            [f'СПО {paker_short} на НКТ{nkt_diam}м  до глубины {well_data.current_bottom}м', None,
             f'Спустить {paker_select} на НКТ{nkt_diam}м  до глубины {well_data.current_bottom}м'
             f' с замером, шаблонированием шаблоном {well_data.nkt_template}мм. ',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(well_data.current_bottom, 1)],
            [f'Посадить пакер на глубину {paker_depth}м', None,
             f'Посадить пакер на глубину {paker_depth}м',
             None, None, None, None, None, None, None,
             'мастер КРС', 1.2],
            [None, None,
             f'Вызвать геофизическую партию. Заявку оформить за 16 часов через ЦИТС "Ойл-сервис". '
             f' Составить акт готовности скважины и передать его начальнику партии',
             None, None, None, None, None, None, None,
             'мастер КРС', None],
            [None, None,
             f'Произвести  монтаж СВАБа согласно схемы  №8 при свабированиии утвержденной главным инженером от '
             f'14.10.2021г. '
             f'Обвязать устье скважины с ЕДК на жесткую линию. Опрессовать ПВО максимально допустимое давление '
             f'опрессовки э/колонны на устье {well_data.max_admissible_pressure._value}атм,'
             f' по невозможности на давление поглощения, но не менее 30атм в течении 30мин Провести практическое '
             f'обучение вахт по '
             f'сигналу "выброс" с записью в журнале проведения учебных тревог',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', 1.35],
            [None, None,
             f'Фоновая запись. Произвести  опрессовку колонны снижением уровня свабированием по Задаче №2.1.17 '
             f'Понижение уровня '
             f'до глубины {depth_opy}м, тех отстой 3ч. КВУ в течение 3 часов после тех.отстоя. Интервал времени '
             f'между замерами '
             f'1 час. В случае негерметичности произвести записи по тех карте 2.1.13 с целью определения НЭК',
             None, None, None, None, None, None, None,
             'мастер КРС, подрядчика по ГИС', 20],
            [None, None,
             f'Свабирование проводить в емкость для дальнейшей утилизации на НШУ'
             f' с целью недопущения попадания кислоты в систему сбора. (Протокол №095-ПП от 19.10.2015г).',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', None]]

        fluid_change_quest = QMessageBox.question(self, 'Смена объема',
                                                  'Нужна ли смена удельного веса рабочей жидкости?')
        if fluid_change_quest == QMessageBox.StandardButton.Yes:
            well_data.fluid_work, well_data.fluid_work_short, plast, expected_pressure = need_h2s(self)

            fluid_change_list = [
                [None, None,
                 f'Допустить до {well_data.current_bottom}м. Произвести смену объема обратной '
                 f'промывкой по круговой циркуляции  жидкостью  {well_data.fluid_work} '
                 f'(по расчету по вскрываемому пласта {plast} Рожид- {expected_pressure}атм) в объеме не '
                 f'менее {round(well_volume(self, well_data.current_bottom), 1)}м3  в присутствии '
                 f'представителя заказчика, Составить акт. '
                 f'(Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 '
                 f'часа до начала работ)',
                 None, None, None, None, None, None, None,
                 'мастер КРС', round(well_volume_norm(well_volume(self, well_data.current_bottom))
                                     + descentNKT_norm(well_data.current_bottom - depth_opy - 200, 1), 1)],
                [None, None,
                 f'Поднять {paker_select} на НКТ{nkt_diam} c глубины {well_data.current_bottom}м с '
                 f'доливом скважины в '
                 f'объеме {round((well_data.current_bottom) * 1.12 / 1000, 1)}м3 удельным весом {well_data.fluid_work}',
                 None, None, None, None, None, None, None,
                 'мастер КРС',
                 liftingNKT_norm(well_data.current_bottom, 1)]
            ]

            for row in fluid_change_list:
                paker_list.append(row)
        else:
            paker_list.append(
                [None, None,
                   f'Поднять {paker_select} на НКТ{nkt_diam} c глубины {depth_opy + 200}м с доливом скважины в '
                   f'объеме {round((depth_opy + 200) * 1.12 / 1000, 1)}м3 удельным весом {well_data.fluid_work}',
                   None, None, None, None, None, None, None,
                   'мастер КРС',
                   liftingNKT_norm(depth_opy + 200, 1)])
        return paker_list

    def swabbing_opy(self, depth_opy, fluid_new, need_change_zgs_combo, plast_new, pressuar_new):
        from .template_work import TabPage_SO_with

        if well_data.column_additional is False or (well_data.column_additional and
                                                   well_data.head_column_additional._value >= well_data.current_bottom):
            first_template, template_second = TabPage_SO_with.template_diam_ek(self)
        else:
            first_template, template_second = TabPage_SO_with.template_diam_additional_ek(self)

        nkt_diam = ''.join(['73' if well_data.column_diametr._value > 110 or (
                well_data.column_diametr._value > 110 and well_data.column_additional is True \
                and well_data.head_column_additional._value < depth_opy is True) else '60'])
        if well_data.head_column_additional._value > depth_opy + 200:
            nkt_diam = '60'
        if well_data.column_additional is False or well_data.column_additional is True and \
                well_data.current_bottom < well_data.head_column_additional._value and \
                well_data.head_column_additional._value > 600:
            paker_select = f'воронку со свабоограничителем + шаблон {first_template}мм L-2 + НКТ{nkt_diam} + НКТ 10м + репер'
            paker_short = f'воронку со с/о + шаблон {first_template} L-2 + НКТ{nkt_diam}  + НКТ 10м + репер'
            dict_nkt = {73: depth_opy}
        elif well_data.column_additional is True and well_data.column_additional_diametr._value < 110 and \
                well_data.current_bottom >= well_data.head_column_additional._value:
            paker_select = f'воронку со свабоограничителем + шаблон {first_template} L-2 + НКТ60мм 10м + репер +НКТ60мм ' \
                           f'{round(well_data.current_bottom - well_data.head_column_additional._value + 10, 0)}м'
            paker_short = f'воронку со с/о + шаблон {first_template} L-2 + НКТ60мм 10м + репер +НКТ60мм'
            dict_nkt = {73: well_data.head_column_additional._value,
                        60: int(well_data.current_bottom - well_data.head_column_additional._value)}
        elif well_data.column_additional is True and well_data.column_additional_diametr._value > 110 and \
                well_data.current_bottom >= well_data.head_column_additional._value:
            paker_select = f'воронку со свабоограничителем + шаблон {first_template}мм L-2 + НКТ{well_data.nkt_diam}мм ' \
                           f'со снятыми фасками + ' \
                           f'НКТ{well_data.nkt_diam}мм со снятыми фасками 10м ' \
                           f'{round(well_data.current_bottom - well_data.head_column_additional._value + 10, 0)}м'
            paker_short = f'в/у со c/о + шаблон {first_template} L-2 + НКТ{well_data.nkt_diam}мм со снятыми фасками + ' \
                          f'НКТ{well_data.nkt_diam}мм со снятыми фасками 10м'
            dict_nkt = {73: depth_opy}
        elif nkt_diam == 60:
            dict_nkt = {60: depth_opy}

        paker_list = [
            [f'СПО {paker_short}до глубины {well_data.current_bottom}м', None,
             f'Спустить {paker_select} на НКТ{nkt_diam}м  до глубины {well_data.current_bottom}м'
             f' с замером, шаблонированием шаблоном {well_data.nkt_template}мм. ',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(well_data.current_bottom, 1)],
            [f'Промыть уд.весом {well_data.fluid_work} в объеме '
             f'{round(well_volume(self, well_data.current_bottom) * 1.5, 1)}м3', None,
             f'Промыть скважину круговой циркуляцией  тех жидкостью уд.весом {well_data.fluid_work}  при '
             f'расходе жидкости 6-8 л/сек '
             f'в присутствии представителя Заказчика в объеме '
             f'{round(well_volume(self, well_data.current_bottom) * 1.5, 1)}м3 ПРИ ПРОМЫВКЕ НЕ ПРЕВЫШАТЬ '
             f'ДАВЛЕНИЕ {well_data.max_admissible_pressure._value}АТМ, ДОПУСТИМАЯ ОСЕВАЯ НАГРУЗКА НА ИНСТРУМЕНТ: '
             f'0,5-1,0 ТН',
             None, None, None, None, None, None, None,
             'Мастер КРС, представитель ЦДНГ', 1.5],
            [None, None,
             f'При необходимости нормализовать забой обратной промывкой тех жидкостью уд.весом '
             f'{well_data.fluid_work} до глубины {well_data.current_bottom}м.', None, None, None, None, None,
             None, None,
             'Мастер КРС', None],
            [f'Приподнять  воронку до глубины {depth_opy + 200}м', None,
             f'Приподнять  воронку до глубины {depth_opy + 200}м',
             None, None, None, None, None, None, None,
             'мастер КРС', liftingNKT_norm(float(well_data.current_bottom) - (depth_opy + 200), 1)],
            [None, None,
             f'Вызвать геофизическую партию. Заявку оформить за 16 часов через ЦИТС "Ойл-сервис". '
             f' Составить акт готовности скважины и передать его начальнику партии',
             None, None, None, None, None, None, None,
             'мастер КРС', None],
            [None, None,
             f'Произвести  монтаж СВАБа согласно схемы  №8 при свабированиии утвержденной главным инженером от 14.10.2021г. '
             f'Обвязать устье скважины с ЕДК на жесткую линию. Опрессовать ПВО максимально допустимое'
             f' давление опрессовки э/колонны на устье {well_data.max_admissible_pressure._value}атм,'
             f' по невозможности на давление поглощения, но не менее 30атм в течении 30мин Провести практическое '
             f'обучение вахт по '
             f'сигналу "выброс" с записью в журнале проведения учебных тревог',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', 1.35],
            [f'ОПУ до глубины {depth_opy}м', None,
             f'Фоновая запись. Произвести  опрессовку колонны снижением уровня свабированием по Задаче №2.1.17 '
             f'Понижение уровня '
             f'до глубины {depth_opy}м, тех отстой 3ч. КВУ в течение 3 часов после тех.отстоя. Интервал времени между замерами '
             f'1 час. В случае негерметичности произвести записи по тех карте 2.1.13 с целью определения НЭК',
             None, None, None, None, None, None, None,
             'мастер КРС, подрядчика по ГИС', 20],
            [None, None,
             f'Свабирование проводить в емкость для дальнейшей утилизации на НШУ'
             f' с целью недопущения попадания кислоты в систему сбора. (Протокол №095-ПП от 19.10.2015г).',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', None]]
        # print(f'перевод {need_change_zgs_combo}')

        if need_change_zgs_combo == 'Да':
            if plast_new not in well_data.plast_project:
                well_data.plast_project.append(plast_new)
            print(f'после 1 {fluid_new}')
            well_data.fluid_work, well_data.fluid_work_short, plast, expected_pressure = need_h2s(
                fluid_new, plast_new, pressuar_new)

            fluid_change_list = [
                [f'Допустить до {well_data.current_bottom}м. Произвести смену объема  {well_data.fluid_work_short} '
                 f'не менее {round(well_volume(self, well_data.current_bottom), 1)}м3', None,
                 f'Допустить до {well_data.current_bottom}м. Произвести смену объема обратной '
                 f'промывкой по круговой циркуляции  жидкостью  {well_data.fluid_work} '
                 f'(по расчету по вскрываемому пласта {plast} Рожид- {expected_pressure}атм) в объеме не '
                 f'менее {round(well_volume(self, well_data.current_bottom), 1)}м3  в присутствии '
                 f'представителя заказчика, Составить акт. '
                 f'(Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 '
                 f'часа до начала работ)',
                 None, None, None, None, None, None, None,
                 'мастер КРС', round(well_volume_norm(well_volume(self, well_data.current_bottom))
                                     + descentNKT_norm(well_data.current_bottom - depth_opy - 200, 1), 1)],
                [None, None,
                 f'Поднять {paker_select} на НКТ{nkt_diam} c глубины {well_data.current_bottom}м с '
                 f'доливом скважины в '
                 f'объеме {round((well_data.current_bottom) * 1.12 / 1000, 1)}м3 удельным весом {well_data.fluid_work}',
                 None, None, None, None, None, None, None,
                 'мастер КРС',
                 liftingNKT_norm(well_data.current_bottom, 1)]
            ]

            paker_list.extend(fluid_change_list)

        else:
            paker_list.append([None, None,
                               f'Поднять {paker_select} на НКТ{nkt_diam} c глубины {depth_opy + 200}м с доливом скважины в '
                               f'объеме {round((depth_opy + 200) * 1.12 / 1000, 1)}м3 удельным весом {well_data.fluid_work}',
                               None, None, None, None, None, None, None,
                               'мастер КРС',
                               liftingNKT_norm(depth_opy + 200, 1)])
        return paker_list

    def swab_select(self, swabTypeCombo, plast_combo, swab_volumeEdit):

        if swabTypeCombo == 'Задача №2.1.13':  # , 'Задача №2.1.16', 'Задача №2.1.11', 'своя задача']'
            swab_select = f'Произвести  геофизические исследования пласта {plast_combo} по технологической ' \
                          f'задаче № 2.1.13 ' \
                          f'Определение профиля ' \
                          f'и состава притока, дебита, источника обводнения и технического состояния ' \
                          f'эксплуатационной колонны и НКТ ' \
                          f'после свабирования с отбором жидкости не менее {swab_volumeEdit}м3. \n' \
                          f'Пробы при свабировании отбирать в стандартной таре на {swab_volumeEdit - 10}, ' \
                          f'{swab_volumeEdit - 5}, {swab_volumeEdit}м3,' \
                          f' своевременно подавать телефонограммы на завоз тары и вывоз проб'
            swab_short = f'сваб не менее {swab_volumeEdit}м3 + профиль притока'
        elif swabTypeCombo == 'Задача №2.1.16':
            swab_select = f'Произвести  геофизические исследования {plast_combo} по технологической задаче № 2.1.16 ' \
                          f'Определение дебита и ' \
                          f'обводнённости по прослеживанию уровней, ВНР и по регистрации забойного ' \
                          f'давления после освоения ' \
                          f'свабированием  не менее не менее {swab_volumeEdit}м3. \n' \
                          f'Пробы при свабировании отбирать в стандартной таре на {swab_volumeEdit - 10}, ' \
                          f'{swab_volumeEdit - 5}, {swab_volumeEdit}м3,' \
                          f' своевременно подавать телефонограммы на завоз тары и вывоз проб'
            swab_short = f'сваб не менее {swab_volumeEdit}м3 + КВУ, ВНР'
        elif swabTypeCombo == 'Задача №2.1.11':
            swab_select = f'Произвести  геофизические исследования {plast_combo} по технологической задаче № 2.1.11' \
                          f' свабирование в объеме не ' \
                          f'менее  {swab_volumeEdit}м3. \n ' \
                          f'Отобрать пробу на химический анализ воды на ОСТ-39 при последнем рейсе сваба ' \
                          f'(объем не менее 10литров).' \
                          f'Обязательная сдача в этот день в ЦДНГ'
            swab_short = f'сваб не менее {swab_volumeEdit}м3'
        elif swabTypeCombo == 'ГРР':
            swab_select = f'Провести освоение объекта {plast_combo} свабированием (объем согласовать с ОГРР) не менее ' \
                          f'{swab_volumeEdit}м3 с отбором поверхностных ' \
                          f'проб через каждые 5м3 сваб и передачей представителю ЦДНГ, выполнить прослеживание уровней ' \
                          f'и ВНР с регистрацией КВУ глубинными манометрами, записать профиль притока, в случае ' \
                          f'получения притока нефти отобрать глубинные пробы (при выполнении условий отбора), ' \
                          f'провести ГДИС (КВДз).'
            swab_short = f'сваб профиль не менее ' \
                          f'{swab_volumeEdit}'

        return swab_short, swab_select

    def swabbing_with_paker_stub(self, diametr_paker, paker_depth, paker_khost, plast_combo, swabTypeCombo,
                                 swab_volumeEdit, depthGaugeCombo, need_change_zgs_combo,
                                             plast_new, fluid_new, pressuar_new):
        from .opressovka import OpressovkaEK, TabPage_SO

        swab_short, swab_select = Swab_Window.swab_select(self, swabTypeCombo, plast_combo, swab_volumeEdit)

        if depthGaugeCombo == 'Да':
            depthGauge = 'контейнер с манометром МТГ-25 + '
        else:
            depthGauge = ''

        nkt_diam = ''.join(['73' if well_data.column_diametr._value > 110 or (
                well_data.column_diametr._value > 110 and well_data.column_additional is True and
                well_data.head_column_additional._value > 800) else '60'])

        if well_data.column_additional is False or (well_data.column_additional is True and \
                                                   paker_depth < well_data.head_column_additional._value and well_data.head_column_additional._value > 800) or \
                (well_data.column_additional_diametr._value < 110 and paker_depth > well_data.head_column_additional._value):
            paker_select = f'заглушка + {depthGauge} НКТ{nkt_diam} {paker_khost}м + пакер ' \
                           f'ПРО-ЯМО-{diametr_paker}мм (либо аналог) ' \
                           f'для ЭК {well_data.column_diametr._value}мм х {well_data.column_wall_thickness._value}мм + ' \
                           f'щелевой фильтр + {depthGauge} НКТ 10м'
            paker_short = f'заглушка {depthGauge} + НКТ{nkt_diam} {paker_khost}м + пакер ПРО-ЯМО-{diametr_paker}мм +' \
                          f' {depthGauge} щелевой фильтр  +НКТ 10м + репер'

            dict_nkt = {int(nkt_diam): paker_depth + paker_khost}
        elif well_data.column_additional is True and well_data.column_additional_diametr._value < 110 and \
                paker_depth > well_data.head_column_additional._value:
            paker_select = f'заглушка + НКТ{60}мм {paker_khost}м + пакер ПРО-ЯМО-' \
                           f'{diametr_paker}мм (либо аналог) ' \
                           f'для ЭК {well_data.column_additional_diametr._value}мм х' \
                           f' {well_data.column_additional_wall_thickness._value}мм + НКТ60мм 10м '
            paker_short = f'заглушка + НКТ{60}мм {paker_khost}м + пакер ПРО-ЯМО-{diametr_paker}мм  + ' \
                          f'НКТ60мм 10м '
            dict_nkt = {int(nkt_diam): well_data.head_column_additional._value, 60:
                int(paker_depth - well_data.head_column_additional._value)}
        elif well_data.column_additional is True and well_data.column_additional_diametr._value > 110 \
                and paker_depth > well_data.head_column_additional._value:
            paker_select = f'заглушка +  НКТ{well_data.nkt_diam}мм со' \
                           f' снятыми фасками {paker_khost}м + ' \
                           f'пакер ПРО-ЯМО-{diametr_paker}мм (либо аналог) ' \
                           f'для ЭК {well_data.column_additional_diametr._value}мм х ' \
                           f'{well_data.column_additional_wall_thickness._value}мм' \
                           f' + щелевой фильтр + НКТ{well_data.nkt_diam}мм со снятыми фасками 10м'
            paker_short = f'заглушка + НКТ{well_data.nkt_diam}мм со снятыми фасками {paker_khost}м + ' \
                          f'пакер ПРО-ЯМО-{diametr_paker}мм + щелевой фильтр + НКТ{well_data.nkt_diam}мм ' \
                          f'со снятыми фасками 10м'
            dict_nkt = {int(nkt_diam): paker_depth + paker_khost}
        elif nkt_diam == 60:
            dict_nkt = {60: paker_depth + paker_khost}

        paker_list = [
            [f'СПО {paker_short} на НКТ{nkt_diam}м до H- {paker_depth}м, заглушкой до {paker_depth + paker_khost}м',
             None,
             f'Спустить {paker_select} на НКТ{nkt_diam}м до глубины {paker_depth}м, воронкой до'
             f' {paker_depth + paker_khost}м'
             f' с замером, шаблонированием шаблоном {well_data.nkt_template}мм.'
             f' {("Произвести пробную посадку на глубине 50м" if well_data.column_additional is False else "")} '
             f'ПРИ ОТСУТСТВИИ ЦИРКУЛЯЦИИ ПРЕДУСМОТРЕТЬ НАЛИЧИИ В КОМПОНОВКЕ УРАВНИТЕЛЬНЫХ КЛАПАНОВ',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(paker_depth, 1.2)],
            [f'Посадить пакер на глубине {paker_depth}м', None, f'Посадить пакер на глубине {paker_depth}м, заглушкой на '
                                                                f'глубине {paker_khost + paker_depth}м',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.4],

            [None, None,
             f'Вызвать геофизическую партию. Заявку оформить за 16 часов через ЦИТС "Ойл-сервис". '
             f' Составить акт готовности скважины и передать его начальнику партии',
             None, None, None, None, None, None, None,
             'мастер КРС', None],
            [None, None,
             f'Произвести  монтаж СВАБа согласно схемы  №8 при свабированиии утвержденной главным инженером от 14.10.2021г.'
             f'Обвязать устье скважины с ЕДК на жесткую линию. Опрессовать ПВО на максимально допустимое '
             f'давление на устье {well_data.max_admissible_pressure._value}атм,'
             f' по невозможности на давление поглощения, но не менее 30атм в течении 30мин Провести '
             f'практическое обучение вахт по '
             f'сигналу "выброс" с записью в журнале проведения учебных тревог',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', 1.3],
            [swab_short, None,
             swab_select,
             None, None, None, None, None, None, None,
             'мастер КРС, подрядчика по ГИС', 30],
            [None, None,
             f'Свабирование проводить в емкость для дальнейшей утилизации на НШУ'
             f' с целью недопущения попадания кислоты в систему сбора. (Протокол №095-ПП от 19.10.2015г).',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', None],

            [f'Срыв пакера 30мин Промывка менее {round(well_volume(self, paker_depth) * 1.5, 1)}м3', None,
             f'Произвести срыв пакера с поэтапным увеличением нагрузки на 3-4т выше веса НКТ в течении 30мин и '
             f'с выдержкой 1ч  для возврата резиновых элементов в исходное положение. При наличии избыточного давления: '
             f'произвести промывку скважину обратной промывкой ' \
             f'по круговой циркуляции  жидкостью уд.весом {well_data.fluid_work} при расходе жидкости не ' \
             f'менее 6-8 л/сек в объеме не менее {round(well_volume(self, paker_depth) * 1.5, 1)}м3 ' \
             f'в присутствии представителя заказчика ДО ЧИСТОЙ ВОДЫ.Составить акт.',
             None, None, None, None, None, None, None,
             'Мастер КРС', 1.26],
            ['выполнить снятие КВУ в течение часа с интервалом 15 минут', None,
             f'Перед подъемом подземного оборудования, после проведённых работ по освоению выполнить снятие КВУ в '
             f'течение часа с интервалом 15 минут для определения стабильного стистатического уровня в скважине. '
             f'При подъеме уровня в скважине и образовании избыточного давления наустье, выполнить '
             f'замер пластового давления '
             f'или вычислить его расчетным методом.',
             None, None, None, None, None, None, None,
             'Мастер КРС', 0.5],
        ]
        ovtr = 'ОВТР 4ч' if well_data.region == 'ЧГМ' else 'ОВТР 10ч'
        ovtr4 = 4 if well_data.region == 'ЧГМ' else 10
        if swabTypeCombo == 'Задача №2.1.13' and well_data.region not in ['ИГМ', 'ТГМ']:
            paker_list.insert(3, [ovtr, None, ovtr,
                                  None, None, None, None, None, None, None,
                                  'мастер КРС', ovtr4])

        # Добавление привязки компоновки при посадке пакера близко к интервалу перфорации
        for plast in list(well_data.dict_perforation.keys()):
            for interval in well_data.dict_perforation[plast]['интервал']:
                if abs(float(interval[1] - paker_depth)) < 10 or abs(float(interval[0] - paker_depth)) < 10:
                    if privyazkaNKT(self) not in paker_list and well_data.privyazkaSKO == 0:
                        well_data.privyazkaSKO += 1
                        paker_list.insert(1, privyazkaNKT(self)[0])

        if need_change_zgs_combo == 'Да':
            paker_list.extend(Change_fluid_Window.fluid_change(self, plast_new, fluid_new, pressuar_new))
            paker_list.append([None, None,
                               f'Поднять {paker_select} на НКТ{nkt_diam} c глубины {paker_depth}м с доливом скважины в '
                               f'объеме {round(paker_depth * 1.12 / 1000, 1)}м3 удельным весом {well_data.fluid_work}',
                               None, None, None, None, None, None, None,
                               'мастер КРС',
                               liftingNKT_norm(paker_depth, 1.2)])
        else:
            paker_list.append([None, None,
             f'Поднять {paker_select} на НКТ{nkt_diam} c глубины {paker_depth}м с доливом скважины в '
             f'объеме {round(paker_depth * 1.12 / 1000, 1)}м3 удельным весом {well_data.fluid_work}',
             None, None, None, None, None, None, None,
             'мастер КРС',
             liftingNKT_norm(paker_depth, 1.2)])
        return paker_list

    def swabbing_with_paker(self, diametr_paker, paker_depth, paker_khost, plast_combo, swabTypeCombo, swab_volumeEdit,
                            depthGaugeCombo, need_change_zgs_combo='нет', plast_new = '', fluid_new = '', pressuar_new = ''):
        from .opressovka import OpressovkaEK

        swab_short, swab_select = Swab_Window.swab_select(self, swabTypeCombo, plast_combo, swab_volumeEdit)

        if depthGaugeCombo == 'Да':
            depthGauge = 'контейнер с манометром МТГ-25 + '
        else:
            depthGauge = ''

        nkt_diam = ''.join(['73' if well_data.column_diametr._value > 110 or (
                well_data.column_diametr._value > 110 and well_data.column_additional is True and
                well_data.head_column_additional._value > 800) else '60'])

        if well_data.column_additional is False or (well_data.column_additional is True and \
                                                   paker_depth < well_data.head_column_additional._value and \
                                                    well_data.head_column_additional._value > 800) or \
                (well_data.column_additional_diametr._value < 110 and paker_depth > well_data.head_column_additional._value):
            paker_select = f'воронку со свабоограничителем + {depthGauge} НКТ{nkt_diam} {paker_khost}м + пакер ' \
                           f'ПРО-ЯМО-{diametr_paker}мм (либо аналог) ' \
                           f'для ЭК {well_data.column_diametr._value}мм х {well_data.column_wall_thickness._value}мм ' \
                           f'+ {depthGauge} НКТ 10м'
            paker_short = f'в/ку со с/о {depthGauge} + НКТ{nkt_diam} {paker_khost}м + пакер ПРО-ЯМО-{diametr_paker}мм' \
                          f' + {depthGauge}НКТ 10м + репер'

            dict_nkt = {int(nkt_diam): paker_depth + paker_khost}
        elif well_data.column_additional is True and well_data.column_additional_diametr._value < 110 and \
                paker_depth > well_data.head_column_additional._value:
            paker_select = f'воронку со свабоограничителем+ НКТ{60}мм {paker_khost}м + пакер ПРО-ЯМО-' \
                           f'{diametr_paker}мм (либо аналог) ' \
                           f'для ЭК {well_data.column_additional_diametr._value}мм х' \
                           f' {well_data.column_additional_wall_thickness._value}мм + НКТ60мм 10м '
            paker_short = f'в-ку со свабоогр.+ НКТ{60}мм {paker_khost}м + пакер ПРО-ЯМО-{diametr_paker}мм  + ' \
                          f'НКТ60мм 10м '
            dict_nkt = {int(nkt_diam): well_data.head_column_additional._value, 60:
                int(paker_depth - well_data.head_column_additional._value)}
        elif well_data.column_additional is True and well_data.column_additional_diametr._value > 110 \
                and paker_depth > well_data.head_column_additional._value:
            paker_select = f'воронку со свабоограничителем+ НКТ{well_data.nkt_diam}мм со' \
                           f' снятыми фасками {paker_khost}м + ' \
                           f'пакер ПРО-ЯМО-{diametr_paker}мм (либо аналог) ' \
                           f'для ЭК {well_data.column_additional_diametr._value}мм х ' \
                           f'{well_data.column_additional_wall_thickness._value}мм' \
                           f' + НКТ{well_data.nkt_diam}мм со снятыми фасками 10м'
            paker_short = f'в-ку со свабоогр.+ НКТ{well_data.nkt_diam}мм со снятыми фасками {paker_khost}м + ' \
                          f'пакер ПРО-ЯМО-{diametr_paker}мм + НКТ{well_data.nkt_diam}мм ' \
                          f'со снятыми фасками 10м'
            dict_nkt = {int(nkt_diam): paker_depth + paker_khost}
        elif nkt_diam == 60:
            dict_nkt = {60: paker_depth + paker_khost}

        paker_list = [
            [f'СПО {paker_short} на НКТ{nkt_diam}м до H- {paker_depth}м, воронкой до {paker_depth + paker_khost}м',
             None,
             f'Спустить {paker_select} на НКТ{nkt_diam}м до глубины {paker_depth}м, воронкой до'
             f' {paker_depth + paker_khost}м'
             f' с замером, шаблонированием шаблоном {well_data.nkt_template}мм.'
             f' {("Произвести пробную посадку на глубине 50м" if well_data.column_additional is False else "")} '
             f'ПРИ ОТСУТСТВИИ ЦИРКУЛЯЦИИ ПРЕДУСМОТРЕТЬ НАЛИЧИИ В КОМПОНОВКЕ УРАВНИТЕЛЬНЫХ КЛАПАНОВ',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(paker_depth, 1.2)],
            [f'Посадить пакер на глубине {paker_depth}м', None, f'Посадить пакер на глубине {paker_depth}м, воронку на '
                                                                f'глубине {paker_khost + paker_depth}м',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.4],
            [OpressovkaEK.testing_pressure(self, paker_depth)[1],
             None, OpressovkaEK.testing_pressure(self, paker_depth)[0],
             None, None, None, None, None, None, None,
             'мастер КРС, предст. заказчика', 0.67],

            [None, None,
             f'В случае негерметичности э/к, по согласованию с заказчиком произвести ОТСЭК для определения интервала '
             f'негерметичности эксплуатационной колонны с точностью до одного НКТ или запись РГД, ВЧТ с '
             f'целью определения места нарушения в присутствии представителя заказчика, составить акт. '
             f'Определить приемистость НЭК.',
             None, None, None, None, None, None, None,
             'мастер КРС', None],
            [None, None,
             f'Вызвать геофизическую партию. Заявку оформить за 16 часов через ЦИТС "Ойл-сервис". '
             f' Составить акт готовности скважины и передать его начальнику партии',
             None, None, None, None, None, None, None,
             'мастер КРС', None],
            [None, None,
             f'Произвести  монтаж СВАБа согласно схемы  №8 при свабированиии утвержденной главным инженером от 14.10.2021г.'
             f'Обвязать устье скважины с ЕДК на жесткую линию. Опрессовать ПВО на максимально допустимое '
             f'давление на устье {well_data.max_admissible_pressure._value}атм,'
             f' по невозможности на давление поглощения, но не менее 30атм в течении 30мин Провести '
             f'практическое обучение вахт по '
             f'сигналу "выброс" с записью в журнале проведения учебных тревог',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', 1.3],
            [swab_short, None,
             swab_select,
             None, None, None, None, None, None, None,
             'мастер КРС, подрядчика по ГИС', 30],
            [None, None,
             f'Свабирование проводить в емкость для дальнейшей утилизации на НШУ'
             f' с целью недопущения попадания кислоты в систему сбора. (Протокол №095-ПП от 19.10.2015г).',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', None],

            [f'Срыв пакера 30мин  Промывка менее {round(well_volume(self, paker_depth) * 1.5, 1)}м3', None,
             f'Произвести срыв пакера с поэтапным увеличением нагрузки на 3-4т выше веса НКТ в течении 30мин и '
             f'с выдержкой 1ч  для возврата резиновых элементов в исходное положение. При наличии избыточного давления: '
             f'произвести промывку скважину обратной промывкой ' \
             f'по круговой циркуляции  жидкостью уд.весом {well_data.fluid_work} при расходе жидкости не ' \
             f'менее 6-8 л/сек в объеме не менее {round(well_volume(self, paker_depth) * 1.5, 1)}м3 ' \
             f'в присутствии представителя заказчика ДО ЧИСТОЙ ВОДЫ.Составить акт.',
             None, None, None, None, None, None, None,
             'Мастер КРС', 1.26],
            ['выполнить снятие КВУ в течение часа с интервалом 15 минут', None,
             f'Перед подъемом подземного оборудования, после проведённых работ по освоению выполнить снятие КВУ в '
             f'течение часа с интервалом 15 минут для определения стабильного стистатического уровня в скважине. '
             f'При подъеме уровня в скважине и образовании избыточного давления наустье, выполнить '
             f'замер пластового давления '
             f'или вычислить его расчетным методом.',
             None, None, None, None, None, None, None,
             'Мастер КРС', 0.5]
        ]
        ovtr = 'ОВТР 4ч' if well_data.region == 'ЧГМ' else 'ОВТР 10ч'
        ovtr4 = 4 if well_data.region == 'ЧГМ' else 10
        if swabTypeCombo == 'Задача №2.1.13' and well_data.region not in ['ИГМ', 'ТГМ']:
            paker_list.insert(3, [ovtr, None, ovtr,
                                  None, None, None, None, None, None, None,
                                  'мастер КРС', ovtr4])

        # Добавление привязки компоновки при посадке пакера близко к интервалу перфорации
        for plast in list(well_data.dict_perforation.keys()):
            for interval in well_data.dict_perforation[plast]['интервал']:
                if abs(float(interval[1] - paker_depth)) < 10 or abs(float(interval[0] - paker_depth)) < 10:
                    if privyazkaNKT(self) not in paker_list and well_data.privyazkaSKO == 0:
                        well_data.privyazkaSKO += 1
                        paker_list.insert(1, privyazkaNKT(self)[0])

        if need_change_zgs_combo == 'Да':
            # print(plast_new, fluid_new, pressuar_new)
            paker_list.extend(Change_fluid_Window.fluid_change(self, plast_new, fluid_new, pressuar_new))
            paker_list.append([None, None,
                               f'Поднять {paker_select} на НКТ{nkt_diam} c глубины {paker_depth}м с доливом скважины в '
                               f'объеме {round(paker_depth * 1.12 / 1000, 1)}м3 удельным весом {well_data.fluid_work}',
                               None, None, None, None, None, None, None,
                               'мастер КРС',
                               liftingNKT_norm(paker_depth, 1.2)])
        else:
            paker_list.append([None, None,
             f'Поднять {paker_select} на НКТ{nkt_diam} c глубины {paker_depth}м с доливом скважины в '
             f'объеме {round(paker_depth * 1.12 / 1000, 1)}м3 удельным весом {well_data.fluid_work}',
             None, None, None, None, None, None, None,
             'мастер КРС',
             liftingNKT_norm(paker_depth, 1.2)])

        return paker_list

    def swabbing_with_2paker(self, diametr_paker, paker1_depth, paker2_depth, paker_khost, plast_combo, swabTypeCombo,
                             swab_volumeEdit, depthGaugeCombo, need_change_zgs_combo,
                                             plast_new, fluid_new, pressuar_new):
       
        from .opressovka import OpressovkaEK

        swab_short, swab_select = Swab_Window.swab_select(self, swabTypeCombo, plast_combo, swab_volumeEdit)

        nkt_diam = '73' if well_data.column_diametr._value > 110 or (
                well_data.column_diametr._value > 110 and well_data.column_additional is True and \
                well_data.head_column_additional._value > 700) else '60'
        if depthGaugeCombo == 'Да':
            depthGauge = 'контейнер с манометром МТГ-25 + '
        else:
            depthGauge = ''

        if well_data.column_additional is False or well_data.column_additional is True and \
                paker1_depth < float(well_data.head_column_additional._value) and \
                float(well_data.head_column_additional._value) > 600:

            paker_select = f'заглушка + {depthGauge} НКТ{nkt_diam} {paker_khost}м + пакер ПРО-ЯМО-{diametr_paker}мм (либо аналог) ' \
                           f'для ЭК {well_data.column_diametr._value}мм х {well_data.column_wall_thickness._value}мм + щелевой фильтр + ' \
                           f'{depthGauge} НКТ l-{round(paker1_depth - paker2_depth, 0)} + пакер ПУ для ЭК ' \
                           f'{well_data.column_diametr._value}мм х {well_data.column_wall_thickness._value}мм + {depthGauge} НКТ{nkt_diam} 20мм + репер'
            paker_short = f'заглушка + {depthGauge}НКТ{nkt_diam} {paker_khost}м + пакер ПРО-ЯМО-{diametr_paker}мм  + щелевой фильтр + {depthGauge}' \
                          f'НКТ l-{round(paker1_depth - paker2_depth, 0)} + пакер ПУ {depthGauge}  + НКТ{nkt_diam} 20мм + репер'
            dict_nkt = {73: paker1_depth + paker_khost}
        elif well_data.column_additional is True and well_data.column_additional_diametr._value < 110 and paker1_depth > float(
                well_data.head_column_additional._value):
            paker_select = f'заглушка +  НКТ{60}мм {paker_khost}м + пакер ПРО-ЯМО-{diametr_paker}мм (либо аналог) ' \
                           f'для ЭК {well_data.column_diametr._value}мм х {well_data.column_wall_thickness._value}мм + щелевой фильтр + ' \
                           f'НКТ l-{round(paker1_depth - paker2_depth, 0)} + пакер ПУ НКТ{60} 20мм + репер + НКТ60мм ' \
                           f'{round(float(well_data.head_column_additional._value) - paker2_depth, 0)}м '
            paker_short = f'заглушка + НКТ{60}мм {paker_khost}м + пакер ПРО-ЯМО-{diametr_paker}мм ' \
                          f' + щелевой фильтр + НКТ l-{round(paker1_depth - paker2_depth, 0)} + пакер ПУ + НКТ{60} 20мм + репер +' \
                          f' НКТ60мм {round(float(well_data.head_column_additional._value) - paker2_depth, 0)}м '
            dict_nkt = {73: well_data.head_column_additional._value,
                        60: int(paker1_depth - well_data.head_column_additional._value)}
        elif well_data.column_additional is True and well_data.column_additional_diametr._value > 110 and paker1_depth > well_data.head_column_additional._value:
            paker_select = f'заглушка + {depthGauge}НКТ{73}мм со снятыми фасками {paker_khost}м + пакер ПРО-ЯМО-' \
                           f'{diametr_paker}мм (либо аналог) для ЭК {well_data.column_diametr._value}мм х ' \
                           f'{well_data.column_wall_thickness._value}мм + щелевой фильтр + {depthGauge}' \
                           f'НКТ l-{round(paker1_depth - paker2_depth, 0)} {depthGauge} + пакер ПУ  со снятыми фасками 20мм + репер + ' \
                           f'НКТ{73}мм со снятыми фасками {round(float(well_data.head_column_additional._value) - paker2_depth, 0)}м '
            paker_short = f'заглушка +{depthGauge}  НКТ{73}мм со снятыми фасками {paker_khost}м + пакер ПРО-ЯМО-' \
                          f'{diametr_paker}мм + щелевой фильтр + {depthGauge}' \
                          f'НКТ l-{round(paker1_depth - paker2_depth, 0)} + пакер ПУ  со снятыми фасками 20мм + {depthGauge} + репер + ' \
                          f'НКТ{73}мм со снятыми фасками {round(float(well_data.head_column_additional._value) - paker2_depth, 0)}м '
            dict_nkt = {73: paker1_depth + paker_khost}
        elif nkt_diam == 60:
            dict_nkt = {60: paker1_depth + paker_khost}

        paker_list = [
            [f'Спуск {paker_short} до глубины {paker1_depth}/{paker2_depth}м', None,
             f'Спустить {paker_select} на НКТ{nkt_diam}м до глубины {paker1_depth}/{paker2_depth}м'
             f' с замером, шаблонированием шаблоном {well_data.nkt_template}мм. '
             f'{("Произвести пробную посадку на глубине 50м" if well_data.column_additional is False else "")} '
             f'ПРИ ОТСУТСТВИИ ЦИРКУЛЯЦИИ ПРЕДУСМОТРЕТЬ НАЛИЧИИ В КОМПОНОВКЕ УРАВНИТЕЛЬНЫХ КЛАПАНОВ',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(paker1_depth, 1.2)],
            [f'Посадить пакера на глубине {paker1_depth}/{paker2_depth}м',
             None, f'Посадить пакера на глубине {paker1_depth}/{paker2_depth}м',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.4],
            [OpressovkaEK.testing_pressure(self, paker2_depth)[1],
             None,
             OpressovkaEK.testing_pressure(self, paker2_depth)[0],
             None, None, None, None, None, None, None,
             'мастер КРС, предст. заказчика', 0.67],

            [None, None,
             f'В случае негерметичности э/к, по согласованию с заказчиком произвести ОТСЭК для определения интервала '
             f'негерметичности эксплуатационной колонны с точностью до одного НКТ или запись РГД, ВЧТ с '
             f'целью определения места нарушения в присутствии представителя заказчика, составить акт. '
             f'Определить приемистость НЭК.',
             None, None, None, None, None, None, None,
             'мастер КРС', None],
            [None, None,
             f'Вызвать геофизическую партию. Заявку оформить за 16 часов через ЦИТС "Ойл-сервис". '
             f' Составить акт готовности скважины и передать его начальнику партии',
             None, None, None, None, None, None, None,
             'мастер КРС', None],
            [None, None,
             f'Произвести  монтаж СВАБа согласно схемы  №8 при свабированиии утвержденной главным инженером от 14.10.2021г. '
             f'Обвязать устье скважины с ЕДК на жесткую линию. Опрессовать ПВО на максимально допустимое давление на устье {well_data.max_admissible_pressure._value}атм,'
             f' по невозможности на давление поглощения, но не менее 30атм в течении 30мин Провести практическое обучение вахт по '
             f'сигналу "выброс" с записью в журнале проведения учебных тревог',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', 1.3],
            [swab_short, None,
             swab_select,
             None, None, None, None, None, None, None,
             'мастер КРС, подрядчика по ГИС', 30],
            [None, None,
             f'Свабирование проводить в емкость для дальнейшей утилизации на НШУ'
             f' с целью недопущения попадания кислоты в систему сбора. (Протокол №095-ПП от 19.10.2015г).',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', None],

            [f'Срыв пакера 30мин. Промывка менее {round(well_volume(self, paker1_depth) * 1.5, 1)}м3',
             None,
             f'Произвести срыв пакера с поэтапным увеличением нагрузки на 3-4т выше веса НКТ в течении 30мин и '
             f'с выдержкой 1ч  для возврата резиновых элементов в исходное положение. При наличии избыточного давления: '
             f'произвести промывку скважину обратной промывкой ' \
             f'по круговой циркуляции  жидкостью уд.весом {well_data.fluid_work} при расходе жидкости не ' \
             f'менее 6-8 л/сек в объеме не менее {round(well_volume(self, paker1_depth) * 1.5, 1)}м3 ' \
             f'в присутствии представителя заказчика ДО ЧИСТОЙ ВОДЫ.Составить акт.',
             None, None, None, None, None, None, None,
             'Мастер КРС', 1.26],
            [f' выполнить снятие КВУ в течение часа с интервалом 15 минут', None,
             f'Перед подъемом подземного оборудования, после проведённых работ по освоению выполнить снятие КВУ в '
             f'течение часа с интервалом 15 минут для определения стабильного стистатического уровня в скважине. '
             f'При подъеме уровня в скважине и образовании избыточного давления наустье, выполнить замер пластового давления '
             f'или вычислить его расчетным методом.',
             None, None, None, None, None, None, None,
             'Мастер КРС', 0.5]
        ]

        # Добавление привязки компоновки при посадке пакера близко к интервалу перфорации
        for plast in list(well_data.dict_perforation.keys()):
            for interval in well_data.dict_perforation[plast]['интервал']:
                if abs(float(interval[1] - paker1_depth)) < 10 or abs(float(interval[0] - paker1_depth)) < 10:
                    if privyazkaNKT(self) not in paker_list and well_data.privyazkaSKO == 0:
                        well_data.privyazkaSKO += 1
                        paker_list.insert(1, *privyazkaNKT(self))
        if need_change_zgs_combo == 'Да':
            paker_list.extend(Change_fluid_Window.fluid_change(self, plast_new, fluid_new, pressuar_new))
            paker_list.append([None, None,
                               f'Поднять {paker_select} на НКТ{nkt_diam} c глубины {paker1_depth}м с доливом скважины в '
                               f'объеме {round(paker1_depth * 1.12 / 1000, 1)}м3 удельным весом {well_data.fluid_work}',
                               None, None, None, None, None, None, None,
                               'мастер КРС',
                               liftingNKT_norm(paker1_depth, 1.2)])
        else:
            paker_list.append([None, None,
             f'Поднять {paker_select} на НКТ{nkt_diam} c глубины {paker1_depth}м с доливом скважины в '
             f'объеме {round(paker1_depth * 1.12 / 1000, 1)}м3 удельным весом {well_data.fluid_work}',
             None, None, None, None, None, None, None,
             'мастер КРС',
             liftingNKT_norm(paker1_depth, 1.2)])

        return paker_list

    def swabbing_with_voronka(self, paker_depth, plast_combo, swabTypeCombo, swab_volumeEdit, depthGaugeCombo,
                              need_change_zgs_combo, plast_new, fluid_new, pressuar_new):
       
        swab_short, swab_select = Swab_Window.swab_select(self, swabTypeCombo, plast_combo, swab_volumeEdit)
        nkt_diam = '73' if well_data.column_diametr._value > 110 or (
                well_data.column_diametr._value > 110 and well_data.column_additional is True and \
                well_data.head_column_additional._value > 700) else '60'

        if depthGaugeCombo == 'Да':
            depthGauge = 'контейнер с манометром МТГ-25 + '
        else:
            depthGauge = ''

        if well_data.column_additional is False or well_data.column_additional is True and paker_depth < well_data.head_column_additional._value:
            paker_select = f'воронку + {depthGauge} свабоограничитель  НКТ{nkt_diam} +репер + НКТ 10м'
            paker_short = f'в/у + {depthGauge} со с/о НКТ{nkt_diam} +репер + НКТ 10м'
            dict_nkt = {73: paker_depth}
        elif well_data.column_additional is True and well_data.column_additional_diametr._value < 110 and \
                paker_depth > well_data.head_column_additional._value:
            paker_select = f'воронку со свабоограничителем  + НКТ{60}мм  + НКТ60мм 10м '
            paker_short = f'в/у + НКТ{60}мм  + НКТ60мм 10м + {round(paker_depth - well_data.head_column_additional._value, 1)}м {depthGauge}'
            dict_nkt = {60: paker_depth}

        paker_list = [
            [paker_short, None,
             f'Спустить {paker_select} на НКТ{nkt_diam}м  воронкой до {paker_depth}м'
             f' с замером, шаблонированием шаблоном {well_data.nkt_template}мм. ',
             None, None, None, None, None, None, None,
             'мастер КРС', round(
                well_data.current_bottom / 9.52 * 1.51 / 60 * 1.2 * 1.2 * 1.04 + 0.18 + 0.008 * paker_depth / 9.52 + 0.003 * well_data.current_bottom / 9.52,
                2)],
            [None, None,
             f'Вызвать геофизическую партию. Заявку оформить за 16 часов через ЦИТС "Ойл-сервис". '
             f' Составить акт готовности скважины и передать его начальнику партии',
             None, None, None, None, None, None, None,
             'мастер КРС', None],
            [None, None,
             f'Произвести  монтаж СВАБа согласно схемы  №8 при свабированиии утвержденной главным инженером от 14.10.2021г. '
             f'Обвязать устье скважины с ЕДК на жесткую линию. Опрессовать ПВО на максимально допустимое давление на устье '
             f'{well_data.max_admissible_pressure._value}атм,'
             f' по невозможности на давление поглощения, но не менее 30атм в течении 30мин Провести практическое обучение вахт по '
             f'сигналу "выброс" с записью в журнале проведения учебных тревог',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', 1.2],
            [swab_short, None,
             swab_select,
             None, None, None, None, None, None, None,
             'мастер КРС, подрядчика по ГИС', 30],
            [None, None,
             f'Свабирование проводить в емкость для дальнейшей утилизации на НШУ'
             f' с целью недопущения попадания кислоты в систему сбора. (Протокол №095-ПП от 19.10.2015г).',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', None],

            [f'промывка в объеме не менее {round(well_volume(self, paker_depth) * 1.5, 1)}м3', None,
             f' При наличии избыточного давления: '
             f'произвести промывку скважину обратной промывкой ' \
             f'по круговой циркуляции  жидкостью уд.весом {well_data.fluid_work} при расходе жидкости не ' \
             f'менее 6-8 л/сек в объеме не менее {round(well_volume(self, paker_depth) * 1.5, 1)}м3 ' \
             f'в присутствии представителя заказчика ДО ЧИСТОЙ ВОДЫ.Составить акт.',
             None, None, None, None, None, None, None,
             'Мастер КРС', well_volume_norm(well_volume(self, paker_depth))],
            [f' выполнить снятие КВУ в течение часа с интервалом 15 минут', None,
             f'Перед подъемом подземного оборудования, после проведённых работ по освоениювыполнить снятие КВУ в '
             f'течение часа с интервалом 15 минут для определения стабильного стистатического уровня в скважине. '
             f'При подъеме уровня в скважине и образовании избыточного давления наустье, выполнить замер пластового давления '
             f'или вычислить его расчетным методом.',
             None, None, None, None, None, None, None,
             'Мастер КРС', 0.5],
        ]
        ovtr = 'ОВТР 4ч' if well_data.region == 'ЧГМ' else 'ОВТР 10ч'
        ovtr4 = 4 if well_data.region == 'ЧГМ' else 10
        if swabTypeCombo == 'Задача №2.1.13' and well_data.region not in ['ИГМ']:
            paker_list.insert(1, [ovtr, None, ovtr,
                                  None, None, None, None, None, None, None,
                                  'мастер КРС', ovtr4])

        if need_change_zgs_combo == 'Да':
            paker_list.extend(Change_fluid_Window.fluid_change(self, plast_new, fluid_new, pressuar_new))
            paker_list.append([None, None,
                               f'Поднять {paker_select} на НКТ{nkt_diam} c глубины {paker_depth}м с доливом скважины в '
                               f'объеме {round(paker_depth * 1.12 / 1000, 1)}м3 удельным весом {well_data.fluid_work}',
                               None, None, None, None, None, None, None,
                               'мастер КРС',
                               liftingNKT_norm(paker_depth, 1.2)])
        else:
            paker_list.append([None, None,
             f'Поднять {paker_select} на НКТ{nkt_diam} c глубины {paker_depth}м с доливом скважины в '
             f'объеме {round(paker_depth * 1.12 / 1000, 1)}м3 удельным весом {well_data.fluid_work}',
             None, None, None, None, None, None, None,
             'мастер КРС',
             liftingNKT_norm(paker_depth, 1.2)])
        return paker_list


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    # app.setStyleSheet()

    window = Swab_Window()
    window.show()
    sys.exit(app.exec_())
