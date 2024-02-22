from http.client import BAD_REQUEST, METHOD_NOT_ALLOWED
import json
from xml.dom import NotFoundErr
from django.contrib.auth import  authenticate
from rest_framework.authtoken.models import Token
import logging
from rest_framework import authentication
from rest_framework import exceptions
from django.contrib.auth.models import User
import base64
from rest_framework import status
from django_user_agents.utils import get_user_agent
# from .utils.exceptions import CustomException

logger=logging.getLogger('django')

class CustomAuthorization(authentication.BaseAuthentication):
    def authenticate(self, request):
        try:
            user_agent = get_user_agent(request)
            if user_agent.is_pc:
                data = json.loads(request.body)
                username = data['useraname'].strip() if 'username' in data else ''
                if not username:
                    raise exceptions.APIException()
                password = data['password'].strip() if 'password' in data else ''
                if not password:
                    raise exceptions.APIException()
                user = authenticate(request, username=username ,password=password)
                return(user, None)
            else:
                Token1=request.headers.get('Authorization')
                
                token_value=Token1.replace("token ","")
                print(token_value)
                token=Token.objects.get(key=token_value)
                print(token)
                user = User.objects.get(id=token.user_id)
                print(user)
                
                return(user, None)
        except NotFoundErr as e:
            logger.error(str(e),exc_info=True)
            
            message={
                "resultCode":"0",
                "resultDescription":"no mthod !!!"
            }
            raise CustomException(message, status_code=status.HTTP_404_NOT_FOUND)
        except Token.DoesNotExist as e:
            logger.error(str(e),exc_info=True)
            
            message={
                "resultCode":"0",
                "resultDescription":"unavailable token !!!"
            }
            raise CustomException(message, status_code=status.HTTP_404_NOT_FOUND)
        except AttributeError as e:
            logger.error(str(e),exc_info=True)
            
            message={
                "resultCode":"0",
                "resultDescription":"unavailable token"
            }
            raise CustomException(message, status_code=status.HTTP_404_NOT_FOUND)
       
        except Exception as e:
            logger.error(str(e),exc_info=True)
            
            message={
                "resultCode":"0",
                "resultDescription":"invalid token"
            }
            raise CustomException(message, status_code=status.HTTP_404_NOT_FOUND)
                
            
            

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
