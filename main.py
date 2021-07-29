def parse(string):  # Рабочий код
    tab = dict()
    keys = list()
    values = list()
    if re.search(r'\?[\W]*(.+?)[\W]*=', string) is not None:
        qe_tmp = re.search(r'\?[\W]*(.+?)[\W]*=', string)
        keys.append(qe_tmp.group(1))
    if re.search(r'\=[\W]*(.+?)[\W]*&', string) is not None:
        eu_tmp = re.search(r'\=[\W]*(.+?)[\W]*&', string)
        values.append(eu_tmp.group(1))
    if re.search(r'\&[\W]*(.+?)[\W]*=', string) is not None:
        ue_tmp = re.search(r'\&[\W]*(.+?)[\W]*=', string)
        keys.append(ue_tmp.group(1))
    if re.search(r'=(?!.*=)(.+?)\b', string) is not None:
        el_tmp = re.search(r'=(?!.*=)(.+?)\b', string)  # abc(?!.*abc)
        values.append(el_tmp.group(1))
    for i in range(len(keys)):
        tab.update({keys[i]:values[i]})  # {qe: eu, ue: el}
    return tab

if __name__ == '__main__':
    assert parse('https://example.com/path/to/page?name=ferret&color=purple') == {'name': 'ferret', 'color': 'purple'}
    assert parse('https://example.com/path/to/page?name=ferret&color=purple&') == {'name': 'ferret', 'color': 'purple'}
    assert parse('http://example.com/') == {}
    assert parse('http://example.com/?') == {}
    assert parse('http://example.com/?name=Dima') == {'name': 'Dima'}
    assert parse('http://example.com/?name%=Dima') == {'name': 'Dima'}
    assert parse('http://example.com/?name%=Dima()') == {'name': 'Dima'}
    assert parse('http://example.com/?name=Dima#') == {'name': 'Dima'}
    assert parse('http://example.com/?name=Dima=Dima#') == {'name': 'Dima'}
    assert parse('http://example.com/?surname=Dima=Dimonchik ') == {'surname': 'Dimonchik'}
    assert parse('http://example.com/?surname=    Dima =Dimonchik  ') == {'surname': 'Dimonchik'}
    assert parse('http://example.com/?surname      =    Dima =Dimonchik  ') == {'surname': 'Dimonchik'}
    assert parse('https://example.com/path/to/page?$name$=ferret&color=purple') == {'name': 'ferret', 'color': 'purple'}
    assert parse('https://example.com/path/to/page?$name$=ferret&color&^=purple*') == {'name': 'ferret', 'color': 'purple'}
    assert parse('https://example.com/path/to/page?$name=ferret#&color&%=purple&') == {'name': 'ferret', 'color': 'purple'}

def parse_cookie(string):  #  Рабочий код
    def name_n(string):  # получаем поле 'name' ^(.*?)=
        tmp = re.findall(r'[\W]*(.*?)[\W]*=', string)
        if tmp != []:
            return tmp[0]

    def name(string):  # получаем name
        if re.findall(r'=[\W]*(.*=.*);.*[\W]*=', string) != []:
            tmp = re.findall(r'=[\W]*(.*=.*);.*[\W]*=', string)
            return tmp[0]
        elif re.findall(r'=[\W]*(.*?)[\W]*;', string) != []:
            tmp = re.findall(r'=[\W]*(.*?)[\W]*;', string)
            return tmp[0]

    def age_n(string):  # получаем поле 'age'
        tmp = re.findall(r';[\W]*(\w*)[\W]*=', string)
        if tmp != []:
            return tmp[0]

    def age(string):  # получаем age
        tmp = re.findall(r';.*=[\W]*(.*?)[\W]*;', string)
        if tmp != []:
            return tmp[0]

    tab = {name_n(string): name(string), age_n(string): age(string)}  # Заполняем словарь
    if None in tab:  # Проверяем словарь на наличие None
        tab.pop(None)
    elif '' in tab:
        tab.pop('')
    return tab

if __name__ == '__main__':
    assert parse_cookie('name=Dima;') == {'name': 'Dima'}
    assert parse_cookie('') == {}
    assert parse_cookie('name=Dima;age=28;') == {'name': 'Dima', 'age': '28'}
    assert parse_cookie('name=Dima=User;age=28;') == {'name': 'Dima=User', 'age': '28'}
    assert parse_cookie('dfsdfsd') == {}
    assert parse_cookie('ewri;uy234lkjdsfljs35') == {}
    assert parse_cookie('name') == {}
    assert parse_cookie('name=Petya; age=8;') == {'name': 'Petya', 'age': '8'}
    assert parse_cookie('name = Borya ; color = WSGI ;') == {'name': 'Borya', 'color': 'WSGI'}
    assert parse_cookie('=;=;') == {}
    assert parse_cookie(' k = B ; G = 34 ; Акакий ') == {'k': 'B', 'G': '34'}
    assert parse_cookie('$Surname=Gogy; job = Traktor;') == {'Surname': 'Gogy', 'job': 'Traktor'}
    assert parse_cookie('(*)surname@=&Griboedov&;#age#=(198);') == {'surname': 'Griboedov', 'age': '198'}
    assert parse_cookie('%passport%=!FA345846!; sex=^male^;') == {'passport': 'FA345846','sex': 'male'}
    assert parse_cookie('*&@^#name      (*@&#=    Dima)(@#)&;') == {'name': 'Dima'}
