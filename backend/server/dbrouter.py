from django.db import models
from .models import *

allmodels = dict([(name.lower(), cls) for name, cls in models.__dict__.items() if isinstance(cls, type)])

class mydbrouter(object):

    def db_for_read(self, model, **hints):
        """ reading book_instance from book_db """
        if model == Book_Instance:
            return 'book_db'
        return None


    def db_for_write(self, model, **hints):
        """ writing book_instance to book_db """
        if model == Book_Instance:
            return 'book_db'
        return None


    def allow_migrate(self, db, app_label, model_name = None, **hints):
        """ migrate to appropriate database per model """
        try:
            model = allmodels.get(model_name)
            return(model.params.db == db)
        except:
            pass

