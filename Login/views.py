from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect,Http404
from django.views.generic import TemplateView
from django.urls import reverse
from django.views import View
from . forms import NewUserForm,UserForm
from . models import Profile
from django.contrib import auth
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Profile
from .serializers import ProfileSerializer
from rest_framework import status

# Create your views here.
class HomePage(TemplateView):
    template_name='Login/home.html'


class SignUp(View):
    form_class = NewUserForm()
    template_name='Login/signup.html'

    def get(self,request):
        return render(request,self.template_name,{'form':self.form_class})

    def post(self,request,*args,**kwargs):
        user_form = NewUserForm(data=request.POST)
        if user_form.is_valid():
            if request.POST['password'] == request.POST['password2']:
                try:
                    user_profile=Profile.objects.get(username=request.POST['username'])
                    return render(request,self.template_name,{'error':'Username already taken',
                                                                'form':self.form_class})
                except Profile.DoesNotExist:
                    """ Takes data from the form and saves the raw password but .set_password hashes it and then it is saved"""
                    user =  user_form.save()
                    user.set_password(user.password)
                    user.save()
                    return HttpResponseRedirect(reverse('homepage'))
            else:
                return render(request,self.template_name,{'error':'passwords dont match','form':self.form_class})
        """ else:
        #     print('*********')
        #     print(user_form.error)"""



class Login(View):
    form_class = UserForm()
    template_name = 'Login/login.html'

    def get(self,request):
        return render(request,self.template_name,{'form':self.form_class})

    def post(self,request,*args,**kwargs):
        user_form = UserForm(data=request.POST)
        model = Profile
        if user_form.is_valid():
                    user_name = request.POST['username']
                    pass_word = request.POST['password']
                    """ authenticates takes a password and hashes it and then it checks in the db  """
                    user = auth.authenticate(username=user_name,password=pass_word)
                    if user is not None and user.is_active:
                        auth.login(request,user)
                        return HttpResponseRedirect(reverse('homepage'))
                    else:
                        return render(request,self.template_name,{'form':self.form_class,'error':'Incorrect Credentials','username':user_name})

class LogoutView(View):
    def get(self,request):
        auth.logout(request)
        return HttpResponseRedirect(reverse('homepage'))




class ProfileList(APIView):
    model = Profile

    def get(self,request):
        profile = self.model.objects.all()
        serializer = ProfileSerializer(profile,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class ProfileDetailView(APIView):
    model = Profile

    def get_object(self,pk):
        try:
            return self.model.objects.get(pk=pk)
        except:
            raise Http404

    def get(self,request,pk):
        profile =self.get_object(pk=pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def patch(self,request,pk):
        profile = get_object_or_404(self.model,pk=pk)
        serializer = ProfileSerializer(profile,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
