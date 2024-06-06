
from datetime import datetime

import well_data
from cdng import region_dict
import json


def region(cdng):
    region = ''.join([key for key, value in region_dict.items() if cdng in value])
    return region


# выбор подписантов в зависимости от вида ГТМ
def curator_sel(self, curator, region):
    with open('_internal/podpisant.json', 'r', encoding='utf-8') as file:
        podpis_dict = json.load(file)
    if curator == 'ОР':
        return (podpis_dict[region]['ruk_orm']['post'], podpis_dict[region]["ruk_orm"]['surname'])
    elif curator == 'ГТМ':
        return (podpis_dict[region]["ruk_gtm"]['post'], podpis_dict[region]["ruk_gtm"]['surname'])
    elif curator == 'ГО':
        return (podpis_dict[region]['go']['post'], podpis_dict[region]["go"]['surname'])
    elif curator == 'ВНС':
        return (podpis_dict[region]['go']['post'], podpis_dict[region]["go"]['surname'])
    elif curator == 'ГРР':
        return (podpis_dict[region]['grr']['post'], podpis_dict[region]["grr"]['surname'])


current_datetime = datetime.today()


# Выбор подписантов в зависимости от региона
def pop_down(self, region, curator_sel):
    from users.login_users import LoginWindow

    nach_tkrs_list = [' ', 'З.К. Алиев', 'М.К.Алиев']
    if region == 'ЧГМ' or region == 'ТГМ':
        nach_tkrs = nach_tkrs_list[0]
    elif region == 'КГМ' or region == 'АГМ':
        nach_tkrs = nach_tkrs_list[1]
    elif region == 'ИГМ':
        nach_tkrs = nach_tkrs_list[2]

    with open('_internal/podpisant.json', 'r', encoding='utf-8') as file:
        podpis_dict = json.load(file)



    podp_down = [
        [None, f'План работ составил {well_data.user[1]}', None, None, None, None, '___________________', None,
         None,
         f'{well_data.user[0]}', None, None],
        [None, None, None, None, None, None, None, None, 'дата составления', None, datetime.now().strftime('%d.%m.%Y'),
         None],
        [None, None, 'Начальник ЦТКРС ООО  " Ойл-Сервис"', None, None, None, None, None, None,
         ''.join(nach_tkrs), None, None],
        [None, None, None, None, None, None, None, None, None, '     дата подписания', None, None],
        [None, ' ', 'Согласовано:', None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, '', None, None, '', None, None],
        [None, curator_sel[0], None, None, None, None, '___________________', None, None,
         curator_sel[1], None, None],
        [None, None, None, None, None, None, '"___"___________', None, None, '     дата подписания', None,
         None],
        [None, podpis_dict[region]['ruk_pto']['post'], None, None, None, None, '___________________', None, None,
         podpis_dict[region]["ruk_pto"]['surname'], None, ' '],
        [None, None, None, None, None, None, '"___"___________', None, None, '     дата подписания', None,
         None],
        [None, podpis_dict[region]['usrs']['post'], None, None, None, None,
         '___________________', None, None, podpis_dict[region]['usrs']['surname'], None, None],
        [None, None, None, None, None, None, '"___"___________', None, None, '     дата подписания', None,
         None],
        [None, None, None, None, None, None, None, None, None, None, None, None],

        [None, 'Замечания:', None, None, None, None, None, None, None, None, None, None],
        [None, '1.', '________________________________________________________________________________________________',
         None, None, None, None,
         None,
         None,
         None, None, None],
        [None, '2.', '________________________________________________________________________________________________',
         None, None, None, None,
         None,
         None,
         None, None, None],
        [None, '3.', '________________________________________________________________________________________________',
         None, None, None, None,
         None,
         None,
         None, None, None],
        [None, '4.', '________________________________________________________________________________________________',
         None, None, None, None,
         None,
         None,
         None, None, None],
        [None, '5.', '________________________________________________________________________________________________',
         None, None, None, None,
         None,
         None,
         None, None, None],
        [None, None, None, 'Проинструктированы, с планом работ ознакомлены:                         ', None,
         None, None, None, None, None, None, None],
        [None, None, 'Мастер бригады', None, None, None, 'Инструктаж провел мастер бригады ООО "Ойл-Сервис"',
         None, None, None, None, None],
        [None, None, 'Мастер бригады', None, None, None, None, None, None, None, 'подпись', None],
        [None, 'Бурильщик ООО "Ойл-Сервис"', None, None,
         '_____________________Бурильщик ООО "Ойл-Сервис"________________________', None, None, None, None,
         None, None, None],
        [None, 'Пом.бур-ка ООО "Ойл-Сервис"', None, None,
         '_____________________Пом.бур-ка ООО "Ойл-Сервис"_______________________', None, None, None, None,
         None, None, None],
        [None, 'Пом.бур-ка ООО "Ойл-Сервис"', None, None,
         '_____________________Пом.бур-ка ООО "Ойл-Сервис"_______________________', None, None, None, None,
         None, None, None],
        [None, None, 'Машинист', None,
         '_____________________ МашинисТ                     ________________________', None, None, None,
         None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None]]

    ved_gtm_list = [None, podpis_dict[region]['ved_gtm']['post'], None, None, None, None, '_______________', None, None,
                    podpis_dict[region]['ved_gtm']['surname'], None, None]

    ved_orm_list = [None, podpis_dict[region]['ved_orm']['post'], None, None, None, None, '_______________', None, None,
                    podpis_dict[region]['ved_orm']['surname'], None, None]
    if (region == 'ЧГМ') and well_data.curator == 'ОР':
        podp_down.insert(13, ved_orm_list)
        podp_down.insert(14,
                         [None, None, None, None, None, None, '"___"___________', None, None, '     дата подписания',
                          None,
                          None])
    elif (region == 'КГМ') and well_data.curator == 'ОР' and well_data.work_plan == 'gnkt_opz':

        podp_down.insert(13, ved_orm_list)
        podp_down.insert(14,
                         [None, None, None, None, None, None, '"___"___________', None, None, '     дата подписания',
                          None,
                          None])
    elif (region == 'КГМ') and well_data.curator == 'ОР':

        podp_down.insert(13, ved_gtm_list)
        podp_down.insert(14,
                         [None, None, None, None, None, None, '"___"___________', None, None, '     дата подписания',
                          None,
                          None])
    elif region == 'КГМ' or region == 'ЧГМ' and well_data.curator == 'ГТМ':
        podp_down.insert(13, ved_gtm_list)
        podp_down.insert(14,
                         [None, None, None, None, None, None, '"___"___________', None, None, '     дата подписания',
                          None,
                          None])
    elif region == 'КГМ' or region == 'ЧГМ' and well_data.curator == 'ГТМ':
        podp_down.insert(13, ved_gtm_list)
        podp_down.insert(14,
                         [None, None, None, None, None, None, '"___"___________', None, None, '     дата подписания',
                          None,
                          None])
    if well_data.curator == "ВНС":
        podp_down.insert(6, [None, 'Менеджер ТКРС БНД', None, None, None, None, '___________________', None, None,
         'А.М. Кузьмин', None, ' '])
        podp_down.insert(7,
                         [None, None, None, None, None, None, '"___"___________', None, None, '     дата подписания',
                          None,
                          None])

    return podp_down


def razdel_1(self, region):


    with open('_internal/podpisant.json', 'r', encoding='utf-8') as file:
        podpis_dict = json.load(file)

    razdel_1 = [
        [None, 'СОГЛАСОВАНО:', None, None, None, None, None, 'УТВЕРЖДАЕМ:', None, None, None, None],
                [None, podpis_dict[region]['gi']['post'], None, None, None, None, None,
                 'Главный Инженер ООО "Ойл-Сервис"', None, None, None, None],
                [None, f'____________{podpis_dict[region]["gi"]["surname"]}', None, None, None, None, None,
                 '_____________А.Р. Хасаншин', None, None, None, None],
                [None, f'"____"_____________________{current_datetime.year}г.', None, None, None, None, None,
                 f'"____"_____________________{current_datetime.year}г.', None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None],
                [None, podpis_dict[region]['gg']['post'], None, None, None,
                 None,
                 None, 'Главный геолог ООО "Ойл-Сервис"', None, None, None, None],
                [None, f'_____________{podpis_dict[region]["gg"]["surname"]}', None, None, None, None, None,
                 '_____________Д.Д. Шамигулов', None, None, '',
                 None],
                [None, f'"____"_____________________{current_datetime.year}г.', None, None, '', None, None,
                 f'"____"_____________________{current_datetime.year}г.', None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None, None, None]]

    podp_grp = [[None, 'Представитель подрядчика по ГРП', None, None, None, None, None, None, None, None, None,
                 None],
                [None, '_____________', None, None, None, None, None, None, None, None, None, None],
                [None, f'"____"_____________________{current_datetime.year}г.', None, None, None, None, None, None,
                 None, None, None,
                 None]]
    podp_bvo = [
        [None, 'Районный инженер Башкирского ', None, None, None, None, None, None, None, None, None, None],
        [None, 'военизированного отряда ', None, None, None, None, None, None, None, None, None, None],
        [None, '_____________', None, None, None, None, None, None, None, None, None, None],
        [None, f'"____"_____________________{current_datetime.year}г.', None, None, None, None, None, None,
         None, None, None,
         None]]
    if well_data.data_in_base is False:
        if len(well_data.plast_work) != 0:
            # print(well_data.plast_work, well_data.dict_category)
            try:
                cat_P_1 = well_data.dict_category[well_data.plast_work[0]]['по давлению'].category
                cat_h2s_list = well_data.dict_category[well_data.plast_work[0]]['по сероводороду'].category
                cat_gaz = well_data.dict_category[well_data.plast_work[0]]['по газовому фактору'].category
            except:
                cat_P_1 = well_data.cat_P_1[0]
                cat_h2s_list = well_data.cat_h2s_list[0]
                cat_gaz = well_data.cat_gaz_f_pr[0]
        else:
            cat_P_1 = well_data.cat_P_1[0]
            cat_h2s_list = well_data.cat_h2s_list[0]
            cat_gaz = well_data.cat_gaz_f_pr[0]
        try:
            cat_P_1_plan = well_data.dict_category[well_data.plast_project[0]]['по давлению'].category
            cat_h2s_list_plan = well_data.dict_category[well_data.plast_project[0]]['по сероводороду'].category
            cat_gaz_plan = well_data.dict_category[well_data.plast_project[0]]['по газовому фактору'].category
        except:
            cat_P_1_plan = 3
            cat_h2s_list_plan = 3
            cat_gaz_plan = 3

        if 1 in [cat_P_1, cat_P_1_plan, cat_h2s_list, cat_gaz, cat_h2s_list_plan, cat_gaz_plan,
                 well_data.category_pressuar] or '1' in [cat_P_1, cat_P_1_plan, cat_h2s_list, cat_gaz,
                                                       cat_h2s_list_plan, cat_gaz_plan,
                                                         well_data.category_pressuar] or \
                well_data.curator == 'ВНС':
            for row in range(len(podp_bvo)):
                for col in range(len(podp_bvo[row])):
                    razdel_1[row + 9][col] = podp_bvo[row][col]
        if 1 in [cat_P_1, cat_h2s_list, cat_gaz] or \
                well_data.curator == 'ВНС':
            well_data.kat_pvo = 1
            well_data.bvo = True

        if well_data.grp_plan is True:
            for row in range(len(podp_grp)):
                for col in range(len(podp_grp[row])):
                    razdel_1[row + 12][col] = podp_grp[row][col]

    return razdel_1
