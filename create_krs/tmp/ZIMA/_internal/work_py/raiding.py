import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QInputDialog, QMessageBox, QWidget, QLabel, QLineEdit, QComboBox, QGridLayout, QTabWidget, \
    QTableWidget, QHeaderView, QPushButton, QTableWidgetItem, QApplication, QMainWindow

import well_data
from main import MyWindow

from .rationingKRS import descentNKT_norm, liftingNKT_norm, well_volume_norm
from .advanted_file import change_True_raid



class TabPage_SO_raid(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.raid_diametr_label = QLabel("Диаметр райбера", self)
        self.raid_diametr_line = QLineEdit(self)

        self.raid_type_label = QLabel("Тип райбера", self)
        self.raid_type_combo = QComboBox(self)
        raid_type_list = ['ФКК', 'арбузный ФА']
        self.raid_type_combo.addItems(raid_type_list)

        self.raid_select_label = QLabel("компоновка НКТ", self)
        self.raid_select_combo = QComboBox(self)
        self.raid_select_combo.addItems(['райбер в ЭК', 'райбер в ДП'])

        self.downhole_motor_label = QLabel("Забойный двигатель", self)
        self.downhole_motor_line = QLineEdit(self)
        self.downhole_motor_line.setClearButtonEnabled(True)

        if well_data.column_additional is False or (well_data.column_additional and
                                                    well_data.head_column_additional._value < well_data.current_bottom):
            self.raid_select_combo.setCurrentIndex(0)
            if well_data.column_diametr._value > 127:
                self.downhole_motor_line.setText('Д-106')
            else:
                self.downhole_motor_line.setText('Д-76')
        else:
            if well_data.column_additional_diametr._value > 127:
                self.downhole_motor_line.setText('Д-106')
            else:
                self.downhole_motor_line.setText('Д-76')
            self.raid_select_combo.setCurrentIndex(1)

        self.roof_raid_label = QLabel("Кровля", self)
        self.roof_raid_line = QLineEdit(self)
        self.roof_raid_line.setClearButtonEnabled(True)

        self.sole_raid_label = QLabel("Подошва", self)
        self.sole_raid_line = QLineEdit(self)
        self.sole_raid_line.setClearButtonEnabled(True)

        self.raid_True_label = QLabel("необходимость райбировать интервал", self)
        self.raid_label = QLabel("добавление дополнительного интервала райбирования", self)
        self.raid_True_combo = QComboBox(self)
        self.raid_True_combo.addItems(
            ['нужно', 'не нужно'])

        self.nkt_str_label = QLabel("НКТ или СБТ", self)
        self.nkt_str_combo = QComboBox(self)
        self.nkt_str_combo.addItems(
            ['НКТ', 'СБТ'])
        self.raid_select_combo.currentTextChanged.connect(self.update_nkt)

        self.grid = QGridLayout(self)
        self.grid.setColumnMinimumWidth(1, 150)

        self.grid.addWidget(self.raid_select_label, 2, 0)
        self.grid.addWidget(self.raid_select_combo, 3, 0)

        self.grid.addWidget(self.raid_type_label, 2, 1)
        self.grid.addWidget(self.raid_type_combo, 3, 1)

        self.grid.addWidget(self.nkt_str_label, 2, 2)
        self.grid.addWidget(self.nkt_str_combo, 3, 2)

        self.grid.addWidget(self.raid_diametr_label, 2, 3)
        self.grid.addWidget(self.raid_diametr_line, 3, 3)

        self.grid.addWidget(self.downhole_motor_label, 2, 4)
        self.grid.addWidget(self.downhole_motor_line, 3, 4)

        self.grid.addWidget(self.raid_label, 4, 1, 2, 2)

        self.grid.addWidget(self.roof_raid_label, 7, 0)
        self.grid.addWidget(self.sole_raid_label, 7, 1)
        self.grid.addWidget(self.raid_True_label, 7, 2)

        self.grid.addWidget(self.roof_raid_line, 8, 0)
        self.grid.addWidget(self.sole_raid_line, 8, 1)
        self.grid.addWidget(self.raid_True_combo, 8, 2, 2, 1)

        self.raid_select_combo.currentTextChanged.connect(self.update_raid_edit)
        self.raid_select_combo.setCurrentIndex(1)

        if well_data.column_additional is False or \
                (well_data.column_additional and well_data.current_bottom < well_data.head_column_additional._value):
            self.raid_select_combo.setCurrentIndex(0)
        else:

            self.raid_select_combo.setCurrentIndex(1)

    def update_nkt(self, index):
        if index == 'СБТ':
            self.downhole_motor_label.setParent(None)
            self.downhole_motor_line.setParent(None)
        else:
            self.grid.addWidget(self.downhole_motor_label, 2, 4)
            self.grid.addWidget(self.downhole_motor_line, 3, 4)

    def update_raid_edit(self, index):

        if index == 'райбер в ЭК':
            self.raid_diametr_line.setText(str(self.raiding_Bit_diam_select(well_data.head_column_additional._value - 10)))
            if well_data.column_diametr._value > 127:
                self.downhole_motor_line.setText('Д-106')
            else:
                self.downhole_motor_line.setText('Д-76')


        if index == 'райбер в ДП':
            self.raid_diametr_line.setText(str(self.raiding_Bit_diam_select(well_data.current_bottom)))
            if well_data.column_additional_diametr._value > 127:
                self.downhole_motor_line.setText('Д-106')
            else:
                self.downhole_motor_line.setText('Д-76')

    def raiding_Bit_diam_select(self, depth):

        raiding_Bit_dict = {
            85: (88, 92),
            91: (92.1, 96.6),
            95: (96.7, 102),
            103: (102.1, 109),
            106: (109, 115),
            115: (118, 120),
            117: (120.1, 121.9),
            120: (122, 123.9),
            121: (124, 127.9),
            125: (128, 133),
            140: (144, 148),
            144: (148.1, 154),
            146: (154.1, 164),
            160: (166, 176),
            190: (190.6, 203.6),
            204: (215, 221)
        }
        print(well_data.column_additional is False, well_data.column_additional, well_data.column_diametr._value, well_data.column_additional_wall_thickness._value)
        if well_data.column_additional is False or (
                well_data.column_additional is True and depth <= well_data.head_column_additional._value):
            diam_internal_ek = well_data.column_diametr._value - 2 * well_data.column_wall_thickness._value
        else:
            diam_internal_ek = well_data.column_additional_diametr._value - 2 * well_data.column_additional_wall_thickness._value
        print(f'ваап {diam_internal_ek, (well_data.column_additional is True and depth <= well_data.head_column_additional._value)}')
        for diam, diam_internal_bit in raiding_Bit_dict.items():
            if diam_internal_bit[0] <= diam_internal_ek <= diam_internal_bit[1]:
                bit_diametr = diam

        if 'ПОМ' in str(well_data.paker_do["posle"]).upper() and '122' in str(well_data.paker_do["posle"]):
            bit_diametr = 126

        return bit_diametr


class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.addTab(TabPage_SO_raid(), 'Райбер')


class Raid(MyWindow):
    def __init__(self, ins_ind, table_widget, parent=None):
        super(MyWindow, self).__init__(parent)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.ins_ind = ins_ind
        self.table_widget = table_widget
        self.tabWidget = TabWidget()
        self.tableWidget = QTableWidget(0, 3)
        self.tableWidget.setHorizontalHeaderLabels(
            ["Кровля", "Подошва", "необходимость райбирования"])
        for i in range(3):
            self.tableWidget.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)

        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.setAlternatingRowColors(True)

        self.buttonAdd = QPushButton('Добавить записи в таблицу')
        self.buttonAdd.clicked.connect(self.addRowTable)
        self.buttonDel = QPushButton('Удалить записи из таблице')
        self.buttonDel.clicked.connect(self.del_row_table)
        self.buttonadd_work = QPushButton('Добавить в план работ')
        self.buttonadd_work.clicked.connect(self.add_work, Qt.QueuedConnection)
        self.buttonAddString = QPushButton('Добавить интервалы райбирования')
        self.buttonAddString.clicked.connect(self.addString)
        vbox = QGridLayout(self.centralWidget)

        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.tableWidget, 1, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)
        vbox.addWidget(self.buttonDel, 2, 1)
        vbox.addWidget(self.buttonadd_work, 3, 0)
        vbox.addWidget(self.buttonAddString, 3, 1)

    def addRowTable(self):

        roof_raid = self.tabWidget.currentWidget().roof_raid_line.text().replace(',', '.')
        sole_raid = self.tabWidget.currentWidget().sole_raid_line.text().replace(',', '.')
        ryber_key = self.tabWidget.currentWidget().raid_select_combo.currentText()

        raid_True_combo = QComboBox(self)
        raid_True_combo.addItems(
            ['нужно', 'не нужно'])
        index_raid_True = self.tabWidget.currentWidget().raid_True_combo.currentIndex()
        raid_True_combo.setCurrentIndex(index_raid_True)

        if not roof_raid or not sole_raid:
            msg = QMessageBox.information(self, 'Внимание', 'Заполните все поля!')
            return
        if well_data.column_additional and int(roof_raid) > well_data.head_column_additional._value and \
                ryber_key == 'райбер в ЭК':
            msg = QMessageBox.information(self, 'Внимание', 'Компоновка подобрана не корректно')
            return
        if well_data.column_additional and int(sole_raid) < well_data.head_column_additional._value \
                and ryber_key == 'райбер в ДП':
            msg = QMessageBox.information(self, 'Внимание', 'Компоновка подобрана не корректно')
            return

        if well_data.current_bottom < float(sole_raid):
            msg = QMessageBox.information(self, 'Внимание', 'глубина НЭК ниже искусственного забоя')
            return

        self.tableWidget.setSortingEnabled(False)
        rows = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rows)

        self.tableWidget.setItem(rows, 0, QTableWidgetItem(roof_raid))
        self.tableWidget.setItem(rows, 1, QTableWidgetItem(sole_raid))
        self.tableWidget.setCellWidget(rows, 2, raid_True_combo)

        self.tableWidget.setSortingEnabled(True)

    def addString(self):

        from .advanted_file import raiding_interval
        ryber_key = self.tabWidget.currentWidget().raid_select_combo.currentText()
        self.downhole_motor = self.tabWidget.currentWidget().downhole_motor_line.text()
        raiding_interval = raiding_interval(ryber_key)
        # 'райбер в ЭК': ryber_str_EK, 'райбер в ДП'
        if raiding_interval:
            if ryber_key == 'райбер в ЭК' and well_data.column_additional and \
                    raiding_interval[0][1] > well_data.head_column_additional._value:
                mes = QMessageBox.warning(self, 'Ошибка',
                                          'Не корректно выбрана компоновка')
                return
            elif ryber_key == 'райбер в ДП' and well_data.column_additional and \
                    raiding_interval[0][0] < well_data.head_column_additional._value:
                mes = QMessageBox.warning(self, 'Ошибка',
                                          'Не корректно выбрана компоновка')
                return
        if len(raiding_interval) == 0:
            mes = QMessageBox.warning(self, 'Ошибка',
                                      'Не выбраны интервалы райбирования')
            return

        rows = self.tableWidget.rowCount()

        for roof, sole in raiding_interval:
            self.tableWidget.insertRow(rows)
            self.tableWidget.setItem(rows, 0, QTableWidgetItem(str(int(roof))))
            self.tableWidget.setItem(rows, 1, QTableWidgetItem(str(int(sole))))
            self.tableWidget.setSortingEnabled(False)

    def add_work(self):
        nkt_str_combo = self.tabWidget.currentWidget().nkt_str_combo.currentText()
        ryber_key = self.tabWidget.currentWidget().raid_select_combo.currentText()
        rows = self.tableWidget.rowCount()
        raid_tuple = []
        if rows == 0:
            mes = QMessageBox.warning(self, 'ОШИБКА', 'Нужно до,авить интервалы')
            return
        for row in range(rows):
            roof_raid = self.tableWidget.item(row, 0)
            sole_raid = self.tableWidget.item(row, 1)

            if roof_raid and sole_raid:
                roof = int(roof_raid.text())
                sole = int(sole_raid.text())
                if sole > well_data.current_bottom:
                    mes = QMessageBox.warning(self, 'Ошибка',
                                              f'подошвы райбирования {sole}м больше текущего забоя'
                                              f' {well_data.current_bottom}м')
                    return
                raid_tuple.append((roof, sole))


        if nkt_str_combo == 'НКТ':
            raid_list = self.raidingColumn(raid_tuple[::-1], ryber_key)
        else:
            raid_list = self.raiding_sbt(raid_tuple[::-1], ryber_key)

        MyWindow.populate_row(self, self.ins_ind, raid_list, self.table_widget)
        well_data.pause = False
        self.close()

    def del_row_table(self):
        row = self.tableWidget.currentRow()
        if row == -1:
            msg = QMessageBox.information(self, 'Внимание', 'Выберите строку для удаления')
            return
        self.tableWidget.removeRow(row)

    def raidingColumn(self, raiding_interval_tuple, ryber_key):
        from .template_work import TemplateKrs
        from .advanted_file import raiding_interval, raid
        from work_py.alone_oreration import fluid_change

        ryber_diam = self.tabWidget.currentWidget().raid_diametr_line.text()
        ryber_key = self.tabWidget.currentWidget().raid_select_combo.currentText()
        downhole_motor = self.tabWidget.currentWidget().downhole_motor_line.text()
        raid_type_combo = self.tabWidget.currentWidget().raid_type_combo.currentText()
        nkt_pod = 0
        current_str = well_data.current_bottom
        if well_data.column_additional:
            if ryber_key == 'райбер в ЭК' and well_data.head_column_additional._value < well_data.current_bottom:
                current_str = well_data.head_column_additional._value

            nkt_pod = '60мм' if well_data.column_additional_diametr._value < 110 else '73мм со снятыми фасками'

        nkt_diam = well_data.nkt_diam
        nkt_template = well_data.nkt_template

        ryber_str_EK = f'райбер {raid_type_combo}-{ryber_diam} для ЭК {well_data.column_diametr._value}мм х ' \
                       f'{well_data.column_wall_thickness._value}мм +' \
                       f' забойный двигатель {downhole_motor} + НКТ{well_data.nkt_diam} 20м + репер '

        ryber_str_DP = f'райбер {raid_type_combo}-{ryber_diam} для ЭК {well_data.column_additional_diametr._value}мм х ' \
                       f'{well_data.column_additional_wall_thickness._value}мм + забойный двигатель ' \
                       f'{downhole_motor} + НКТ{nkt_pod} 20м + репер + ' \
                       f'НКТ{nkt_pod} {round(well_data.current_bottom - float(well_data.head_column_additional._value))}м'

        rayber_dict = {'райбер в ЭК': ryber_str_EK, 'райбер в ДП': ryber_str_DP}

        ryber_str = rayber_dict[ryber_key]


        if len(raiding_interval_tuple) != 0:
            krovly_raiding = int(raiding_interval_tuple[0][0])
        else:
            krovly_raiding = well_data.perforation_roof

        raiding_interval = raid(raiding_interval_tuple)
        change_True_raid(self, raiding_interval_tuple)
        ryber_list = [
            [f'СПО {ryber_str}  на НКТ{nkt_diam} до Н={krovly_raiding}м', None,
             f'Спустить {ryber_str}  на НКТ{nkt_diam} до Н={krovly_raiding}м с замером, '
             f'шаблонированием шаблоном {nkt_template}мм (При СПО первых десяти НКТ на спайдере дополнительно '
             f'устанавливать элеватор ЭХЛ). '
             f'В случае разгрузки инструмента  при спуске, проработать место посадки с промывкой скв., составить акт.'
             f'СКОРОСТЬ СПУСКА НЕ БОЛЕЕ 1 М/С (НЕ ДОХОДЯ 40 - 50 М ДО ПЛАНОВОГО '
             f'ИНТЕРВАЛА СКОРОСТЬ СПУСКА СНИЗИТЬ ДО 0,25 М/С). '
             f'ЗА 20 М ДО ЗАБОЯ СПУСК ПРОИЗВОДИТЬ С ПРОМЫВКОЙ',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(krovly_raiding, 1.2)],
            [None, None,
             f'Собрать промывочное оборудование: вертлюг, ведущая труба (установить вставной фильтр под ведущей трубой), '
             f'буровой рукав, устьевой герметизатор, нагнетательная линия. Застраховать буровой рукав за вертлюг. ',
             None, None, None, None, None, None, None,
             'Мастер КРС, УСРСиСТ', 0.6],
            [f'райбирование ЭК в инт. {raiding_interval}', None,
             f'Произвести райбирование ЭК в инт. {raiding_interval}м с наращиванием, с промывкой и проработкой 5 раз каждого наращивания. '
             f'Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа '
             f'до начала работ) Работы производить согласно сборника технологических регламентов и инструкций в присутствии'
             f' представителя заказчика. Допустить до глубины {current_str}м.',
             None, None, None, None, None, None, None,
             'Мастер КРС, УСРСиСТ', 8],
            [None, None,
             f'ПРИМЕЧАНИЕ: РАСХОД РАБОЧЕЙ ЖИДКОСТИ 8-10 Л/С;'
             f' ОСЕВАЯ НАГРУЗКА НЕ БОЛЕЕ 75% ОТ ДОПУСТИМОЙ НАГРУЗКИ (УТОЧНИТЬ ПО ПАСПОРТУ ЗАВЕЗЁННОГО ГЗД И ДОЛОТА);'
             f' РАБОЧЕЕ ДАВЛЕНИЕ 4-10 МПА (УТОЧНИТЬ ПО ПАСПОРТУ ЗАВЕЗЁННОГО ВЗД);'
             f' ПРЕДУСМОТРЕТЬ КОМПЕНСАЦИЮ РЕАКТИВНОГО МОМЕНТА НА ВЕДУЩЕЙ ТРУБЕ))',
             None, None, None, None, None, None, None,
             'Мастер КРС, УСРСиСТ', None],
            [f'Промывка уд.весом {well_data.fluid_work[:6]}  в объеме {round(TemplateKrs.well_volume(self) * 2, 1)}м3',
             None,
             f'Промыть скважину круговой циркуляцией  тех жидкостью уд.весом {well_data.fluid_work}  '
             f'в присутствии представителя заказчика в объеме {round(TemplateKrs.well_volume(self) * 2, 1)}м3. Составить акт.',
             None, None, None, None, None, None, None,
             'мастер КРС, предст. заказчика', well_volume_norm(TemplateKrs.well_volume(self))],
            [None, None,
             f'Поднять  {ryber_str} на НКТ{nkt_diam}м с глубины {current_str}м с доливом скважины в '
             f'объеме {round(well_data.current_bottom * 1.12 / 1000, 1)}м3 тех. жидкостью  уд.весом {well_data.fluid_work}',
             None, None, None, None, None, None, None,
             'мастер КРС', liftingNKT_norm(current_str, 1.2)]]

        # print(f' после отрайбирования {[well_data.dict_perforation[plast]["отрайбировано"] for plast in well_data.plast_work]}')
        if len(well_data.plast_work) == 0:
            acid_true_quest = QMessageBox.question(self, 'Необходимость смены объема',
                                                   'Нужно ли изменять удельный вес?')
            try:
                if acid_true_quest == QMessageBox.StandardButton.Yes:
                    for row in fluid_change(self):
                        ryber_list.insert(-1, row)
            except:
                mes = QMessageBox.warning(self, 'ОШИБКА', 'Смена объема вставить не получитлось')


        return ryber_list

    def raiding_sbt(self, raiding_interval_tuple, ryber_key):
        from .template_work import TemplateKrs
        from .advanted_file import raid
        from .alone_oreration import fluid_change

        ryber_diam = self.tabWidget.currentWidget().raid_diametr_line.text()
        ryber_key = self.tabWidget.currentWidget().raid_select_combo.currentText()
        raid_type_combo = self.tabWidget.currentWidget().raid_type_combo.currentText()

        current_str = well_data.current_bottom
        if well_data.column_additional:
            if ryber_key == 'райбер в ЭК':
                current_str = well_data.head_column_additional._value

        nkt_pod = "2'3/8"
        nkt_diam = "2'7/8" if well_data.column_diametr._value > 110 else "2'3/8"

        ryber_str_EK = f'райбер {raid_type_combo}-{ryber_diam} для ЭК {well_data.column_diametr._value}мм х {well_data.column_wall_thickness._value}мм '
        ryber_str_short_ek = f'райбер ФКК-{ryber_diam} для ЭК {well_data.column_diametr._value}мм х {well_data.column_wall_thickness._value}мм '

        ryber_str_DP = f'райбер {raid_type_combo}-{ryber_diam} для ЭК {well_data.column_additional_diametr._value}мм х ' \
                       f'{well_data.column_additional_wall_thickness._value}мм + СБТ {nkt_pod} ' \
                       f'{int(well_data.current_bottom - well_data.head_column_additional._value)}м'
        ryber_str_short_dp = f'райбер ФКК-{ryber_diam}  + СБТ {nkt_pod} {int(well_data.current_bottom - well_data.head_column_additional._value)}м'

        rayber_dict = {'райбер в ЭК': (ryber_str_EK, ryber_str_short_ek),
                       'райбер в ДП': (ryber_str_DP, ryber_str_short_dp)}

        ryber_str, ryber_str_short = rayber_dict[ryber_key]

        if len(raiding_interval_tuple) != 0:
            krovly_raiding = int(raiding_interval_tuple[0][0])
        else:
            krovly_raiding = well_data.perforation_roof

        raiding_interval = raid(raiding_interval_tuple)
        ryber_list = [
            [f'СПО {ryber_str_short} на СБТ {nkt_diam} до Н= {krovly_raiding - 30}', None,
             f'Спустить {ryber_str}  на СБТ {nkt_diam} до Н= {krovly_raiding - 30}м с замером, '
             f' (При СПО первых десяти СБТ на спайдере дополнительно устанавливать элеватор ЭХЛ). '
             f'В случае разгрузки инструмента  при спуске, проработать место посадки с промывкой скв., '
             f'составить акт. СКОРОСТЬ СПУСКА НЕ БОЛЕЕ 1 М/С (НЕ ДОХОДЯ 40 - 50 М ДО ПЛАНОВОГО ИНТЕРВАЛА СКОРОСТЬ '
             f'СПУСКА СНИЗИТЬ ДО 0,25 М/С). '
             f'ЗА 20 М ДО ЗАБОЯ СПУСК ПРОИЗВОДИТЬ С ПРОМЫВКОЙ',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(well_data.current_bottom, 1.1)],
            [f'монтаж мех.ротора', None,
             f'Произвести монтаж мех.ротора. Собрать промывочное оборудование: вертлюг, ведущая труба (установить '
             f'вставной фильтр под ведущей трубой), '
             f'буровой рукав, устьевой герметизатор, нагнетательная линия. Застраховать буровой рукав за вертлюг. ',
             None, None, None, None, None, None, None,
             'Мастер КРС, УСРСиСТ', round(0.14 + 0.17 + 0.08 + 0.48 + 1.1, 1)],
            [f'райбирование ЭК в инт. {raiding_interval}', None,
             f'Произвести райбирование ЭК в инт. {raiding_interval}м с наращиванием, с промывкой и проработкой 5 раз каждого наращивания. '
             f'Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа '
             f'до начала работ) Работы производить согласно сборника технологических регламентов и инструкций в присутствии'
             f' представителя заказчика. Допустить до {current_str}м.',
             None, None, None, None, None, None, None,
             'Мастер КРС, УСРСиСТ', 8],
            [None, None,
             f'ПРИМЕЧАНИЕ: РАСХОД РАБОЧЕЙ ЖИДКОСТИ 8-10 Л/С;'
             f' ОСЕВАЯ НАГРУЗКА НЕ БОЛЕЕ 75% ОТ ДОПУСТИМОЙ НАГРУЗКИ (УТОЧНИТЬ ПО ПАСПОРТУ );'
             f' ПРЕДУСМОТРЕТЬ КОМПЕНСАЦИЮ РЕАКТИВНОГО МОМЕНТА НА ВЕДУЩЕЙ ТРУБЕ))',
             None, None, None, None, None, None, None,
             'Мастер КРС, УСРСиСТ', None],
            [f'Промывка уд.весом {well_data.fluid_work[:6]}  в объеме {round(TemplateKrs.well_volume(self) * 2, 1)}м3',
             None,
             f'Промыть скважину круговой циркуляцией  тех жидкостью уд.весом {well_data.fluid_work}  '
             f'в присутствии представителя заказчика в объеме {round(TemplateKrs.well_volume(self) * 2, 1)}м3. Составить акт.',
             None, None, None, None, None, None, None,
             'мастер КРС, предст. заказчика', well_volume_norm(TemplateKrs.well_volume(self))],
            [None, None,
             f'Поднять  {ryber_str} на СБТ{nkt_diam}м с глубины {current_str}м с доливом скважины в '
             f'объеме {round(well_data.current_bottom * 1.12 / 1000, 1)}м3 тех. жидкостью  уд.весом {well_data.fluid_work}',
             None, None, None, None, None, None, None,
             'мастер КРС', liftingNKT_norm(current_str, 1.2)]]

        # print(f' после отрайбирования {[well_data.dict_perforation[plast]["отрайбировано"] for plast in well_data.plast_work]}')
        if len(well_data.plast_work) == 0:
            acid_true_quest = QMessageBox.question(self, 'Необходимость смены объема',
                                                   'Нужно ли изменять удельный вес?')
            if acid_true_quest == QMessageBox.StandardButton.Yes:
                for row in fluid_change(self):
                    ryber_list.insert(-1, row)
        return ryber_list


# if __name__ == "__main__":
#     import sys
#
#     app = QApplication(sys.argv)
#     # app.setStyleSheet()
#     window = Raid()
#     # window.show()
#     sys.exit(app.exec_())
