from django.db import models

class Film(models.Model):
    film_name = models.CharField(max_length=255)
    film_type = models.CharField(max_length=50)
    iso = models.IntegerField()
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='film_covers/')

    def __str__(self):
        return f"{self.id} - {self.film_name} - {self.film_type}"
    

class Artist(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    preferred_name = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    death_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=20, choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    cover_image = models.ImageField(upload_to='artist_covers/', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



class RollScan(models.Model):
    film_type = models.ForeignKey("Film", on_delete=models.CASCADE)
    count = models.PositiveIntegerField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    develop_date = models.DateField(null=True, blank=True)
    scan_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Roll {self.id} - {self.film_type}"


class AllMedia(models.Model):
    id = models.CharField(max_length=10, primary_key=True)  # Unique media ID
    media_type = models.CharField(max_length=255)  # Type of media (e.g., "film_scan")
    title = models.CharField(max_length=255, null=True, blank=True)  # Optional title
    author = models.ForeignKey(Artist, on_delete=models.SET_NULL, null=True, blank=True)  # Link to Artist
    date = models.DateField(null=True, blank=True)  # Optional date
    location = models.CharField(max_length=255, null=True, blank=True)
    media_src = models.CharField(max_length=255, null=True, blank=True)  # Allow null
    media_src_2 = models.CharField(max_length=255, null=True, blank=True)  # Allow null
    description = models.TextField(null=True, blank=True)  # Optional description
    is_active = models.BooleanField(default=True)  # Default to active

    def __str__(self):
        return f"{self.id} - {self.media_type}"