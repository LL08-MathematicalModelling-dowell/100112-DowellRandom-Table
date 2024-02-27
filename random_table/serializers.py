import inspect

from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


from .functions import SearchEngine


# Filter choices gotten from the methods of the Search Engine classes. 
# Used as the value of the choice kwarg argument in filter_method choice field in the randomTableSerializers
filter_choices = [("_".join(name.split("_")[2:]) , "_".join(name.split("_")[2:]))  \
                  for name, _ in inspect.getmembers(SearchEngine) if name.startswith("filter_by")]

choices_required_values = ("regex" , "contains",
                            "not_contains" , "exact", 
                            "exact" , "starts_with" , 
                            "ends_with" , "greater_than" , 
                            "less_than" , "multiple_of") 


class MixedTypeField(serializers.Field):
    def to_internal_value(self, data):
        try:
            # Try to convert to integer
            
            if isinstance(data , str):
                if data.isdigit():
                    return int(data)
                return data
            return data
        except (ValueError, TypeError):
            # If conversion to integer fails, treat it as a string
            if isinstance(data , dict):
                raise ValidationError("Value can't be a dict")
            
            if isinstance(data , type(None)):
                raise ValidationError("Can't accept a null value")
            return str(data)
        
    def to_representation(self, value):
        # Represent the value as either string or integer
        print("values" , value)
        if isinstance(value , str):
            if value.isdigit():
                return int(value)
            return value
        return value


class randomTableSerializers(serializers.Serializer):
    """
        A serializer that validates the user inputs from the GET request
    """
    api_key = serializers.CharField(max_length = 255)
    filter_method = serializers.ChoiceField(choices=filter_choices)
    value = MixedTypeField(required = False)
    mini = serializers.IntegerField(required = False , default = 0)
    maxi = serializers.IntegerField(required = False , default = 0)
    position = serializers.IntegerField(default = 1)
    size = serializers.IntegerField(default = 10)
    set_size = serializers.IntegerField(default = 10)
    value = serializers.CharField(max_length = 255 , required = False)

    def __init__(self, instance=None, data=..., **kwargs):
        payment = kwargs.pop("payment") if "payment" in kwargs else None
        super().__init__(instance, data, **kwargs)
        
        if not (settings.USE_CLIENT_API_KEY or payment) :

            # Change the api_key field to not required if we aren't to accept client's API key.
            self.fields["api_key"].required = False

        filter_method_value = self.initial_data.get("filter_method")

        if filter_method_value in choices_required_values:
            self.fields["value"].required = True

        if filter_method_value in ("between" , "not_between"):
            self.fields["mini"].required = True
            self.fields["maxi"].required = True
            

    def validate_api_key(self , value):
        if not settings.USE_CLIENT_API_KEY:
            # Set the api_key value to our own api key if we aren't accepting the client's API key. 
            return settings.DATACUBE_API_KEY
        
        return value
    
    def validate_value(self , value):
        if isinstance(value , str):
            if value.isdigit():
                return int(value)
            return value
        return value
    
    


