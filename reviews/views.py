from django.shortcuts import render


def reviews(request):
    """" A view to return the index page """
    return render(request, "reviews/reviews.html")
