from django.shortcuts import render, redirect
from .models import Client, Product, Salesman, Sales

# Create your views here.

def index(request):
    return render(request, 'index.html')

def show_clients(request):
    data = Client.objects.all()
    return render(request, 'clients.html', {'data_from_client': data})

def show_client(request, id):
    client = Client.objects.get(id=id)
    return render(request, 'client.html', {'client': client})

def show_salesman(request):
    data = Salesman.objects.all()
    return render(request, 'salesman.html', {'data': data})

def show_seller(request, id):
    data = Salesman.objects.get(id=id)
    return render(request, 'seller.html', {'data': data})

def show_product(request):
    data = Product.objects.all()
    return render(request, 'product.html', {'data': data})

def show_sales(request):
    data = Sales.objects.all()
    return render(request, 'sales.html', {'data': data})

def edit_clients(request, id):
    client = Client.objects.get(id=id)
    return render(request, 'edit_clients.html', {'client': client})

def add_client(request):
    if request.method == 'POST':
        name = request.POST['user_name']
        lastname = request.POST['user_lastname']
        phone = request.POST['user_phone']
        email = request.POST['user_email']
        db = Client(name=name, lastname=lastname, phone=phone, email=email)
        db.save()
        return redirect('show_clients')
    return render(request, 'add_client.html')

def add_sale(request):
    if request.method == 'POST':
        client = Client.objects.get(id=request.POST['client'])
        seller = Salesman.objects.get(id=request.POST['seller'])
        products = Product.objects.get(id=request.POST['products'])
        sale = Sales(cash_amount=request.POST['cash'], sales_date=request.POST['date'], client=client, salesman=seller)
        product_ids = request.POST.getlist('products')
        sale.save()
        for id in product_ids:
            product = Product.objects.get(id = id)
            sale.product.add(product)
            
        return redirect('show_sales')

    context = {
        'product': Product.objects.all(),
        'clients': Client.objects.all(),
        'salesman': Salesman.objects.all()
    }
    return render(request, 'add_sale.html', context)

def show_query(request):
    product = Product.objects.all()
    salesman = Salesman.objects.all()
    if request.method == 'POST':
        choice = request.POST.get('choice')

        if choice == 'ShowAllClientsSalesman':
            clients = Sales.objects.filter(salesman=request.POST['Salesman'])
            return render(request, 'sales.html', {'data': clients})
        
        elif choice == 'ShowAllSalesInDate':
            sale = Sales.objects.filter(sales_date=request.POST['SalesDate'])
            return render(request, 'sales.html', {'data': sale})
        
        elif choice == 'ProductSellers':
            seler = Sales.objects.filter(product=request.POST['ProductSalesman'])
            for s in seler:
                print(s.product.get(id=request.POST['ProductSalesman']))
            return render(request, 'sales.html', {'data': seler})
        
        elif choice == 'ProductCustomers':
            clients = Sales.objects.filter(product=request.POST['ProductCustomer'])
            return render(request, 'sales.html', {'data': clients})

        elif choice == 'SumDate':
            day = Sales.objects.filter(sales_date=request.POST['SalesDate'])
            sum = 0
            for i in day:
                sum += i.cash_amount
            return render(request, 'sales.html', {'data': sum})
        
    return render(request, 'show_query.html', {'product': product, 'salesman': salesman})