from django.contrib.auth.models import User
from rest_framework import serializers,validators
from .models import Request, Accepted_req, Completed_trip

class mobiUser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','password','email',)
        
        USER_FIELD = 'email'
        extra_kwargs = { 'password' : {'write_only': True}, 'email': {'required':True,'allow_blank': False ,'validators':[validators.UniqueValidator(User.objects.all(),'Email already used')]}}


    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],  
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ('request_id', 'patient', 'pickLatitude', 'pickLongitude',
                  'contact', 'hospitalLatitude', 'hospitalLongitude')

    def create(self, validated_data):
        request = Request.objects.create(**validated_data)
        return request
    
class AcceptedRequestSerializer(serializers.ModelSerializer):
    driver = serializers.StringRelatedField()
    request = serializers.StringRelatedField()

    class Meta:
        model = Accepted_req
        fields = '__all__'

class CompletedTripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Completed_trip
        fields = '__all__'

class MpesaSerializer(serializers.Serializer):
    MerchantRequestID = serializers.CharField()
    CheckoutRequestID = serializers.CharField()
    ResponseCode = serializers.CharField()
    ResponseDescription = serializers.CharField()
    CustomerMessage = serializers.CharField()