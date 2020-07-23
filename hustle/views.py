import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

from accounts.forms import UserUpdateForm, ProfileUpdateForm
from .models import Hustle, Category, Comment, Skill, HustleMedia, User
from .forms import HustleForm, CommentForm, SkillForm, HustleFullForm
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse, Http404
from django.contrib import messages
from django.db.models import Q
from accounts.models import Profile
from django.views.generic.edit import CreateView, UpdateView
from django.forms import modelformset_factory
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls.base import reverse_lazy


@login_required
def index(request):
    context = {"hustle_posts": Hustle.objects.all(),  "hustleposts": Hustle.objects.all()[0:5]}
    return render(request, 'index.html', context)


"""def profile_view(request, user):
    user = Profile.objects.get(user=user)
    return render(request, "userprofile.html", {})
"""
@login_required
def user_profile(request, username, **kwargs):
    try:
        user = User.objects.get(username=username)
    except:
        raise Http404
    object = Hustle.objects.filter(user=user)
    context = {
        "user": user,
        "object": object,
    }
    return render(request, "profile.html", context)


def LikeView(request, pk):
    hustle = get_object_or_404(Hustle, id=request.POST.get('post_id'))
    hustle.likes.add(request.user)
    return render(request, 'index.html')


def detail(request, slug):
    hustle = get_object_or_404(Hustle, slug=slug)
    comments = Comment.objects.filter(hustle=hustle).order_by('timestamp')
    if request.method == "POST":
        form = CommentForm(request.POST or None)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.hustle = hustle
            obj.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = CommentForm()
    context = {"object": hustle,
               "comments": comments,
               "form": form}
    return render(request, "details.html", context)


"""
    if request.method == "POST":
        form = CommentForm(request.POST or None)
        if form.is_valid():
            comment = request.POST.get('comment')
            reply_id = request.POST.get('comment_id')
            comment_qs = None
            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)
            comment = Comment.objects.create(hustle=hustle, user=request.user, comment=comment, reply=comment_qs)
            comment.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = CommentForm()
    context = {"object": hustle, "form": form,  "comments": comments}"""
def needskill(request):
    skills = Skill.objects.filter(reply=None).order_by('-timestamp')
    if request.method == "POST":
        form = SkillForm(request.POST or None)
        if form.is_valid():
            skill = request.POST.get("skill")
            reply_id = request.POST.get("skill_id")
            skill_qs = None
            if reply_id:
                skill_qs = Skill.objects.get(id=reply_id)
            skill = Skill.objects.create(user=request.user, post=skill, reply=skill_qs)
            skill.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = SkillForm
    context = {"form": form, "skills": skills}
    if request.is_ajax():
        html = render_to_string("skillpost.html", context, request=request)
        return JsonResponse({"form": html})
    return render(request, "skills.html", context)


def Recently(request):
    hustleposts = Hustle.objects.all()
    context = {"hustleposts": hustleposts[0:5]}
    return render(request, "sidebar.html", context)
"""def search(request):
    query = request.GET.get('q', None)
    user = None
    if request.user.is_authenticated:
        user = request.user
    context = {"query": query}
    if query is not None:
        SearchQuery.objects.create(user=user, query=query)
        hustle_posts = Hustle.objects.search(query=query)
        context['hustle_posts'] = hustle_posts
    return render(request, 'search.html', context)
"""


def post_by_category(request, category_slug):
    categories = Category.objects.all()
    hustle_posts = Hustle.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        hustle_posts = hustle_posts.filter(category=category)
    template = 'categorylist.html'
    context = {"categories": categories, "category": category, "hustle_posts": hustle_posts}
    return render(request, template, context)

"""@login_required
def create(request, **kwargs):
    form = HustleForm(request.POST or None, request.FILES or None)
    files = request.FILES.getlist('media')
    if form.is_valid():
        obj = form.save(commit=False)
        if request.FILES:
            for f in request.FILES.getlist('media'):
                obj = Hustle.objects.create(media=f)
                obj.user = request.user
                obj.save()
                form = HustleForm()
                return redirect('/')
    context = {"form": form}
    return render(request, 'create.html', context)
"""
"""
class HustleCreate(LoginRequiredMixin, CreateView):
    model = Hustle
    form_class = HustleFullForm
    template_name = 'create.html'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('files')
        if form.is_valid():
            user = request.user
            hustle_name = form.cleaned_data['hustle_name']
            content = form.cleaned_data['content']
            category = form.cleaned_data['category']
            hustle_obj = Hustle.objects.create(user=user, hustle_name=hustle_name, content=content, category=category)
            for f in files:
                HustleMedia.objects.create(hustle=hustle_obj, file=f)
            return HttpResponseRedirect('/')
        else:
            return self.form_invalid(form)"""
"""
class HustleUpdateView(LoginRequiredMixin, UpdateView):
    model = Hustle
    form_class = HustleFullForm
    template_name = "update.html"
    success_url = reverse_lazy("/")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)"""


@login_required
def create(request):
    form = HustleFullForm(request.POST or None, request.FILES or None)
    files = request.FILES.getlist('files')
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        for f in files:
            HustleMedia.objects.create(hustle=obj, file=f)
        form = HustleForm()
        return redirect('/')
    context = {"form": form}
    return render(request, 'create.html', context)



@login_required
def update(request, slug):
    obj = get_object_or_404(Hustle, slug=slug)
    form = HustleFullForm(request.POST or None, request.FILES or None, instance=obj)
    files = request.FILES.getlist('files')
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        for f in files:
            HustleMedia.objects.create(hustle=obj, file=f)
        messages.info(request, "Successfully Updated!")
        return HttpResponseRedirect('/')
    context = {"form": form, "object": obj, "hustle_name": f"Update {obj.hustle_name}"}
    return render(request, 'update.html', context)


@login_required
def delete(request, slug):
    obj = get_object_or_404(Hustle, slug=slug)
    if request.method == 'POST':
        obj.delete()
        return redirect('/')
    context = {"object": obj}
    return render(request, 'delete.html', context)


def search(request):
    if request.method == "GET":
        q = request.GET.get('q')
        hustle = Hustle.objects.filter((Q(hustle_name__icontains=q) |
                  Q(category__name__icontains=q) |
                  Q(content__icontains=q) |
                  Q(user__username__icontains=q) |
                  Q(user__first_name__icontains=q) |
                  Q(user__last_name__icontains=q)
                  ))
        return render(request, 'search.html', {"hustle": hustle})


def search_auto(request):
  if request.is_ajax():
    q = request.GET.get('term', None)
    hustles = Hustle.objects.filter((Q(hustle_name__icontains=q) |
                                    Q(category__name__icontains=q) |
                                    Q(content__icontains=q) |
                                    Q(user__username__icontains=q) |
                                    Q(user__first_name__icontains=q) |
                                    Q(user__last_name__icontains=q)
                                    ))
    results = []
    for rs in hustles:
      hustle_json = {}
      hustle_json = rs.hustle_name
      results.append(hustle_json)
    data = json.dumps(results)
  else:
    data = 'fail'
  mimetype = 'application/json'
  return HttpResponse(data, mimetype)
