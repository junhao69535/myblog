from django.shortcuts import render,get_object_or_404

from .forms import ContactForm
from django.core.mail import send_mail,get_connection
from django.http import Http404, HttpResponse, HttpResponseRedirect
from .models import Post,Category,Tag
from comments.forms import CommentForm
from django.views.generic import ListView,DetailView
from django.db.models import Q

class IndexView(ListView):
        model=Post
        template_name='blog/index.html'
        context_object_name='post_list'
        paginate_by=10

        def get_context_data(self,**kwargs):
                context=super().get_context_data(**kwargs)
                paginator=context.get('paginator')
                page=context.get('page_obj')
                is_paginated=context.get('is_paginated')

                pagination_data=self.pagination_data(paginator,page,is_paginated)

                context.update(pagination_data)
                return context

        def pagination_data(self,paginator,page,is_paginated):
                if not is_paginated:
                        return {}
                left=[]
                right=[]

                left_has_more=False

                right_has_more=False

                first=False
                last=False

                page_number=page.number

                total_pages=paginator.num_pages

                page_range=paginator.page_range

                if page_number==1:
                    right=page_range[page_number:page_number+2]

                    if right[-1]<total_pages-1:
                        right_has_more=True

                    if right[-1]< total_pages:
                        last=True

                elif page_number==total_pages:
                    left=page_range[(page_number-3)if(page_number-3)>0 else 0:page_number-1]
                    if left[0]>2:
                        left_has_more=True

                    if left[0]>1:
                        first=True
                else:
                    left=page_range[(page_number-3) if (page_number-3) >0 else 0:page_number-1]
                    right=page_range[page_number:page_number+2]

                    if right[-1]<total_pages-1:
                        right_has_more=True

                    if right[-1]<total_pages:
                        last=True

                    if left[0]>2:
                        left_has_more=True

                    if left[0]>1:
                        first=True

                data={
                        'left':left,
                        'right':right,
                        'left_has_more':left_has_more,
                        'right_has_more':right_has_more,
                        'first':first,
                        'last':last,
                        }

                return data

def blog(request):
        return render(request,'blog/blog.html')

def about(request):
        return render(request,'blog/about.html')
	
def contact(request):
	if request.method=='POST':
		form=ContactForm(request.POST)
		if form.is_valid():
			cd=form.cleaned_data
			send_mail(
				cd.get('email','632226765@qq.com')+cd['subject'],
				cd['message'],
				'632226765@qq.com',
				['632226765@qq.com'],
				fail_silently=False
				)
			return HttpResponseRedirect('/contact/thanks/')
	else:
		form=ContactForm()
	return render(request,'blog/contact.html',{'form':form})

def thanks(request):
	return render(request,'blog/thanks.html')

def search(request):
        q=request.GET.get('q')
        error_msg=''

        if not q:
                error_msg="请输入关键词"
                return render(request,'blog/index.html',{'error_msg':error_msg})
        post_list=Post.objects.filter(Q(title__icontains=q)|Q(body__icontains=q))
        return render(request,'blog/index.html',{'error_msg':error_msg,
                                                 'post_list':post_list
                                                 })

class TagView(ListView):
        model=Post
        template_name='blog/index.html'
        context_object_name='post_list'

        def get_queryset(self):
                tag=get_object_or_404(Tag,pk=self.kwargs.get('pk'))
                return super(TagView,self).get_queryset().filter(tags=tag)


class PostDetailView(DetailView):
        model=Post
        template_name='blog/detail.html'
        context_object_name='post'

        def get(self,request,*args,**kwargs):
                response=super(PostDetailView,self).get(request,*args,**kwargs)
                self.object.increase_views()
                return response

        def get_object(self,queryset=None):
                post=super(PostDetailView,self).get_object(queryset=None)
                return post

        def get_context_data(self,**kwargs):
                context=super(PostDetailView,self).get_context_data(**kwargs)
                form=CommentForm()
                comment_list=self.object.comment_set.all()
                context.update({
                        'form':form,
                        'comment_list':comment_list
                        })
                return context

class ArchivesView(ListView):
        model=Post
        template_name='blog/index.html'
        context_object_name='post_list'

        def get_queryset(self):
                return super(ArchivesView,self).get_queryset().filter(created_time__year=self.kwargs.get('year'),created_time__month=self.kwargs.get('month'))



class CategoryView(ListView):
        model=Post
        template_name='blog/index.html'
        context_object_name='post_list'

        def get_queryset(self):
                cate=get_object_or_404(Category,pk=self.kwargs.get('pk'))
                return super(CategoryView,self).get_queryset().filter(category=cate)
