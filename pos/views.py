from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (
    View,
    CreateView,
    UpdateView,
    ListView,
    DeleteView,
    TemplateView,
)
from .models import *
from .forms import *
from .filters import StockFilter
from django_filters.views import FilterView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime,date
from django.db.models import Sum



def login(request):
     if request.method == 'POST':
       username = request.POST['username']
       password = request.POST['password']

       user = auth.authenticate(username=username, password=password)

       if user is not None:
         auth.login(request, user)
         messages.success(request, 'Welcome')
         return redirect('dashboard')
       else:
         messages.error(request, 'Invalid credentials')
         return redirect('login')
     else:
       return render(request, 'login.html')


def dashboard(request):
        labels = []
        data = []
        stockqueryset = Stock.objects.filter(is_deleted=False).order_by('-quantity')
        for item in stockqueryset:
            labels.append(item.name)
            data.append(item.quantity)
        sales = SaleBill.objects.order_by('-time')[:3]
        purchases = PurchaseBill.objects.order_by('-time')[:3]
        total_sales = SaleBillDetails.objects.aggregate(Sum('total'))
        today_customers = SaleBill.objects.filter(time__gte = datetime.now().replace(hour=0,minute=0,second=0)).count()
        today_purchases = PurchaseBill.objects.filter(time__gte = datetime.now().replace(hour=0,minute=0,second=0)).count()
        context = {
            'labels'    : labels,
            'data'      : data,
            'sales'     : sales,
            'purchases' : purchases,
            'total_sales' : total_sales,
            'today_customers' : today_customers,
            'today_purchases': today_purchases,
        }
        return render(request,'index.html', context)




@login_required
def logout(request):
    if request.method == 'POST':
      auth.logout(request)
      messages.success(request, 'You are now logged out')
      return redirect('login')

class StockCreateView(SuccessMessageMixin, CreateView):                                 # createview class to add new stock, mixin used to display message
    model = Stock                                                                       # setting 'Stock' model as model
    form_class = StockForm                                                              # setting 'StockForm' form as form
    template_name = "edit_stock.html"                                                   # 'edit_stock.html' used as the template
    success_url = '/inventory/'                                                          # redirects to 'inventory' page in the url after submitting the form
    success_message = "Stock has been created successfully"                             # displays message when form is submitted

    def get_context_data(self, **kwargs):                                               # used to send additional context
        context = super().get_context_data(**kwargs)
        context["title"] = 'New Stock'
        context["savebtn"] = 'Add to Inventory'
        return context

class StockListView(FilterView):
    filterset_class = StockFilter
    queryset = Stock.objects.filter(is_deleted=False)
    template_name = 'inventory.html'
    paginate_by = 10


class StockUpdateView(SuccessMessageMixin, UpdateView):                                 # updateview class to edit stock, mixin used to display message
    model = Stock                                                                       # setting 'Stock' model as model
    form_class = StockForm                                                              # setting 'StockForm' form as form
    template_name = "edit_stock.html"                                                   # 'edit_stock.html' used as the template
    success_url = '/inventory/'                                                          # redirects to 'inventory' page in the url after submitting the form
    success_message = "Stock has been updated successfully"                             # displays message when form is submitted

    def get_context_data(self, **kwargs):                                               # used to send additional context
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit Stock'
        context["savebtn"] = 'Update Stock'
        context["delbtn"] = 'Delete Stock'
        return context


class StockDeleteView(View):                                                            # view class to delete stock
    template_name = "delete_stock.html"                                                 # 'delete_stock.html' used as the template
    success_message = "Stock has been deleted successfully"                             # displays message when form is submitted

    def get(self, request, pk):
        stock = get_object_or_404(Stock, pk=pk)
        return render(request, self.template_name, {'object' : stock})

    def post(self, request, pk):
        stock = get_object_or_404(Stock, pk=pk)
        stock.is_deleted = True
        stock.save()
        messages.success(request, self.success_message)
        return redirect('inventory')


# used to add a new supplier
class SupplierCreateView(SuccessMessageMixin, CreateView):
    model = Supplier
    form_class = SupplierForm
    success_url = '/suppliers/'
    success_message = "Supplier has been created successfully"
    template_name = "edit_supplier.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'New Supplier'
        context["savebtn"] = 'Add Supplier'
        return context


# shows a lists of all suppliers
class SupplierListView(ListView):
    model = Supplier
    template_name = "suppliers_list.html"
    queryset = Supplier.objects.filter(is_deleted=False)
    paginate_by = 10


# used to update a supplier's info
class SupplierUpdateView(SuccessMessageMixin, UpdateView):
    model = Supplier
    form_class = SupplierForm
    success_url = '/suppliers/'
    success_message = "Supplier details has been updated successfully"
    template_name = "edit_supplier.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit Supplier'
        context["savebtn"] = 'Save Changes'
        context["delbtn"] = 'Delete Supplier'
        return context


# used to delete a supplier
class SupplierDeleteView(View):
    template_name = "delete_supplier.html"
    success_message = "Supplier has been deleted successfully"

    def get(self, request, pk):
        supplier = get_object_or_404(Supplier, pk=pk)
        return render(request, self.template_name, {'object' : supplier})

    def post(self, request, pk):
        supplier = get_object_or_404(Supplier, pk=pk)
        supplier.is_deleted = True
        supplier.save()
        messages.success(request, self.success_message)
        return redirect('suppliers-list')


# used to view a supplier's profile
class SupplierView(View):
    def get(self, request, name):
        supplierobj = get_object_or_404(Supplier, name=name)
        bill_list = PurchaseBill.objects.filter(supplier=supplierobj)
        page = request.GET.get('page', 1)
        paginator = Paginator(bill_list, 10)
        try:
            bills = paginator.page(page)
        except PageNotAnInteger:
            bills = paginator.page(1)
        except EmptyPage:
            bills = paginator.page(paginator.num_pages)
        context = {
            'supplier'  : supplierobj,
            'bills'     : bills
        }
        return render(request, 'supplier.html', context)


# used to select the supplier
class SelectSupplierView(View):
    form_class = SelectSupplierForm
    template_name = 'select_supplier.html'

    def get(self, request, *args, **kwargs):                                    # loads the form page
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):                                   # gets selected supplier and redirects to 'PurchaseCreateView' class
        form = self.form_class(request.POST)
        if form.is_valid():
            supplierid = request.POST.get("supplier")
            supplier = get_object_or_404(Supplier, id=supplierid)
            return redirect('new-purchase', supplier.pk)
        return render(request, self.template_name, {'form': form})


# used to generate a bill object and save items
class PurchaseCreateView(View):
    template_name = 'new_purchase.html'

    def get(self, request, pk):
        formset = PurchaseItemFormset(request.GET or None)                      # renders an empty formset
        supplierobj = get_object_or_404(Supplier, pk=pk)                        # gets the supplier object
        context = {
            'formset'   : formset,
            'supplier'  : supplierobj,
        }                                                                       # sends the supplier and formset as context
        return render(request, self.template_name, context)

    def post(self, request, pk):
        formset = PurchaseItemFormset(request.POST)                             # recieves a post method for the formset
        supplierobj = get_object_or_404(Supplier, pk=pk)                        # gets the supplier object
        if formset.is_valid():
            # saves bill
            billobj = PurchaseBill(supplier=supplierobj)                        # a new object of class 'PurchaseBill' is created with supplier field set to 'supplierobj'
            billobj.save()                                                      # saves object into the db
            # create bill details object
            billdetailsobj = PurchaseBillDetails(billno=billobj)
            billdetailsobj.save()
            for form in formset:                                                # for loop to save each individual form as its own object
                # false saves the item and links bill to the item
                billitem = form.save(commit=False)
                billitem.billno = billobj                                       # links the bill object to the items
                # gets the stock item
                stock = get_object_or_404(Stock, name=billitem.stock.name)       # gets the item
                # calculates the total price
                billitem.totalprice = billitem.perprice * billitem.quantity
                # updates quantity in stock db
                stock.quantity += billitem.quantity                              # updates quantity
                # saves bill item and stock
                stock.save()
                billitem.save()
            messages.success(request, "Purchased items have been registered successfully")
            return redirect('purchase-bill', billno=billobj.billno)
        formset = PurchaseItemFormset(request.GET or None)
        context = {
            'formset'   : formset,
            'supplier'  : supplierobj
        }
        return render(request, self.template_name, context)


# used to display the purchase bill object
class PurchaseBillView(View):
    model = PurchaseBill
    template_name = "purchase_bill.html"
    bill_base = "bill_base.html"

    def get(self, request, billno):
        context = {
            'bill'          : PurchaseBill.objects.get(billno=billno),
            'items'         : PurchaseItem.objects.filter(billno=billno),
            'billdetails'   : PurchaseBillDetails.objects.get(billno=billno),
            'bill_base'     : self.bill_base,
        }
        return render(request, self.template_name, context)

    def post(self, request, billno):
        form = PurchaseDetailsForm(request.POST)
        if form.is_valid():
            billdetailsobj = PurchaseBillDetails.objects.get(billno=billno)

            billdetailsobj.eway = request.POST.get("eway")
            billdetailsobj.veh = request.POST.get("veh")
            billdetailsobj.destination = request.POST.get("destination")
            billdetailsobj.po = request.POST.get("po")
            billdetailsobj.bank = request.POST.get("bank")
            billdetailsobj.acno = request.POST.get("acno")
            billdetailsobj.add = request.POST.get("add")
            billdetailsobj.total = request.POST.get("total")

            billdetailsobj.save()
            messages.success(request, "Bill details have been modified successfully")
        context = {
            'bill'          : PurchaseBill.objects.get(billno=billno),
            'items'         : PurchaseItem.objects.filter(billno=billno),
            'billdetails'   : PurchaseBillDetails.objects.get(billno=billno),
            'bill_base'     : self.bill_base,
        }
        return render(request, self.template_name, context)



# used to delete a bill object
class PurchaseDeleteView(SuccessMessageMixin, DeleteView):
     model = PurchaseBill
     template_name = "delete_purchase.html"
     success_url = '/suppliers/'


     def delete(self, *args, **kwargs):
         self.object = self.get_object()
         items = PurchaseItem.objects.filter(billno=self.object.billno)
         for item in items:
             stock = get_object_or_404(Stock, name=item.stock.name)
             if stock.is_deleted == False:
                 stock.quantity -= item.quantity
                 stock.save()
         messages.success(self.request, "Purchase bill has been deleted successfully")
         return super(PurchaseDeleteView, self).delete(*args, **kwargs)
         return redirect('suppliers-list')


# shows the list of bills of all purchases
class PurchaseView(ListView):
     model = PurchaseBill
     template_name = "purchases_list.html"
     context_object_name = 'bills'
     ordering = ['-time']
     paginate_by = 10




# shows the list of bills of all sales
class SaleView(ListView):
    model = SaleBill
    template_name = "sales_list.html"
    context_object_name = 'bills'
    ordering = ['-time']
    paginate_by = 10


# used to generate a bill object and save items
class SaleCreateView(View):
    template_name = 'new_sale.html'

    def get(self, request):
        form = SaleForm(request.GET or None)
        formset = SaleItemFormset(request.GET or None)                          # renders an empty formset
        stocks = Stock.objects.filter(is_deleted=False)
        context = {
            'form'      : form,
            'formset'   : formset,
            'stocks'    : stocks
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = SaleForm(request.POST)
        formset = SaleItemFormset(request.POST)                                 # recieves a post method for the formset
        if form.is_valid() and formset.is_valid():
            # saves bill
            billobj = form.save(commit=False)
            billobj.save()
            # create bill details object
            billdetailsobj = SaleBillDetails(billno=billobj)
            billdetailsobj.save()
            for form in formset:                                                # for loop to save each individual form as its own object
                # false saves the item and links bill to the item
                billitem = form.save(commit=False)
                billitem.billno = billobj                                       # links the bill object to the items
                # gets the stock item
                stock = get_object_or_404(Stock, name=billitem.stock.name)
                # calculates the total price
                billitem.totalprice = billitem.perprice * billitem.quantity
                # updates quantity in stock db
                stock.quantity -= billitem.quantity
                # saves bill item and stock
                stock.save()
                billitem.save()
            messages.success(request, "Sold items have been registered successfully")
            return redirect('sale-bill', billno=billobj.billno)
        form = SaleForm(request.GET or None)
        formset = SaleItemFormset(request.GET or None)
        context = {
            'form'      : form,
            'formset'   : formset,
        }
        return render(request, self.template_name, context)


# used to delete a bill object
class SaleDeleteView(SuccessMessageMixin, DeleteView):
    model = SaleBill
    template_name = "delete_sale.html"
    success_url = '/sales/'

    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        items = SaleItem.objects.filter(billno=self.object.billno)
        for item in items:
            stock = get_object_or_404(Stock, name=item.stock.name)
            if stock.is_deleted == False:
                stock.quantity += item.quantity
                stock.save()
        messages.success(self.request, "Sale bill has been deleted successfully")
        return super(SaleDeleteView, self).delete(*args, **kwargs)





# used to display the sale bill object
class SaleBillView(View):
    model = SaleBill
    template_name = "sale_bill.html"
    bill_base = "bill_base.html"

    def get(self, request, billno):
        context = {
            'bill'          : SaleBill.objects.get(billno=billno),
            'items'         : SaleItem.objects.filter(billno=billno),
            'billdetails'   : SaleBillDetails.objects.get(billno=billno),
            'bill_base'     : self.bill_base,
        }
        return render(request, self.template_name, context)

    def post(self, request, billno):
        form = SaleDetailsForm(request.POST)
        if form.is_valid():
            billdetailsobj = SaleBillDetails.objects.get(billno=billno)

            billdetailsobj.eway = request.POST.get("eway")
            billdetailsobj.veh = request.POST.get("veh")
            billdetailsobj.destination = request.POST.get("destination")
            billdetailsobj.po = request.POST.get("po")
            billdetailsobj.add = request.POST.get("add")
            billdetailsobj.total = request.POST.get("total")

            billdetailsobj.save()
            messages.success(request, "Bill details have been modified successfully")
        context = {
            'bill'          : SaleBill.objects.get(billno=billno),
            'items'         : SaleItem.objects.filter(billno=billno),
            'billdetails'   : SaleBillDetails.objects.get(billno=billno),
            'bill_base'     : self.bill_base,
        }
        return render(request, self.template_name, context)

#adding employees
class EmployeeCreateView(SuccessMessageMixin, CreateView):
    model = Employee
    form_class = EmployeeForm
    success_url = '/employees/'
    success_message = "Employee has been created successfully"
    template_name = "edit_employee.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'New Employee'
        context["savebtn"] = 'Add Employee'
        return context


# shows a lists of all employees
class EmployeeListView(ListView):
    model = Employee
    template_name = "employee_list.html"
    queryset = Employee.objects.filter(is_deleted=False)
    paginate_by = 10


# used to update a employee's info
class EmployeeUpdateView(SuccessMessageMixin, UpdateView):
    model = Employee
    form_class = EmployeeForm
    success_url = '/employees/'
    success_message = "Employee details has been updated successfully"
    template_name = "edit_employee.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit Employee'
        context["savebtn"] = 'Save Changes'
        context["delbtn"] = 'Delete Employee'
        return context

# used to delete an employee
class EmployeeDeleteView(View):
    template_name = "delete_employee.html"
    success_message = "Employee has been deleted successfully"

    def get(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        return render(request, self.template_name, {'object' : employee})

    def post(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        employee.is_deleted = True
        employee.save()
        messages.success(request, self.success_message)
        return redirect('employees-list')

# used to view a supplier's profile
class EmployeerView(View):
    def get(self, request, name):
        employeeobj = get_object_or_404(Employee, name=name)

        context = {
            'employee'  : employeeobj,
        }
        return render(request, 'employee.html', context)

#attendence records
# class AttendenceMarkView(SuccessMessageMixin, CreateView):                                 # createview class to add new stock, mixin used to display message
#     model = EmployeeAttendence                                                                       # setting 'Stock' model as model
#     form_class = EmployeeAttendenceForm                                                              # setting 'StockForm' form as form
#     template_name = "today_attendence.html"                                                   # 'edit_stock.html' used as the template
#     success_url = '/inventory'                                                          # redirects to 'inventory' page in the url after submitting the form
#     success_message = "Attendence marked successfully"                             # displays message when form is submitted
#
#     def get_context_data(self, **kwargs):                                               # used to send additional context
#         context = super().get_context_data(**kwargs)
#         context["title"] = 'Attendence Records'
#         context["savebtn"] = 'Add to Log'
#         return context

def AttendenceMarkView(request):
    if request.method == 'GET':
        date = datetime.today()
        employees = Employee.objects.all()
        print (employees)

        return render(request,'today_attendence.html',{'form':EmployeeAttendenceForm(),'date':date,'employees':employees})
    else:
        #getting inputs from user
        form = EmployeeAttendenceForm(request.POST,request.FILES or None)
        #validate user inputs and save to database
        if form.is_valid():
            newform = form.save(commit=False)
            newform.save()
            messages.success(request, 'Attendence marked successfully')
            return HttpResponseRedirect(reverse('#'))
        return render(request,'today_attendence.html',{'form':EmployeeAttendenceForm()})
