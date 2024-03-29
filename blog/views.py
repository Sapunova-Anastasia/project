from django.http import Http404
from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import get_object_or_404, render_to_response
from .forms import PostForm
from .models import Post

# Create your views here.
def post_add(request):
	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return render(request, 'blog/post_edit.html', {'form': form})
	else:
		form = PostForm()
	return render(request, 'blog/post_edit.html', {'form': form})

def post_list(request):
	posts = Post.objects.for_user(user=request.user)
	return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, id):
	post = get_object_or_404(Post, id=id)
	if not post.is_publish() and not request.user.is_staff:
		raise Http404("Запись в блоге не найдена")
	return render(request, 'blog/post_detail.html', {'post': post})

def handler404(request, exception, template_name="404.html"):
    response = render_to_response("404.html")
    response.status_code = 404
    return response
	