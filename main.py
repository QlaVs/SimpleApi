from datetime import datetime
from pytz import timezone
from transliterate import translit
from transliterate.base import TranslitLanguagePack, registry


class LanguagePack(TranslitLanguagePack):
    language_code = "my_ru"
    language_name = "MyRU"
    mapping = (
        u"абвгдезийклмнопрстуфъыьэАБВГДЗИКЛМНОПРСТУФЫЭ",
        u"abvgdeziyklmnoprstuf”y'eABVGDZIKLMNOPRSTUFYE",
    )
    pre_processor_mapping = {
        u"ё": u"yo",
        u"ж": u"zh",
        u"х": u"kh",
        u"ц": u"ts",
        u"ч": u"ch",
        u"ш": u"sh",
        u"щ": u"shch",
        u"ю": u"yu",
        u"я": u"ya",
        u"Е": u"Ye",
        u"Ё": u"Yo",
        u"Ж": u"ZH",
        u"Х": u"Kh",
        u"Ц": u"Ts",
        u"Ч": u"Ch",
        u"Ш": u"Sh",
        u"Щ": u"Shch",
        u"Ю": u"Yu",
        u"Я": u"Ya",
    }


registry.register(LanguagePack)


def get_cities(page, count):
    if page == 1:
        page = 0
    else:
        page = (page - 1) * count

    results = []
    file = open('RU.txt', 'r', encoding='utf-8')
    lines = file.readlines()
    for i in range(page, page + count):
        try:
            city = main_dictionary(lines[i])
            results.append(city)
        except IndexError:
            break
    return results


def main_dictionary(city_line):
    city = city_line.split('\t')
    return {
            'geonameid': city[0],
            'name': city[1],
            'asciiname': city[2],
            'alternatenames': city[3],
            'latitude': city[4],
            'longitude ': city[5],
            'feature class': city[6],
            'feature code': city[7],
            'country code': city[8],
            'cc2': city[9],
            'admin1 code': city[10],
            'admin2 code': city[11],
            'admin3 code': city[12],
            'admin4 code': city[13],
            'population': city[14],
            'elevation': city[15],
            'dem': city[16],
            'timezone': city[17],
            'modification date': city[18].split('\n')[0]
            }


def city_from_id(geonameid):
    file = open('RU.txt', 'r', encoding='utf-8')
    for line in file:
        if line.split('\t')[0] == str(geonameid):
            return line
    return False


def ru_to_eng(ru_name):
    file = open('RU.txt', 'r', encoding='utf-8')

    eng_name = translit(ru_name, 'my_ru')

    city_name = ''
    for line in file:
        eng_name_from_file = line.split('\t')[1]
        if eng_name_from_file == eng_name:
            if city_name == '':
                city_name = line
            else:
                if population(city_name) < population(line):
                    city_name = line
    if city_name:
        return city_name

    else:
        return False


def comparison(requested_city_1, requested_city_2, city_1=None, city_2=None):
    response = {}

    if city_1:
        data_1 = main_dictionary(city_1)
        response['Город 1'] = data_1
    else:
        if requested_city_1 == "*" or requested_city_1 == "":
            response['Город 1'] = 'Город 1 не был указан в запросе'
        else:
            response['Город 1'] = 'Информация о городе ' + requested_city_1 + ' отсутсвует.'

    if city_2:
        data_2 = main_dictionary(city_2)
        response['Город 2'] = data_2
    else:
        if requested_city_2 == "*" or requested_city_2 == "":
            response['Город 2'] = 'Город 2 не был указан в запросе'
        else:
            response['Город 2'] = 'Информация о городе ' + requested_city_2 + ' отсутсвует.'

    response['Город, расположенный севернее'] = compare_location(city_1, city_2)
    response['Временые зоны совпадают'] = compare_timezones(city_1, city_2)

    return response


def compare_location(city_1, city_2):
    if city_1 and city_2:
        city_1_info = main_dictionary(city_1)
        city_2_info = main_dictionary(city_2)

        if float(city_1_info['latitude']) > float(city_2_info['latitude']):
            return city_1
        else:
            return city_2

    elif city_1:
        return "Город 1 не был указан в запросе"

    elif city_2:
        return "Город 2 не был указан в запросе"

    else:
        return "Невозможно определить"


def compare_timezones(city_1, city_2):
    if city_1 and city_2:
        city_1_info = main_dictionary(city_1)
        city_2_info = main_dictionary(city_2)

        if (city_1_info['timezone']) == (city_2_info['timezone']):
            return "True"

        else:
            timezone_1 = city_1_info['timezone']
            timezone_2 = city_2_info['timezone']

            return "False, разница в часах: " + str(time_difference(timezone_1, timezone_2))

    elif city_1:
        return "Отсутсвует информация о городе 2, невозможно сравнить время"

    elif city_2:
        return "Отсутсвует информация о городе 1, невозможно сравнить время"

    else:
        return "Невозможно определить"


def population(city):
    return float(city.split('\t')[14])


def time_difference(timezone_1, timezone_2):
    fmt = '%H'
    tz_1 = datetime.now(timezone(timezone_1))
    tz_2 = datetime.now(timezone(timezone_2))
    tz_1_h = int(tz_1.strftime(fmt))
    tz_2_h = int(tz_2.strftime(fmt))
    return abs(tz_1_h - tz_2_h)
