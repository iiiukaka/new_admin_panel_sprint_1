from django.contrib import admin

from .models import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmWork


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmWork
    autocomplete_fields = ('person',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'created_at', 'updated_at'
    )
    search_fields = (
        'name', 'description', 'id'
    )


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = (
        'full_name', 'created_at', 'updated_at'
    )
    search_fields = (
        'full_name', 'id'
    )


@admin.register(FilmWork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInline)
    list_display = (
        'title', 'type', 'creation_date',
        'rating', 'created_at', 'updated_at'
    )
    search_fields = (
        'title', 'description', 'id'
    )
    list_filter = (
        'type', 'genres'
    )
