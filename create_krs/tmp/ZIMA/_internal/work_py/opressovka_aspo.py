from PyQt5.QtGui import QDoubleValidator, QIntValidator

import well_data
from main import MyWindow
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QMainWindow, QWidget, QLabel, QComboBox, QLineEdit, QGridLayout, \
    QTabWidget, QPushButton

from work_py.alone_oreration import privyazkaNKT
from .opressovka import OpressovkaEK, TabPage_SO
from .rationingKRS import descentNKT_norm, liftingNKT_norm



class TabPage_SO_aspo(QWidget):
    def __init__(self, parent=None):

        super().__init__(parent)

        self.validator = QIntValidator(0, 5000)

        self.diametr_paker_labelType = QLabel("Диаметр пакера", self)
        self.diametr_paker_edit = QLineEdit(self)
        self.diametr_paker_edit.setValidator(self.validator)

        self.paker_khost_Label = QLabel("Длина хвостовика", self)
        self.paker_khost_edit = QLineEdit(self)
        self.paker_khost_edit.setValidator(self.validator)

        self.paker_depth_Label = QLabel("Глубина посадки", self)
        self.paker_depth_edit = QLineEdit(self)
        self.paker_depth_edit.setValidator(self.validator)
        self.paker_depth_edit.textChanged.connect(self.update_paker)

        if len(well_data.plast_work) != 0:
            pakerDepth = well_data.perforation_roof - 20
        else:
            if well_data.leakiness:
                pakerDepth = min([well_data.dict_leakiness['НЭК']['интервал'][nek][0] - 10
                                       for nek in well_data.dict_leakiness['НЭК']['интервал'].keys()])

        self.paker_depth_edit.setText(str(int(pakerDepth)))

        self.grid_layout = QGridLayout(self)

        self.grid_layout.addWidget(self.diametr_paker_labelType, 3, 1)
        self.grid_layout.addWidget(self.diametr_paker_edit, 4, 1)

        self.grid_layout.addWidget(self.paker_khost_Label, 3, 2)
        self.grid_layout.addWidget(self.paker_khost_edit, 4, 2)

        self.grid_layout.addWidget(self.paker_depth_Label, 3, 3)
        self.grid_layout.addWidget(self.paker_depth_edit, 4, 3)


    def update_paker(self):

        if well_data.open_trunk_well is True:
            paker_depth = self.paker_depth_edit.text()
            if paker_depth != '':
                paker_khost = well_data.current_bottom - int(paker_depth)
                self.paker_khost_edit.setText(f'{paker_khost}')
                self.diametr_paker_edit.setText(f'{TabPage_SO.paker_diametr_select(int(paker_depth))}')
        else:
            paker_depth = self.paker_depth_edit.text()
            if paker_depth != '':
                paker_khost = 10
                self.paker_khost_edit.setText(f'{paker_khost}')
                self.diametr_paker_edit.setText(f'{TabPage_SO.paker_diametr_select(int(paker_depth))}')


class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.addTab(TabPage_SO(self), 'Очистка колонны с пакером')

class PakerAspo(QMainWindow):
    def __init__(self, ins_ind, table_widget, parent=None):
        super().__init__(parent)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.table_widget = table_widget
        self.ins_ind = ins_ind

        self.tabWidget = TabWidget()

        self.buttonAdd = QPushButton('Добавить данные в план работ')
        self.buttonAdd.clicked.connect(self.add_work)
        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)

    def add_work(self):
        diametr_paker = int(float(self.tabWidget.currentWidget().diametr_paker_edit.text()))
        paker_khost = int(float(self.tabWidget.currentWidget().paker_khost_edit.text()))
        paker_depth = int(float(self.tabWidget.currentWidget().paker_depth_edit.text()))

        if int(paker_khost) + int(paker_depth) > well_data.current_bottom:
            mes = QMessageBox.warning(self, 'Некорректные данные', f'Компоновка НКТ c хвостовик + пакер '
                                                                   f'ниже текущего забоя')
            return
        if MyWindow.check_true_depth_template(self, paker_depth) is False:
            return
        if MyWindow.true_set_Paker(self, paker_depth) is False:
            return
        if MyWindow.check_depth_in_skm_interval(self, paker_depth) is False:
            return

        work_list = PakerAspo.paker_list(self, diametr_paker, paker_khost, paker_depth)
        MyWindow.populate_row(self, self.ins_ind, work_list, self.table_widget)
        well_data.pause = False
        self.close()

    # Добавление строк с опрессовкой ЭК
    def paker_list(self, paker_diametr, paker_khost, paker_depth):
        if well_data.column_additional is False or well_data.column_additional is True \
                and paker_depth < well_data.head_column_additional._value:

            paker_select = f'Заглушка сбивной клапан с ввертышем + НКТ{well_data.nkt_diam}мм {paker_khost}м +' \
                           f' пакер ПРО-ЯМО-{paker_diametr}мм (либо аналог) ' \
                           f'для ЭК {well_data.column_diametr._value}мм х {well_data.column_wall_thickness._value}мм + щелевой фильтр' \
                           f' {OpressovkaEK.nktOpress(self)[0]}'
            paker_short = f'Заглушка сбивной клапан с ввертышем + + НКТ{well_data.nkt_diam}мм {paker_khost}м +' \
                          f' пакер ПРО-ЯМО-{paker_diametr}мм  + ' \
                          f'  + щелевой фильтр'
        elif well_data.column_additional is True and well_data.column_additional_diametr._value < 110 and \
                paker_depth > well_data.head_column_additional._value:
            paker_select = f'Заглушка сбивной клапан с ввертышем + НКТ{60}мм {paker_khost}м + пакер ПРО-ЯМО-' \
                           f'{paker_diametr}мм (либо аналог) ' \
                           f'для ЭК {well_data.column_additional_diametr._value}мм х ' \
                           f'{well_data.column_additional_wall_thickness._value}мм ' \
                           f'+ НКТ60мм L- {round(paker_depth - well_data.head_column_additional._value, 0)}м'
            paker_short = f'Заглушка сбивной клапан с ввертышем + НКТ{60}мм {paker_khost}м + пакер ПРО-ЯМО-' \
                          f'{paker_diametr}мм + щелевой фильтр' \
                          f'+ НКТ60мм L- {round(paker_depth - well_data.head_column_additional._value, 0)}м'
        elif well_data.column_additional is True and well_data.column_additional_diametr._value > 110 and \
                paker_depth > well_data.head_column_additional._value:
            paker_select = f'Заглушка сбивной клапан с ввертышем + НКТ{well_data.nkt_diam}мм со снятыми фасками {paker_khost}м + ' \
                           f'пакер ПРО-ЯМО-{paker_diametr}мм (либо аналог) ' \
                           f'для ЭК {well_data.column_additional_diametr._value}мм х ' \
                           f'{well_data.column_additional_wall_thickness._value}мм + щелевой фильтр' \
                           f'+ НКТ{well_data.nkt_diam}мм со снятыми фасками L- ' \
                           f'{round(paker_depth - well_data.head_column_additional._value, 0)}м'
            paker_short = f'Заглушка сбивной клапан с ввертышем + НКТ{well_data.nkt_diam}мм со снятыми фасками {paker_khost}м + ' \
                          f'пакер ПРО-ЯМО-{paker_diametr}мм + щелевой фильтр' \
                          f'+ НКТ{well_data.nkt_diam}мм со снятыми фасками L- ' \
                          f'{round(paker_depth - well_data.head_column_additional._value, 0)}м'

        nktOpress_list = OpressovkaEK.nktOpress(self)


        paker_list = [
                [f'СПо {paker_short} до глубины {paker_depth}м', None,
                 f'Спустить {paker_select} на НКТ{well_data.nkt_diam}мм до глубины {paker_depth}м, '
                 f'воронкой до {paker_depth + paker_khost}м'
                 f' с замером, шаблонированием шаблоном {well_data.nkt_template}мм. {nktOpress_list[1]} '
                 f'{("Произвести пробную посадку на глубине 50м" if well_data.column_additional is False else "")} '
                 f'ПРИ ОТСУТСТВИИ ЦИРКУЛЯЦИИ ПРЕДУСМОТРЕТЬ НАЛИЧИИ В КОМПОНОВКЕ УРАВНИТЕЛЬНЫХ КЛАПАНОВ ИЛИ СБИВНОГО '
                 f'КЛАПАНА С ВВЕРТЫШЕМ НАД ПАКЕРОМ',
                 None, None, None, None, None, None, None,
                 'мастер КРС', descentNKT_norm(paker_depth, 1.2)],
                [None, None, f'Посадить пакер на глубине {paker_depth}м',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 0.4],
                [f'Очистить колонну от АСПО растворителем - 2м3', None,
                 f'Очистить колонну от АСПО растворителем - 2м3. При открытом затрубном пространстве закачать в '
                 f'трубное пространство растворитель в объеме 2м3, продавить в трубное пространство тех.жидкостью '
                 f'в объеме {round(3 * well_data.current_bottom / 1000, 1)}м3. Приподнять. Закрыть трубное и затрубное '
                 f'пространство. Реагирование 2 часа.',
                 None, None, None, None, None, None, None,
                 'Мастер КРС, предст. заказчика', 4],
                [f'cрыв пакера 30мин +1ч', None,
                 f'Сбить ввертыш. Произвести срыв пакера с поэтапным увеличением нагрузки на 3-4т выше веса НКТ '
                 f'в течении 30мин и с '
                 f'выдержкой 1ч для возврата резиновых элементов в исходное положение. ',
                 None, None, None, None, None, None, None,
                 'мастер КРС', 0.7],

                [None, None,
                 f'В случае негерметичности э/к, по согласованию с заказчиком произвести ОТСЭК для определения интервала '
                 f'негерметичности эксплуатационной колонны с точностью до одного НКТ или запись РГД, ВЧТ с '
                 f'целью определения места нарушения в присутствии представителя заказчика, составить акт. '
                 f'Определить приемистость НЭК.',
                 None, None, None, None, None, None, None,
                 'мастер КРС', None],
                [None, None,
                 f'Поднять {paker_select} на НКТ{well_data.nkt_diam}мм c глубины {paker_depth}м с доливом скважины в '
                 f'объеме {round(paker_depth * 1.12 / 1000, 1)}м3 удельным весом {well_data.fluid_work}',
                 None, None, None, None, None, None, None,
                 'мастер КРС', liftingNKT_norm(paker_depth, 1.2)]]



        return paker_list













