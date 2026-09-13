from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Movie, Review


def index(request):
    search_term = request.GET.get('search')

    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()

    template_data = {
        'title': 'Movies',
        'movies': movies,
    }

    return render(
        request,
        'movies/index.html',
        {'template_data': template_data}
    )


def show(request, id):
    movie = get_object_or_404(Movie, id=id)

    reviews = Review.objects.filter(
        movie=movie,
        reported=False
    )

    template_data = {
        'title': movie.name,
        'movie': movie,
        'reviews': reviews,
    }

    return render(
        request,
        'movies/show.html',
        {'template_data': template_data}
    )


@login_required
def create_review(request, id):
    movie = get_object_or_404(Movie, id=id)

    if request.method == 'POST':
        comment = request.POST.get('comment', '').strip()

        if comment:
            Review.objects.create(
                comment=comment,
                movie=movie,
                user=request.user
            )

    return redirect('movies.show', id=id)


@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(
        Review,
        id=review_id,
        movie_id=id
    )

    if request.user != review.user:
        return redirect('movies.show', id=id)

    if request.method == 'POST':
        comment = request.POST.get('comment', '').strip()

        if comment:
            review.comment = comment
            review.save()

            return redirect('movies.show', id=id)

    template_data = {
        'title': 'Edit Review',
        'review': review,
    }

    return render(
        request,
        'movies/edit_review.html',
        {'template_data': template_data}
    )


@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(
        Review,
        id=review_id,
        movie_id=id,
        user=request.user
    )

    review.delete()

    return redirect('movies.show', id=id)


@login_required
def report_review(request, id, review_id):
    review = get_object_or_404(
        Review,
        id=review_id,
        movie_id=id
    )

    if review.user != request.user:
        review.reported = True
        review.save()

    return redirect('movies.show', id=id)