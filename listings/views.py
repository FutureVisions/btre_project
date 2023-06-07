from django.shortcuts import render, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .choices import price_choices, bedroom_choices, state_choices

from .models import Listing

def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)

    paginator = Paginator(listings, 6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context = {
        'listings': paged_listings
    }
    return render(request, 'listings.html', context)

def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    context = {
        'listing': listing
    }
    return render(request, 'listing.html', context)

def search(request):
    queryset_list = Listing.objects.order_by('-list_date')

    # Keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords)
    # City
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = queryset_list.filter(city__iexact=city)
    # State (exact match)
    if "state" in request.GET:
        state = request.GET["state"]
        if state:
            if state != "State (All)":
                queryset_list = queryset_list.filter(state__iexact=state)
    
    # bedrooms 
    if "bedrooms" in request.GET:
        bedrooms = request.GET["bedrooms"]
        if bedrooms:
            try:
                check_integer = int(bedrooms)
                queryset_list = queryset_list.filter(bedrooms__iexact=bedrooms)
            except ValueError:
                pass  # ignore non numeric values and show them all
    
    # price (less than or equal match)
    #Price
    if 'price' in request.GET:
        price = request.GET['price']
        if (int(price)>=1000000):
            filterValue = queryset_list.filter(price__gte=price)
            queryset_list = filterValue  
        else:
            filterValue = queryset_list.filter(price__lte=price)
            queryset_list = filterValue  
    context = {
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'listings': queryset_list,
        'value': request.GET
    }
    return render(request, 'search.html', context)

