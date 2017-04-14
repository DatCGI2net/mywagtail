from __future__ import absolute_import, unicode_literals

from django.db import models

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel,\
    MultiFieldPanel
from django.db.models import SET_NULL
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch.index import SearchField
from wagtail.wagtailforms.models import AbstractForm, AbstractFormField
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.wagtailforms.edit_handlers import FormSubmissionsPanel



from wagtail.wagtailsnippets.models import register_snippet
from django import forms

from wagtail.wagtaildocs.models import Document



from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel




@register_snippet
class FooterItem(models.Model):
    #order = models.IntegerField(default=1)
    title = models.CharField(max_length=100)
    body = models.TextField(blank=True, null=True)
    
    panels = [
        #FieldPanel(order),
        FieldPanel('title'),
        FieldPanel('body'),
        
        ]
    
    def __str__(self):
        return self.title
    
    def __unicode__(self):
        return self.title
    

@register_snippet
class Client(models.Model):
    name = models.CharField(max_length=50)
    contact_title = models.CharField(max_length=20, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    testimonial = models.TextField(blank=True, null=True)
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=SET_NULL, related_name='+',
        blank=True, null=True
        )
    
    
    def __str__(self):
        return self.name
    
    
    panels = [
        FieldPanel('name'),
        FieldPanel('url'),
        FieldPanel('contact_title'),
        FieldPanel('testimonial', classname='full'),
        ImageChooserPanel('image')
        ]
    

class ProjectDocument(Document):
    project = ParentalKey('home.ProjectPage', blank=True,
                          related_name='project_docs')

    
class ProjectPage(Page):
    
    
    page = ParentalKey('blog.BlogPage', related_name='projectpage',
                       on_delete=models.SET_NULL, blank=True, null=True)
    
    client = models.ForeignKey(Client, on_delete=models.SET_NULL,
                               blank=True,
                               null=True, related_name='projects')
    
    search_fields = Page.search_fields + [
        SearchField('project_docs'),
        
        
        ]
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            #FieldPanel('start_date'),
            #FieldPanel('end_date'),
            FieldPanel('client')
            
            ], "Project Info"),
        
        InlinePanel("project_docs"),
        FieldPanel('page')                                       
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
    

class FAQIndexPage(Page):
    body = RichTextField()
    
    content_panels = Page.content_panels + [
        FieldPanel('body')
        ]
    
class FAQPage(Page):
    ##ask = RichTextField()
    answer = RichTextField()
    
    content_panels = Page.content_panels + [
        #FieldPanel('ask'),
        FieldPanel('answer')
        ]
    
    search_fields = Page.search_fields + [
        ##SearchField('ask'),
        SearchField('answer')
        ] 
        
class HomePage(Page):
    heading = models.TextField(blank=True, null=True)
    subheading = models.TextField(blank=True, null=True)
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=SET_NULL, related_name='+',
        blank=True, null=True
        )
    body = RichTextField()
    
    featured_portfolio =  models.ForeignKey('PortfolioIndexPage', blank=True,
                                    on_delete=SET_NULL, null=True)
    
    ourservices =  models.ForeignKey('ServiceIndexPage', blank=True,
                                    on_delete=SET_NULL, null=True)
    
        
    aboutAgent = RichTextField(blank=True, null=True)
    
    ourfaqs = models.ForeignKey('FAQIndexPage', blank=True,
                                    on_delete=SET_NULL, null=True)
    
    latestposts = models.ForeignKey('blog.BlogIndexPage', blank=True,
                                    on_delete=SET_NULL, null=True)
    
    """
    clientblock = models.ForeignKey('ClientPageBlock', blank=True, null=True,
                              on_delete=SET_NULL, related_name='+')
    """
    
    testimonial = models.ForeignKey(Client, blank=True, null=True,
                                    on_delete=SET_NULL, related_name='+')
    
    
    content_panels = Page.content_panels + [
        SnippetChooserPanel('testimonial'),
        FieldPanel('heading'),
        FieldPanel('subheading'),
        ImageChooserPanel('image'),
        FieldPanel('body', classname='full'),
        #InlinePanel("teams",label="Home Teams"),
        InlinePanel("clients", label="Home Clients"),
        FieldPanel("featured_portfolio"),
        FieldPanel("ourservices"),
        FieldPanel("ourfaqs"),
        FieldPanel("ourfaqs"),
        FieldPanel('latestposts'),
        ##FieldPanel('clientblock'),
        
        ]
    
    def get_context(self, request, *args, **kwargs):
        ctx = super(HomePage, self).get_context(request, *args, **kwargs)
        if self.featured_portfolio is not None:
                
            portfolios = ProjectPage.objects.child_of(self.featured_portfolio).order_by('-first_published_at')
            ctx['portfolios'] = portfolios
            print('portfolios:', portfolios)
            
        if self.ourservices is not None:
            print('ourservice:', self.ourservices)
            
                
            services = ProjectPage.objects.child_of(self.ourservices)
            
            ##services = self.ourservices.get_children().live().order_by('-first_published_at')
            ctx['services'] = services
            print('services:', services)
            
        if self.ourfaqs is not None:
            faqs = self.ourfaqs.get_children()
            ctx['faqpages'] = faqs
            print('faqpages:', faqs)
            
        if self.latestposts is not None:
            latestposts = self.latestposts.get_children()
            ctx['posts'] = latestposts
            print('latestposts:', latestposts)
            
        
        return ctx 
    
class ClientHomePage(Orderable, models.Model):
    
    homepage = ParentalKey(HomePage, related_name="clients")
    client = models.ForeignKey(Client, related_name='+')
    
    panels = [
        SnippetChooserPanel('client'),
        ]    
    
    def __str__(self):
        return self.page.title + ' -> ' + self.client.name    

    
COLUMNS_CHOICES = (
    ('6', 'Two columns'), # two columns use span6
    ('4', 'Three columns'), # three columns use span4
    ('3', 'Four Columns'), # four columns use span3
)
    
class ServiceIndexPage(Page):
    
    column = models.CharField(choices=COLUMNS_CHOICES, default=3,
                              max_length=1)
    body = RichTextField(blank=True, null=True)
    
"""
@register_snippet    
class ClientPageBlock(models.Model):
    testimonial = models.ForeignKey(Client, blank=True, null=True,
                                    on_delete=SET_NULL, related_name='+')
    
    panels =   [
        SnippetChooserPanel('testimonial'),
        SnippetChooserPanel('clientblocks')
        ]
    
    

class ClientPagePlacements(Orderable, models.Model):
    
    clientblock = models.ForeignKey(ClientPageBlock, related_name="clientblocks")
    client = models.ForeignKey(Client, related_name='+')
    
    panels = [
        SnippetChooserPanel('client'),
        ]    
    
    def __str__(self):
        return self.page.title + ' -> ' + self.client.name
    
"""
    
class PortfolioIndexPage(Page):
    
    column = models.CharField(choices=COLUMNS_CHOICES, default=3,
                              max_length=1)

    body = RichTextField(blank=True, null=True)
    
    
    

    

##AbstractPage
class AboutPage(Page):
    body = RichTextField()
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=SET_NULL, related_name='+',
        blank=True, null=True
        )
    testimonial = models.ForeignKey(Client, blank=True, null=True,
                                    on_delete=SET_NULL, related_name='+')
    
    teams = ParentalManyToManyField('blog.Profile', blank=True)
    
    ##clientblock = models.ForeignKey('ClientPageBlock', blank=True, null=True,
    ##                          on_delete=SET_NULL, related_name='+')
    
    #clients = ParentalManyToManyField(Client, blank=True)
    
    search_fields = Page.search_fields + [
        SearchField('body')
        ]
    
    
    
    content_panels = Page.content_panels + [
        FieldPanel('body', classname='full'),
        ImageChooserPanel('image'),
        FieldPanel("teams", widget=forms.CheckboxSelectMultiple),
        #FieldPanel("clientblock"),
        SnippetChooserPanel('testimonial'),
        InlinePanel("clients", label="Our Clients"),                                       
        ]


    
class ClientAboutPage(Orderable, models.Model):
    
    aboutpage = ParentalKey(AboutPage, related_name="clients")
    client = models.ForeignKey(Client, related_name='+')
    
    panels = [
        SnippetChooserPanel('client'),
        ]    
    
    def __str__(self):
        return self.page.title + ' -> ' + self.client.name    

    