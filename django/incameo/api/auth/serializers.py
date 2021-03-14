from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model

class SignupSerializer(ModelSerializer):
    class Meta: 
        model = get_user_model() 
        fields =  ('user_fullname', 'user_username', 'user_email', 'password',)
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}}
        }

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user