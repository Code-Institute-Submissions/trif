from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Image
import functools

# ------- only run this to initially populate database with Image objects
if len(Image.objects.all()) == 0:
    import fract.populate_db 

STATIC_SMALL_IMAGE_DIR = 'images/zarg438/'
STATIC_LARGE_IMAGE_DIR = 'images/zarg877/'

# OLD view-function, replaced by class-based view below
# def index(request):
#     #image_names = map(lambda img: STATIC_IMAGE_DIR + img.name, Image.objects.filter(id__lt=13)) # for testing

#     # Get image data as a list of tuples like ('xtsM2f101C431-pre167-438x310x0.0y0.0_6594.png', 74)
#     image_data = map(lambda img: (STATIC_IMAGE_DIR + img.name, img.id), Image.objects.all())
#     context = {
#         'image_data': image_data
#     }
#     return render(request, 'fract/index.html', context)


class ImageListView(ListView):
    """ List view of all images. """
    model = Image
    paginate_by = 30
    template_name = 'fract/index.html'
    context_object_name = 'image_list'
    ordering = '?'      # random ordering

    def get_context_data(self, **kwargs):
        """
        Get the context and append the STATIC_IMAGE_DIR to it, so we can 
        use this in the template for the image source path.
        """
        context = super(ImageListView, self).get_context_data(**kwargs)
        context['STATIC_SMALL_IMAGE_DIR'] = STATIC_SMALL_IMAGE_DIR
        return context


class LikedImageListView(ListView):
    """ List view of all images. """
    paginate_by = 30
    template_name = 'fract/index.html'  # re-use "list all" template for '/likes'
    context_object_name = 'image_list'
    ordering = 'id'      # random ordering

    def get_queryset(self):
        queryset = self.request.user.profile.liked_images.all()
        return queryset

    def get_context_data(self, **kwargs):
        """
        Get the context and append the STATIC_IMAGE_DIR to it, so we can 
        use this in the template for the image source path.
        """
        context = super(LikedImageListView, self).get_context_data(**kwargs)
        context['STATIC_SMALL_IMAGE_DIR'] = STATIC_SMALL_IMAGE_DIR
        context['likes'] = True
        return context


class FilteredImageListView(ListView):
    """ List view of all images. """
    paginate_by = 30
    template_name = 'fract/index.html'  # re-use "list all" template for '/likes'
    context_object_name = 'image_list'
    ordering = 'id'

    def get_queryset(self):
        EMPTY = ''
        func = self.request.GET.get("func")
        alt_func = self.request.GET.get("alt_func")
        exponent = self.request.GET.get("exponent")
        flavour = self.request.GET.get("flavour")
        queryset = list(filter(lambda img:
            (func == EMPTY or img.params()['func'] == func) and
            (alt_func == EMPTY or img.params()['alt_func'] == alt_func) and
            (exponent == EMPTY or img.params()['power'] == exponent) and
            (flavour == EMPTY or flavour == "*" or img.params()['type'] == flavour),
          Image.objects.all()))
        return queryset

    def get_context_data(self, **kwargs):
        """
        Get the context and append the STATIC_IMAGE_DIR to it, so we can 
        use this in the template for the image source path.
        """
        context = super(FilteredImageListView, self).get_context_data(**kwargs)
        context['STATIC_SMALL_IMAGE_DIR'] = STATIC_SMALL_IMAGE_DIR
        context['filtered'] = True
        return context


class ImageDetailView(DetailView):
    """ Detail view of a single image """
    model = Image
    def get_context_data(self, **kwargs):
        """
        Get the context and append the STATIC_IMAGE_DIR to it, so we can 
        use this in the template for the image source path
        """
        context = super(ImageDetailView, self).get_context_data(**kwargs)
        context['STATIC_LARGE_IMAGE_DIR'] = STATIC_LARGE_IMAGE_DIR
        return context

def about(request):
    """ Return the 'About' page. """
    return render(request, 'fract/about.html')

# def images_filtered(request):
#     """ Return the list of images, filtered by the specified criteria. """
#     # Currently a stub
#     return render(request, 'fract/about.html')    
