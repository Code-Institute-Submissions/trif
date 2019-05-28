# Trif

## Overview

Trif is a web application which classifies and offers for sale high-definition prints of abstract fractal images created in Java using a plethora of mathematical functions iterated over the complex plane.

The project has been developed using [Django][4], with the goal of fulfilling the requirements of the final, Full-Stack Milestone Project of the [Code Institute Full-Stack Software Developer Course][5].

All images displayed are stored in an [AWS S3][6] bucket, as are static files like CSS, icons and user-uploded profile pictures.

The project is hosted at [Heroku][8].   A [Postgresql][9] database, also hosted at Heroku, is used to store image data and user data.

The E-Commerce side is handled by [Snipcart][7].

At the outset, 348 images will be available, printed with professional fade-resistant pigments on high-quality photo paper.

I generate these images by pouring equal measures of mathematics and computer programming into a pot, mixing well and cooking gently for a long time! ;)

They are the result of several years of developing a Java program which uses polynomial and trigonometric functions iterated over the complex plane to produce often highly detailed, high-resolution images (normally 14032 x 9920 pixels), which can consequently be printed even on large format media without having to be scaled up and thereby losing quality and in extreme cases becoming pixellated.

All prints, and the images on this site, are made from these 14032x9920 originals. The images in the grid view are scaled down to 438 x 310 pixels, and the individual views show a higher-resolution version, 877 x 620 pixels.

### tl;dr

Each image is generated by a combination of two complex functions iterated over the complex plane. In most cases the functions are composed, while sometimes they're alternated and now and then combined by taking the arithmetic or geometric mean of the two at each iteration.

Most images are produced using somewhere between 32 and 1024 maximum iterations per pixel. Most functions have a strong trigonometric element, using the real sine and cosine functions applied separately to the real and imaginary parts, in various combinations, as the complex trig functions tend to produce fragmented, jagged images.

## UX

### User Stories

- Bob, who happens to like abstract but not figurative or representational art, finds the site by chance.   He should be drawn in by the images, be able to view other images similar to ones he likes and be tempted to click "Buy!".

- Alice, who's looking for a large colourful print for a white wall in her new flat, should be encouraged to browse all the images until she finds one she likes and is drawn to buy it.

## UI

### Sketches for list view and detailed (single image) view:
 
I wanted a simple design because the images themselves are complex.   I just sketched out on paper (scans embedded below) some rough ideas for the main views, as a starting point, knowing that that could change during the development process.   In the end, knowing that design is not my strongpoint, I am fairly satisfied with how it has turned out.

Some ideas for improvement will no doubt become apparent with time, and will be appraised for possible implementation as appropriate.   Pull requests welcome!

![](design_docs/trif-layout-0.jpg)
![](design_docs/trif-layout-1.jpg)
![](design_docs/trif-layout-2.jpg)

## Specification

The application must store an indeterminate number of images in non-volatile web-accessible storage.

It must provide methods to classify and filter these images based on various characteristics.

In order to do this, it must store or be able to extract data about the functions used to generate an image.   This will be facilitated by these data having being encoded in the filenames of the images.

The administrator must be able to add or delete images.

Images must be stored in low resolution (877x620 pixels and 436x310 pixels) but the originals are 14032x9920 pixels, and it is these originals from which high-definition prints (A0, A1, A2, A3) will be made for purchasers.   The filenames of the originals have a one-to-one relationship to the filenames of the low-resolution versions, so orders can be processed without ambiguity.

The application must be able to display the full set of images to the user, suitably scaled in size so as to display a number per viewport, and also let the user select images similar to a given image.   An "Images like this" link should be available for all images, which filters the set by the functions used to generate the images.   Most images have been generated by two functions, usually composed but in some cases alternated, so the user should be able to filter the set by either or both, and by an optional pre-transform.

Advanced functionality should allow the user to filter by other parameters used in the image generation and encoded in the filename, in particular `subc`, `scp` and `sri`.   These are Boolean parameters which when true signify, respectively, that the added constant in the escape-time fractal algorithm has subsequently been subracted, that the same has been done for the pre-transformation function, and that the real and imaginary parts of z have been switched prior to iteration.

In future versions the user should also be able to filter by the predominant colour or quantity of black.   This, however, requires some thinking about as it involves building logic to create histograms and make decisions based on their values, so will not be available in the initial version.

The application must provide secure user registration, authentication and authorisation.   It must provide a secure password reset facility in case of forgotten passwords.   It will not provide a "Forgot my email" facility.

When a user clicks on an image it should be enlarged, and a link to buy should be prominent.

An authenticated user should also be able to 'like' an image, and subsequently view the set of images s/he has liked.

If a user clicks to buy, they should be taken to a page where they can select a size, be informed of the price and complete the transaction with a credit card or Paypal etc.

The application must maintain a "shopping basket" or "cart" so that the user can buy more than one print in a single transaction.   These data should be stored in the database so that if the user does not complete a purchase the items will remain in the basket and be there next time they log in.

A checkout and payment facility must be provided using a trusted third-party library compatible with Django.

In order not to distract or detract from the images themselves, the layout and design of the rendered pages should be as clean and simple as possible.

## Design decisions

- Deployment platform:      Heroku
- Database:                 Postgresql as Heroku add-on
- Image storage:            S3
- Versions:                 Python(3.7.1), Django(2.1.7)
- CI / testing:             Travis
- Payment processing:       ~Stripe~ Snipcart
- Styling:                  ~Materialize~ Bootstrap and own CSS

### Models

#### User

- Represents a user, who can register with an email address and thereafter be authenticated;
- Fields:  for each user we need name, email, id, whether registered and whether authenticated. We will need to link to the orders table with a foreign key.

#### Image

- Represents a fractal image that can be displayed, that can be ordered as a print, that contains information about the functions and parameters used to create it, and that remembers orders;
- Fields: name, image_id.   We could pre-extract the creation data from the filenames and store as fields, but it will perhaps be simpler, and minimally expensive, to create functions to extract the data as needed. Each Image item must provide a method to get both small and large versions from storage. 

#### Order 

- Represents an Order made by a User for an Image;
- Fields: order_id, user_id (foreign key), order_details (containing despatch address, list of Image items and quantities, whether paid).
- It was not found necessary to implement this as Snipcart handles and stores the orders; however, in a future version it could be useful.    

### Views and Templates

- `base.html` will contain header and footer with links to register / login.   Other templates will inherit from this:
- `index.html` will be a Home Page displaying some images with links;
- `about.html` will provide information about the application and the developer;
- Other views will enable the user to view the entire set of images (maybe with pagination) or subset based on filtering criteria;
- Clicking on a single image will cause it to be rendered alone, at \~80% screen width, with a "Buy" button at bottom right.
- Other views will enable a user to register, deregister or amend account details.

## Development process log / overview

* Set up S3 and Stripe accounts, create S3 bucket for static files
* Set up basic Django 2 project structure (project: 'trif')
* Create and set environment variables
* S3 and Stripe settings into settings.py
* Other configuration in settings.py
* Set up on Heroku and connected Github for automatic deployment on push
* Configure Heroku Postgres database; using SQLite locally
* Upload images to S3 bucket: Source Location: "trif-store/static/images/"
* Create app: 'fract' and tested with 'Hello World' page
* Do migrations, create superuser etc.
* Store secrets in environment variables (config vars in Heroku)
* Create User model and views following [Corey Schafer's Django 2 tutorials][0], as suggested using code from Bootstrap and CS in base template.   So I will try Bootstrap instead of Materialize
* Create Image model, migrate
* Instantiate a set of Image objects (which simply contain the filename and size, as strings), corresponding to the images actually stored as static assets in my S3 bucket
* Iterate over this set, saving each Image object to the database.   Used local images folder.   See the [console log][1]
* Many issues ensued, initially caused, I think, by my mistaken deletion of a migrations directory. At one point I upgraded Django from 2.1 to 2.2, backed up relevant files, recreated the project and apps.   Later, after mistakenly pushing a faulty commit, I got into a mess with git and ended up doing a `git rebase --hard` and then `git push -f`.   Not a very clean solution, rewriting history etc. but it got me sorted.
* Minor tweaks to styling etc.
* Change home page to a class-based view, subclassing ListView
* Implement random ordering and [pagination][2] using a [custom template tag][3]
* Style pagination buttons
* Add favicon.ico
* Set up gmail address with two-factor authentication
* Implement and debug password reset via gmail, using Django's built-in PasswordResetView etc.
* Improve styling
* Attempt unsuccessfully to override save() method of django.contrib.auth.models.Model in order to resize profile images before saving; also tried by using the post_save() signal method; need to revisit this as otherwise large profile images will take too long to load
* Create branch to implement Snipcart shopping facility
* When mostly working, merge into master and deploy
* Added and styled footer with social media icons
* Implement code to let an authenticated user 'like' an image, and display the number of likes for each image
* Tweak styling and fonts
* Make sidebar into tabbed panel, 2nd tab displaying a form for filtering
* Successfully implement views filtered by image parameters, by using a lambda in the override of 'get_queryset()' in class FilteredImageListView in fract/views.py
* Write content for 'About' page and style it



### Final Stages: To Do:
    - Snipcart - Empty cart on logout
    - Fix Snipcart sometimes not finding product when scraping page
    - Finish this README.md, including acknowledgements and deployment guide
    - Redirect user back to previous page upon login (if straightforward) - DONE
    - Scan draft sketches of list & detail pages and include here above - DONE
    - Fix favicon not being seen by browser - DONE
    - Write content for "About" page - DONE
    - Add 'Details' popup or toast to show image parameters in detail view - DONE
    - Side panel - make tabs, show filtering options - DONE
    - Fix footer background - DONE
    - Adjust navbar icon placement and font size - DONE
    - Implement filtering options - DONE
    - Make background black beneath image card text - DONE
    - Fix disappearing 'Heart' icon on mobile -DONE 
    - Fix issue of Django admin static files being included in 'collectstatic'
    - Testing; maybe CT/CI with Travis
    - Code linting / validation
    - Run CSS through Autoprefixer
    - Test responsiveness on mobile devices -ONGOING
    - Repeat testing in Firefox and Opera
    
### Features left to implement in future versions:
    - Find best way to shrink profile pictures, to obviate storing and serving too-large user-uploaded images
    - Multiple sizes of prints
    - Send a 'Like' to the server with Javascript rather than reloading the page, I guess with an AJAX request
    - Store a user's cart in case s/he logs out or clears browser cache
    - Improve styling and find a better way to present the images, perhaps with a higher-resolution version (perhaps 2806 x 1984) for users prepared to wait, and a smaller version for list view on mobile and thumbnail for shopping cart
    - Further customise the Snipcart workflow 
    - Store orders in the user profile, display for the user's convenience, and think how to use for marketing purposes
    - Add Java function definitions to database so we can display as image detail for geeks
    - Test in Safari, Edge

## Testing

* The project was tested manually at all stages, both on my local machine and on the Heroku dynos:
    - by testing navigation from page to page
    - by logging in and out
    - by registering new users
    - by clicking 'Forgot password' and checking the reset email arrives and the link it supplies works
    - by changing things in the admin panel and trying to break stuff (e.g. deleting a user and then checking the profile is removed by CASCADE)
    - by testing the 'Like' buttons for images, with different users, and checking the counter is incremented as expected
    - by testing the filtering options and checking the result sets in the shell

* In this way many bugs were uncovered and subsequently fixed.


## Deployment

- The project's git repository is hosted at [Github][14] and a push to this remote origin triggers a subsequent push and new build on [Heroku][8], where the project is hosted on the Heroku free tier.
- For security, all secret keys (Django, Amazon, Snipcart) are stored in Heroku config variables (environment variables).
- The database used is Heroku's own Postgresql database.
- The project uses [Amazon S3 free tier][6] for non-volatile static and media files, like CSS, icons, uploaded user profile pictures and the actual images displayed on the site.
- The project uses [Snipcart][7] to handle user purchase orders, shopping cart, payments and backend notifications
- The deployed site can be accessed with a web browser at [Teraspora Fractals][15]



## Acknowledgements

- The tutors, mentors and support staff at [Code Institute][5]
- The tutors, mentors, alumni and fellow students on the Code Institute [Slack][12] channels
- [Corey Schafer][10] for his excellent teaching on Youtube about Django, Python, Server setup and more
- The [Django docs][11], which are a paragon of documentation
- The [Python docs][13]
- My mentor Nishant Kumar
- All the good answers and guides and tutorials and blogs on the web, on [Stack Overflow][14] and elsewhere, that have helped me on the way

<p>
    This website is the culmination of over a year of study online.   It is my fifth and final "Milestone Project" for the Code Institute course.   It is built in <a target="_blank" href="https://www.python.org/downloads/">Python 3.7</a> on the backend, with <a target="_blank" href="https://www.djangoproject.com/">Django 2.2</a>. The frontend templates are built using <a target="_blank" href="https://docs.djangoproject.com/en/2.2/topics/templates/#the-django-template-language">the Django template language</a>, with <a target="_blank" href="https://getbootstrap.com/docs/4.3/getting-started/introduction/">Bootstrap 4</a> and my own <a target="_blank" href="https://developer.mozilla.org/en-US/docs/Web/CSS">CSS</a>.  It is hosted at <a target="_blank" href="https://ztrif.herokuapp.com/">Heroku</a>. It uses a <a target="_blank" href="https://www.postgresql.org/">PostgreSQL</a> database also hosted at Heroku to store image data and user profile data.   The images themselves are stored in an <a target="_blank" href="https://aws.amazon.com/s3/">Amazon S3 bucket</a>, along with other static files.
</p>


[0]: https://www.youtube.com/playlist?list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p
[1]: file://shell.log
[2]: https://www.caktusgroup.com/blog/2018/10/18/filtering-and-pagination-django/
[3]: https://docs.djangoproject.com/en/2.2/howto/custom-template-tags/
[4]: https://www.djangoproject.com/
[5]: https://codeinstitute.net/full-stack-software-development-diploma/
[6]: https://aws.amazon.com/s3/
[7]: https://snipcart.com/
[8]: https://www.heroku.com/
[9]: https://www.postgresql.org/
[10]: https://twitter.com/CoreyMSchafer
[11]: https://docs.djangoproject.com/en/2.2/
[12]: https://slack.com/intl/en-ie/
[13]: https://docs.python.org/3/
[14]: https://github.com/teraspora/trif
[15]: https://ztrif.herokuapp.com/
