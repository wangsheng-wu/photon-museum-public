from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('film-dictionary/', views.film_dictionary, name='film_dictionary'),
    path('film-dictionary/add/', views.film_dictionary_add, name='film_dictionary_add'),
    path('film-dictionary/modify/', views.film_dictionary_modify, name='film_dictionary_modify'),
    path('film-dictionary/data/<int:film_id>/', views.get_film_data, name='get_film_data'),
    path('artist-dictionary/', views.artist_dictionary, name='artist_dictionary'),
    path('artist-dictionary/add/', views.artist_dictionary_add, name='artist_dictionary_add'),
    path('artist-dictionary/modify/', views.artist_dictionary_modify, name='artist_dictionary_modify'),
    path("rollscan/add/", views.rollscan_add, name="rollscan_add"),
    path("rollscan/add/modify/", views.rollscan_add_modify, name="rollscan_add_modify"),
    path("rollscan/populate/", views.rollscan_populate, name="rollscan_populate"),
    path("rollscan/edit/", views.rollscan_edit, name="rollscan_edit"),
    path("home/", views.archive_home, name="archive_home"),
    path("library/rolls", views.roll_library, name="roll_library"),
    path("library/rolls/film-viewer/<int:roll_id>/", views.film_viewer, name="film_viewer"),
]

if settings.DEBUG:  # Serve media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
