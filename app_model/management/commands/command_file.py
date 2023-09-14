from django.core.management.base import BaseCommand
from django.db import models
from django.apps import apps

class Command(BaseCommand):
    help = "Create a Django model with custom fields"

    def add_arguments(self, parser):
        parser.add_argument('model_name', type=str, help='Name of the model to create')
        parser.add_argument('fields', type=str, nargs='+', help='Fields in the format name:type')

    def handle(self, *args, **kwargs):
        model_name = kwargs['model_name']
        fields = kwargs['fields']

        
        model_definition = f"class {model_name}(models.Model):\n"
        for field in fields:
            name, field_type = field.split(':')
            
            if hasattr(models, field_type):
                model_definition += f"    {name} = models.{field_type}()\n"
            else:
                self.stderr.write(self.style.ERROR(f"Invalid field type: {field_type}"))
                return

        
        app_config = apps.get_app_config('app_model')
        models_module = app_config.models_module

        
        exec(model_definition, models_module.__dict__)

        
        with open(models_module.__file__, 'a') as models_file:
            models_file.write(model_definition)

        self.stdout.write(self.style.SUCCESS(f"Model '{model_name}' created and added to models.py"))
