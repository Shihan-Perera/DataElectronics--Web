"""DataElectronics URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from pos import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    #pos urls
    path('', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),

    #inventory
    path('inventory/', views.StockListView.as_view(), name='inventory'),
    path('new/', views.StockCreateView.as_view(), name='new-stock'),
    path('stock/<pk>/edit', views.StockUpdateView.as_view(), name='edit-stock'),
    path('stock/<pk>/delete', views.StockDeleteView.as_view(), name='delete-stock'),

    #Purchase
    path('purchases/', views.PurchaseView.as_view(), name='purchases-list'),
    path('purchases/new', views.SelectSupplierView.as_view(), name='select-supplier'),
    path('purchases/new/<pk>', views.PurchaseCreateView.as_view(), name='new-purchase'),
    path('purchases/<pk>/delete', views.PurchaseDeleteView.as_view(), name='delete-purchase'),
    path("purchases/<billno>", views.PurchaseBillView.as_view(), name="purchase-bill"),


    #Supplier
    path('suppliers/new', views.SupplierCreateView.as_view(), name='new-supplier'),
    path('suppliers/', views.SupplierListView.as_view(), name='suppliers-list'),
    path('suppliers/<pk>/edit', views.SupplierUpdateView.as_view(), name='edit-supplier'),
    path('suppliers/<pk>/delete', views.SupplierDeleteView.as_view(), name='delete-supplier'),
    path('suppliers/<name>', views.SupplierView.as_view(), name='supplier'),


    #SaleBill
    path('sales/', views.SaleView.as_view(), name='sales-list'),
    path('sales/new', views.SaleCreateView.as_view(), name='new-sale'),
    path('sales/<pk>/delete', views.SaleDeleteView.as_view(), name='delete-sale'),
    path("sales/<billno>", views.SaleBillView.as_view(), name="sale-bill"),

    #Employee
    path('employee/new', views.EmployeeCreateView.as_view(), name='new-employee'),
    path('employees/', views.EmployeeListView.as_view(), name='employees-list'),
    path('employees/<pk>/edit', views.EmployeeUpdateView.as_view(), name='edit-employee'),
    path('employees/<pk>/delete', views.EmployeeDeleteView.as_view(), name='delete-employee'),
    path('employee/<name>', views.EmployeerView.as_view(), name='employee'),


    #Payroll
    path('attendence/today', views.AttendenceMarkView, name='today-attendence'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
