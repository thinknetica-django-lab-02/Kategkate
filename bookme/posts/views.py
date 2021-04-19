from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import UpdateView, CreateView
from django_filters import FilterSet
from django_filters.views import FilterView

from posts.forms import SearchForm, ApartCreateForm
from posts.models import Apartment

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from accounts.models import User
from django.core.mail import EmailMessage


def index(request):
    turn_on_block = False
    # многострочный перенос строки с аргументами
    return render(
        request,
        'index.html',
        {
            'turn_on_block': turn_on_block
        }
    )


class AboutView(TemplateView):
    template_name = 'about.html'


class ContactView(TemplateView):
    template_name = 'contact.html'


class ExperienceView(TemplateView):
    """
    This class is for the creation of the Experience Object.
    """
    template_name = 'experience.html'


class NewsroomView(TemplateView):
    """
    This class is for the creation of the News Object.
    """
    template_name = 'newsroom.html'


class ApartmentFilter(FilterSet):
    """
    This class is for the filters which are set for the apartments.
    """

    class Meta:
        model = Apartment
        fields = ['tags', 'price']


class ApartListView(ListView):
    template_name = 'apartments/apartment.html'
    paginate_by = 1
    model = Apartment
    context_object_name = 'item_list'

    def get_context_data(self, **kwargs):
        context = super(ApartListView, self).get_context_data(**kwargs)
        context['filter'] = ApartmentFilter(data=self.request.GET)
        return context

    def get_queryset(self):
        print(self.request.GET)
        return ApartmentFilter(
            self.request.GET,
            super(ApartListView, self).get_queryset()
        ).qs


class ApartDetailView(DetailView):
    """
    This class is for the detailed review of the Apartment.
    """

    template_name = 'apartments/apartment-detail.html'
    model = Apartment
    context_object_name = 'item'


class ApartmentCreateView(CreateView):
    """
    This class is for the creation of the Apartment.
    """

    template_name = 'apartments/apartment-create.html'
    form_class = ApartCreateForm
    success_url = '/apartment'
    model = Apartment


class ApartmentEditView(UpdateView):
    """
    This class is for the searching of the Apartment.
    """

    template_name = 'apartments/apartment-edit.html'
    form_class = SearchForm
    success_url = '/'
    model = Apartment


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('acc_active_email.html', {
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
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
