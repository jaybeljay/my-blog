from tag.models import Tag


def display_tags(request):
    tagslist = Tag.objects.values_list('title', 'slug', named=True)
    return {
        'tagslist': tagslist
    }
