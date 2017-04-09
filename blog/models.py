from django.db import models
from wagtail.wagtailcore.models import Page, Orderable, AbstractPage

from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel,\
    InlinePanel
from django.utils.translation import gettext_lazy as _
from wagtail.wagtailsearch import index
from wagtail.wagtailcore.fields import RichTextField, StreamField
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from taggit.models import TaggedItemBase
#from modelcluster.contrib.taggit import ClusterTaggableManager
##from cProfile import runctx
from modelcluster.tags import ClusterTaggableManager
from wagtail.wagtailsnippets.models import register_snippet
from django import forms
from django.contrib.auth.models import User
from wagtail.wagtailcore import blocks
from pip._vendor.pkg_resources import require
from wagtail.wagtailimages.blocks import ImageChooserBlock

#User = get_user_model()

class PersonBlock(blocks.StructBlock):
    first_name = blocks.CharBlock(required=True)
    last_name = blocks.CharBlock(required=True)
    photo = ImageChooserBlock()
    title = blocks.CharBlock(required=False)
    biography = blocks.RichTextBlock()
    webssite = blocks.URLBlock(required=False)

    class Meta:
        template  = 'blog/parts/person.html'
        icon  = 'user'
        
    def __str__(self):
        return self.first_name
    
    def __unicode__(self):
        return self.first_name

@register_snippet        
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    person = StreamField(PersonBlock())
    
    def __str__(self):
        return self.person
    
    def __unicode__(self):
        return self.person
    
    

@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=50)
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL,
                              related_name="+", null=True, blank=True)
    
    panels = [
        FieldPanel('name'),
        ImageChooserPanel('image')
        ]
    
    def __str__(self):
        return self.name
    
    def __unicode__(self):
        return self.name

class BlogIndexPage(Page):
    intro = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full')
        ]
    
    
    def get_context(self, request, *args, **kwargs):
        ctx = super(BlogIndexPage, self).get_context(request, *args, **kwargs)
        blogpages = self.get_children().live().order_by('-first_published_at')
        ctx['blogpages'] = blogpages
        
        return ctx
    

class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey('BlogPage', related_name="tagged_items")
    
    
class PageMixin(Page):
    date = models.DateField(_('Post Date'))
    intro = RichTextField(max_length=250)
    body = RichTextField()
    ##tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    categories = ParentalManyToManyField(BlogCategory, blank=True) 
    
    
    search_fields = Page.search_fields + [
            index.SearchField('intro'),
            index.SearchField('body'),
            ]
    
    content_panels = Page.content_panels +[
        MultiFieldPanel([
            FieldPanel('tags'),
            FieldPanel('date'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
            
            ], heading='Basic Information'),
        
        FieldPanel('intro'),
        FieldPanel('body', classname='full'),
        InlinePanel('gallery_images', label='Gallery Images')
        ]
    
    
    def main_image(self):
        
        gallery_image = self.gallery_images.first()
        
        if gallery_image:
            return gallery_image.image
        
        return None
    
        
    class Meta:
        abstract = True
        
class BlogPage(PageMixin):
    #date = models.DateField(_('Post Date'))
    #intro = RichTextField(max_length=250)
    #body = RichTextField()
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    #categories = ParentalManyToManyField(BlogCategory, blank=True)
    #author = models.ForeignKey(User, on_delete=models.SET_NULL,
    #                           related_name='blogs', null=True, blank=True)
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL,
                               related_name='blogauthors', null=True, 
                               blank=True)
    
    ### categories
    """
    search_fields = Page.search_fields + [
            index.SearchField('intro'),
            index.SearchField('body'),
            ]
    """
    content_panels = PageMixin.content_panels +[
        MultiFieldPanel([
            ##FieldPanel('tags'),
            FieldPanel('author')
            ], heading='Basic Information'),
        
        
        ]
    """
    
    
    def main_image(self):
        
        gallery_image = self.gallery_images.first()
        
        if gallery_image:
            return gallery_image.image
        
        return None
    
    """
            
    
class BlogPageGalleryImage(Orderable):
    
    page = ParentalKey(BlogPage, related_name='gallery_images')
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE,
                              related_name="+")
    caption = models.CharField(blank=True, max_length=250)
    
    
    panels =  [
            ImageChooserPanel('image'),
            FieldPanel('caption')
        ]
    
    
class BlogTagIndexPage(Page):
    
    def get_context(self, request, *args, **kwargs):
        ctx = super(BlogTagIndexPage, self).get_context(request, *args, **kwargs)
        tag = self.request.GET.get('tag', None)
        if tag is None:
            tag = 'blog'
            
        blogpages = BlogPage.objects.filter(tags__name=tag)
        
        ctx['blogpages'] = blogpages
            
        
        return ctx
    
@register_snippet   
class BlogPageComment(models.Model):
    post = models.ForeignKey(BlogPage, on_delete=models.CASCADE,
                             related_name='comments')
    commenter = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name='mycomments')
    body = RichTextField()
    
    