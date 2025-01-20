from django.contrib import admin
from .models import Film
from .models import Artist
from .models import RollScan
from .models import AllMedia

@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ('film_name', 'film_type', 'iso', 'description', 'cover_image')

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('preferred_name', 'first_name', 'last_name', 'birth_date', 'gender')
    search_fields = ('preferred_name', 'first_name', 'last_name')
    list_filter = ('gender', 'birth_date')

@admin.register(RollScan)
class RollScanAdmin(admin.ModelAdmin):
    list_display = ('id', 'film_type', 'count', 'location', 'develop_date', 'scan_date', 'is_active')
    list_filter = ('film_type', 'is_active', 'develop_date', 'scan_date')
    search_fields = ('film_type__film_name', 'location', 'description')

@admin.register(AllMedia)
class AllMediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'media_type', 'title', 'author', 'date', 'location', 'is_active')  # Adjust fields as needed
    search_fields = ('id', 'media_type', 'title')  # Add fields for searching
    list_filter = ('media_type', 'is_active')  # Add filters if needed