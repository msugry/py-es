from django.core.validators import RegexValidator
from django.shortcuts import render, redirect

# Create your views here.
from app01 import models


def depart_list(request):
    """部门列表"""

    # 取数据库中获取所有的部门列表
    # [对象，对象，对象]
    queryset = models.Department.objects.all()

    return render(request, '../templates/depart_list.html', {'queryset': queryset})


def depart_add(request):
    """添加部门页面"""
    if request.method == "GET":
        return render(request, 'depart_add.html')
    # 获取用户post提交过来的数据(title输入为空)
    title = request.POST.get("title")

    # 保存到数据库
    models.Department.objects.create(title=title)

    # 重定向回部门列表
    return redirect('/depart/list/')


def depart_del(request):
    """删除部门"""
    # 获取id
    #
    nid = request.GET.get('nid')
    # 删除
    models.Department.objects.filter(id=nid).delete()
    return redirect('/depart/list/')


# http://127.0.0.1:8000/depart/4/edit/
# http://127.0.0.1:8000/depart/10/edit/
def depart_edit(request, nid):
    """修改部门"""
    if request.method == "GET":
        # 根据nid，获取他的数据[obj,]
        row_object = models.Department.objects.filter(id=nid).first()
        # row_object = models.Department.objects.filter(id=nid).all()  #会报错

        # print(row_object.id,row_object.title)
        return render(request, 'depart_edit.html', {"row_object": row_object})

    # 获取用户提交的标题
    title = request.POST.get("title")

    # 根据id找到数据库中的数据并进行更新
    models.Department.objects.filter(id=nid).update(title=title)

    # 重定向回部门列表
    return redirect("/depart/list/")


def user_list(request):
    """用户管理"""

    # 获取所有用户列表
    queryset = models.UserInfo.objects.all()

    # 用Python的语法获取数据
    # for obj in queryset:
    #     # print(obj.id, obj.name, obj.account, obj.gender, obj.get_gender_display())
    #     print(obj.name,obj.depart_id)
    #     obj.depart_id  # 获取数据库中存储的那个字段值
    #     obj.depart.title    # 根据ID自动去关联的表中获取哪一行数据depart对象

    return render(request, 'user_list.html', {"queryset": queryset})


def user_add(request):
    """添加用户(原始方法)"""
    if request.method == "GET":
        context = {
            'gender_choices': models.UserInfo.gender_choices,
            'depart_list': models.Department.objects.all()
        }
        return render(request, 'user_add.html', context)

    # 获取用户提交的数据
    user = request.POST.get("user")
    pwd = request.POST.get("pwd")
    age = request.POST.get("age")
    account = request.POST.get("ac")
    ctime = request.POST.get("ctime")
    gender = request.POST.get("gd")
    depart_id = request.POST.get("dp")

    # 添加数据到数据库
    models.UserInfo.objects.create(name=user, password=pwd, age=age, account=account, create_time=ctime, gender=gender,
                                   depart_id=depart_id)

    # 返回到用户列表界面
    return redirect("/user/list/")


######################## ModelForm 示例 ##########################
from django import forms


class UserModelForm(forms.ModelForm):
    name = forms.CharField(min_length=2, label="用户名")

    # password =forms.CharField(label="密码")

    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age", "account", "create_time", "gender", "depart"]

        # widgets = {
        #     "name": forms.TextInput(attrs={"class": "form-control"})
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 循环找到所有的插件，添加class="form-control"
        for name, field in self.fields.items():
            # if name == "password":
            # continue
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}
            # print(name,field)


def user_model_form_add(request):
    """添加用户（ModelForm版本）"""
    if request.method == "GET":
        form = UserModelForm()
        return render(request, 'user_model_form_add.html', {"form": form})

    # 用户提交数据,数据校验。
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        # 如果数据合法，保存到数据库
        # print(form.cleaned_data)
        form.save()
        return redirect('/user/list/')
    # 校验失败，在页面上显示错误信息
    return render(request, 'user_model_form_add.html', {"form": form})


def user_edit(request, nid):
    """ 编辑用户 """
    row_object = models.UserInfo.objects.filter(id=nid).first()

    if request.method == "GET":
        # 根据ID去数据库获取要编辑的那一行数据
        form = UserModelForm(instance=row_object)
        return render(request, 'user_edit.html', {'form': form})

    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # 默认保存的是用户输入的所有数据，如果想要在用户输入以外增加一点值
        # form.instance.字段名 = 值
        form.save()
        return redirect('/user/list/')
    return render(request, 'user_edit.html', {"form": form})


def user_delete(request, nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')


# def pretty_list(request):
#     """ 靓号列表 """
#
#     # select * from table by id asc;
#     models.PrettyNum.objects.all().order_by("-id")

def pretty_list(request):
    """靓号列表"""
    # select * from table by level desc;
    queryset = models.PrettyNum.objects.all().order_by("-level")
    return render(request, 'pretty_list.html', {'queryset': queryset})


from django.core.exceptions import ValidationError


class PrettyModeForm(forms.ModelForm):
    # 验证方法一
    # 完成对于字符串的校验
    # mobile = forms.CharField(
    #     label="手机号",
    #     validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')],
    # )

    class Meta:
        model = models.PrettyNum
        # fields = "__all__"   # 表示所有字段
        fields = ["mobile", 'price', 'level', 'status']  # 自定义字段
        # exclude = ['level']  # 表示除此处字段以外所有字段

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    # 验证方法二
    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        if len(txt_mobile) != 11:
            # 验证不通过
            raise ValidationError("格式错误")
        # 验证通过,用户输入的值返回
        return txt_mobile


def pretty_add(request):
    """添加靓号"""
    if request.method == "GET":
        form = PrettyModeForm()
        return render(request, "pretty_add.html", {"form": form})
    form = PrettyModeForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')
    return render(request, 'pretty_add.html', {"form": form})


class PrettyEditModeForm(forms.ModelForm):
    # mobile = forms.CharField(disabled=True, label="手机号")
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')],
    )
    class Meta:
        model = models.PrettyNum
        fields = ['mobile', 'price', 'level', 'status']  # 自定义字段

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


def pretty_edit(request, nid):
    """编辑靓号页面"""
    row_object = models.PrettyNum.objects.filter(id=nid).first()

    if request.method == "GET":
        form = PrettyEditModeForm(instance=row_object)
        return render(request, 'pretty_edit.html', {"form": form})
    form = PrettyEditModeForm(data=request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')
    return render(request, 'pretty_edit.html', {"form": form})