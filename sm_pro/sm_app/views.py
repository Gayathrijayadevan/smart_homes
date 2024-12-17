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
    # if 'admin' in req.session:
    #     data=Product.objects.all()
    return render(req,'admin/ad_home.html')
    # else:
    #     return redirect(sm_login)

def ad_viewp(req):
    data=Category.objects.get(Category_name='lighting')
    lighting=Product.objects.filter(category=data)

    data=Category.objects.get(Category_name='multimedia')
    multimedia=Product.objects.filter(category=data)

    data=Category.objects.get(Category_name='home appliances')
    home_applia=Product.objects.filter(category=data)

    return render(req,'admin/view_pro.html',{'light':lighting, 'multimedia':multimedia,'homeapp':home_applia})

def ad_pro_dtls(req,pid):
    pro_dtl=Product.objects.get(pk=pid)

    data=pro_dtl.des.split('Product Features')
    des=data[0]
    fet=data[-1]
    split_data=fet.split('\n')
    split_data=[i for i in split_data if len(i)>5]
    return render(req,'admin/pro_details.html', {'dtl':pro_dtl,'split_data':split_data,'des':des})

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
    
def edit_product(req, pid):
    if req.method == 'POST':
        proid = req.POST['proid']
        pname = req.POST['name']
        des = req.POST['descrip']
        pprice = req.POST['price']
        oprice = req.POST['off_price']
        cate = req.POST['Category']
        pstock = req.POST['stock']
        file = req.FILES.get('img')
        
        product = Product.objects.get(pk=pid)

        # Update fields with the new values
        product.pid = proid
        product.name = pname
        product.des = des
        product.price = pprice
        product.offer_price = oprice
        product.stock = pstock
        product.category = Category.objects.get(Category_name=cate) 
        
        if file:
            product.img = file
        
        product.save()
        return redirect(admin_home)
    else:
        cate=Category.objects.all()
        data = Product.objects.get(pk=pid)
        return render(req, 'admin/edit_pro.html', {'data': data,'cate':cate})


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
        return render(req,'admin\cate.html')
    
def enquire(req):
    enq=Enquire.objects.all()    
    return render(req,'admin/u_enquire.html' ,{'enquri':enq})

#-------------user------------------------------
def user_home  (req)  :
    categories=Category.objects.all()
    return render(req,'user/user_home.html',{'nav_cat':categories})

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
    categories=Category.objects.all()
    return render(req,'user/about.html',{'nav_cat':categories})

def contact(req) :
    if 'user' in req.session:
        if req.method=='POST':
            print(req.POST)
            name=req.POST['fullname']
            email=req.POST['email']
            phone=req.POST['phone']
            prod=req.POST['e_pro']
            brand=req.POST['e_brand']
            enqu=req.POST['enqri']
            data=Enquire.objects.create(name=name,email=email,product=prod,Phone=phone,brand=brand,enq=enqu)
            data.save()
            print('data saved')
        categories=Category.objects.all()
        return render(req,'user/contact.html',{'nav_cat':categories})
    else:
        return redirect(user_home)  
    
def store(req):
 if req.method=='POST':
    search=req.POST['searches']
    if search:
        product=Product.objects.filter(brand=search)|Product.objects.filter(name=search)
        print(product)
        return render(req,'user/search_result.html',{'pro':product})
 else:
        categories=Category.objects.all()

        data=Category.objects.get(Category_name='lighting')
        lighting=Product.objects.filter(category=data)

        data=Category.objects.get(Category_name='multimedia')
        multimedia=Product.objects.filter(category=data)

        data=Category.objects.get(Category_name='home appliances')
        home_applia=Product.objects.filter(category=data)

        return render(req,'user/store.html',{ 'nav_cat':categories,'light':lighting, 'multimedia':multimedia,'homeapp':home_applia})
    
    
def view_pro_dtls(req,pid):
    pro_dtl=Product.objects.get(pk=pid)

    data=pro_dtl.des.split('Product Features')
    des=data[0]
    fet=data[-1]
    split_data=fet.split('\n')
    split_data=[i for i in split_data if len(i)>5]
    print(split_data)
    return render(req,'user/product_dtls.html', {'dtl':pro_dtl,'split_data':split_data,'des':des})

def cart(req):
    user=User.objects.get(username=req.session['user'])
    data=Cart.objects.filter(user=user)
    return render(req,'user/cart.html',{'cart':data})

def qty_in(req,cid):
    data=Cart.objects.get(pk=cid)
    data.qty+=1
    data.save()
    return redirect(cart)

def qty_dec(req,cid):
    data=Cart.objects.get(pk=cid)
    data.qty-=1
    data.save()
    print(data.qty)
    if data.qty==0:
        data.delete()
    return redirect(cart)

def remove_pro(req,cid):
    data=Cart.objects.get(pk=cid)
    data.delete()
    return redirect(store)

def add_to_cart(req,pid):
    product=Product.objects.get(pk=pid)   
    user=User.objects.get(username=req.session['user'])
    try:
        cart=Cart.objects.get(user=user,product=product)
        cart.qty+=1
        cart.save()
    except:    
        data=Cart.objects.create(product=product,user=user,qty=1)
        data.save()
    return redirect(store)