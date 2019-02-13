from django.shortcuts import render, HttpResponse, redirect
from .models import Record, Category
from .forms import RecordForm
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def hello(request):
    #return HttpResponse('hello!') #simplest view to template
    #a = 1
    #return render(request,'app/hello.html',{'key':a}) #return a value by dictionary
    return render(request,'app/hello.html',{}) #記得去setting註冊app雖然已經startapp!!
@login_required
def frontpage(request):
    # Model Form operation
    user = request.user #
    record_form = RecordForm(initial={'balance_type':'支出'})#初始化form的欄位
    records = Record.objects.filter(user=user)#
    income_list = [record.cash for record in records if record.balance_type == '收入']
    outcome_list = [record.cash for record in records if record.balance_type == '支出']
    income = sum(income_list) if len(income_list)!=0 else 0
    outcome = sum(outcome_list) if len(outcome_list)!=0 else 0
    net = income - outcome
    '''
    太多變數需要回傳給template時，可以直接使用locals()
    return render(request, 'app/index.html', {'records':records, 'income':income,
                                              'outcome':outcome, 'net':net})
    '''
    return render(request, 'app/index.html', locals())
@login_required
def settings(request):
    user = request.user #
    categories = Category.objects.filter(user=user)#
    return render(request, 'app/settings.html', locals())

# Template form operation
@login_required
def addCategory(request):
    if request.method == 'POST':
        user = request.user #
        posted_data = request.POST #request 的屬性.POST 把POST的資料傳進來(dictionary的格式)
        category = posted_data["add_category"]
        Category.objects.get_or_create(category=category, user=user)#
    return redirect('/settings')
@login_required
def deleteCategory(request, category):
    user = request.user#
    Category.objects.filter(category=category, user=user).delete()#
    return redirect('/settings')
@login_required
def addRecord(request):
    if request.method == 'POST':
        user=request.user#
        #ModelForm的威力!! 賦予RecordForm一個dictionary(request.POST)，並存成一個form的物件
        #把form的值填滿，並對form進行檢測(檢測需另外定義)，本例沒有使用
        form = RecordForm(request.POST)
        if form.is_valid():
            #form.save() #original
            record = form.save(commit=False)
            record.user = user
            record.save()
    return redirect('/')
@login_required
def deleteRecord(request):
    if request.method == 'POST':
        id = request.POST['delete_val']
        Record.objects.filter(id=id).delete()
    return redirect('/')

