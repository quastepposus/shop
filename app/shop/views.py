from urllib.parse import urlencode

from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View

from shop.forms import ProductForm, SearchForm, OrderForm
from shop.models import Product, ShoppingCart, Order, ShoppingCartForOrder

categories = ['Drinks', 'Meat', 'Frozen', 'Food', 'Drinks']


class ProductListView(ListView):
    template_name = 'products.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 5

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.search_value = None
        self.form = None

    def post(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        count = Q(count__gt=1)
        if self.search_value:
            query = Q(title__icontains=self.search_value) | Q(description__icontains=self.search_value) & count
        else:
            query = count
        queryset = queryset.filter(query).order_by('title', 'category')

        return queryset

    def get_search_form(self):
        return SearchForm(self.request.POST)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']

        return None


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'product'

class ProductCreateView(CreateView):
    template_name = 'add_product.html'
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse('product', kwargs={'pk': self.object.pk})

class ProductUpdateView(UpdateView):
    template_name = 'edit_product.html'
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse('product', kwargs={'pk': self.object.pk})

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product_confirm_delete.html'

    def get_success_url(self):
        return reverse('products')

class ShoppingCartListView(ListView):
    model = ShoppingCart
    template_name = 'basket.html'
    context_object_name = 'shopping_cart'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_deleted=False)
        return queryset


class ShoppingCartAddProductView(View):
    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        shoppingcart_product = ShoppingCart.objects.filter(product_id=self.kwargs['pk']).first()
        if shoppingcart_product:
            if not shoppingcart_product.is_deleted:
                shoppingcart_product.count = shoppingcart_product.count + 1
                shoppingcart_product.total = shoppingcart_product.product.price * shoppingcart_product.count
                shoppingcart_product.save()
            else:
                ShoppingCart.total = product.price
                shoppingcart_product.count = 1
                shoppingcart_product.is_deleted = False
                shoppingcart_product.save()
        else:
            product = get_object_or_404(Product, pk=self.kwargs['pk'])
            ShoppingCart.objects.create(product_id=self.kwargs['pk'], count=1, total=product.price)

        return redirect('shopping_cart')

class ShoppingCartProductDeleteView(DeleteView):
    model = ShoppingCart
    template_name = 'basket.html'

    def get_success_url(self):
        return reverse('shopping_cart')

class OrderCreateView(CreateView):
    model = Order
    template_name = 'order.html'
    form_class = OrderForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shopping_cart'] = ShoppingCart.objects.all()

        total = 0
        for product in context['shopping_cart']:
            product_total = product.product.price * product.count
            total += product_total
        context['total'] = total
        return context

    def get_success_url(self):
        return reverse('shopping_cart')

    # def form_valid(self, form):
    #     products = ShoppingCart.objects.all()
    #     self.form = self.get_form()
    #
    #     for product in products:
    #         ShoppingCartForOrder.objects.create(product_id=product.pk, order_id=order.pk)
    #
    #     return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            products = ShoppingCart.objects.all()
            order = instance

            for product in products:
                ShoppingCartForOrder.objects.create(product_id=product.pk, order_id=order.pk)
                product.is_deleted = True
                product.save()

            return HttpResponseRedirect(reverse('shopping_cart'))
        return self.form_invalid(form)
