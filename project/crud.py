# project/crud.py
from project.models import *
from flask import current_app

class Flask_crud():
    def insert_data(self,records):
        try:
            with current_app.app_context():
                data = self(**records)
                models.session.add(data)
                models.session.commit()
                models.session.close()
                return 'operation completed'
        except Exception as error:
            return f'Ocurrio un error: {error}'   
    
    def insert_data_all(self, records):
        try:
            with current_app.app_context():
                for i in records:
                    data = self(**i)
                    models.session.add(data)
                    models.session.commit()
                    models.session.close()
                return 'operation completed'
        except Exception as error:
            return f'Ocurrio un error: {error}'   
        
    def read_data_all(self):
        try:
            with current_app.app_context():
                data = self.query.all()
                return data
        except Exception as error:
            return f'Ocurrio un error: {error}' 
    
    def read_data(self, **filter):
        try:    
            with current_app.app_context():
                for column, record in filter.items():
                    query = self.query.filter(getattr(self, column) == record)
                data = query.all()
                return data
            
        except Exception as error:
            return f'Ocurrio un error: {error}' 
        
    def read_data_filter(self, **filter):
        try:    
            with current_app.app_context():
                for column, record in filter.items():
                    if column.split('__')[1] == 'exact':
                        query = self.query.filter(getattr(self, column.split('__')[0]) == record)
                    elif column.split('__')[1] == 'gt':
                        query = self.query.filter(getattr(self, column.split('__')[0]) > record)
                    elif column.split('__')[1] == 'gte':
                        query = self.query.filter(getattr(self, column.split('__')[0]) >= record)
                    elif column.split('__')[1] == 'lt':
                        query = self.query.filter(getattr(self, column.split('__')[0]) < record)
                    elif column.split('__')[1] == 'lte':
                        query = self.query.filter(getattr(self, column.split('__')[0]) <= record)
                    elif column.split('__')[1] == 'ne':
                        query = self.query.filter(getattr(self, column.split('__')[0]) != record)
                    elif column.split('__')[1] == 'isnull':
                        query = self.query.filter(getattr(self, column.split('__')[0]) == None)
                    elif column.split('__')[1] == 'contains':
                        query = self.query.filter(getattr(self, column.split('__')[0]).contains(record))
                    elif column.split('__')[1] == 'startswith':
                        query = self.query.filter(getattr(self, column.split('__')[0]).startswith(record))
                    elif column.split('__')[1] == 'endswith':
                        query = self.query.filter(getattr(self, column.split('__')[0]).endswith(record))
                data = query.all()
                return data
            
        except Exception as error:
            return f'Ocurrio un error: {error}' 


    def update_data(self, recordUp, **filter):
        try:    
            with current_app.app_context():
                for column, record in filter.items():
                    query = self.query.filter(getattr(self, column) == record)
                data = query.all()

                for row in data:
                    for key, value in recordUp.items():
                        setattr(row, key, value)

                models.session.commit()
                models.session.close()
                return 'operation completed'
            
        except Exception as error:
            return f'Ocurrio un error: {error}'     
        

    def delete_data(self, **filter):
        try:    
            with current_app.app_context():
                for column, record in filter.items():
                    query = self.query.filter(getattr(self, column) == record)
                data = query.all()

                for row in data:
                    models.session.delete(row) 

                models.session.commit()
                return 'operation completed'
            
        except Exception as error:
            return f'Ocurrio un error: {error}'     