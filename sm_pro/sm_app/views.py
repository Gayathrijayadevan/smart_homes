from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
from django.contrib.auth.models import User
import os

# Create your views here.
def sm_login(req):
        if 'admin' in req.session:
            return redirect(admin_home)
        if 'user' in req.session:
            return redirect(user_home)
        if req.method=='POST':
            uname=req.POST['uname']
            password=req.POST['password']
            data=authenticate(username=uname,password=password)
            if data:
                login(req,data)
                if data.is_superuser:
                    req.session['admin']=uname 
                    return redirect(admin_home)
                else:
                    req.session['user']=uname 
                    return redirect(user_home)
            else:
                messages.warning(req,'invalid username or password')
                return redirect(sm_login)  
        else:
            return render(req,'login.html')

def sm_logout(req):
    logout(req)
    req.session.flush() 
    return redirect(sm_login)
#--------------------admin----------------------
def admin_home(req):
    if 'admin' in req.session:
        data=Product.objects.all()
        return render(req,'admin/ad_home.html',{'Products':data})
    else:
        return redirect(sm_login)

def add_products(req) :
    if 'admin' in req.session:
        if req.method=='POST':
            pid=req.POST['pid']
            pname=req.POST['name']
            des=req.POST['descrip']
            pprice=req.POST['price']
            oprice=req.POST['off_price']
            cate=req.POST['category']
            pstock=req.POST['stock']
            file=req.FILES['img']
            cat=Category.objects.get(pk=cate)
            data=Product.objects.create(pid=pid,name=pname,des=des,price=pprice,offer_price=oprice,categorie=cat,stock=pstock,img=file)
            data.save()
            return redirect(admin_home)
        else:
            cate=Category.objects.all()
            return render(req,'admin/add_pro.html',{'cate':cate})
    else:
        return redirect(sm_login)    
    
def edit_product(req,pid) :
        if req.method=='POST':
            proid=req.POST['proid']
            pname=req.POST['name']
            des=req.POST['descrip']
            pprice=req.POST['price']
            oprice=req.POST['off_price']
            cate=req.POST['Category']
            pstock=req.POST['stock']
            file=req.FILES.get('img')
            if file:
                Product.objects.filter(pk=pid).update(pid=proid,name=pname,des=des,price=pprice,offer_price=oprice,categorie=cate,stock=pstock,img=file)
                data=Product.objects.get(pk=pid)
                data.img=file
                data.save()
            else:  
                Product.objects.filter(pk=pid).update(pid=pid,name=pname,des=des,price=pprice,offer_price=oprice,stock=pstock,img=file)
            return redirect(admin_home)
        else:
            data=Product.objects.get(pk=pid)
            return render(req,'admin/edit_pro.html',{'data':data})

def delete_product(req,pid):
    data=Product.objects.get(pk=pid)
    file=data.img.url
    file=file.split('/')[-1]
    os.remove('media/'+file)
    data.delete()
    return redirect(admin_home)    

def add_category(req):
    if 'admin' in req.session:
        if req.method=='POST':
            c_name=req.POST['cate_name']
            c_name=c_name.lower()
            try:
                cate=Category.objects.get(Category_name=c_name)
            except:
                data=Category.objects.create(Category_name=c_name)
                data.save()
            return redirect(add_category)
        categories=Category.objects.all()
        return render(req,'admin/cate.html' ,{'cate':categories})
    else:
        return render(admin_home)
#-------------user------------------------------
def user_home  (req)  :
    return render(req,'user/user_home.html')

def register(req):
    if req.method=='POST':
        uname=req.POST['uname']
        email=req.POST['email']
        pswd=req.POST['pswd']
        try:
            data=User.objects.create_user(first_name=uname,email=email,username=email,password=pswd)
            data.save()
        except:
            messages.warning(req,'invalid username or password')
            return redirect(register)   
        return redirect(sm_login) 
    else:
        return render(req,'user/register.html') 
    
def about(req) :
    return render(req,'user/about.html')
def contact(req) :
    return render(req,'user/contact.html')
def store(req):
    return render(req,'user/store.html')