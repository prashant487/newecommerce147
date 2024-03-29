from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import *
from django.core.mail import EmailMultiAlternatives
# Create your views here.

from django.views.generic.base import View


class BaseView(View):
    views = {}


class HomeVIew(BaseView):
    def get(self, request):
        self.views['categories'] = Categorie.objects.all()
        self.views['brands'] = Brand.objects.all()
        self.views['sliders'] = Slider.objects.all()
        self.views['ads1'] = Ad.objects.filter(rank=1)
        self.views['ads2'] = Ad.objects.filter(rank=2)
        self.views['ads3'] = Ad.objects.filter(rank=3)
        self.views['ads4'] = Ad.objects.filter(rank=4)
        self.views['ads5'] = Ad.objects.filter(rank=5)
        self.views['ads6'] = Ad.objects.filter(rank=6)
        self.views['ads7'] = Ad.objects.filter(rank=7)
        self.views['ads8'] = Ad.objects.filter(rank=8)

        self.views['items'] = Item.objects.all()
        self.views['new_items'] = Item.objects.filter(label='new')
        self.views['hot_items'] = Item.objects.filter(label='hot')
        self.views['sale_items'] = Item.objects.filter(label='sale')
        return render(request, 'index.html', self.views)


class ProductDetailView(BaseView):
    def get(self, request, slug):
        category = Item.objects.get(slug=slug).category
        self.views['detail_item'] = Item.objects.filter(slug=slug)
        self.views['categories'] = Categorie.objects.all()
        self.views['related_product'] = Item.objects.filter(category=category)
        return render(request, 'product-detail.html', self.views)


class SearchView(BaseView):
    def get(self, request):
        query = request.GET.get('query', None)
        if not query:
            return redirect("/")
        self.views['search_query'] = Item.objects.filter(
            description__icontains=query,
        )
        self.views['searched_for'] = query
        return render(request, 'search.html', self.views)


class CategoryView(BaseView):
    def get(self, request, slug):
        cat = Categorie.objects.get(slug=slug).id
        self.views['category_item'] = Item.objects.filter(category=cat)

        return render(request, 'category.html', self.views)


class BrandView(BaseView):
    def get(self, request, name):
        cat = Brand.objects.get(name=name).id
        self.views['brand_item'] = Item.objects.filter(brand=cat)

        return render(request, 'brand.html', self.views)


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'The username is already used.')
                return redirect('home:signup')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'This email is already used.')
                return redirect('home:signup')
            else:
                data = User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    password=password,
                )
                data.save()
                messages.error(request, 'You are signed up.')
                return redirect('home:signup')
        else:
            messages.error(request, 'Password does not match to each other.')
            return redirect('home:signup')

    return render(request, 'signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.error(request, 'logged in')
            return redirect('/')
        else:
            messages.error(request, 'Username and password do not match.')
            return redirect('home:signin')
    return render(request, 'signin.html')


class ViewCart(BaseView):
    def get(self, request):
        self.views['carts'] = Cart.objects.filter(user=request.user.username)
        return render(request, 'cart.html', self.views)


def cart(request, slug):
    if Cart.objects.filter(slug=slug, user=request.user.username).exists():
        quantity = Cart.objects.get(slug=slug, user=request.user.username).quantity
        quantity = quantity + 1
        price = Item.objects.get(slug=slug).price
        discounted_price = Item.objects.get(slug=slug).discounted_price
        if discounted_price > 0:
            total = discounted_price * quantity
        else:
            total = price * quantity
        Cart.objects.filter(slug=slug, user=request.user.username).update(quantity=quantity, total=total)

    else:
        price = Item.objects.get(slug=slug).price
        discounted_price = Item.objects.get(slug=slug).discounted_price
        if discounted_price > 0:
            total = discounted_price
        else:
            total = price
        data = Cart.objects.create(
            user=request.user.username,
            slug=slug,
            item=Item.objects.filter(slug=slug)[0],
            total=total
        )
        data.save()
    return redirect('home:mycart')


def deletecart(request, slug):
    if Cart.objects.filter(slug=slug, user=request.user.username).exists():
        Cart.objects.filter(slug=slug, user=request.user.username).delete()
        messages.success(request, 'The item is deleted')

    return redirect('home:mycart')


def minusitem(request, slug):
    if Cart.objects.get(slug=slug, user=request.user.username).quantity > 1:
        quantity = Cart.objects.get(slug=slug, user=request.user.username).quantity
        quantity = quantity - 1
        price = Item.objects.get(slug=slug).price
        discounted_price = Item.objects.get(slug=slug).discounted_price
        if discounted_price > 0:
            total = discounted_price * quantity
        else:
            total = price * quantity
        Cart.objects.filter(slug=slug, user=request.user.username).update(quantity=quantity, total=total)
    elif Cart.objects.get(slug=slug, user=request.user.username).quantity == 1:
        Cart.objects.filter(slug=slug, user=request.user.username).delete()
        messages.success(request, 'The item is deleted.')
    return redirect('home:mycart')


def grand_total(request, slug):
    for citem in Cart.objects.filter(user=request.user.username).total:
        subtotal = subtotal + citem
    return redirect('home:mycart')


def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        data = Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        data.save()
        messages.success(request, 'Message is submitted.')
        html_content = f"<p> The customer having name {name} , mail address {email} and subject (subject) has some , message and the message is {message} "
        msg = EmailMultiAlternatives(subject, message, 'kushwahaprashant165@gmail.com',
                                     ['kushwahaprashant165@gmail.com'])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    return render(request, 'contact.html')




from rest_framework import viewsets
from .serializers import *


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


from django.views.generic import View, DetailView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter, SearchFilter


class ItemFilterListView(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_fields = ['id', 'title', 'price', 'label', 'category']
    ordering_fields = ['price', 'title', 'id']
    search_fields = ['title', 'description']












































































































