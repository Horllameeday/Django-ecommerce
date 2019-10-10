from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from .forms import *
from .models import *
import random
import string

# Create your views here.

class IndexView(ListView):
    model = Item
    template_name = "core/index.html"
    context_object_name = 'item_list'

    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({'category_list': Category.objects.all()})
        return context
    
    def get_queryset(self):
        return Item.objects.all()

class CartView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            return render(self.request, "core/cart.html", {'object': order})
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("core:index")

class DetailView(DetailView):
    model = Item
    template_name = "core/single.html"

class OptionView(View):
    def get(self, *args, **kwargs):
        form = OptionForm()
        return render(self.request, "core/option.html", {'form': form})

    def post(self, *args, **kwargs):
        form = OptionForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                payment_option = form.cleaned_data.get('payment_option')

                if payment_option == "C":
                    return redirect('core:cash-checkout')
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("core:cart")

class CashCheckoutView(View):
    def get(self, *args, **kwargs):
        form = CashCheckoutForm()
        return render(self.request, "core/cash-checkout.html", {'form': form})

    def post(self, *args, **kwargs):
        form = CashCheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                address = form.cleaned_data.get('address')
                phone_number = form.cleaned_data.get('phone_number')
                address = Address(
                    user=self.request.user,
                    address=address,
                    phone_number=phone_number
                )
                address.save()
                order.order_address = address
                order.ordered = True
                order.ref_code = create_ref_code() 
                order.save()
                return redirect('core:index')
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("core:cart")

@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk=item.pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated")
            return redirect("core:cart")
        else:
            messages.info(request, "This item was added to your cart")
            order.items.add(order_item)
            return redirect("core:cart")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart")
        return redirect("core:cart")
    return redirect("core:cart")

@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            order.items.remove(order_item)
            messages.info(request, "This item was removed from your cart")
            return redirect("core:detail", pk=pk)
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:index", pk=pk)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:index", pk=pk)

@login_required
def remove_single_item_from_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item was quantity was updated")
            return redirect("core:cart")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:cart")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:cart") 

def create_ref_code():
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=20))

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("core:index")
    else:
        form = SignupForm()
    return render(request, 'core/signup.html', {'form': form})