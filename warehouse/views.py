from django.shortcuts import render, get_object_or_404, redirect
from .forms import FilmForm
from .models import Film
from django.http import JsonResponse
import logging
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings
LIBRARY_DIR = os.path.join(settings.MEDIA_ROOT, "library")
from .models import AllMedia
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import F, Value
from django.db.models.functions import Concat
from collections import defaultdict
from datetime import datetime
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from django.db.models.functions import Concat
from datetime import date, timedelta
import json

# Display film dictionary
def film_dictionary(request):
    films = Film.objects.all()
    return render(request, 'warehouse/film_dictionary.html', {'films': films})

def film_dictionary_add(request):
    if request.method == 'POST':
        form = FilmForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            # Check if it's an AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Film added successfully!'})
            
            # For non-AJAX form submissions, redirect
            return redirect('film_dictionary_add')
        
        # Handle invalid form submissions for AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': 'Invalid form data.'}, status=400)
    else:
        form = FilmForm()
    
    # Render the form for traditional GET requests
    return render(request, 'warehouse/film_dictionary_add.html', {'form': form})

def film_dictionary_modify(request):
    films = Film.objects.all()
    if request.method == 'POST':
        if 'modify-film-type' in request.POST:
            film_id = request.POST.get('film_id')
            film = get_object_or_404(Film, id=film_id)
            form = FilmForm(request.POST, request.FILES, instance=film)
            if form.is_valid():
                # Handle cover image replacement
                if 'cover_image' in request.FILES:
                    # Delete the old file if it exists
                    if film.cover_image:
                        original_file_name = Film.objects.get(id=film.id).cover_image.name
                        print(f"Original relative path in cover_image.name: {original_file_name}")
                        if not original_file_name.startswith("film_covers/"):
                            original_file_name = f"film_covers/{original_file_name}"
                        old_file_path = os.path.join(settings.MEDIA_ROOT, original_file_name)
                        if os.path.exists(old_file_path):
                            os.remove(old_file_path)

                    # Generate a unique filename if necessary
                    new_file = request.FILES['cover_image']
                    file_name = new_file.name
                    cover_image_path = os.path.join(settings.MEDIA_ROOT, 'film_covers/')
                    os.makedirs(cover_image_path, exist_ok=True)  # Ensure the directory exists
                    existing_files = os.listdir(cover_image_path)

                    if file_name in existing_files:
                        name, ext = os.path.splitext(file_name)
                        random_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
                        file_name = f"{name}_{random_suffix}{ext}"

                    # Save the new file with a unique name
                    file_path = os.path.join(cover_image_path, file_name)
                    with open(file_path, 'wb+') as destination:
                        for chunk in new_file.chunks():
                            destination.write(chunk)

                    # Update the cover_image field in the form
                    film.cover_image = f"film_covers/{file_name}"

                form.save()
                return JsonResponse({'success': True, 'message': 'Film updated successfully.'})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid form submission.', 'errors': form.errors})
        elif 'delete-film-type' in request.POST:
            film_id = request.POST.get('film_id')
            film = get_object_or_404(Film, id=film_id)
            # Delete the associated cover image if it exists
            if film.cover_image:
                original_file_name = Film.objects.get(id=film.id).cover_image.name
                if not original_file_name.startswith("film_covers/"):
                    original_file_name = f"film_covers/{original_file_name}"
                old_file_path = os.path.join(settings.MEDIA_ROOT, original_file_name)
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)
            
            film.delete()
            return JsonResponse({'success': True, 'message': 'Film deleted successfully.'})
    else:
        form = FilmForm()
    films_data = [
        {
            'id': film.id,
            'film_name': film.film_name,
            'film_type': film.film_type,
            'iso': film.iso,
            'description': film.description,
            'cover_image_url': film.cover_image.url if film.cover_image else None,
        }
        for film in films
    ]
    return render(request, 'warehouse/film_dictionary_modify.html', {
        'form': form,
        'films': films,
        'films_data': films_data,
    })

def get_film_data(request, film_id):
    film = get_object_or_404(Film, id=film_id)
    return JsonResponse({
        'film_name': film.film_name,
        'film_type': film.film_type,
        'iso': film.iso,
        'description': film.description,
        'cover_image': film.cover_image.url if film.cover_image else ''
    })


from .models import Artist
from .forms import ArtistForm

def artist_dictionary(request):
    artists = Artist.objects.all()
    return render(request, 'warehouse/artist_dictionary.html', {'artists': artists})

def artist_dictionary_add(request):
    if request.method == 'POST':
        form = ArtistForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Artist added successfully!', 'success': True})
        return JsonResponse({'message': 'Error adding artist.', 'success': False})
    else:
        form = ArtistForm()
    return render(request, 'warehouse/artist_dictionary_add.html', {'form': form})


logger = logging.getLogger(__name__)

def artist_dictionary_modify(request):
    artists = Artist.objects.all()
    if request.method == 'POST':
        if 'modify-artist' in request.POST:
            artist_id = request.POST.get('artist_id')
            artist = get_object_or_404(Artist, id=artist_id)
            form = ArtistForm(request.POST, request.FILES, instance=artist)
            if form.is_valid():
                # Handle cover image replacement
                if 'cover_image' in request.FILES:
                    # Delete the old file if it exists
                    if artist.cover_image:
                        original_file_name = Artist.objects.get(id=artist.id).cover_image.name
                        print(f"Original relative path in cover_image.name: {original_file_name}")
                        if not original_file_name.startswith("artist_covers/"):
                            original_file_name = f"artist_covers/{original_file_name}"
                        old_file_path = os.path.join(settings.MEDIA_ROOT, original_file_name)
                        if os.path.exists(old_file_path):
                            os.remove(old_file_path)

                    # Generate a unique filename if necessary
                    new_file = request.FILES['cover_image']
                    file_name = new_file.name
                    cover_image_path = os.path.join(settings.MEDIA_ROOT, 'artist_covers/')
                    os.makedirs(cover_image_path, exist_ok=True)  # Ensure the directory exists
                    existing_files = os.listdir(cover_image_path)

                    if file_name in existing_files:
                        name, ext = os.path.splitext(file_name)
                        random_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
                        file_name = f"{name}_{random_suffix}{ext}"

                    # Save the new file with a unique name
                    file_path = os.path.join(cover_image_path, file_name)
                    with open(file_path, 'wb+') as destination:
                        for chunk in new_file.chunks():
                            destination.write(chunk)

                    # Update the cover_image field in the form
                    artist.cover_image = f"artist_covers/{file_name}"

                form.save()
                return JsonResponse({'success': True, 'message': 'Artist updated successfully.'})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid form submission.', 'errors': form.errors})
        elif 'delete-artist' in request.POST:
            artist_id = request.POST.get('artist_id')
            artist = get_object_or_404(Artist, id=artist_id)
            if artist.cover_image:
                original_file_name = Artist.objects.get(id=artist.id).cover_image.name
                if not original_file_name.startswith("artist_covers/"):
                    original_file_name = f"artist_covers/{original_file_name}"
                old_file_path = os.path.join(settings.MEDIA_ROOT, original_file_name)
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)
            artist.delete()
            return JsonResponse({'success': True, 'message': 'Artist deleted successfully.'})
    else:
        form = ArtistForm()
    artists_data = [
        {
            'id': artist.id,
            'first_name': artist.first_name,
            'last_name': artist.last_name,
            'middle_name': artist.middle_name,
            'preferred_name': artist.preferred_name,
            'birth_date': artist.birth_date,
            'death_date': artist.death_date,
            'gender': artist.gender,
            'description': artist.description,
            'cover_image_url': artist.cover_image.url if artist.cover_image else None,
        }
        for artist in artists
    ]
    return render(request, 'warehouse/artist_dictionary_modify.html', {
        'form': form,
        'artists': artists,
        'artists_data': artists_data,
    })



from .models import RollScan

def rollscan_add(request):
    if request.method == "POST":
        try:
            film_type = request.POST.get("film_type")
            count = request.POST.get("count", None)
            location = request.POST.get("location", None)
            develop_date = request.POST.get("develop_date", None)
            scan_date = request.POST.get("scan_date", None)
            description = request.POST.get("description", "")
            is_active = request.POST.get("is_active", "on") == "on"

            # Convert empty strings to None for optional fields
            develop_date = develop_date if develop_date else None
            scan_date = scan_date if scan_date else None

            if not film_type:
                return JsonResponse({"success": False, "message": "Film type is required."})

            roll = RollScan.objects.create(
                film_type_id=film_type,
                count=count,
                location=location,
                develop_date=develop_date,
                scan_date=scan_date,
                description=description,
                is_active=is_active,
            )

            return JsonResponse({"success": True, "message": "Roll added successfully!", "roll_id": roll.id})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

    # Handle GET request to render the form
    films = Film.objects.all()
    return render(request, "warehouse/rollscan_add.html", {"films": films})



def rollscan_add_modify(request):
    if request.method == "POST":
        try:
            roll_id = request.POST.get("roll_id")
            roll = get_object_or_404(RollScan, id=roll_id)

            # Update the roll scan's details
            roll.film_type_id = request.POST.get("film_type", roll.film_type_id)
            roll.count = request.POST.get("count", roll.count)
            roll.location = request.POST.get("location", roll.location)
            roll.develop_date = request.POST.get("develop_date") or None
            roll.scan_date = request.POST.get("scan_date") or None
            roll.description = request.POST.get("description", roll.description)
            roll.is_active = request.POST.get("is_active", "on") == "on"
            roll.save()

            return JsonResponse({"success": True, "message": "Roll updated successfully!"})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

    # Render the modify page (GET request)
    rolls = RollScan.objects.all()
    films = Film.objects.all()
    return render(request, "warehouse/rollscan_add_modify.html", {"rolls": rolls, "films": films})



def rollscan_populate(request):
    if request.method == "POST":
        try:
            # Retrieve and validate the roll ID
            roll_id = request.POST.get("roll_id")
            roll = get_object_or_404(RollScan, id=roll_id)  # Ensure roll exists

            # Determine if photos are high-quality
            is_high_quality = request.POST.get("high_quality") == "on"
            folder_path = os.path.join(
                settings.MEDIA_ROOT,
                f"library/film_scans_origin/{roll_id}" if is_high_quality else f"library/film_scans/{roll_id}"
            )

            # Create folder if it doesn't exist
            os.makedirs(folder_path, exist_ok=True)

            # Process uploaded files
            uploaded_files = request.FILES.getlist("files")
            successfully_uploaded = []  # Indices of successfully uploaded files
            duplicate_indices = []  # Indices of fully uploaded files

            for file in uploaded_files:
                # Extract the index from the filename
                filename_without_extension = os.path.splitext(file.name)[0]
                index = filename_without_extension[-2:]  # Last 2 characters of the filename

                # Construct the media ID
                media_id = f"1{str(roll_id).zfill(7)}{index}"
                destination = os.path.join(folder_path, file.name)

                # Check if the entry already exists
                existing_entry = AllMedia.objects.filter(id=media_id).first()
                if existing_entry:
                    # Handle existing entries
                    if is_high_quality and not existing_entry.media_src_2:
                        # Save the high-quality file and update the database
                        with open(destination, 'wb') as f:
                            for chunk in file.chunks():
                                f.write(chunk)
                        existing_entry.media_src_2 = os.path.relpath(destination, settings.MEDIA_ROOT)
                        existing_entry.save()
                        successfully_uploaded.append(index)
                    elif not is_high_quality and not existing_entry.media_src:
                        # Save the regular file and update the database
                        with open(destination, 'wb') as f:
                            for chunk in file.chunks():
                                f.write(chunk)
                        existing_entry.media_src = os.path.relpath(destination, settings.MEDIA_ROOT)
                        existing_entry.save()
                        successfully_uploaded.append(index)
                    else:
                        # Both fields are already filled
                        duplicate_indices.append(index)
                else:
                    # Handle completely new uploads
                    # Save the file
                    with open(destination, 'wb') as f:
                        for chunk in file.chunks():
                            f.write(chunk)

                    # Create a new entry in the database
                    AllMedia.objects.create(
                        id=media_id,
                        media_type="film_scan",
                        media_src=os.path.relpath(destination, settings.MEDIA_ROOT) if not is_high_quality else None,
                        media_src_2=os.path.relpath(destination, settings.MEDIA_ROOT) if is_high_quality else None,
                        is_active=True,
                    )
                    successfully_uploaded.append(index)

            # Prepare response messages
            if successfully_uploaded and duplicate_indices:
                message = (
                    f"Successfully uploaded photos for indices: {', '.join(successfully_uploaded)}. "
                    f"Photos for indices {', '.join(duplicate_indices)} were already fully uploaded."
                )
            elif successfully_uploaded:
                message = f"Successfully uploaded photos for indices: {', '.join(successfully_uploaded)}."
            elif duplicate_indices:
                message = f"Photos for indices {', '.join(duplicate_indices)} were already fully uploaded."
            else:
                message = "No files were uploaded."

            # Respond with the message
            return JsonResponse({"success": True, "message": message})

        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

    # For a GET request, render the upload form
    rolls = RollScan.objects.filter(is_active=True)  # Only fetch active rolls
    return render(request, "warehouse/rollscan_populate.html", {"rolls": rolls})


import random
import string

def rollscan_edit(request):
    if request.method == "GET":
        action = request.GET.get("action")

        if action == "get_scans":
            roll_id = request.GET.get("roll_id")
            if not roll_id:
                return JsonResponse({"film_scans": []})

            # Pad roll ID to 7 digits
            padded_roll_id = str(roll_id).zfill(7)

            # Filter film scans by ID format and media_type
            film_scans = AllMedia.objects.filter(
                id__startswith=f"1{padded_roll_id}", media_type="film_scan"
            )
            data = [
                {
                    "id": scan.id,  # Full ID of the film scan
                    "index": scan.id[-2:],  # Extract the last 2 characters as the index
                    "roll_id": roll_id
                }
                for scan in film_scans
            ]
            return JsonResponse({"film_scans": data})

        elif action == "get_scan_details":
            media_id = request.GET.get("media_id")
            media = get_object_or_404(AllMedia, id=media_id)

            # Construct the correct URL for media_src
            media_src_url = (
                f"{settings.MEDIA_URL}{media.media_src.lstrip('/')}" if media.media_src else ""
            )
            data = {
                "title": media.title,
                "author_id": media.author.id if media.author else "",
                "date": str(media.date) if media.date else "",
                "location": media.location if media.location else "",
                "description": media.description,
                "is_active": media.is_active,
                "media_src": media_src_url,  # Ensure no double slashes
            }
            return JsonResponse(data)

    elif request.method == "POST":
        media_id = request.POST.get("media_id")
        media = get_object_or_404(AllMedia, id=media_id)

        # Handle delete request
        if "delete" in request.POST:
            try:
                # Delete associated files
                if media.media_src:
                    media_src_path = os.path.join(settings.MEDIA_ROOT, media.media_src)
                    if os.path.exists(media_src_path):
                        os.remove(media_src_path)

                if media.media_src_2:
                    media_src_2_path = os.path.join(settings.MEDIA_ROOT, media.media_src_2)
                    if os.path.exists(media_src_2_path):
                        os.remove(media_src_2_path)

                # Delete the media record
                media.delete()
                return redirect("rollscan_edit")

            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)

        # Handle modify request
        try:
            roll_id = media.id[1:8]  # Extract roll ID from the 2nd to 8th characters
            roll_directory = roll_id.lstrip("0")  # Convert padded roll ID to an integer-like string

            # Update fields
            media.title = request.POST.get("title")

            # Handle the author field (optional)
            author_id = request.POST.get("author_id")
            media.author_id = author_id if author_id else None

            # Handle the date field (optional)
            date_input = request.POST.get("date")
            media.date = date_input if date_input else None

            media.location = request.POST.get("location")

            media.description = request.POST.get("description")
            media.is_active = request.POST.get("is_active") == "on"

            # Replace files if uploaded
            if request.FILES.get("media_src"):
                media_src_path = os.path.join(settings.MEDIA_ROOT, f"library/film_scans/{roll_directory}/")
                os.makedirs(media_src_path, exist_ok=True)  # Ensure the directory exists
                # Delete old file if it exists
                if media.media_src:
                    old_file_path = os.path.join(settings.MEDIA_ROOT, media.media_src)
                    if os.path.exists(old_file_path):
                        os.remove(old_file_path)
                
                # Generate unique filename if a conflict exists
                file_name = request.FILES["media_src"].name
                existing_files = os.listdir(media_src_path)
                if file_name in existing_files:
                    name, ext = os.path.splitext(file_name)
                    random_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
                    file_name = f"{name}_{random_suffix}{ext}"

                file_path = os.path.join(media_src_path, file_name)
                with open(file_path, 'wb+') as destination:
                    for chunk in request.FILES["media_src"].chunks():
                        destination.write(chunk)
                # Save the relative path to the database
                media.media_src = os.path.relpath(file_path, settings.MEDIA_ROOT)

            if request.FILES.get("media_src_2"):
                media_src_2_path = os.path.join(settings.MEDIA_ROOT, f"library/film_scans_origin/{roll_directory}/")
                os.makedirs(media_src_2_path, exist_ok=True)  # Ensure the directory exists
                # Delete old file if it exists
                if media.media_src_2:
                    old_file_path_2 = os.path.join(settings.MEDIA_ROOT, media.media_src_2)
                    if os.path.exists(old_file_path_2):
                        os.remove(old_file_path_2)

                # Generate unique filename if a conflict exists
                file_name_2 = request.FILES["media_src_2"].name
                existing_files_2 = os.listdir(media_src_2_path)
                if file_name_2 in existing_files_2:
                    name_2, ext_2 = os.path.splitext(file_name_2)
                    random_suffix_2 = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
                    file_name_2 = f"{name_2}_{random_suffix_2}{ext_2}"
                
                file_path_2 = os.path.join(media_src_2_path, file_name_2)
                with open(file_path_2, 'wb+') as destination:
                    for chunk in request.FILES["media_src_2"].chunks():
                        destination.write(chunk)
                # Save the relative path to the database
                media.media_src_2 = os.path.relpath(file_path_2, settings.MEDIA_ROOT)

            media.save()
            return redirect("rollscan_edit")  # Redirect after modification

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    # Fetch rolls and artists for the form
    rolls = RollScan.objects.all()
    artists = Artist.objects.all()  # Fetch authors for the dropdown
    return render(request, "warehouse/rollscan_edit.html", {"rolls": rolls, "artists": artists})


def archive_home(request):
    rolls = RollScan.objects.select_related('film_type').order_by('-id')[:5]

    # Get current and previous years
    current_year = datetime.now().year
    previous_year = current_year - 1

    # Initialize month data with 0 for all 12 months
    def get_month_data(year):
        month_data = defaultdict(int)
        data = (
            RollScan.objects.filter(develop_date__year=year)
            .annotate(month=ExtractMonth('develop_date'))
            .values('month')
            .annotate(total=Count('id'))
        )
        for entry in data:
            month_data[entry['month']] = entry['total']
        return [month_data[month] for month in range(1, 13)]
    
    def get_mostly_used_film_type(year):
        film_counts = (
            RollScan.objects.filter(develop_date__year=year)
            .values('film_type__film_name', 'film_type__cover_image')
            .annotate(total=Count('film_type'))
            .order_by('-total')
        )
        if not film_counts:
            return [{"film_name": "N/A", "cover_image": None, "count": 0}]
        
        max_count = film_counts[0]['total']
        return [
            {
                "film_name": entry['film_type__film_name'],
                "cover_image": entry['film_type__cover_image'],
                "count": entry['total']
            }
            for entry in film_counts if entry['total'] == max_count
        ]
    
    def get_total_rolls(year):
        return RollScan.objects.filter(develop_date__year=year).count()
    
    def get_top_film_types(year, top_n=3):
        film_counts = (
            RollScan.objects.filter(develop_date__year=year)
            .annotate(
                film_name_type=Concat(
                    F('film_type__film_name'),
                    Value(' ('), 
                    F('film_type__film_type'), 
                    Value(')')
                )
            )
            .values('film_name_type', 'film_type__cover_image')
            .annotate(total=Count('film_type'))
            .order_by('-total')
        )
        if not film_counts:
            return [{"film_name_type": "N/A", "cover_image": None, "count": 0}]
        
        # Get the counts of the top_n film types
        top_counts = [film['total'] for film in film_counts[:top_n]]
        if len(top_counts) < top_n:
            min_top_count = top_counts[-1] if top_counts else 0
        else:
            min_top_count = top_counts[top_n - 1]
        
        # Include all film types with counts equal to or greater than min_top_count
        return [
            {
                "film_name_type": entry['film_name_type'],
                "cover_image": entry['film_type__cover_image'],
                "count": entry['total']
            }
            for entry in film_counts if entry['total'] >= min_top_count
        ]
    
    def get_heatmap_data():
        # one_year_ago = date.today() - timedelta(days=365)
        today = date.today()
        start_date = date(today.year, 1, 1)
        rolls = (
            RollScan.objects.filter(develop_date__gte=start_date, is_active=True)
            .values('develop_date')
            .annotate(total=Count('id'))
            .order_by('develop_date')
        )
        # Prepare the data as a dictionary
        return {roll['develop_date'].strftime('%Y-%m-%d'): roll['total'] for roll in rolls}


    current_year_data = get_month_data(current_year)
    previous_year_data = get_month_data(previous_year)

    current_year_top_film = get_mostly_used_film_type(current_year)
    previous_year_top_film = get_mostly_used_film_type(previous_year)

    current_year_total_rolls = get_total_rolls(current_year)
    previous_year_total_rolls = get_total_rolls(previous_year)

    current_year_top_film_types = get_top_film_types(current_year, top_n=3)
    previous_year_top_film_types = get_top_film_types(previous_year, top_n=3)

    heatmap_data = get_heatmap_data()
    transformed_heatmap_data = [{"date": key, "value": value} for key, value in heatmap_data.items()]

    context = {
        'rolls': rolls,
        'current_year': current_year,
        'previous_year': previous_year,
        'current_year_data': current_year_data,
        'previous_year_data': previous_year_data,
        'current_year_top_film': current_year_top_film,
        'previous_year_top_film': previous_year_top_film,
        'current_year_total_rolls': current_year_total_rolls,
        'previous_year_total_rolls': previous_year_total_rolls,
        'current_year_top_film_types': current_year_top_film_types,
        'previous_year_top_film_types': previous_year_top_film_types,
        'heatmap_data': json.dumps(transformed_heatmap_data),
    }
    return render(request, "warehouse/archive_home.html", context)


def roll_library(request):
    # Fetch all rolls and include the related film_type data
    rolls = RollScan.objects.select_related('film_type').order_by('-id')
    
    # Paginate the rolls, 20 items per page
    paginator = Paginator(rolls, 20)
    page_number = request.GET.get('page')  # Get the current page number from the URL
    page_obj = paginator.get_page(page_number)  # Get the page object for the current page

    return render(request, 'warehouse/roll_library.html', {'page_obj': page_obj})


def film_viewer(request, roll_id):
    # Fetch roll information
    roll = get_object_or_404(RollScan, id=roll_id)
    
    # Fetch film scans related to the roll
    roll_id_str = str(roll_id).zfill(7)  # Ensure 7-digit formatting
    film_scans = AllMedia.objects.filter(id__startswith=f"1{roll_id_str}").order_by('id')

    # Preprocess film_scans
    for scan in film_scans:
        scan.roll_id = str(int(scan.id[1:8]))  # Remove leading zeros
        scan.photo_index = scan.id[8:]        # Extract photo index
        scan.display_id = f"1-{scan.roll_id}-{scan.photo_index}"

    scan_count = film_scans.count()
    
    context = {
        'roll': roll,
        'film_scans': film_scans,
        'scan_count': scan_count,
    }
    
    return render(request, 'warehouse/film_viewer.html', context)