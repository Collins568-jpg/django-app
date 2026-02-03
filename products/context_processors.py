from .models import Category

def categories_context(request):
    """Make categories available to all templates"""
    categories = Category.objects.all()
    return {'all_categories': categories}