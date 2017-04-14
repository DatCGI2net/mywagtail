from django import template
from home.models import FooterItem

register = template.Library()

@register.inclusion_tag('home/tags/footer.html', takes_context=True)
def footer(context):
    items = []
    
    try:
        
        items = FooterItem.objects.all()[:3]
    
        print('items:')
    except Exception as err:
        print('error:', err)
    
    return {
        'footerItems': items,
        'request': context['request']
        }
    