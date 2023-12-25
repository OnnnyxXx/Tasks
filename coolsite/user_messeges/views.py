from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from tasks_app_user.models import Articles
from user_messeges.forms import ConversationMessageForm
from user_messeges.models import Conversation


@login_required
def new_conversation(request, item_pk):
    item = get_object_or_404(Articles, pk=item_pk)

    if item.author == request.user:
        return redirect('home')

    conversations = Conversation.objects.filter(item=item, members=request.user)

    if conversations.exists():
        return redirect('inbox')

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.author)

            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            return redirect('inbox')
    else:
        form = ConversationMessageForm()

    return render(request, 'new.html', {
        'form': form,
        'item': item
    })


@login_required
def inbox(request):
    conversations = Conversation.objects.filter(members__in=[request.user.id])
    return render(request, 'inbox.html', {
        'conversations': conversations,

    })


@login_required
def detail(request, pk):
    conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)
    interlocutor = conversation.members.exclude(id=request.user.id).first()

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            conversation.save()

            return redirect('detail', pk=pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'detail.html', {
        'conversation': conversation,
        'form': form,
        'interlocutor': interlocutor
    })
