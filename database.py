class Table:
    from app import mysql
    def __init__(self, name):
        self.name = name

    def create_table(self, columns, primary):
        with Table.mysql.connection.cursor() as mycursor:
            mycursor.execute(f'CREATE TABLE {self.name} ({columns}, PRIMARY KEY({primary}))')

    def add_item(self, item):
        keys = ','.join(item.keys())
        values = tuple(item.values())
        with Table.mysql.connection.cursor() as mycursor:
            mycursor.execute(f'INSERT INTO {self.name} ({keys}) VALUES {values}')
        Table.mysql.connection.commit()

    def load_items(self):
        with Table.mysql.connection.cursor() as mycursor:
            mycursor.execute(f'SELECT * FROM {self.name}')
            return [Item(self, self.convert_item(x)) for x in mycursor]
    
    def find_items(self, where):
        with Table.mysql.connection.cursor() as mycursor:
            mycursor.execute(f'SELECT * FROM {self.name} WHERE {whereand(where)}')
            return [Item(self, self.convert_item(x)) for x in mycursor]

    def first(self, where):
        items = self.find_items(where = where)
        if items:
            return items[0]
        return None
        
    def item_by_id(self, itemid):
        return self.first(where = {'ID': itemid})

    def update_item(self, item, where):
        with Table.mysql.connection.cursor() as mycursor:
            mycursor.execute(f'UPDATE {self.name} SET {first(item.keys())}  = {first(item.values())} WHERE {whereand(where)}')
        Table.mysql.connection.commit()

    def update_items(self, items, where):
        with Table.mysql.connection.cursor() as mycursor:
            mycursor.execute(f'UPDATE {self.name} SET {moreitems(items)} WHERE {whereand(where)}')
        Table.mysql.connection.commit()
        
    def remove_item(self, where):
        with Table.mysql.connection.cursor() as mycursor:
            mycursor.execute(f'DELETE FROM {self.name} WHERE {whereand(where)}')
        Table.mysql.connection.commit()

    def convert_item(self, item):
        return dict(zip(self.columns, item))

    @property
    def columns(self):
        with Table.mysql.connection.cursor() as mycursor:
            mycursor.execute(f'SHOW COLUMNS FROM {self.name}')
            return (x[0] for x in mycursor)
class Item:
    def __init__(self, table, itemdict):
        self.table = table
        self.itemdict = itemdict
        for key, value in itemdict.items():
            setattr(self, key, value)
    
    def update(self, item):
        self.table.update_item(item = item, where = self.itemdict)

    def updates(self, items):
        self.table.update_items(items = items, where = self.itemdict)

    def remove(self):
        self.table.remove_item(where = self.itemdict)

    def __repr__(self):
        return str(self.itemdict)

def moreitems(lista):
    items = (f'{key} = "{value}"' for key, value in lista.items())
    string = ','.join(items)
    return string

def whereand(lista):
    items = (f'{key} = "{value}"' for key, value in lista.items())
    string = ' AND '.join(items)
    return string

def first(item):
    return next(iter(item))