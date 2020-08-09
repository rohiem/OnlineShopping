from django.shortcuts import render,redirect
from .forms import ContactForm,LoginForm,RegisterForm,GuestForm
from django.contrib.auth import authenticate , login,get_user_model
from billing.models import GuestEmail
def home_page(request):
    if not request.user.is_authenticated:
        return redirect("login")
    print(request.session.get("cart_id" ,"unknown"))
    return render(request,"home-page.html")



def about_page(request):
    return render(request,"about-page.html")


def contact_page(request):
    contact_form=ContactForm(request.POST or None)
    if contact_form.is_valid():
        print(contact_form.cleaned_data)

    if request.method=="POST":
        print(request.POST)
        print(request.POST['fullname'])

        print(request.POST['email'])
        print(request.POST['content'])


    return render(request,"contact-page.html",{"form":contact_form})
def guest_login_view(request):
    form=GuestForm(request.POST or None)
    context={"form":form}
#    print(request.user.is_authenticated)
    if form.is_valid():
        email=form.cleaned_data["email"]
        new_guest_email=GuestEmail.objects.create(email=email)
        request.session["guest_email_id"]=new_guest_email.id

        context["form"]=GuestForm()


    return redirect("/")


User=get_user_model()
def register_page(request):
    form=RegisterForm(request.POST or None)
    context={"form":form}

    if form.is_valid():
        print(form.cleaned_data)
        username=form.cleaned_data['username']
        email=form.cleaned_data['email']
        password=form.cleaned_data['password']
        new_user=User.objects.create_user(username,email,password)
        print(new_user)

    return render(request,"register.html",context)



def login_page(request):
    form=LoginForm(request.POST or None)
    context={"form":form}
#    print(request.user.is_authenticated)
    if form.is_valid():
        print(form.cleaned_data)
        username=form.cleaned_data["username"]
        password=form.cleaned_data['password']
        context["form"]=LoginForm()
        user=authenticate(request,username=username,password=password)
        if user is not None:
            print(request.user.username)
            login(request,user)
            try:
                del request.session['guest_email_id']
            except:
                pass

            # context["form"]=LoginForm()
            return redirect("/")
        else:
            print("error")

    return render(request,"login.html",context)