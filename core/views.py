import random
import string

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, View
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.utils import timezone
from django.shortcuts import redirect
from django.db.models.signals import post_save
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import Item, OrderItem, Order, UserProfile, Kind, Grinch
from .forms import CheckoutForm, PaymentForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage





def home(request):
    items = Item.get_all_items().order_by('id')



    kinds = Kind.get_all_kinds()
    kindDN = request.GET.get('kind')
    if kindDN:
        items = Item.get_all_items_by_kinddn(kindDN)
    else:
        items

    grinchs = Grinch.get_all_grinchs()
    grinchID = request.GET.get('grinch')
    if grinchID:
        items = Item.get_all_items_by_grinchid(grinchID)
    else:
        items

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data('query')
            query = form.cleaned_data('catid')
            if catid == 0:
                items
            else:
                items = Item.get_all_items_by_grinchid(title_icontains=query, grinchID=catid)


    page = request.GET.get('page', 1)
    paginator = Paginator(items, 8)
    try:
       items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    data = {}
    data['items'] = items
    data['grinchs'] = grinchs
    data['kinds'] = kinds

    return render(request, 'index.html', data)





def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'order': order,
            }

            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("core:checkout")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                return redirect('core:checkout')

        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("core:order-summary")




class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"



class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")




@login_required
def remove_from_cart(request, slug):
    item=get_object_or_404(Item, slug=slug)
    order_qs=Order.objects.filter(
        user=request.user,
        ordered=False
)
    if order_qs.exists():
        order=order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item=OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
        )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)

@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("core:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("core:order-summary")


