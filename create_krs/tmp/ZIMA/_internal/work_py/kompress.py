from PyQt5.QtWidgets import QInputDialog, QWidget, QLabel, QComboBox, QLineEdit, QTabWidget, QMainWindow, QPushButton, \
    QGridLayout, QMessageBox

import well_data
from .rationingKRS import descentNKT_norm, liftingNKT_norm,well_volume_norm
from .template_work import TemplateKrs


class TabPage_SO_kompress(QWidget):
    def __init__(self, paker_layout_combo, parent=None):
        from .acid_paker import CheckableComboBox
        from .opressovka import OpressovkaEK, TabPage_SO

        super().__init__()

        self.kompress_true_label = QLabel("компоновка", self)
        self.kompress_true_combo = QComboBox(self)
        paker_layout_list = ['воронка', 'с пакером']
        self.kompress_true_combo.addItems(paker_layout_list)
        self.paker_layout_combo = paker_layout_combo

        self.kompress_true_combo.setCurrentIndex(0)

        self.depth_gauge_label = QLabel("глубинные манометры", self)
        self.depth_gauge_combo = QComboBox(self)
        self.depth_gauge_combo.addItems(['Нет', 'Да'])

        self.khovst_label = QLabel("глубина воронки", self)
        self.khvost_edit = QLineEdit(self)
        self.khvost_edit.setText(f'{well_data.perforation_roof-100}')        

        plast_work = well_data.plast_work
        self.plast_label = QLabel("Выбор пласта", self)
        self.plast_combo = CheckableComboBox(self)
        self.plast_combo.combo_box.addItems(plast_work)
        self.plast_combo.combo_box.currentTextChanged.connect(self.update_plast_edit)

        self.kompress_TypeLabel = QLabel("задача при освоении", self)
        self.kompress_TypeCombo = QComboBox(self)
        self.kompress_TypeCombo.addItems(['Задача №2.1.15', 'своя задача'])

        self.kompress_volumeEditLabel = QLabel("объем освоения", self)
        self.kompress_volumeEdit = QLineEdit(self)
        self.kompress_volumeEdit.setText('20')

        self.count_muft_label = QLabel("Количество муфт", self)
        self.count_muft_edit = QLineEdit(self)
        self.count_muft_edit.setText(f'{3}')

        self.dictance_without_murt_label = QLabel("Расстояние между муфтами", self)
        self.dictance_without_murt_edit = QLineEdit(self)
        self.dictance_without_murt_edit.setText(f'{200}')

        self.grid = QGridLayout(self)
        self.grid.addWidget(self.kompress_true_label, 0, 0)
        self.grid.addWidget(self.kompress_true_combo, 1, 0)

        self.grid.addWidget(self.plast_label, 0, 1)
        self.grid.addWidget(self.plast_combo, 1, 1)
        self.grid.addWidget(self.khovst_label, 0, 3)
        self.grid.addWidget(self.khvost_edit, 1, 3)

        self.grid.addWidget(self.kompress_TypeLabel, 6, 2)
        self.grid.addWidget(self.kompress_TypeCombo, 7, 2)
        self.grid.addWidget(self.kompress_volumeEditLabel, 6, 3)
        self.grid.addWidget(self.kompress_volumeEdit, 7, 3)
        self.grid.addWidget(self.depth_gauge_label, 6, 4)
        self.grid.addWidget(self.depth_gauge_combo, 7, 4)
        self.grid.addWidget(self.count_muft_label, 6, 5)
        self.grid.addWidget(self.count_muft_edit, 7, 5)
        self.grid.addWidget(self.dictance_without_murt_label, 6, 6)
        self.grid.addWidget(self.dictance_without_murt_edit, 7, 6)

        self.kompress_true_combo.currentTextChanged.connect(self.kompress_TrueEdit_select)

        self.labels_muft = {}


    def kompress_TrueEdit_select(self):
        if self.kompress_true_combo.currentText() == 'воронка':
            pass
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

        self.khvost_edit.setText(f"{roof_plast -100}")
class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.addTab(TabPage_SO_kompress(self), 'Освоение компрессором')


class Kompress_Window(QMainWindow):
    def __init__(self, ins_ind, table_widget, parent=None):
        super(QMainWindow, self).__init__(parent)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.table_widget = table_widget
        self.ins_ind = ins_ind

        self.tabWidget = TabWidget()
        self.dict_nkt = {}

        self.buttonAdd = QPushButton('Добавить данные в план работ')
        self.buttonAdd.clicked.connect(self.add_work)
        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)

    def add_work(self):
        from main import MyWindow

        kompress_true_combo = self.tabWidget.currentWidget().kompress_true_combo.currentText()
        depth_gauge_combo = self.tabWidget.currentWidget().depth_gauge_combo.currentText()
        khvost_edit = int(float(self.tabWidget.currentWidget().khvost_edit.text()))
        kompress_TypeCombo = self.tabWidget.currentWidget().kompress_TypeCombo.currentText()
        kompress_volume = int(float(self.tabWidget.currentWidget().kompress_volumeEdit.text()))
        count_muft = int(float(self.tabWidget.currentWidget().count_muft_edit.text()))
        dictance_without_murt = int(float(self.tabWidget.currentWidget().dictance_without_murt_edit.text()))
        plast_combo = str(self.tabWidget.currentWidget().plast_combo.combo_box.currentText())
        depth_gauge_combo = str(self.tabWidget.currentWidget().depth_gauge_combo.currentText())


        if int(khvost_edit) - (count_muft * int(dictance_without_murt)) - 100 < well_data.static_level:
            mes = QMessageBox.warning(self, 'Некорректные данные',
                                      f'Статический уровень в скважине {well_data.static_level} ниже глубины '
                                      f'вверхней муфты {int(khvost_edit) - (count_muft * int(dictance_without_murt))}'
                                       f'ниже текущего забоя')
            return

        if int(khvost_edit) - (count_muft * int(dictance_without_murt)) - 100 < 600:
            mes = QMessageBox.warning(self, 'Некорректные данные',
                          f'вверхняя муфта на Н -{int(khvost_edit) - (count_muft * int(dictance_without_murt))},'
                           f'это слишком высото')
            return

        if kompress_true_combo == 'воронка':
            work_list = self.kompress(plast_combo, kompress_TypeCombo, khvost_edit, kompress_volume, count_muft,
                                      depth_gauge_combo, dictance_without_murt)
        else:
            pass

        MyWindow.populate_row(self, self.ins_ind, work_list, self.table_widget)
        well_data.pause = False
        self.close()

    def kompress(self, plast_combo, kompress_TypeCombo, khvost_edit, kompress_volume, count_muft,
                                      depth_gauge_combo, dictance_without_murt):

        if kompress_TypeCombo == 'Задача №2.1.15':  # , 'Задача №2.1.16', 'Задача №2.1.11', 'своя задача']'
            kompress_select = f'ЗАДАЧА 2.1.5. Определение профиля и состава притока, дебита, источника ' \
                              f'обводнения  пласта {plast_combo} и ' \
                          f'технического состояния эксплуатационной колонны при компрессировании' \
                          f' с отбором жидкости не менее {kompress_volume}м3. \n' \
                          f'Пробы при освоении отбирать в стандартной таре на {kompress_volume - 10}, ' \
                              f'{kompress_volume - 5}, {kompress_volume}м3,' \
                          f' своевременно подавать телефонограммы на завоз тары и вывоз проб'
        gauge = ''
        if depth_gauge_combo == 'Да':
            gauge = ' + Контейнер с МТГ-25'




        nkt_diam = well_data.nkt_diam

        if well_data.column_additional is False or well_data.column_additional is True and\
                khvost_edit < well_data.head_column_additional._value:
            paker_select = f'воронку + c/о {gauge} + НКТ{nkt_diam} '
            paker_short = f'в-ку + c/о {gauge} + НКТ{nkt_diam} '
            for ind in range(count_muft, 1, -1):
                paker_select += f' {dictance_without_murt}м + ПМ - {ind}мм + НКТ{nkt_diam}'
                paker_short += f' {dictance_without_murt}м + ПМ - {ind}мм + НКТ{nkt_diam}'

            paker_select += f' ПМ - 1мм '
            paker_short += f' ПМ - 1мм '
            dict_nkt = {73: khvost_edit}
        elif well_data.column_additional is True and well_data.column_additional_diametr._value < 110 and \
                khvost_edit > well_data.head_column_additional._value:
            paker_select = f'воронку + НКТ{60} '
            paker_short = f'в-ку + НКТ{60} '
            for ind in range(count_muft):
                paker_select += f' {dictance_without_murt}м + ПМ - {ind}мм + НКТ{60}'
                paker_short += f' {dictance_without_murt}м + ПМ - {ind}мм + НКТ{60}'

            paker_select += f' ПМ - 1мм  + НКТ{60} {int(khvost_edit - (count_muft * dictance_without_murt) - well_data.head_column_additional._value)}м'
            paker_short += f' ПМ - 1мм + НКТ{60} {int(khvost_edit - (count_muft * dictance_without_murt) - well_data.head_column_additional._value)}м'

            dict_nkt = {73: well_data.head_column_additional._value, 60: int(khvost_edit - well_data.head_column_additional._value)}

        paker_list = [
            [f'СПО {paker_short} на НКТ{nkt_diam}м до глубины {khvost_edit}м.', None,
             f'Спустить {paker_select} на НКТ{nkt_diam}м до глубины {khvost_edit}м'
             f' с замером, шаблонированием шаблоном {well_data.nkt_template}мм.',
             None, None, None, None, None, None, None,
             'мастер КРС', round(
                descentNKT_norm(khvost_edit, 1))],
            [None, None,
             f'Вызвать геофизическую партию. Заявку оформить за 16 часов через ЦИТС "Ойл-сервис". '
             f' Составить акт готовности скважины и передать его начальнику партии',
             None, None, None, None, None, None, None,
             'мастер КРС', None],
            [None, None,
             f'Произвести  монтаж ГИС согласно схемы  №8 при свабированиии утвержденной главным инженером от 14.10.2021г. '
             f'Обвязать устье скважины с ЕДК на жесткую линию. Опрессовать ПВО максимально допустимое давление опрессовки э/колонны на устье '
             f'{well_data.max_admissible_pressure._value}атм,'
             f' по невозможности на давление поглощения, но не менее 30атм в течении 30мин Провести практическое обучение вахт по '
             f'сигналу "выброс" с записью в журнале проведения учебных тревог',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', 1.2],
            [f'Компрессирование', None,
             kompress_select,
             None, None, None, None, None, None, None,
             'мастер КРС, подрядчика по ГИС', 30],
            [None, None,
             f'Освоение проводить в емкость для дальнейшей утилизации на НШУ'
             f' с целью недопущения попадания кислоты в систему сбора. (Протокол №095-ПП от 19.10.2015г).',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', None],
            [f'Промывка скважины  не менее {round(TemplateKrs.well_volume(self) * 1.5, 1)}м3', None,
             f' При наличии избыточного давления: '
             f'произвести промывку скважину обратной промывкой ' \
             f'по круговой циркуляции  жидкостью уд.весом {well_data.fluid_work} при расходе жидкости не ' \
             f'менее 6-8 л/сек в объеме не менее {round(TemplateKrs.well_volume(self) * 1.5, 1)}м3 ' \
             f'в присутствии представителя заказчика ДО ЧИСТОЙ ВОДЫ.Составить акт.',
             None, None, None, None, None, None, None,
             'Мастер КРС', well_volume_norm(TemplateKrs.well_volume(self))],
            [f'выполнить снятие КВУ в течение часа с интервалом 15 минут',
             None,
             f'Перед подъемом подземного оборудования, после проведённых работ по освоению выполнить снятие КВУ в '
             f'течение часа с интервалом 15 минут для определения стабильного стистатического уровня в скважине. '
             f'При подъеме уровня в скважине и образовании избыточного давления наустье, выполнить замер пластового давления '
             f'или вычислить его расчетным методом.',
             None, None, None, None, None, None, None,
             'Мастер КРС', 0.5],
            [None, None,
             f'Поднять {paker_select} на НКТ{nkt_diam} c глубины {khvost_edit}м с доливом скважины в '
             f'объеме {round(khvost_edit * 1.12 / 1000, 1)}м3 удельным весом {well_data.fluid_work}',
             None, None, None, None, None, None, None,
             'мастер КРС',
             liftingNKT_norm(khvost_edit,1)]
        ]

        return paker_list