from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator

class SignUpView(View):
    template="auth/register.html"
    def get(self, request):
        return render(request, self.template, )
    def post(self,request):
        current_site=get_current_site(request)
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        userModel=get_user_model()
        try:
            user=userModel.objects.create(username=username,email=email, password=password)
        except:

            user=userModel.objects.get(email=email)
            if user.is_active==False:
                message="Account not activated"
                return render(request, self.template, {'message':message})
            else:
                message="Account Exists"
                return render(request, self.template, {'message':message})
            
        user.is_active=False # The users account is not yet verified
        user.save()


        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        current_site = get_current_site(request)
        confirmation_url = reverse('activate_account', kwargs={'uidb64':uidb64 , 'token': token})
        activation_link = f'http://{current_site.domain}{confirmation_url}'
        email_subject = 'Activate Your Account'
        email_body = f'Please click the following link to activate your account: {activation_link}'
        email = EmailMessage(email_subject, email_body, to=[email])
        email.send()  
         
        return render(request, 'auth/activation_email.html',{'uidb64':uidb64, 
                                                             'token':token})

class ActivateAccount(View):
    def validate_user_token(self, uidb64, token):
        try:
            userPk_bytes=urlsafe_base64_decode(uidb64)
            user_pk= userPk_bytes.decode('utf-8')
            userModel=get_user_model()
            user=userModel.objects.get(pk=user_pk)
            if default_token_generator.check_token(user, token):
                return user.pk
            
        except Exception as e:
            return None
    
    def get(self,request,uidb64, token):
        user_pk=self.validate_user_token(uidb64, token)
        if user_pk:
            print(user_pk)
            userModel=get_user_model()
            user=userModel.objects.get(pk=user_pk)
            user.is_active=True
            user.save()
            return render(request, 'auth/activate_account.html')
        else:
            return HttpResponse('wahala')

    

class CustomLoginView(LoginView):
    template_name="auth/login.html"
    
    def get_success_url(self) -> str:
        return  reverse('dashboard')
    
class DashboardTemplateView(TemplateView):
    template_name="auth/dashboard.html"
    
