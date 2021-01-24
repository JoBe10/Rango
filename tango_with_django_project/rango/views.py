from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page

def index(request):
    # Query the database for a list of ALL categories currently stored.
    # Order the categories by no. likes in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    # Place the list in your context_dict dictionary
    # that will be passed to the template engine.

    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list, 'pages': page_list}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render(request, 'rango/index.html', context_dict)

def about(request):
    return render(request, 'rango/about.html')

def show_category(request, category_name_slug):
    # Create a context dictionary which we can pass to the template rendering machine.
    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # Use get method to return the model instance ir raise DoesNotExist exception.
        category = Category.objects.get(slug=category_name_slug)

        # Retrieve all of the associated pages.
        # Filter() will return a list of page objects or an empty list.
        pages = Page.objects.filter(category=category)

        # Add our results list to the template context under name pages.
        context_dict['pages'] = pages

        # Also add the category object from teh database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category

    except Category.DoesNotExist:
        # Don't do anything - the template wll display the "no category" message for us.
        context_dict['category'] = None
        context_dict['pages'] = None

    # Render the response and return it to the client.
    return render(request, 'rango/category.html', context_dict)