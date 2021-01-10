from django.shortcuts import render,redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

def index(request):
    """Domashnaya stranica prilojeniya Learning Log"""
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    """Vivodit spisok tem"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """Vivodit odnu temu i vse ee zapisi"""
    topic = Topic.objects.get(id=topic_id)
    #Proverka togo, chto tema prinadlejit tekusheu polzovatelyu
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic':topic, 'entries':entries}
    return render(request,'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """Opredelaet novuyu temu"""
    if request.method != 'POST':
        #Dannie ne otpravlalis; sozdaetsa pustaya forma.
        form = TopicForm()
    else:
        #Otpravleni dannie POST; obrabotat'dannie.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')

    context= {'form':form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """Dobavlaet novuyu zapis' po konkretnoy teme."""
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        #Dannie ne otpravlalis; sozdaetsa pustaya forma.
        form = EntryForm()
    else:            
        #Otpravleni dannie POST; obrabotat' dannie
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)

    context = {'topic':topic, 'form':form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Redaktiruet sushestvuyushuyu zapis'"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        #Isxodniy zapros; forma zapolnaetsa dannimi tekushey zapisi
        form = EntryForm(instance=entry)
    else:
        #Otpravka dannix POST; obrabotat' dannie.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topi_id=topic.id)

    context = {'entry':entry, 'topic':topic, 'form':form}
    return render(request, 'learning_logs/edit_entry.html', context)

