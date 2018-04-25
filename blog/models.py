from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.six import python_2_unicode_compatible
import markdown
from django.utils.html import strip_tags

# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length = 100)

	def __str__(self):
		return self.name

class Tag(models.Model):
	name = models.CharField(max_length = 100)

	def __str__(self):
		return self.name

@python_2_unicode_compatible
class Post(models.Model):
	#标题
	title = models.CharField(max_length = 70)
	#正文
	body = models.TextField()
	#创建时间
	created_time = models.DateTimeField()
	#修改时间
	modified_time = models.DateTimeField()
	#摘要
	excerpt = models.CharField(max_length = 200, blank = True)
	#分类
	category = models.ForeignKey(Category, on_delete = models.CASCADE)
	#标签
	tags = models.ManyToManyField(Tag, blank = True)
	#作者
	author = models.ForeignKey(User, on_delete = models.CASCADE)
	#阅读量
	views = models.PositiveIntegerField(default = 0)

	def __str__(self):
		return "title is %s, body is %s, category is %s, tags is %s, author is %s" % (self.title, self.body, self.category, self.tags, self.author)

	def get_absolute_url(self):
		return reverse('blog:detail', kwargs = {'post_id':self.pk})

	def increase_views(self):
		self.views += 1
		self.save(update_fields = ['views'])

	def save(self, *args, **kwargs):
		if not self.excerpt:
			md = markdown.Markdown(extensions = ['markdown.extensions.extra', 'markdown.extensions.codehilite'])
			self.excerpt = strip_tags(md.convert(self.body))[:54]

		super(Post,self).save(*args, **kwargs)

	class Meta:
		ordering = ['-created_time']