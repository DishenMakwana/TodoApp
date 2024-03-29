# Create your views here.
from django.core.mail import send_mail
from todoapp import settings
from .models import TodoList, Category
from django.contrib.auth.models import User


def index(request):  # the index view

    username = request.user.username

    if username == "":
        return render(request, "index.html")
    else:
        todos = TodoList.objects.filter(user=request.user)  # quering all todos with the object manager
        categories = Category.objects.all()  # getting all categories with object manager

        if request.method == "POST":  # checking if the request method is a POST

            if "taskAdd" in request.POST:  # checking if there is a request to add a todo

                if request.POST["description"] == "" or str(request.POST["date"]) == "" or request.POST["category_select"] == "":
                    error = "Please enter All Data Field properly"
                    return render(request, "index.html", {"todos": todos, "categories": categories, "error": error})

                title = request.POST["description"]  # title
                date = str(request.POST["date"])  # date
                category = request.POST["category_select"]  # category
                content = title + " -- " + date + " " + category  # content

                ur = User.objects.get(username=request.user)  # get log-in username from already registered users

                Todo = TodoList(title=title, content=content, due_date=date,
                                category=Category.objects.get(name=category), user=ur)
                Todo.save()  # saving the todo
                return redirect("/")  # reloading the page

            if "taskDelete" in request.POST:  # checking if there is a request to delete a todo
                checkedlist = request.POST.get("checkedbox")  # checked todos to be deleted

                if checkedlist is None:
                    error = "Please select the task, you want to delete"
                    return render(request, "index.html", {"todos": todos, "categories": categories, "error": error})

                for todo_id in checkedlist:
                    todo = TodoList.objects.get(id=int(todo_id))  # getting todo id
                    todo.delete()  # deleting todo

        return render(request, "index.html", {"todos": todos, "categories": categories})


from django import template

register = template.Library()


@register.filter
def sort_by(queryset, order):
    return queryset.order_by(order)


from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect
from todolist.forms import RegisterForm


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request, user)

            subject = 'Welcome to TodoList World'
            message = 'Hi {}, thank you for registering in TodoList. Your can now explore our todolist anytime and anywhere threw web services. \n\n https://todoapp-dm.herokuapp.com/'.format(username)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            send_mail(subject, message, email_from, recipient_list)

            return redirect("index")
        else:
            for msg in form.error_messages:
                print(form.error_messages[msg])
            return render(request=request, template_name="registration/register.html", context={"form": form})

    form = RegisterForm
    return render(request=request, template_name="registration/register.html", context={"form": form})
