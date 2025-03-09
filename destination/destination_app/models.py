from django.db import models
import uuid
from .validators import validate_email, validate_website
## uuid --> secure and unique app secret token 
## Account Model ##

class Account(models.Model):
    account_id = models.AutoField(primary_key=True)
    account_name = models.CharField(max_length=250)
    app_secret_token = models.CharField(max_length=255, default=uuid.uuid4, editable=False)
    website = models.URLField(validators=[validate_website], blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add =True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=250)
    updated_by = models.CharField(max_length=250)

    def save(self, *args,**kwargs):
        if not self.app_secret_token:
            self.auto_now = str (uuid.uuid4())
        super().save(*args,**kwargs)

    def __str__(self):
        return self.account_name

class Destination(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='destinations')
    url = models.URLField(max_length=255) 
    http_method = models.CharField(max_length=10, choices=[('GET', 'GET'), ('POST', 'POST'), ('PUT', 'PUT'), ('DELETE', 'DELETE')])  
    headers = models.JSONField()  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  
    created_by = models.CharField(max_length=250)  
    updated_by = models.CharField(max_length=250) 


    def __str__(self):
        return self.account.account_name




class User(models.Model):   
    email = models.EmailField(validators=[validate_email],unique=True)
    password = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=250)
    updated_by = models.CharField(max_length=250)

    def __str__(self):
        return self.email


class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    ADMIN = 'Admin'
    NORMAL_USER = 'Normal user'
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (NORMAL_USER, 'Normal user'),
    ]
    role_name = models.CharField(max_length=20,choices=ROLE_CHOICES,default=NORMAL_USER )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.role_name


class AccountMember(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=250)
    updated_by = models.CharField(max_length=250)

    def __str__(self):
        return self.user.email



class Log(models.Model):
    event_id = models.CharField(max_length=250, unique=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    received_timestamp = models.DateTimeField()
    processed_timestamp = models.DateTimeField()
    received_data = models.TextField()
    status = models.CharField(max_length=20, choices=[("Success","Success"),("Faild","Faild")])

    def __str__(self):
        return self.account.account_name


