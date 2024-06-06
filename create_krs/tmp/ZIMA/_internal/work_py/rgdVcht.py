from PyQt5.QtWidgets import QMessageBox

import well_data
from .descent_gno import GnoDescentWindow


def rgdWithoutPaker(self):

    rgd_list = [
        [f'СП НКТ 300м', None, f'Спустить с замером воронку на НКТ до  глубины 300м с замером, шаблонированием шаблоном {well_data.nkt_template}мм . '
                     f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ)',
         None, None, None, None, None, None, None,
         'мастер КРС', 1.3  ],
        [None, None, f'Произвести  монтаж ГИС согласно схемы  №8 при работе ГИС с утвержденной главным инженером оТ 14.10.2021г '
                     f'Обвязать устье скважины с ЕДК на жесткую линию. Опрессовать ПВО максимально допустимое давление опрессовки э/колонны на '
                     f'устье {well_data.max_admissible_pressure._value}атм, по невозможности на давление поглощения, но не менее 30атм '
                     f'в течении 30мин Провести практическое обучение вахт по сигналу "выброс" с записью в журнале проведения учебных тревог',
         None, None, None, None, None, None, None,
         'мастер КРС', 0.75],
        [''.join(['ОВТР 10ч' if well_data.region != 'ЧГМ' else 'ОВТР 4ч']), None, ''.join(['ОВТР 10ч' if well_data.region != 'ЧГМ' else 'ОВТР 4ч']),
             None, None, None, None, None, None, None,
             'мастер КРС', ''.join(['10' if well_data.region != 'ЧГМ' else '4'])],
        [None, None, 'Вызвать геофизическую партию. Заявку оформить за 16 часов через ЦИТС "Ойл-сервис". Составить'
                         ' акт готовности скважины и передать его начальнику партии. При необходимости подготовить площадку'
                         ' напротив мостков для постановки партии ГИС.',
             None, None, None, None, None, None, None,
             'мастер КРС', None],
            [f'РГД по колонне при закачке не менее {GnoDescentWindow.PzakPriGis(self)}атм',
             None,
             f'Произвести запись по техкарте 2.3.1: Определение профиля приемистости скважины и оценка технического состояния '
             f'эксплуатационной колонны при закачке (скважинная аппаратура на кабеле, НКТ подняты). '
             f'Давление закачки должно быть согласно ожидаемой закачки ППД. при закачке не менее '
             f'{GnoDescentWindow.PzakPriGis(self)}атм '
             f'при открытой затрубной задвижке',
             None, None, None, None, None, None, None,
             'Мастер КРС, подрядчик по ГИС', 20]]
    ori = QMessageBox.question(self, 'ОРИ', 'Нужна ли интерпретация?')
    if ori == QMessageBox.StandardButton.Yes:
        rgd_list.append([f'ОРИ', None,
                                    f'Интерпретация данных ГИС, согласовать с ПТО и Ведущим инженером ЦДНГ опрессовку фНКТ ',
                                    None, None, None, None, None, None, None,
                                    'Мастер КРС, подрядчик по ГИС', 8])
        rgd_list.append([None, None,
                         f'Поднять компоновку с доливом скважины в объеме 0.3м3 тех. жидкостью  уд.весом {well_data.fluid_work}',
                         None, None, None, None, None, None, None,
                         'Мастер КРС', 1.3])
    else:
        rgd_list.append([None, None,
                  f'Поднять компоновку с доливом скважины в объеме 0.3м3 тех. жидкостью  уд.весом {well_data.fluid_work}',
                  None, None, None, None, None, None, None,
                  'Мастер КРС', 1.3])
    return rgd_list

def rgdWithPaker(self):
   

    vcht_rgd = [[''.join(['ОВТР 10ч' if well_data.region != 'ЧГМ' else 'ОВТР 4ч']),
                 None, ''.join(['ОВТР 10ч' if well_data.region != 'ЧГМ' else 'ОВТР 4ч']),
                 None, None, None, None, None, None, None,
                 'мастер КРС', ''.join(['10' if well_data.region != 'ЧГМ' else '4'])],
                [None, None,
                 'Вызвать геофизическую партию. Заявку оформить за 16 часов через ЦИТС "Ойл-сервис". Составить'
                 ' акт готовности скважины и передать его начальнику партии. При необходимости подготовить площадку'
                 ' напротив мостков для постановки партии ГИС.',
                 None, None, None, None, None, None, None,
                 'мастер КРС', None],
                [f'ГИС РГД', None,
                 f'Произвести запись по техкарте 2.3.2: определение профиля приемистости и оценку технического состояния '
                 f'эксплуатационной колонны и НКТ при закачке не менее {GnoDescentWindow.PzakPriGis(self)}атм '
                 f'при открытой затрубной задвижке',
                 None, None, None, None, None, None, None,
                 'Мастер КРС, подрядчик по ГИС', 20],
                [None, None,
                 f'Интерпретация данных ГИС',
                 None, None, None, None, None, None, None,
                 'мастер КРС, подрядчик по ГИС', 8]]
    return vcht_rgd