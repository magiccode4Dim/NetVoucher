class ClienteRouter:
    app_label = 'Cliente'
    def db_for_read(self, model, **hints):
        if model._meta.app_label == self.app_label:
            return 'default'  
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == self.app_label:
            return 'default' 
        return None
