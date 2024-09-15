from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Choice, Question


class IndexView(generic.ListView):
    """
    View to display the list of the latest questions.
    
    Attributes:
        template_name (str): The template to use for rendering this view.
        context_object_name (str): The name of the context variable to use in the template.
    """
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).

        Returns:
            QuerySet: A QuerySet of the latest five published questions.

        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    """
    View to display details of a specific question.
    
    Attributes:
        model (Model): The model to use for this view.
        template_name (str): The template to use for rendering this view.
    """
    model = Question
    template_name = 'polls/detail.html'
    
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        Returns:
            QuerySet: A QuerySet of questions that are published.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())
    
    def get(self, request, *args, **kwargs):
        """
        Handle GET requests. Redirect to index page with an error message if voting is not allowed.
        
        Args:
            request (HttpRequest): The request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        
        Returns:
            HttpResponse: A redirect response if voting is not allowed, or the standard GET response otherwise.
        """
        question = self.get_object()
        if not question.can_vote():
            messages.error(request, "Voting is not allowed for this question.")
            return redirect('polls:index')
        
        # Proceed with the normal get method if voting is allowed
        return super().get(request, *args, **kwargs)


class ResultsView(generic.DetailView):
    """
    View to display the results of a specific question.
    
    Attributes:
        model (Model): The model to use for this view.
        template_name (str): The template to use for rendering this view.
    """
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    """
    Handle the voting process for a specific question.
    
    Args:
        request (HttpRequest): The request object.
        question_id (int): The ID of the question to vote on.
        
    Returns:
        HttpResponseRedirect: Redirects to the results page of the question after processing the vote.
    """
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))