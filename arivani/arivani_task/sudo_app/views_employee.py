from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth.models import User
from sudo_app.models import *
from auth_user.models import *

from django.contrib.auth.models  import User

from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login as login_user
from django.contrib.auth import authenticate
from django.contrib.auth import logout as logout_user
from django.db import IntegrityError
import json
import random
from django.urls import reverse

#custom user password validation related import
import re

from django.utils.encoding import smart_str, force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
#Email related import
from django.conf import settings
#email backend
from django.core.mail import EmailMessage

#django messeges related imports
from django.contrib import messages

def employee_page(request):
    if request.user.is_authenticated:
        logged_in_user = request.user.id
        user = User.objects.get(id=logged_in_user)
        if user.is_superuser:
            data = {
                'is_superuser':1
            }
            return render(request,'sudo_app/employee_page.html',data)
        else:
            return redirect("loginUserPage")
    else:
        return redirect("loginUserPage")