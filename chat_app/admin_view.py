import json

from chat_app import models
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser


@api_view(['GET'])
def get_all_users(request):
    if request.session.get('user_login') is not None and request.session.get('is_admin') is not None:
        all_users = models.Credential.objects.all()
        users_json = {'users': []}
        for user in all_users:
            temp = {}
            b = models.BlackList.objects.filter(id_user=user).first()
            temp['user'] = user.login
            if b is not None:
                temp['blacklist'] = 'Y'
            else:
                temp['blacklist'] = 'N'
            users_json['users'].append(temp)
        return HttpResponse(json.dumps(users_json), content_type='application/json', status=status.HTTP_200_OK)
    else:
        return HttpResponse('Error login', status=status.HTTP_401_UNAUTHORIZED)


@csrf_exempt
@api_view(['GET', 'POST'])
def add_user_to_blacklist(request):
    if request.session.get('user_login') is not None and request.session.get('is_admin') is not None:
        json_data = JSONParser().parse(request)
        name = json_data['user']
        c = models.Credential.objects.filter(login=name).first()
        b = models.BlackList(id_user=c)
        b.save()
        return HttpResponse('OK', status=status.HTTP_200_OK)
    else:
        return HttpResponse('Error login', status=status.HTTP_401_UNAUTHORIZED)


@csrf_exempt
@api_view(['DELETE'])
def delete_user_from_blacklist(request, name):
    if request.session.get('user_login') is not None and request.session.get('is_admin') is not None:
        # c = models.Credential.objects.filter(login=name).first()
        b = models.BlackList.objects.filter(id_user__login=name).first()
        b.delete()
        return HttpResponse('OK', status=status.HTTP_200_OK)
    else:
        return HttpResponse('Error login', status=status.HTTP_401_UNAUTHORIZED)
