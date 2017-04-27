from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from django.db.models.query import QuerySet
from rest_framework.views import APIView
from django.template.context_processors import request
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, permission_classes
from django.core.files.storage import FileSystemStorage
import os
import json
from models import Registration_Request,UserProfile,book,others
from django.contrib.auth.models import User
from django.contrib import auth





@api_view(http_method_names=['POST'])  
@permission_classes((permissions.AllowAny,))
def Register(request): 
    registration=json.loads(request.body)
    username=registration['username']
    password=registration['password']
    permission=registration['permission']
    email=registration['email']
    comment=registration['comment']
    try:
        user=User.objects.filter(username=username)
        if user.exists() is False:
            user=Registration_Request.objects.filter(Username=username)
            if user.exists() is False:
                new_request=Registration_Request(Username=username,Password=password,Email=email,
                                     Permission=permission,Comment=comment)
                new_request.save()
                return Response({'ststus':200})
            else:
                return Response({'ststus':400})
        else:
            return Response({'ststus':400})
    except:
        return Response({'ststus':400})


@api_view(http_method_names=['POST'])  
@permission_classes((permissions.IsAdminUser,))  
def AcceptRequest(request): 
    infor = json.loads(request.body)
    requestID = infor['requestID'] 
    try: 
        registration = Registration_Request.objects.get(id=requestID)
        new_user=User.objects.create_user(username=registration.Username,password=registration.Password,email=registration.Email)
        new_user.save()
        new_user=User.objects.get(username=new_user.username)
        new_user.userprofile.permission=registration.Permission
        new_user.userprofile.save()
        registration.delete()
        return Response({'ststus':200})
    except:
        return Response({'ststus':400})
        
@api_view(http_method_names=['POST'])  
@permission_classes((permissions.IsAdminUser,))  
def RejectRequest(request): 
    infor = json.loads(request.body)
    requestID = infor['requestID']
    try: 
        registration = Registration_Request.objects.get(id=requestID)
        registration.delete()
        return Response({'ststus':200})
    except:
        return Response({'ststus':400})


@api_view(http_method_names=['POST'])  
@permission_classes((permissions.IsAdminUser,))  
def AddAdminUser(request): 
    infor = json.loads(request.body)
    username=infor['username']
    password=infor['password']
    email=infor['email']
    try:
        user=User.objects.filter(username=username)
        if user.exists() is True:
            return Response({'ststus':400})
        else:
            new_user=User.objects.create_superuser(username,email,password)
            new_user.save()
            new_user=User.objects.get(username=new_user.username)
            new_user.userprofile.permission=1     
            new_user.userprofile.save()
            return Response({'ststus':200})
    except:
        return Response({'ststus':400})
    
    
@api_view(http_method_names=['POST'])  
@permission_classes((permissions.AllowAny,))  
def Login(request):  
    infor = json.loads(request.body)
    username=infor['username']
    password=infor['password']
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        return Response({'status':200, 'permission':user.userprofile.permission})
    else:
        return Response({'status':400})


@api_view(http_method_names=['GET'])  
@permission_classes((permissions.IsAdminUser,))  
def GetRequestList(request):
    try:
        user_list = Registration_Request.objects.all().values_list('id','Username','Permission','Comment','Email')
        return Response(user_list)
    except:
        return Response({'status':400})
    


@api_view(http_method_names=['GET'])  
@permission_classes((permissions.IsAdminUser,))  
def ChangePassword(request):
    infor = json.loads(request.body)
    password=infor['password']
    userID=infor['userID']
    try:
        user=User.objects.get(id=userID)
        user.set_password(password)
        user.save()
        return Response({'status':200})
    except:
        return Response({'status':400})
    
    
@api_view(http_method_names=['POST'])  
@permission_classes((permissions.AllowAny,))
def ForgetPassword(request): 
    infor = json.loads(request.body)
    username=infor['username']
    try:
        user=User.objects.get(username=username)
        email=user.email
        return Response({'status':200})
    except:
        return Response({'status':400})
    

        
    
@api_view(http_method_names=['POST'])  
@permission_classes((permissions.AllowAny,))
def FirstSearch(request): 
    infor = json.loads(request.body)
    type=infor['type']
    keyword=infor['keyword']
    if type=='Title':
        book_list=book.objects.filter(titles__contains=keyword).values_list('titles','monograph_part','file_ownership','modification_time')
        other_list=others.objects.filter(titles__contains=keyword).values_list('titles','monograph_part','file_ownership','modification_time')
        content = {
        'book_list': book_list,
        'other_list':other_list
        }
        return Response(content)
    elif type=='type':
        book_list=book.objects.filter(file_type=keyword).values_list('titles','monograph_part','file_ownership','modification_time')
        return Response(book_list)
    elif type=='study reference':
        book_list=book.objects.filter(study_reference=keyword).values_list('titles','monograph_part','file_ownership','modification_time')
        return Response(book_list)
    else:
        return Response({'status':400})
    
    
        
        
        
        

@api_view(http_method_names=['GET'])  
@permission_classes((permissions.AllowAny,))
def ViewFile(request): 
    pass
    
    
    
    
    
    
@api_view(http_method_names=['POST'])  
@permission_classes((permissions.AllowAny,))
def DownloadFile(request): 
    pass    



