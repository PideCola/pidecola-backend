from rest_framework import serializers

class BaseSerializer(serializers.ModelSerializer):
    def get_fields(self):
        fields = super().get_fields()
        exclude_fields = self.context.get('excluded_fields', [])
        
        
        for f in exclude_fields:
            if f in fields:
                fields.pop(f)

        return fields