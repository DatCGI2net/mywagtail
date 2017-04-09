from __future__ import absolute_import, unicode_literals

from django.db import models

from wagtail.wagtailcore.models import Page, Orderable, AbstractPage
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel,\
    MultiFieldPanel, FieldRowPanel
from django.db.models import SET_NULL
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch.index import SearchField
from wagtail.wagtailforms.models import AbstractForm, AbstractFormField,\
    AbstractFormSubmission
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.wagtailforms.edit_handlers import FormSubmissionsPanel
from django.db.models.fields import DateField
from modelcluster.tags import ClusterTaggableManager
from django.contrib.auth.models import User
from wagtail.wagtailsnippets.models import register_snippet
from django import forms
from taggit.models import TaggedItemBase
from wagtail.wagtaildocs.models import Document
from blog.models import PageMixin
from wagtail.wagtailcore import blocks




@register_snippet
class Client(models.Model):
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=20, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    testimonial = RichTextField(blank=True, null=True)
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=SET_NULL, related_name='+',
        blank=True, null=True
        )
    
    
    def __str__(self):
        return self.name
    
    
    panels = [
        FieldPanel('name'),
        FieldPanel('url'),
        FieldPanel('testimonial', classname='full'),
        ImageChooserPanel('image')
        ]
    

class ProjectDocument(Document):
    project = ParentalKey('home.ProjectPage', blank=True,
                          related_name='project_docs')


    
class ProjectPage(PageMixin):
    #page = ParentalKey(BlogPage, on_delete=models.CASCADE)
    #start_date = DateField(blank=True, null=True)
    #end_date = DateField(blank=True, null=True)
    
    ## override
    author = models.ForeignKey(User, on_delete=models.SET_NULL,
                               related_name='pageauthors', null=True, 
                               blank=True)
    
    client = models.ForeignKey(Client, on_delete=models.SET_NULL,
                               blank=True,
                               null=True, related_name='projects')
    
    search_fields = PageMixin.search_fields + [
        SearchField('project_docs'),
        
        
        ]
    
    content_panels = PageMixin.content_panels + [
        MultiFieldPanel([
            #FieldPanel('start_date'),
            #FieldPanel('end_date'),
            FieldPanel('client')
            
            ], "Project Info"),
        
        InlinePanel("project_docs")                                       
        ]


class PageGalleryImage(Orderable):
    
    page = ParentalKey(ProjectPage, related_name='gallery_images')
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE,
                              related_name="+")
    caption = models.CharField(blank=True, max_length=250)
    
    
    panels =  [
            ImageChooserPanel('image'),
            FieldPanel('caption')
        ]
    
        
class FormField(AbstractFormField):
    
    page = ParentalKey('ContactPage', related_name='form_fields')
        
class ContactPage(AbstractForm):
    intro = RichTextField()
    thankyou_text = RichTextField(blank=True)
    
    
    search_fields = Page.search_fields + [
        SearchField('intro')
        ]
    
    content_panels = AbstractForm.content_panels + [
                 FormSubmissionsPanel(),
                 FieldPanel('intro', classname="full"),
                 InlinePanel('form_fields', label='Form Fields'),
                 FieldPanel('thankyou_text', classname="full"),
                
                 ]
    
    
    def process_form_submission(self, form):
        
        results = super(ContactPage, self).process_form_submission(form)
        print('form:', form.cleaned_data)
        print('results:', results)
        return results
    
"""    
class HomeClient(Orderable):
    page = ParentalKey('HomePage', blank=True, related_name='clients')
    client = models.ForeignKey(Client, blank=True, on_delete=models.SET_NULL,
                               null=True)
class HomeUser(Orderable):
    page = ParentalKey('HomePage', blank=True, related_name='teams')
    profile = models.ForeignKey('blog.Profile', blank=True, on_delete=models.SET_NULL,
                               null=True)
class HomePortfolio(Orderable):
    page = ParentalKey('HomePage', blank=True, related_name='portfolios')
    projectpage = models.ForeignKey(ProjectPage, blank=True, on_delete=models.SET_NULL,
                               null=True)
    
class HomeService(Orderable):
    page = ParentalKey('HomePage', blank=True, related_name='services')
    projectpage = models.ForeignKey(ProjectPage, blank=True, on_delete=models.SET_NULL,
                               null=True)
"""
                               
                               
class TestimonialBlock(blocks.StaticBlock):
    
    class Meta:
        icon = 'comment-o'
        label = 'Testimonial Block'
        admin_text = '{label}: Configure elsewhere'.format(label=label)
        template = 'home/parts/testimonial.html'
        
class ClientBlock(blocks.StaticBlock):
    
    class Meta:
        icon = 'client'
        label = 'OUR CLIENTS'
        admin_text = '{label}: Configure elsewhere'.format(label=label)
        template = 'home/parts/homeclients.html'
    
        
class HomePage(Page):
    heading = RichTextField()
    subheading = RichTextField()
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=SET_NULL, related_name='+',
        blank=True, null=True
        )
    body = RichTextField()

    
    
    #portfolios = ParentalManyToManyField(ProjectPage, blank=True, 
    #                                     related_name="portfolio_projects")
    #services = ParentalManyToManyField(ProjectPage, blank=True,
    #                                   related_name="service_project")
    #teams = ParentalManyToManyField('blog.Profile', blank=True)
    #clients = ParentalManyToManyField(Client, blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('heading', classname="full"),
        FieldPanel('subheading', classname="full"),
        ImageChooserPanel('image'),
        FieldPanel('body', classname='full'),
        #InlinePanel("teams",label="Home Teams"),
        #InlinePanel("clients", label="Home Clients"),
        #InlinePanel("portfolios", label="Home Portfolios"),
        #InlinePanel("services", label="Home Services"),
                                               
        ]
    
    
#class Blurb():

##AbstractPage
class AboutPage(Page):
    body = RichTextField()
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=SET_NULL, related_name='+',
        blank=True, null=True
        )
    
    
    teams = ParentalManyToManyField('blog.Profile', blank=True)
    clientblock = StreamField([
            ('testimonial', TestimonialBlock()),
            ('client', ClientBlock()),
        ]
        )
    
    #clients = ParentalManyToManyField(Client, blank=True)
    
    search_fields = Page.search_fields + [
        SearchField('body')
        ]
    
    
    
    content_panels = Page.content_panels + [
        FieldPanel('body', classname='full'),
        
        FieldPanel("teams", widget=forms.CheckboxSelectMultiple),
        #FieldPanel("clients", widget=forms.CheckboxSelectMultiple),
                                               
        ]

    