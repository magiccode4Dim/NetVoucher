#guardar os aplicativos do django na base de dados default

class DjangoContribRouter:
    app_label = 'User'
    def db_for_read(self, model, **hints):
        if model._meta.app_label in ['auth', 'django', 'authtoken']:
            return 'default'  
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in ['auth', 'django', 'authtoken']:
            return 'default' 
        return None