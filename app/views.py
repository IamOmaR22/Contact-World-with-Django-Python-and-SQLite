from django.shortcuts import render,get_object_or_404,redirect
from .models import Contact
from django.views.generic import ListView,DetailView
from django.db.models import Q  # Q for multiple search
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin  # It will making views to require login to acces.
from django.contrib.auth.decorators import login_required # It will making search to require login to acces.
from django.urls import reverse_lazy
from django.contrib import messages


# Create your views here.
# def home(request):
#     context = {'contacts':Contact.objects.all()}
#     return render(request, 'index.html', context)

# def detail(request,id):
#     context = {'contact':get_object_or_404(Contact,pk=id)}
#     return render(request, 'detail.html', context)


###--##--### Home view Start ###--##--###
# By using LoginRequiredMixin, You must have to login first to enter the website.
class HomePageView(LoginRequiredMixin, ListView):
    template_name = 'index.html'
    model = Contact
    context_object_name = 'contacts'

    def get_queryset(self):  # Showing contacts of logged in user only. By using this function.
        contacts = super().get_queryset()
        return contacts.filter(manager = self.request.user)
###--##--### Home view End ###--##--###


###--##--### Contact Details View Start ###--##--###
class ContactDetailView(LoginRequiredMixin, DetailView):
    template_name = 'detail.html'
    model = Contact
    context_object_name = 'contact'
###--##--### Contact Details View End ###--##--###


###--##--### Search Start ###--##--###
@login_required   # By using @login_required, user can't search anything without login
def search(request):
    if request.GET:
        search_term = request.GET['search_term']
        search_results = Contact.objects.filter(
            Q(name__icontains=search_term) |
            Q(email__icontains=search_term) |
            Q(info__icontains=search_term) |
            Q(phone__iexact=search_term)   # when iexact is used, we need to search by exact value
        )
        context = { 'search_term':search_term, 'contacts':search_results.filter(manager=request.user) } # By using filter, only logged in user can search their contacts.
        return render(request, 'search.html', context)
    else:
        return redirect('home')
###--##--### Search End ###--##--###


###--##--### Contact Create View Start ###--##--###
class ContactCreateView(LoginRequiredMixin, CreateView):
    model = Contact
    template_name = 'create.html'
    fields = ['name','email','phone','info','gender','image']
    # success_url = '/'
    def form_valid(self,form):
        instance = form.save(commit=False)
        instance.manager = self.request.user
        instance.save()
        messages.success(self.request, 'Your contact has been successfully created!')
        return redirect('home')
###--##--### Contact Create View End ###--##--###


###--##--### Contact Update View Start ###--##--###
class ContactUpdateView(LoginRequiredMixin, UpdateView):
    model = Contact
    template_name = 'update.html'
    fields = ['name','email','phone','info','gender','image']
    # success_url = '/'
    def form_valid(self,form):
        instance = form.save()
        messages.success(self.request, 'Your contact has been successfully updated!')
        return redirect('detail',instance.pk)
###--##--### Contact Update View End ###--##--###


###--##--### Contact Delete View Start ###--##--###
class ContactDeleteView(LoginRequiredMixin, DeleteView):
    model = Contact
    template_name = 'delete.html'
    success_url = '/'

    def delete(self,request,*args,**kwargs): # we this function for messages
        messages.success(self.request, 'Your contact has been successfully deleted!')
        return super().delete(self,request,*args,**kwargs)
###--##--### Contact Delete View End ###--##--###


###--##--### Sign Up Start ###--##--###
class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('home') # By using reverse_lazy, we can go to home directly
###--##--### Sign Up End ###--##--###


def about(reqest):

    context = {
        'about_text':"Welcome To About Page",
        'omar1':"Hi! I am Md. Omar Faruk,",
        'omar2':" a web developer focused on crafting great web experiences."
    }
    return render(reqest, 'about.html', context)
