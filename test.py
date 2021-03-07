def whereand(lista):
    items = (f'{key} = {value}' for key, value in lista.items())
    string = ' AND '.join(items)
    return string


bla = {'name': 'Majica'}

print(whereand(bla))