from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
import gettext
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login as signin
from .models import Contact
from .forms import UserUpdateForm,ProfileUpdateForm
import warnings
from urllib3.exceptions import InsecureRequestWarning
from .models import sp_product
from django.views.decorators.csrf import csrf_protect
from .utils import extract_product_data, compare_clothing_products, SHOP1_URL, SHOP2_URL,extract_products_by_category


warnings.filterwarnings('ignore', category=InsecureRequestWarning)
# from .forms import ProfileForm

# Create your views here.
def index(request):
    products = sp_product.objects.all()
    
    context={
        'product':products,
        
    }
    return render(request,"index.html",context)
def products(request):
    return render(request,"products.html")
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.info(request,'You logged Out')
    return redirect('/')
@csrf_protect
def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['pwd']

        user = authenticate(username= username , password = password)

        if user is not None:
            # signin(request,user)
            auth.login(request,user)
            messages.info(request,"You logged in")
            return render(request, 'index.html')
        else:
            messages.error(request, "Bad credentials")
            return redirect('login')
    return render(request, 'login.html')
def register(request): 
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        email_condition = r"^[a-z]+[\._]?[a-z0-9]+[@]\w+\.\w{2,3}$"
        password = request.POST['pwd']
        r_password = request.POST['r_pwd']

        if User.objects.filter(username = username):
            messages.error(request, "User already exists! Please try any other username")
            return redirect('register')
        if User.objects.filter(email=email):
            messages.error(request, "Email already exists! Please try to signin")
        if re.search(email_condition,email):
            pass
        else:
            messages.error(request,"Enter a valid Email")
            return redirect('register')
        if password!=r_password:
            messages.error(request, "Passwords dosn't match!")
            return redirect('register')
        if len(username)>10:
            messages.error(request, 'username must be under 10 characters')
        if not username.isalnum():
            messages.error(request, 'username should only contain 0-9,A-Z,a-z')

            return redirect('register')
            

        myuser = User.objects.create_user(username, email, password)
        

        myuser.save()
        messages.info(request, "you're Account has been successfully created")    
        return redirect('login')
    return render(request, 'registration.html')

@login_required(login_url='login')
def profile(request):
    
    return render(request,'profile.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    if request.method=="POST":
        contact=Contact()
        name=request.POST.get('name')
        email=request.POST.get('email')
        number=request.POST.get('number')
        subject=request.POST.get('subject')
        msg=request.POST.get('msg')
        contact.name=name
        contact.email=email
        contact.number=number
        contact.subject=subject
        contact.message=msg
        contact.save()   
        if "contactFormSubmit" in request.POST:
            messages.info(request,"Form submitted successfully!")
    return render(request,'contact.html')


def search(request):
    if request.method == 'POST':
        category = request.POST.get('category', '').lower()
        brand1 = request.POST.get('brand1', '').lower()
        brand2 = request.POST.get('brand2', '').lower()
        keyword = request.POST.get('search', '').strip()

        if category == 'clothes' and keyword:
            products1 = extract_product_data(SHOP1_URL, keyword, category)
            products2 = extract_product_data(SHOP2_URL, keyword, category)
            matches = compare_clothing_products(products1, products2)
            context = {
                'matches': matches,
                'products1': products1,
                'products2': products2,
                'category': category
            }
            return render(request, 'search.html', context)

        elif category in ['mobiles', 'laptops'] and brand1 and brand2:
            url1 = f"{SHOP1_URL}{category}.html"
            url2 = f"{SHOP2_URL}{category}.html"
            prod1 = extract_product_data(url1, brand1, category)
            prod2 = extract_product_data(url2, brand2, category)
            context = {
                'brand1': brand1,
                'brand2': brand2,
                'category': category,
                'products1': prod1,
                'products2': prod2,
            }
            return render(request, 'select_compare.html', context)

    return render(request, 'Prnotfound.html')


def compare(request):
    if request.method == 'POST':
        category = request.POST.get('category', '')
        selected_items = request.POST.getlist('selected_products')

        product_data = []

        SHOP1_URL = "https://shop-fmsg.vercel.app/"
        SHOP2_URL = "https://shop2-mauve.vercel.app/"

        for item in selected_items:
            fields =item.split('#FIELD#')

            if len(fields) == 9:
                name, img, price, rating, specs, sentiment, final, features_raw, link = fields

            else:
                print(f"Error: Unexpected field count {len(fields)}. Data: {fields}")
                continue
            if img.strip().startswith(SHOP1_URL):
                link = f"{SHOP1_URL}{category}.html"
            else:
                link = f"{SHOP2_URL}{category}.html"
            features_cleaned = features_raw.replace('<br>', '\n').replace('<br/>', '\n').replace('<br />', '\n')
            feature_list = [f.strip() for f in features_cleaned.split('\n') if f.strip()]
            
            # Append to product data
            product_data.append({
                'name': name.strip(),
                'image': img.strip(),
                'price': price.strip(),
                'rating': rating.strip(),
                'specs_score': specs.strip(),
                'sentiment_score': sentiment.strip(),
                'final_score': final.strip(),
                'features': feature_list,
                'link': link,
            })
        # Render the comparison table
        return render(request, 'comparison_table.html', {'products': product_data, 'category': category})

    return render(request, 'Prnotfound.html')

    
def smartwatch(request):
    data1 = extract_products_by_category(SHOP1_URL, "smartwatches")
    data2 = extract_products_by_category(SHOP2_URL, "smartwatches")
    return render(request, 'smartwatch.html', {'smartwatcha': data1, 'smartwatchb': data2})

def offsmartwatch(request):
    data1 = extract_products_by_category(SHOP1_URL, "smartwatches", offer_only=True)
    data2 = extract_products_by_category(SHOP2_URL, "smartwatches", offer_only=True)
    return render(request, 'offsmartwatch.html', {'offsmartwatcha': data1, 'offsmartwatchb': data2})

def headphone(request):
    data1 = extract_products_by_category(SHOP1_URL, "headphones")
    data2 = extract_products_by_category(SHOP2_URL, "headphones")
    return render(request, 'headphone.html', {'headphonea': data1, 'headphoneb': data2})

def offheadphone(request):
    data1 = extract_products_by_category(SHOP1_URL, "headphones", offer_only=True)
    data2 = extract_products_by_category(SHOP2_URL, "headphones", offer_only=True)
    return render(request, 'offheadphone.html', {'offheadphonea': data1, 'offheadphoneb': data2})

def speaker(request):
    data1 = extract_products_by_category(SHOP1_URL, "speakers")
    data2 = extract_products_by_category(SHOP2_URL, "speakers")
    return render(request, 'speaker.html', {'speakera': data1, 'speakerb': data2})

def offspeaker(request):
    data1 = extract_products_by_category(SHOP1_URL, "speakers", offer_only=True)
    data2 = extract_products_by_category(SHOP2_URL, "speakers", offer_only=True)
    return render(request, 'offspeaker.html', {'offspeakera': data1, 'offspeakerb': data2})
def camera(request):
    data1 = extract_products_by_category(SHOP1_URL, "camera")
    data2 = extract_products_by_category(SHOP2_URL, "camera")
    return render(request, 'camera.html', {'cameraa': data1, 'camerab': data2})
def television(request):
    data1 = extract_products_by_category(SHOP1_URL, "television")
    data2 = extract_products_by_category(SHOP2_URL, "television")
    return render(request, 'television.html', {'televisiona': data1, 'televisionb': data2})