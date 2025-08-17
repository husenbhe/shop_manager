
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Product, Sale
from .forms import ProductForm, SaleForm
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


@login_required
def dashboard(request):
    total_products = Product.objects.count()
    total_stock = Product.objects.aggregate(total=Sum('stock'))['total'] or 0
    total_sales = Sale.objects.count()
    recent_sales = Sale.objects.select_related('product').order_by('-date')[:10]
    low_products = Product.objects.filter(stock__lte=5)

    context = {
        'total_products': total_products,
        'total_stock': total_stock,
        'total_sales': total_sales,
        'recent_sales': recent_sales,
        'low_products': low_products,
    }
    return render(request, 'inventory/dashboard.html', context)

@login_required
def product_list(request):
    q = request.GET.get('q')
    if q:
        products = Product.objects.filter(name__icontains=q)
    else:
        products = Product.objects.all().order_by('name')
    return render(request, 'inventory/product_list.html', {'products': products})

@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('inventory:product_list')
    else:
        form = ProductForm()
    return render(request, 'inventory/product_form.html', {'form': form, 'title': 'Add Product'})

@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('inventory:product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'inventory/product_form.html', {'form': form, 'title': 'Edit Product'})

@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('inventory:product_list')
    return render(request, 'inventory/product_form.html', {'product': product, 'confirm_delete': True})

@login_required
def sale_create(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save()
            product = sale.product
            product.stock = max(0, product.stock - sale.quantity)
            product.save()
            return redirect('inventory:dashboard')
    else:
        form = SaleForm()
    return render(request, 'inventory/sale_form.html', {'form': form})

@login_required
def scanner(request):
    return render(request, 'inventory/scan.html')

@login_required
def invoice_pdf(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="invoice_{pk}.pdf"'
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Header
    p.setFont("Helvetica-Bold", 16)
    p.drawString(40, height-50, "BURHANI SHOP — INVOICE")
    p.setFont("Helvetica", 10)
    p.drawString(40, height-70, "Address line 1")
    p.drawString(40, height-85, "Phone: +91-00000-00000")

    # Body
    y = height - 130
    p.setFont("Helvetica", 12)
    p.drawString(40, y, f"Invoice #: {pk}")
    p.drawString(300, y, f"Date: {sale.date.strftime('%Y-%m-%d %H:%M')}")
    y -= 30
    p.setFont("Helvetica-Bold", 12)
    p.drawString(40, y, "Product")
    p.drawString(300, y, "Qty")
    p.drawString(360, y, "Unit Price")
    p.drawString(460, y, "Total")
    y -= 20
    p.setFont("Helvetica", 12)
    p.drawString(40, y, sale.product.name)
    p.drawString(300, y, str(sale.quantity))
    p.drawString(360, y, f"{sale.product.selling_price}")
    total = sale.total_price()
    p.drawString(460, y, f"{total}")
    y -= 40
    p.setFont("Helvetica-Bold", 12)
    p.drawString(40, y, f"Grand Total: {total}")
    p.showPage()
    p.save()
    return response
