from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login,logout
from django.contrib.auth.forms import UserCreationForm

def logout_view(request):
    """Zavershaet seans raboti s prilojeniem."""
    logout(request)
    return redirect('learning_logs:index')

def register(request):
    """Registriruet novogo polzovatela"""
    if request.method != 'POST':
        #Display blank registration form
        form = UserCreationForm()
    else:
        #Obrabotka zapolnennoy formi
        form = UserCreationForm(data=request.POST)

    if form.is_valid():
        new_user = form.save()
        #Vipolnenie vxoda i perenapravlenie na domashnuyu starnicu
        login(request, new_user)
        return redirect('learning_logs:index')

    context = {'form':form}
    return render(request, 'users/register.html', context)


