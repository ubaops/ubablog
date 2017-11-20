from django.shortcuts import render
from .models import Post,Category,Tag
from django.shortcuts import render, get_object_or_404
# Create your views here.
from django.http import HttpResponse
import markdown
from comments.forms import CommentForm
#首页
def uba(request):
    return render(request, 'blog/uba.html')

#blog index
def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})

#详情页
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.increase_views()
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                     'markdown.extensions.extra',
                                     'markdown.extensions.codehilite',
                                     'markdown.extensions.toc',
                                  ])
    form = CommentForm()
    # 获取这篇 post 下的全部评论
    comment_list = post.comment_set.all()
    tag_list = post.tags.all()   
    # 将文章、表单、以及文章下的评论列表作为模板变量传给 detail.html 模板，以便渲染相应数据。
    context = {'post': post,
               'form': form,
               'comment_list': comment_list,
               'tag_list':tag_list
               }
    return render(request, 'blog/detail.html', context=context)

#归档
def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month).order_by('-created_time')
    print(post_list)
    return render(request, 'blog/index.html', context={'post_list': post_list})
#分类
def category(request, pk):
    # 记得在开始部分导入 Category 类
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})

def tag(request,pk):
    tags=get_object_or_404(Tag,pk=pk)
    post_list = Post.objects.filter(tags=tags).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})