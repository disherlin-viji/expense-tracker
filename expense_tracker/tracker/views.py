from django.shortcuts import render, redirect

# Create your views here.
from .models import Transaction, TYPE_CHOICES, CATEGORY_CHOICES, PAYMENT_CHOICES
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.db.models.functions import TruncMonth

@login_required
def home(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')

    recent_transactions = transactions[:5]

    total_income = 0
    total_expense = 0 
    for t in transactions:
        if t.transaction_type == 'Income':
            total_income += t.amount
        else:
            total_expense += t.amount
    total_balance = total_income-total_expense
    
    context = {
        'transactions':transactions,
        'recent_transactions':recent_transactions,
        'total_income':total_income, 
        'total_expense':total_expense,
        'total_balance':total_balance,
    }

    return render(request,'home.html',context)

def categories(request):
    transactions = Transaction.objects.filter(user=request.user)

    income_data = transactions.filter(transaction_type='Income').values('category').annotate(total=Sum('amount'))
    expense_data = transactions.filter(transaction_type='Expense').values('category').annotate(total=Sum('amount'))

    monthly_income = transactions.filter(transaction_type='Income').annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('amount')).order_by('month')
    monthly_expense = transactions.filter(transaction_type='Expense').annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('amount')).order_by('month')

    return render(request,'categories.html',
                    {'income_data':income_data,
                    'expense_data':expense_data,
                    'monthly_income':monthly_income,
                    'monthly_expense':monthly_expense})

@login_required
def add_transaction(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        transaction_type = request.POST.get('transaction_type')
        category = request.POST.get('category')
        description = request.POST.get('description')
        payment_method = request.POST.get('payment_method')
        date = request.POST.get('date')

        Transaction.objects.create(
            user = request.user,
            amount = amount,
            transaction_type = transaction_type,
            category = category,
            description = description,
            payment_method = payment_method,
            date = date
        )
        return redirect('home')
    return render(request,'add.html',{
        'type_choices':TYPE_CHOICES,
        'category_choices':CATEGORY_CHOICES,
        'payment_choices':PAYMENT_CHOICES
    })

@login_required
def edit_transaction(request,id):
    transaction = Transaction.objects.get(id=id)

    if request.method == 'POST':
        transaction.amount = request.POST.get('amount')
        transaction.transaction_type = request.POST.get('transaction_type')
        transaction.category = request.POST.get('category')
        transaction.description = request.POST.get('description')
        transaction.payment_method = request.POST.get('payment_method')
        transaction.date = request.POST.get('date')

        transaction.save()
        return redirect('transactions_page')
    
    return render(request,'edit.html',{
        'transaction':transaction,
        'type_choices':TYPE_CHOICES,
        'category_choices':CATEGORY_CHOICES,
        'payment_choices':PAYMENT_CHOICES
    })

@login_required
def delete_transaction(request,id):
    transaction = Transaction.objects.get(id=id)
    transaction.delete()
    return redirect('home')

def transactions_page(request):
    filter_type = request.GET.get('filter','all')

    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    
    if filter_type == 'income':
        transactions = transactions.filter(transaction_type='Income')
    elif filter_type == 'expense':
        transactions = transactions.filter(transaction_type='Expense')

    total_count = transactions.count()
    return render(request,'transactions.html',{'transactions':transactions, 'total_count':total_count, 'filter_type':filter_type})

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')

        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1!=password2:
            messages.error(request,'Passwords do not match')
            return render(request,'signup.html',{
                'username':username,
                'email':email
            })
        
        if User.objects.filter(username=username).exists():
            messages.error(request,'Username already exists')
            return render(request,'signup.html',{
                'email':email
            })
        
        User.objects.create_user(
            username = username,
            email=email,
            password = password1
        )

        messages.success(request,'Account created successfully')
        return redirect('home')
    return render(request,'signup.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,'Invalid username or password')
            return render(request, 'login.html')
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('login')

@login_required
def change_username(request):
    if request.method == 'POST':
        new_username = request.POST.get('username')

        if User.objects.filter(username=new_username).exists():
            messages.error(request,'Username already exists')
            return redirect('change_username')
        
        request.user.username = new_username
        request.user.save()

        return redirect('home')
    return render(request,'change_username.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not request.user.check_password(current_password):
            messages.error(request,'Current password is incorrect')
            return redirect('change_password')
        
        if new_password != confirm_password:
            messages.error(request,'Passwords do not match')
            return redirect('change_password')
        
        request.user.set_password(new_password)
        request.user.save()

        update_session_auth_hash(request,request.user)
        return redirect('home')
    return render(request,'change_password.html')

@login_required
def delete_account(request):
    if request.method == 'POST':
        request.user.delete()
        messages.success(request,'Account deleted successfully')

        return redirect('login')
    return render(request,'delete_account.html')


