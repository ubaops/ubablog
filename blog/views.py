from django.shortcuts import render
from .models import Post,Category,Tag
from django.shortcuts import render, get_object_or_404
# Create your views here.
from django.http import HttpResponse
import markdown
from comments.forms import CommentForm
from django.views.generic import ListView, DetailView
#首页
def uba(request):
    return render(request, 'blog/uba.html')


#index类视图
class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

#blog index
def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})

#detail类视图
class PostdetailView(DetailView):
    model=Post
    template_name='blog/detail.html'
    context_object_name='post'

    def get(self,request,*args,**kwargs):
        response = super(PostdetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response

    def get_object(self,queryset=None):
        post = super(PostdetailView, self).get_object(queryset=None)
        post.body = markdown.markdown(post.body,
                                  extensions=[
                                     'markdown.extensions.extra',
                                     'markdown.extensions.codehilite',
                                     'markdown.extensions.toc',
                                  ])
        return post

    def get_context_data(self,**kwargs):
        context = super(PostdetailView, self).get_context_data(**kwargs)
        tag_list = self.object.tags.all()
        form=CommentForm()
        comment_list=self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list,
            'tag_list':tag_list
        })
        return context

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

#archives类视图
class ArchivesView(IndexView):
    def get_queryset(self):
        #cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(ArchivesView, self).get_queryset().filter(created_time__year=self.kwargs.get('year'),created_time__month=self.kwargs.get('month')).order_by('-created_time')

#归档
def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month).order_by('-created_time')
    #print(post_list)
    return render(request, 'blog/index.html', context={'post_list': post_list})

#category类视图
class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)

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