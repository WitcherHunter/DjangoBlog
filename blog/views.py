from django.shortcuts import render,get_object_or_404
from .models import Post, Category, Tag
from django.http import HttpResponse
import markdown
from comments.forms import CommentForm
from django.views.generic import ListView,DetailView

# Create your views here.
class IndexView(ListView):
	model = Post
	template_name = 'blog/index.html'
	context_object_name = 'post_list'
	paginate_by = 1

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		paginator = context.get('paginator')
		page = context.get('page_obj')
		is_paginated = context.get('is_paginated')

		pagination_data = self.pagination_data(paginator, page, is_paginated)

		context.update(pagination_data)

		return context


	def pagination_data(self, paginator, page, is_paginated):
		if not is_paginated:
			return {}
		#当前页左边的连续页码
		left = []
		#当前页右边的连续页码
		right = []
		#是否显示左边省略号
		left_has_more = False
		#是否显示右边省略号
		right_has_more = False
		#是否显示第一页页码
		first = False
		#是否显示最后一页页码
		last = False

		page_number = page.number

		total_pages = paginator.num_pages

		page_range = paginator.page_range

		if page_number == 1:
			right = page_range[page_number : page_number + 2]

			if right[-1] < total_pages - 1:
				right_has_more = True

			if right[-1] < total_pages:
				last = True
		elif page_number == total_pages:
			left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

			if left[0] > 2:
				left_has_more = True

			if left[0] > 1:
				first = True
		else:
			left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
			right = page_range[page_number:page_number + 2]

			if right[-1] < total_pages - 1:
				right_has_more = True
			if right[-1] < total_pages:
				last = True

			if left[0] > 2:
				left_has_more = True
			if left[0] > 1:
				first = True

		data = {
			'left':left,
			'right':right,
			'left_has_more':left_has_more,
			'right_has_more':right_has_more,
			'first':first,
			'last':last
		}

		return data

class PostDetailView(DetailView):
	model = Post
	template_name = 'blog/detail.html'
	context_object_name = 'post'
	pk_url_kwarg = "post_id"

	def get(self, request, *args, **kwargs):
		response = super(PostDetailView, self).get(request, *args, **kwargs)
		self.object.increase_views()
		return response

	def get_object(self, queryset = None):
		post = super(PostDetailView, self).get_object(queryset = None)
		post.body = markdown.markdown(post.body, extensions = ['markdown.extensions.extra','markdown.extensions.codehilite', 'markdown.extensions.toc'])
		return post

	def get_context_data(self, **kwargs):
		context = super(PostDetailView, self).get_context_data(**kwargs)
		form = CommentForm()
		comment_list = self.object.comment_set.all()
		context.update({'form': form, 'comment_list': comment_list})
		return context

class ArchiveView(ListView):
	model = Post
	template_name = 'blog/index.html'
	context_object_name = 'post_list'

	def get_queryset(self):
		post_year = self.kwargs.get('year')
		post_month = self.kwargs.get('month')
		return super(ArchiveView, self).get_queryset().filter(created_time__year = post_year, created_time__month = post_month)

class CategoryView(ListView):
	model = Post
	template_name = 'blog/index.html'
	context_object_name = 'post_list'

	def get_queryset(self):
		cate = get_object_or_404(Category, pk = self.kwargs.get('category_id'))
		return super(CategoryView, self).get_queryset().filter(category = cate)

class TagView(ListView):
	model = Post
	template_name = 'blog/index.html'
	context_object_name = 'post_list'
	pk_url_kwarg = "tag_id"

	def get_queryset(self):
		tag = get_object_or_404(Tag, pk = self.kwargs.get('tag_id'))
		return super(TagView, self).get_queryset().filter(tags = tag)



