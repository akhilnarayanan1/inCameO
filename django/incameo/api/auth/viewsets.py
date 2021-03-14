from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.exceptions import ValidationError, status
from .serializers import SignupSerializer
from django.contrib.auth import get_user_model
from django.conf import settings
import requests
import json


class SignupViewset(CreateModelMixin, GenericViewSet): 
    '''Viewset to Signup users'''
    queryset = get_user_model().objects.all() 
    serializer_class = SignupSerializer 
    lookup_field = 'user_id'

class AuthFacebook(APIView):
  def get(self, request, format=None):
    access_token, token_type, expires_in = FacebookAuth().GetAccessToken(request.GET.get('code',''))
    if not FacebookAuth().CheckEmailPermission(access_token):
      raise ValidationError({"error":{"message":"Email permission not granted"}})
    user_id, name, email = FacebookAuth().GetNameAndEmail(access_token)
    return Response({"user_id": user_id, "name": name, "email": email,"state": json.loads(json.loads(request.GET.get('state','')))})

class AuthGoogle(APIView):
  def get(self, request, format=None):
    access_token, expires_in, token_type, scope, id_token = GoogleAuth().GetAccessToken(request.GET.get('code',''))
    user_id, name, email = GoogleAuth().GetNameAndEmail(access_token)
    return Response({"user_id": user_id, "name": name, "email": email,"state": json.loads(json.loads(request.GET.get('state','')))})
    


class GoogleAuth:
  def __init__(self):
    self.__client_id = settings.GOOGLE_CLIENT_ID
    self.__client_secret = settings.GOOGLE_CLIENT_SECRET
    self.__key = settings.GOOGLE_KEY
    self.base_url = 'https://oauth2.googleapis.com/token'
    self.redirect_uri = settings.REDIRECT_URI

  def GetAccessToken(self, code):
    payload = {
        'client_id': self.__client_id,
        'client_secret': self.__client_secret,
        'grant_type': 'authorization_code',
        'redirect_uri': self.redirect_uri+'google/',
        'code': code,
    }
    response = requests.post(self.base_url, payload)
    if response.status_code == 200:
      access_token = response.json()["access_token"]
      expires_in = response.json()["expires_in"]
      token_type = response.json()["token_type"] 
      scope = response.json()["scope"]
      id_token = response.json()["id_token"]
      return access_token, expires_in, token_type, scope, id_token
    else:
      raise ValidationError(response.json())
  
  def GetNameAndEmail(self,access_token):
    response = requests.get('https://people.googleapis.com/v1/people/me?personFields=names,emailAddresses'+ \
    '&key='+self.__key+'&access_token='+access_token)
    if response.status_code == 200:
      user_id = response.json()["names"][0]["metadata"]["source"]["id"]
      name = response.json()["names"][0]["displayName"]
      email = response.json()["emailAddresses"][0]["value"]
      return user_id, name, email
    else:
      raise ValidationError(response.json())

  

class FacebookAuth:
  def __init__(self):
    self.__client_id = settings.FACEBOOK_CLIENT_ID
    self.__client_secret = settings.FACEBOOK_CLIENT_SECRET
    self.base_url = settings.FACEBOOK_BASE_URL
    self.redirect_uri = settings.REDIRECT_URI

  
  def GetAccessToken(self, code):
    response = requests.get(self.base_url+'oauth/access_token?client_id='+self.__client_id+ \
    '&redirect_uri='+self.redirect_uri+'facebook/' \
    '&client_secret='+self.__client_secret+  \
    '&code='+code)

    if response.status_code == 200:
      access_token = response.json()["access_token"]
      token_type = response.json()["token_type"]
      expires_in = response.json()["expires_in"]
      return access_token, token_type, expires_in
    else:
      raise ValidationError(response.json())

  def CheckEmailPermission(self, access_token):
    response = requests.get(self.base_url+'me/permissions/email?&access_token='+access_token)
    if response.status_code == 200:
      if response.json()["data"][0]["status"] == "granted":
        return True
      return False
    else:
      raise ValidationError(response.json())

  def GetNameAndEmail(self,access_token):
    response = requests.get(self.base_url+'me?fields=id,name,email&access_token='+access_token)
    if response.status_code == 200:
      user_id = response.json()["id"]
      name = response.json()["name"]
      email = response.json()["email"]
      return user_id, name, email
    else:
      raise ValidationError(response.json())