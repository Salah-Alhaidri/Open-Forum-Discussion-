from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse,Http404
from .models import forummodel
from django.contrib.auth.models import User
from .models import ForumSectionModel,CommentModel
from .forms import NewTopicForm, PostForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import UpdateView, ListView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage



from django.views.generic import ListView
from .models import forummodel

from django.views.generic import ListView
from .models import forummodel  # Replace with your actual model name


from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import ContactForm


def success_view(request):
    
    return render(request,'success.html')

def contact_view(request):
    """
    Handle the contact form submission.
    """
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            subject = form.cleaned_data.get("subject")
            message = form.cleaned_data.get("message")
            
            try:
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
            except BadHeaderError:
                return render(request, "error.html", {"error": "Invalid header found."})
            except Exception as e:
                return render(request, "error.html", {"error": f"Email sending failed: {e}"})

            return redirect(reverse("success"))  # Redirect to a success page
    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form})

class forummodelListView(ListView):
    model = forummodel
    context_object_name = 'boards'
    template_name = 'home.html'
    paginate_by = 6  # Number of boards per page

    def get_queryset(self):
        """
        Override the default queryset to allow search functionality.
        """
        query = self.request.GET.get('query', '')  # Get the search query from the request
        if query:
            return forummodel.objects.filter(ForumTitile__icontains=query)  # Adjust field name as needed
        return forummodel.objects.all()

    def get_context_data(self, **kwargs):
        """
        Add the search query to the context for template rendering.
        """
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('query', '')
        return context




def board_topics(request, board_id):
    # Retrieve the board object based on the provided board_id
    board = get_object_or_404(forummodel, pk=board_id)
    boards = forummodel.objects.all()
    queryset = board.forms.order_by('-created_dt').annotate(comments=Count('comt'))
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 10)

    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)
    return render(request, 'sections.html', {
        'board': board,
        'topics': topics,
        'boards':boards
    })


@login_required
def new_topic(request,board_id):
    board = get_object_or_404(forummodel,pk=board_id)
    # user = User.objects.first()
    if request.method == "POST":
        form =NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.created_by = request.user
            topic.save()

            post = CommentModel.objects.create(
                massg=form.cleaned_data.get('massg'),
                created_by = request.user,
                section=topic

            )
            return redirect('board_topics',board_id=board.pk)
    else:
        form = NewTopicForm()

    return render(request,'new_section.html',{'board':board,'form':form})


def topic_posts(request,board_id,topic_id):
    topic = get_object_or_404(ForumSectionModel,board__pk=board_id,pk=topic_id)

    session_key = 'view_topic_{}'.format(topic.pk)
    if not request.session.get(session_key,False):
        topic.views +=1
        topic.save()
        request.session[session_key] = True
    return render(request,'topic_posts.html',{'topic':topic})


@login_required
def reply_topic(request, board_id,topic_id):
    topic = get_object_or_404(ForumSectionModel,board__pk=board_id,pk=topic_id)
    if request.method == "POST":
        form =PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.section = topic
            post.created_by = request.user
            post.save()

            topic.updated_by = request.user
            topic.updated_dt = timezone.now()
            topic.save()

            return redirect('topic_posts',board_id=board_id, topic_id = topic_id)
    else:
        form = PostForm()
    return render(request,'reply_topic.html',{'topic':topic,'form':form})


@method_decorator(login_required,name='dispatch')
class PostUpdateView(UpdateView):
    model = CommentModel
    fields = ('massg',)
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_dt = timezone.now()
        post.save()
        return redirect('topic_posts',board_id=post.section.board.pk,topic_id=post.section.pk)




