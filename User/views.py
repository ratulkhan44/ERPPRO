from Accountant.models import Transaction
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render, reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from Expense.models import Expense
from Purchases.models import Bill, PurchaseItem, PurchaseOrder
from validate_email import validate_email

from User.decorators import required_role

from . import forms
from .models import CustomUser, UserRole
from .tokens import account_activation_token

# Create your views here.


def user_role(request):
    form = forms.UserRoleForm()

    if request.method == 'POST':
        form = forms.UserRoleForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            messages.success(request, "User Role created successfully")
            return HttpResponseRedirect(reverse('User:user_role'))
    #roles = UserRole.objects.all()
    return render(request, 'user/role.html', context={'form': form})


def create_user(request):
    form = forms.CustomUserCretaionForm()

    if request.method == 'POST':

        form = forms.CustomUserCretaionForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            user.user_permissions.set(
                form.cleaned_data.get('user_permissions'))
            current_site = get_current_site(request)
            mail_subject = 'Activate your user account'

            message = render_to_string('user/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),

            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            messages.success(
                request, 'Please confirm your email address to complete the registration')
            return redirect('user_login')
        else:
            form = forms.CustomUserCretaionForm()

    return render(request, 'user/create_user.html', context={'form': form})


class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, user.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('user_login')
        else:
            messages.warning(
                request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('User:create_user')


def permission_denied(request):
    return render(request, 'user/404.html', context={})


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        # import pdb
        # pdb.set_trace()
        if user:
            if user.is_active and str(user.user_role) == 'Accounts':
                login(request, user)
                return HttpResponseRedirect(reverse('User:accounts_dashboard'))
            elif user.is_active and str(user.user_role) == 'Employee':
                login(request, user)
                return HttpResponseRedirect(reverse('User:employee_dashboard'))
            elif user.is_active and str(user.user_role) == 'Executive':
                login(request, user)
                return HttpResponseRedirect(reverse('User:executive_dashboard'))
            elif user.is_active and str(user.user_role) == 'Supervisor':
                login(request, user)
                return HttpResponseRedirect(reverse('User:supervisor_dashboard'))
            else:
                return HttpResponse('Account doesnt match')

        else:
            return HttpResponse("Username and password wrong")
    else:
        return render(request, 'user/login.html', {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('user_login'))


@login_required
@required_role(allowed_roles=['Employee'])
def employee_dashboard(request):
    order_lists = PurchaseOrder.objects.filter(
        created_by_id=request.user.id).count()
    bill_lists = Bill.objects.filter(status="Draft").count()
    context = {'order_lists': order_lists, 'bill_lists': bill_lists}
    return render(request, 'user/roles/employee/dashboard.html', context)


@login_required
@required_role(allowed_roles=['Supervisor'])
def supervisor_dashboard(request):
    pending_expense = Expense.objects.filter(Q(is_supervisor=False) & Q(
        paid_account__account_name='Petty Cash')).count()
    order_lists = PurchaseOrder.objects.filter(status='Pending').count()
    context = {
        'pending_expense': pending_expense,
        'order_lists': order_lists
    }
    return render(request, 'user/roles/supervisior/dashboard.html', context)


@login_required
@required_role(allowed_roles=['Supervisor'])
def supervisior_petty_cash_expense(request):
    expenses = Expense.objects.filter(Q(is_supervisor=False) & Q(
        paid_account__account_name='Petty Cash'))
    context = {
        'expenses': expenses,
    }
    return render(request, 'user/roles/supervisior/expense_pettycash.html', context)


@login_required
@required_role(allowed_roles=['Supervisor'])
def supervisior_petty_cash_expense_accept(request, id):
    expense = Expense.objects.get(id=id)
    expense.is_supervisor = True
    expense.approved_supervisor_id = request.user.id
    expense.save()
    return HttpResponseRedirect(reverse('User:supervisior_petty_cash_expense'))


@login_required
@required_role(allowed_roles=['Accounts'])
def accounts_dashboard(request):
    pending_expense = Expense.objects.filter(Q(is_supervisor=True) & Q(
        is_accounts_first=False) & Q(paid_account__account_name='Petty Cash')).count()
    approve_expense = Expense.objects.filter(Q(is_supervisor=True) & Q(is_accounts_first=True) & Q(
        is_executive=True) & Q(paid_account__account_name='Petty Cash')).count()
    context = {
        'pending_expense': pending_expense,
        'approve_expense': approve_expense
    }
    return render(request, 'user/roles/accounts/dashboard.html', context)


@login_required
@required_role(allowed_roles=['Accounts'])
def accounts_petty_cash_expense(request):
    expenses = Expense.objects.filter(Q(is_supervisor=True) & Q(
        is_accounts_first=False) & Q(paid_account__account_name='Petty Cash'))
    context = {
        'expenses': expenses,
    }
    return render(request, 'user/roles/accounts/expense_pettycash.html', context)


@login_required
@required_role(allowed_roles=['Accounts'])
def accounts_petty_cash_expense_accept(request, id):
    expense = Expense.objects.get(id=id)
    expense.is_accounts_first = True
    expense.approved_accounts_id = request.user.id
    expense.save()
    return HttpResponseRedirect(reverse('User:accounts_petty_cash_expense'))


@login_required
@required_role(allowed_roles=['Accounts'])
def accounts_petty_cash_expense_accept_recheck(request):
    expenses = Expense.objects.filter(Q(is_supervisor=True) & Q(is_accounts_first=True) & Q(
        is_executive=True) & Q(paid_account__account_name='Petty Cash'))
    context = {
        'expenses': expenses,
    }
    return render(request, 'user/roles/accounts/expense_pettycash_recheck.html', context)


@login_required
@required_role(allowed_roles=['Accounts'])
def accounts_petty_cash_expense_accept_recheck_approve(request, id):
    expense = Expense.objects.get(id=id)

    date = expense.expense_date
    trnsaction_type = "expense"
    account_id_paid = expense.paid_account_id
    total_credit_paid = expense.amount
    total_debit_paid = 0.00
    account_id_expense = expense.expense_account_id
    total_credit_expense = 0.00
    total_debit_expense = expense.amount

    exists_paid = Transaction.objects.filter(
        account_id=account_id_paid, date=date).exists()
    exists_expense = Transaction.objects.filter(
        account_id=account_id_expense, date=date).exists()
    transaction = None

    if exists_paid:
        transaction = Transaction.objects.get(
            account_id=account_id_paid, date=date)
        transaction_debit = transaction.total_debit + \
            decimal.Decimal(total_debit_paid)
        transaction_credit = transaction.total_credit + \
            decimal.Decimal(total_credit_paid)
        transaction.total_debit = transaction_debit
        transaction.total_credit = transaction_credit
        transaction.save()
    else:
        Transaction.objects.create(date=date, trnsaction_type=trnsaction_type,
                                   account_id=account_id_paid, total_debit=total_debit_paid, total_credit=total_credit_paid)

    if exists_expense:
        transaction = Transaction.objects.get(
            account_id=account_id_expense, date=date)
        transaction_debit = transaction.total_debit + \
            decimal.Decimal(total_debit_expense)
        transaction_credit = transaction.total_credit + \
            decimal.Decimal(total_credit_expense)
        transaction.total_debit = transaction_debit
        transaction.total_credit = transaction_credit
        transaction.save()
    else:
        Transaction.objects.create(date=date, trnsaction_type=trnsaction_type,
                                   account_id=account_id_expense, total_debit=total_debit_expense, total_credit=total_credit_expense)

    expense.is_accounts_second = True
    expense.save()

    return redirect('Expense:all_expense')


@login_required
@required_role(allowed_roles=['Executive'])
def executive_dashboard(request):
    pending_expense = Expense.objects.filter(Q(is_supervisor=True) & Q(is_accounts_first=True) & Q(
        is_executive=False) & Q(paid_account__account_name='Petty Cash')).count()
    order_lists = PurchaseOrder.objects.filter(
        status='Checked').count()
    context = {
        'pending_expense': pending_expense,
        'order_lists': order_lists
    }
    return render(request, 'user/roles/executive/dashboard.html', context)


@login_required
@required_role(allowed_roles=['Executive'])
def executive_petty_cash_expense(request):
    expenses = Expense.objects.filter(Q(is_supervisor=True) & Q(is_accounts_first=True) & Q(
        is_executive=False) & Q(paid_account__account_name='Petty Cash'))
    context = {
        'expenses': expenses,
    }
    return render(request, 'user/roles/executive/expense_pettycash.html', context)


@login_required
@required_role(allowed_roles=['Executive'])
def executive_petty_cash_expense_accept(request, id):
    expense = Expense.objects.get(id=id)
    expense.is_executive = True
    expense.approved_executive_id = request.user.id
    expense.save()
    return HttpResponseRedirect(reverse('User:executive_petty_cash_expense'))
