from django import forms
from .models import Stock,Supplier,PurchaseItem,PurchaseBill,PurchaseBillDetails,SaleBill,SaleItem,SaleBillDetails,Employee,EmployeeAttendence
from django.forms import formset_factory

class StockForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):                                                        # used to set css classes to the various fields
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['model'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['manufacturer'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['description'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['quantity'].widget.attrs.update({'class': 'textinput form-control', 'min': '0'})

    class Meta:
        model = Stock
        fields = ['name','model','manufacturer','description', 'quantity',]

# form used for supplier
class SupplierForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'textinput form-control', 'pattern' : '[a-zA-Z\s]{1,50}', 'title' : 'Alphabets and Spaces only'})
        self.fields['phone'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '10', 'pattern' : '[0-9]{10}', 'title' : 'Numbers only'})
        self.fields['email'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['nic'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '10', 'pattern' : '[V,v,0-9]{10}', 'title' : 'NIC Format Required'})
        self.fields['photo_main'].widget.attrs.update({'class': 'file form-control'})
    class Meta:
        model = Supplier
        fields = ['name', 'phone', 'address', 'email', 'nic','photo_main']
        widgets = {
            'address' : forms.Textarea(
                attrs = {
                    'class' : 'textinput form-control',
                    'rows'  : '4'
                }
            )
        }





# form used to select a supplier
class SelectSupplierForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['supplier'].queryset = Supplier.objects.filter(is_deleted=False)
        self.fields['supplier'].widget.attrs.update({'class': 'textinput form-control'})
    class Meta:
        model = PurchaseBill
        fields = ['supplier']

# form used to render a single stock item form
class PurchaseItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['stock'].queryset = Stock.objects.filter(is_deleted=False)
        self.fields['stock'].widget.attrs.update({'class': 'textinput form-control setprice stock', 'required': 'true'})
        self.fields['quantity'].widget.attrs.update({'class': 'textinput form-control setprice quantity', 'min': '0', 'required': 'true'})
        self.fields['perprice'].widget.attrs.update({'class': 'textinput form-control setprice price', 'min': '0', 'required': 'true'})
    class Meta:
        model = PurchaseItem
        fields = ['stock', 'quantity', 'perprice']

# formset used to render multiple 'PurchaseItemForm'
PurchaseItemFormset = formset_factory(PurchaseItemForm, extra=1)

#form used to accept the other details for purchase bill
class PurchaseDetailsForm(forms.ModelForm):
   class Meta:
         model = PurchaseBillDetails
         fields = ['eway','veh', 'destination', 'po','bank','acno', 'add', 'total', ]






# form used to get customer details
class SaleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'textinput form-control', 'pattern' : '[a-zA-Z\s]{1,50}', 'title' : 'Alphabets and Spaces only', 'required': 'true'})
        self.fields['phone'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '10', 'pattern' : '[0-9]{10}', 'title' : 'Numbers only', 'required': 'true'})
        self.fields['email'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['nic'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '10', 'pattern' : '[V,v,0-9]{10}', 'title' : 'NIC Format Required'})
    class Meta:
        model = SaleBill
        fields = ['name', 'phone', 'address', 'email', 'nic']
        widgets = {
            'address' : forms.Textarea(
                attrs = {
                    'class' : 'textinput form-control',
                    'rows'  : '4'
                }
            )
        }

# form used to render a single stock item form
class SaleItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['stock'].queryset = Stock.objects.filter(is_deleted=False)
        self.fields['stock'].widget.attrs.update({'class': 'textinput form-control setprice stock', 'required': 'true'})
        self.fields['quantity'].widget.attrs.update({'class': 'textinput form-control setprice quantity', 'min': '0', 'required': 'true'})
        self.fields['perprice'].widget.attrs.update({'class': 'textinput form-control setprice price', 'min': '0', 'required': 'true'})
    class Meta:
        model = SaleItem
        fields = ['stock', 'quantity', 'perprice']

# formset used to render multiple 'SaleItemForm'
SaleItemFormset = formset_factory(SaleItemForm, extra=1)

# form used to accept the other details for sales bill
class SaleDetailsForm(forms.ModelForm):
    class Meta:
        model = SaleBillDetails
        fields = ['eway','veh', 'destination', 'po', 'add', 'total']


#employee forms
class EmployeeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'textinput form-control', 'pattern' : '[a-zA-Z\s]{1,50}', 'title' : 'Alphabets and Spaces only'})
        self.fields['designation'].widget.attrs.update({'class': 'textinput form-control', 'pattern' : '[a-zA-Z\s]{1,50}', 'title' : 'Alphabets and Spaces only'})
        self.fields['phone'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '10', 'pattern' : '[0-9]{10}', 'title' : 'Numbers only'})
        self.fields['email'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['nic'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '10', 'pattern' : '[V,v,0-9]{10}', 'title' : 'NIC Format Required'})
        self.fields['photo_main'].widget.attrs.update({'class': 'file form-control'})



    class Meta:
        model = Employee
        fields = ['name','designation', 'phone', 'address','birth_date', 'email','joined_date', 'nic','photo_main']
        widgets = {
            'address' : forms.Textarea(
                attrs = {
                    'class' : 'textinput form-control',
                    'rows'  : '4'
                }
            ),
            'birth_date' : forms.TextInput(
                attrs={'type': 'date'}
            ),
            'joined_date' : forms.TextInput(
                attrs={'type': 'date'}
            ),
        }

#EmployeeAttendence inputs
class EmployeeAttendenceForm(forms.ModelForm):
    class Meta:
        model = EmployeeAttendence
        fields = ['employee', 'status',]

EmployeeAttendenceFormset = formset_factory(EmployeeAttendenceForm, extra=1)
