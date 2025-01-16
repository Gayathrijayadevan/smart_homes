from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
from django.contrib.auth.models import User
import os
from django.conf import settings
import razorpay
import json
from django.views.decorators.csrf import csrf_exempt


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
    return redirect(user_home)
#--------------------admin----------------------
def admin_home(req):
    #     data=Product.objects.all()
    return render(req,'admin/ad_home.html')
    # else:
    #     return redirect(sm_login)
def view_users(req):
    if 'admin' in req.session:
        user=User.objects.all()
        return render(req,'admin/view_users.html',{'user':user})
    else:
        return redirect(admin_home)

def ad_viewp(req):
    categories = Category.objects.all()  
    category_products = {category: Product.objects.filter(category=category) for category in categories} 
    return render(req, 'admin/view_pro.html', {'nav_cat': categories, 'category_products': category_products})
    
def ad_pro_dtls(req,pid):
    pro_dtl=Product.objects.get(pk=pid)
    feedbacks = Feedback.objects.filter(product=pro_dtl).order_by('-submitted_at')

    data=pro_dtl.des.split('Product Features')
    des=data[0]
    fet=data[-1]
    split_data=fet.split('\n')
    split_data=[i for i in split_data if len(i)>5]
    return render(req,'admin/pro_details.html', {'dtl':pro_dtl,'split_data':split_data,'des':des, 'feed':feedbacks})

def add_products(req) :
    if 'admin' in req.session:
        if req.method=='POST':
            pid=req.POST['pid']
            pname=req.POST['name']
            des=req.POST['descrip']
            pprice=req.POST['price']
            oprice=req.POST['off_price']
            cate=req.POST['category']
            brand=req.POST['brand']
            dimension=req.POST['dimen']
            wei=req.POST['weight']
            pstock=req.POST['stock']
            file=req.FILES['img']
            cat=Category.objects.get(pk=cate)
            data=Product.objects.create(pid=pid,name=pname,des=des,price=pprice,offer_price=oprice,category=cat,brand=brand,dimension=dimension,weight=wei,stock=pstock,img=file)
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
        cate_id = req.POST['category']  # Retrieve category ID from the form
        brand = req.POST['brand']
        dimension = req.POST['dimen']
        wei = req.POST['weight']
        pstock = req.POST['stock']
        file = req.FILES.get('img')

        product = Product.objects.get(pk=pid)

        # Update fields
        product.pid = proid
        product.name = pname
        product.des = des
        product.price = pprice
        product.offer_price = oprice
        product.brand = brand
        product.dimension = dimension
        product.weight = wei
        product.stock = pstock
        product.category = Category.objects.get(id=cate_id)  # Use ID to get the category
        
        if file:
            product.img = file
        
        product.save()
        return redirect(admin_home)
    else:
        cate = Category.objects.all()
        data = Product.objects.get(pk=pid)
        return render(req, 'admin/edit_pro.html', {'data': data, 'cate': cate})


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

def view_bookings(req):
    buy=Buy.objects.all()[::-1]
    return render( req,'admin/user_bookings.html',{'booking':buy})

def view_vists(req):
    visit=Schedule.objects.all()
    return render(req,'admin/view_vists.html',{'data':visit})

#-------------user------------------------------
def user_home(req):
    categories = Category.objects.all()
    user = None
    if 'user' in req.session:
        user = User.objects.get(username=req.session['user'])
    return render(req, 'user/user_home.html', {'nav_cat': categories, 'dtls': user})

# def user_profile(req):
#     if 'user' in req.session:
#         user = User.objects.get(username=req.session['user'])
#         return render(req, 'user/user_home.html', {'dtls': user, 'nav_cat': Category.objects.all()})
#     else:
#         return redirect(user_home)


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
    categories = Category.objects.all()
    user = None
    if 'user' in req.session:
        user = User.objects.get(username=req.session['user'])
    return render(req,'user/about.html',{'nav_cat':categories,'dtls':user})

def contact(req) :
    categories=Category.objects.all()
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
    user = None    
    if 'user' in req.session:        
        user=User.objects.get(username=req.session['user'])
    else:
        return redirect(sm_login)  
    return render(req,'user/contact.html',{'nav_cat':categories,'dtls':user})
    
def store(req):
    if req.method == 'POST':
        search = req.POST['searches']
        if search:
            product = Product.objects.filter(brand=search) | Product.objects.filter(name=search)
            print(product)
            # Check if the query returned any results
            if product.exists():
                return render(req, 'user/search_result.html', {'pro': product})
            else:
                # If no results found, pass a message to the template
                return render(req, 'user/search_result.html', {
                    'pro': None,
                    'no_results': True,
                    'search_term': search
                })
    else:
        categories = Category.objects.all()
        category_products = {category: Product.objects.filter(category=category) for category in categories}
        return render(req, 'user/store.html', {'nav_cat': categories, 'category_products': category_products})
    
def view_pro_dtls(req, pid):
    if 'user' in req.session:
    # try:
        pro_dtl = Product.objects.get(pk=pid)
        
        # Handle form submission
        if req.method == 'POST':
            # try:
                user = User.objects.get(username=req.session['user'])
                
                # Check if user has already reviewed this product
                existing_feedback = Feedback.objects.filter(user=user, product=pro_dtl).exists()
                if existing_feedback:
                    messages.error(req, 'You have already reviewed this product.')
                    return redirect('view_pro_dtls', pid=pid)
                
                message = req.POST['message']
                rating = req.POST['rating']
                
                feedback = Feedback.objects.create(
                    user=user,
                    product=pro_dtl,
                    message=message,
                    rating=rating,
                )
                messages.success(req, 'Thank you for your feedback!')
                return redirect('view_pro_dtls', pid=pid)
            # except Exception as e:
            #     messages.error(req, 'Error submitting feedback. Please try again.')
            #     return redirect('view_pro_dtls', pid=pid)
        
        # Process product description
        data = pro_dtl.des.split('Product Features')
        des = data[0]
        fet = data[-1]
        split_data = [i for i in fet.split('\n') if len(i)>5]
        
        # Get all feedback for this specific product
        feedbacks = Feedback.objects.filter(product=pro_dtl).order_by('-submitted_at')
        
        # Check if current user has already reviewed
        user = User.objects.get(username=req.session['user'])
        user_has_reviewed = Feedback.objects.filter(user=user, product=pro_dtl).exists()
        
        context = {
            'dtl': pro_dtl,
            'split_data': split_data,
            'des': des,
            'feedbacks': feedbacks,
            'user_has_reviewed': user_has_reviewed
        }
        
        return render(req, 'user/product_dtls.html', context)
    else:
        return redirect(sm_login)
        
    # except Product.DoesNotExist:
    #     messages.error(req, 'Product not found.')
    #     return redirect(user_home)  
    # except Exception as e:
    #     messages.error(req, 'An error occurred. Please try again.')
    #     return redirect(user_home)  
    
def cart(req):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        data=Cart.objects.filter(user=user)
        return render(req,'user/cart.html',{'cart':data})
    else:
        return redirect(sm_login)

def qty_in(req, cid):
    data = Cart.objects.get(pk=cid)
    if data.qty < data.product.stock:
        data.qty += 1
        data.save()
    else:
        messages.warning(req, "You cannot add more than the available stock.")
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

def bookings(req):
    if 'user' in req.session:
        buy=Buy.objects.all()
        return render(req,'user/bookings.html',{'orders':buy})
    else:
        return redirect(sm_login)

def remove_order(req,oid):
    data=Buy.objects.get(pk=oid)
    data.delete()
    return redirect(bookings)

def order(req,pid):
    user = User.objects.get(username=req.session['user'])  

    try:
        detail = User_details.objects.get(user=user)
    except User_details.DoesNotExist:
        detail = None

    if req.method == 'POST':
        address = req.POST['address']
        phone = req.POST['phone']
        pincode = req.POST['pincode']
        state = req.POST['state']
        country = req.POST['country']

        if detail:
            detail.address = address
            detail.phone = phone
            detail.pincode = pincode
            detail.state = state
            detail.country = country
            detail.save()
        else:
            User_details.objects.create(
                user=user,
                address=address,
                phone=phone,
                pincode=pincode,
                state=state,
                country=country,
            )
        return redirect('pay',pid=pid)

    return render(req, 'user/order_details.html', {'detls': detail})

def payment(req, pid):
    if req.method == 'POST':
        payment = req.POST.get('payment_method')
        print(payment)
        if payment=='online':
            product = Product.objects.get(pk=pid)
            user=User.objects.get(username=req.session['user'])  
            pro=product.offer_price
            print(pro)
            
            req.session['payment_data'] = {
                'payment_method': payment,
                'product_id': pid,
            }

            name='anadhu'
            amount='3000'
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            razorpay_order = client.order.create(
            {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
                )
            order_id=razorpay_order['id']
            order = Order.objects.create(
            name=name, amount=amount, provider_order_id=order_id
                )
            order.save()
            return render(
                    req,
                    "user/online_pay.html",
                    {
                        "callback_url": "http://" + "127.0.0.1:8000" + "razorpay/callback",
                        "razorpay_key": settings.RAZORPAY_KEY_ID,
                        "order": order,
                        "product":product ,
                        "user":user
                    },
                )
    
    return render(req, 'user/payment.html', {'pid': pid})

@csrf_exempt
def callback(request):
    def verify_signature(response_data):
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)

    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id
        order.save()
        if not verify_signature(request.POST):
            order.status = PaymentStatus.SUCCESS
            order.save()
            return render(request, "callback.html", context={"status": order.status})   # callback giving html page
            #  or  return redirect(function name of callback giving html page)
        else:
            order.status = PaymentStatus.FAILURE
            order.save()
            return render(request, "callback.html", context={"status": order.status})  # callback giving html page
            #  or  return redirect(function name of callback giving html page)

    else:
        payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
            "order_id"
        )
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.status = PaymentStatus.FAILURE
        order.save()
        return render(request, "callback.html", context={"status": order.status})  # callback giving html page
        #  or  return redirect(function name of callback giving html page)




def pro_buy(req):
    payment_data = req.session.get('payment_data', {})
    print(payment_data)
    if payment_data:
        # try:
            payment_method = payment_data['payment_method']
            product_id = payment_data['product_id']
            print(payment_method,product_id)
            
            product = Product.objects.get(pk=product_id)
            user = User.objects.get(username=req.session['user'])
            user_dtl=User_details.objects.get(user=user)
            
            buy = Buy.objects.create(
                product=product,
                user=user_dtl,
                qty=1,
                price=product.offer_price,
                payment_method=payment_method
            )
            buy.save()
            # Clear the session data
            del req.session['payment_data']
            
            return redirect('store')
            
        # except Exception as e:
        #     print(f"Error in pro_buy: {e}")
        #     return redirect('store')
    
    return redirect('store')


def visit(req):
    if 'user' in req.session:
        if req.method == 'POST':
            name = req.POST.get('name')
            email = req.POST.get('email')
            phone = req.POST.get('phone')
            time = req.POST.get('time')
            date=req.POST.get('date')
            data=Schedule.objects.create(name=name,email=email,Phone=phone,date=date,time=time)
            data.save()
            return render(req,'user/user_home.html')
        else:    
          return render(req,'user/schedule.html')
    else:
        return redirect(sm_login)
