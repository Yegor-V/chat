from django.db import models


class Users(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)


# class Credential(models.Model):
#     login = models.CharField(max_length=20, unique=True)
#     password = models.CharField(max_length=20)
#     is_admin = models.BooleanField()
    # id_users = models.ForeignKey(to=Users, on_delete=models.CASCADE())
    # user = models.OneToOneField(to=Users, on_delete=models.CASCADE(), primary_key=True)


class Credential(Users):
    max_len_cred = 20
    login = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    is_admin = models.BooleanField(default=False)


class Messages(models.Model):
    message = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now=True)
    id_sender = models.ForeignKey(to=Credential, on_delete=models.CASCADE, related_name='sender')
    id_receiver = models.ForeignKey(to=Credential, on_delete=models.CASCADE, related_name='receiver')


class BlackList(models.Model):
    id_user = models.ForeignKey(to=Credential, on_delete=models.CASCADE)