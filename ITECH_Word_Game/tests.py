import os
import re
import importlib
import inspect
import tempfile
import wordgame.models
from wordgame import forms
from django.urls import reverse
from populate_wordgame import populate
from django.test import TestCase
from django.conf import settings
import warnings
from django.contrib.auth.models import User
from django.forms import fields as django_fields
from django.db import models

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

class ProjectStructureTests(TestCase):
    """
    Simple tests to probe the file structure of your project so far.
    We also include a test to check whether you have added wordgame to your list of INSTALLED_APPS.
    """
    def setUp(self):
        self.project_base_dir = os.getcwd()
        self.wordgame_app_dir = os.path.join(self.project_base_dir, 'wordgame')
    
    def test_project_created(self):
        """
        Tests whether the ITECH_Word_Game configuration directory is present and correct.
        """
        directory_exists = os.path.isdir(os.path.join(self.project_base_dir, 'ITECH_Word_Game'))
        urls_module_exists = os.path.isfile(os.path.join(self.project_base_dir, 'ITECH_Word_Game', 'urls.py'))
        
        self.assertTrue(directory_exists, f"{FAILURE_HEADER}Your ITECH_Word_Game configuration directory doesn't seem to exist. Did you use the correct name?{FAILURE_FOOTER}")
        self.assertTrue(urls_module_exists, f"{FAILURE_HEADER}Your project's urls.py module does not exist. Did you use the startproject command?{FAILURE_FOOTER}")
    
    def test_wordgame_app_created(self):
        """
        Determines whether the wordgame app has been created.
        """
        directory_exists = os.path.isdir(self.wordgame_app_dir)
        is_python_package = os.path.isfile(os.path.join(self.wordgame_app_dir, '__init__.py'))
        views_module_exists = os.path.isfile(os.path.join(self.wordgame_app_dir, 'views.py'))
        
        self.assertTrue(directory_exists, f"{FAILURE_HEADER}The wordgame app directory does not exist. Did you use the startapp command?{FAILURE_FOOTER}")
        self.assertTrue(is_python_package, f"{FAILURE_HEADER}The wordgame directory is missing files. Did you use the startapp command?{FAILURE_FOOTER}")
        self.assertTrue(views_module_exists, f"{FAILURE_HEADER}The wordgame directory is missing files. Did you use the startapp command?{FAILURE_FOOTER}")
    
    def test_wordgame_has_urls_module(self):
        """
        Did you create a separate urls.py module for wordgame?
        """
        module_exists = os.path.isfile(os.path.join(self.wordgame_app_dir, 'urls.py'))
        self.assertTrue(module_exists, f"{FAILURE_HEADER}The wordgame app's urls.py module is missing. Read over the instructions carefully, and try again. You need TWO urls.py modules.{FAILURE_FOOTER}")
    
    def test_is_wordgame_app_configured(self):
        """
        Did you add the new wordgame app to your INSTALLED_APPS list?
        """
        is_app_configured = 'wordgame' in settings.INSTALLED_APPS
        
        self.assertTrue(is_app_configured, f"{FAILURE_HEADER}The wordgame app is missing from your setting's INSTALLED_APPS list.{FAILURE_FOOTER}")

class templatesStructureTests(TestCase):
    """
    Have you set templates, static files and media files up correctly?
    """
    def setUp(self):
        self.project_base_dir = os.getcwd()
        self.templates_dir = os.path.join(self.project_base_dir, 'templates')
        self.wordgame_templates_dir = os.path.join(self.templates_dir, 'wordgame')
    
    def test_templates_directory_exists(self):
        """
        Does the templates/ directory exist?
        """
        directory_exists = os.path.isdir(self.templates_dir)
        self.assertTrue(directory_exists, f"{FAILURE_HEADER}Your project's templates directory does not exist.{FAILURE_FOOTER}")
    
    def test_wordgame_templates_directory_exists(self):
        """
        Does the templates/wordgame/ directory exist?
        """
        directory_exists = os.path.isdir(self.wordgame_templates_dir)
        self.assertTrue(directory_exists, f"{FAILURE_HEADER}The wordgame templates directory does not exist.{FAILURE_FOOTER}")
    
    def test_template_dir_setting(self):
        """
        Does the TEMPLATE_DIR setting exist, and does it point to the right directory?
        """
        variable_exists = 'TEMPLATE_DIR' in dir(settings)
        self.assertTrue(variable_exists, f"{FAILURE_HEADER}Your settings.py module does not have the variable TEMPLATE_DIR defined!{FAILURE_FOOTER}")
        
        template_dir_value = os.path.normpath(settings.TEMPLATE_DIR)
        template_dir_computed = os.path.normpath(self.templates_dir)
        self.assertEqual(template_dir_value, template_dir_computed, f"{FAILURE_HEADER}Your TEMPLATE_DIR setting does not point to the expected path. Check your configuration, and try again.{FAILURE_FOOTER}")
    
    def test_template_lookup_path(self):
        """
        Does the TEMPLATE_DIR value appear within the lookup paths for templates?
        """
        lookup_list = settings.TEMPLATES[0]['DIRS']
        found_path = False
        
        for entry in lookup_list:
            entry_normalised = os.path.normpath(entry)
            
            if entry_normalised == os.path.normpath(settings.TEMPLATE_DIR):
                found_path = True
        
        self.assertTrue(found_path, f"{FAILURE_HEADER}Your project's templates directory is not listed in the TEMPLATES>DIRS lookup list. Check your settings.py module.{FAILURE_FOOTER}")
    
    def test_templates_exist(self):
        """
        Do the base.html game.html and leaderboard.html login.html userprofile.htmltemplates exist in the correct place?
        """
        game_path = os.path.join(self.wordgame_templates_dir, 'game.html')
        leaderboard_path = os.path.join(self.wordgame_templates_dir, 'leaderboard.html')
        base_path = os.path.join(self.wordgame_templates_dir, 'game.html')
        login_path = os.path.join(self.wordgame_templates_dir, 'game.html')
        userprofile_path = os.path.join(self.wordgame_templates_dir, 'game.html')
        self.assertTrue(os.path.isfile(game_path), f"{FAILURE_HEADER}Your game.html template does not exist, or is in the wrong location.{FAILURE_FOOTER}")
        self.assertTrue(os.path.isfile(leaderboard_path), f"{FAILURE_HEADER}Your about.html template does not exist, or is in the wrong location.{FAILURE_FOOTER}")
        self.assertTrue(os.path.isfile(base_path), f"{FAILURE_HEADER}Your base.html template does not exist, or is in the wrong location.{FAILURE_FOOTER}")
        self.assertTrue(os.path.isfile(login_path), f"{FAILURE_HEADER}Your login.html template does not exist, or is in the wrong location.{FAILURE_FOOTER}")
        self.assertTrue(os.path.isfile(userprofile_path), f"{FAILURE_HEADER}Your userprofile.html template does not exist, or is in the wrong location.{FAILURE_FOOTER}")

class templateTests:
    def get_template(self, path_to_template):
        """
        Helper function to return the string representation of a template file.
        """
        f = open(path_to_template, 'r')
        template_str = ""

        for line in f:
            template_str = f"{template_str}{line}"

        f.close()
        return template_str

    def test_base_title_block(self):
        """
        Checks if wordgame's new base template has the correct value for the base template.
        """
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'wordgame', 'base.html')
        template_str = self.get_template(template_base_path)
        
        title_pattern = r'<title>(\s*|\n*)w[]rdle(\s*|\n*)-(\s*|\n*){% block title_block %}(\s*|\n*)Game(\s*|\n*){% (endblock|endblock title_block) %}(\s*|\n*)</title>'
        self.assertTrue(re.search(title_pattern, template_str), f"{FAILURE_HEADER}When searching the contents of base.html, we couldn't find the expected title block. We're looking for '<title>w[]rdle - {{% block title_block %}}Game{{% endblock %}}</title>' with any combination of whitespace.{FAILURE_FOOTER}")
    
    def test_template_usage(self):
        """
        Check that each view uses the correct template.
        """
        populate()
        
        urls = [reverse('wordgame:game'),
                reverse('wordgame:leaderboard'),
                reverse('wordgame:login'),
                reverse('wordgame:userprofile'),
                reverse('wordgame:logout'),]

        templates = ['wordgame/game.html',
                     'wordgame/leaderboard.html',
                     'wordgame/login.html',
                     'wordgame/userprofile.html',
                     'wordgame/logout.html',]
        
        for url, template in zip(urls, templates):
            response = self.client.get(url)
            self.assertTemplateUsed(response, template)

    def test_title_blocks(self):
        """
        Tests whether the title blocks in each page are the expected values.
        This is probably the easiest way to check for blocks.
        """
        populate()
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'wordgame')
        
        mappings = {
            reverse('wordgame:game'): {'full_title_pattern': r'<title>(\s*|\n*)w[]rdle(\s*|\n*)-(\s*|\n*)W[]rdle(\s*|\n*)</title>',
                                     'block_title_pattern': r'{% block title_block %}(\s*|\n*)W[]rdle(\s*|\n*){% (endblock|endblock title_block) %}',
                                     'template_filename': 'game.html'},
            reverse('wordgame:leaderboard'): {'full_title_pattern': r'<title>(\s*|\n*)w[]rdle(\s*|\n*)-(\s*|\n*)Leaderboard(\s*|\n*)</title>',
                                            'block_title_pattern': r'{% block title_block %}(\s*|\n*)Leaderboard(\s*|\n*){% (endblock|endblock title_block) %}',
                                            'template_filename': 'leaderboard.html'},
            reverse('wordgame:login'): {'full_title_pattern': r'<title>(\s*|\n*)w[]rdle(\s*|\n*)-(\s*|\n*)Login(\s*|\n*)</title>',
                                                                                 'block_title_pattern': r'{% block title_block %}(\s*|\n*)Login(\s*|\n*){% (endblock|endblock title_block) %}',
                                                                                 'template_filename': 'login.html'},
            reverse('wordgame:userprofile'): {'full_title_pattern': r'<title>(\s*|\n*)w[]rdle(\s*|\n*)-(\s*|\n*)UserProfile(\s*|\n*)</title>',
                                                                                      'block_title_pattern': r'{% block title_block %}(\s*|\n*){% if category %}(\s*|\n*)UserProfile(\s*|\n*){% else %}(\s*|\n*)Unknown Category(\s*|\n*){% endif %}(\s*|\n*){% (endblock|endblock title_block) %}',
                                                                                      'template_filename': 'category.html'},
        }

        for url in mappings.keys():
            full_title_pattern = mappings[url]['full_title_pattern']
            template_filename = mappings[url]['template_filename']
            block_title_pattern = mappings[url]['block_title_pattern']

            request = self.client.get(url)
            content = request.content.decode('utf-8')
            template_str = self.get_template(os.path.join(template_base_path, template_filename))

            self.assertTrue(re.search(full_title_pattern, content), f"{FAILURE_HEADER}When looking at the response of GET '{url}', we couldn't find the correct <title> block. Check the exercises on Chapter 8 for the expected title.{FAILURE_FOOTER}")
            self.assertTrue(re.search(block_title_pattern, template_str), f"{FAILURE_HEADER}When looking at the source of template '{template_filename}', we couldn't find the correct template block. Are you using template inheritence correctly, and did you spell the title as in the book? Check the exercises on Chapter 8 for the expected title.{FAILURE_FOOTER}")
    
    def test_for_links_in_base(self):
        """
        There should be three hyperlinks in base.html, as per the specification of the book.
        Check for their presence, along with correct use of URL lookups.
        """
        template_str = self.get_template(os.path.join(settings.TEMPLATE_DIR, 'wordgame', 'base.html'))

        look_for = [
            'href="{% url \'wordgame:game\' %}"',
            'href="{% url \'wordgame:leaderboard\' %}"',
            'href="{% url \'wordgame:userprofile\' %}"',
            'href="{% url \'wordgame:login\' %}"',
            'href="{% url \'wordgame:logout\' %}"',
        ]
        
        for lookup in look_for:
            self.assertTrue(lookup in template_str, f"{FAILURE_HEADER}In base.html, we couldn't find the hyperlink '{lookup}'. Check your markup in base.html is correct and as written in the book.{FAILURE_FOOTER}")
    
class setupTests(TestCase):
    """
    A simple test to check whether the auth app has been specified.
    """
    def test_installed_apps(self):
        """
        Checks whether the 'django.contrib.auth' app has been included in INSTALLED_APPS.
        """
        self.assertTrue('django.contrib.auth' in settings.INSTALLED_APPS)    

class staticMediaTests(TestCase):
    """
    A series of tests to check whether static files and media files have been setup and used correctly.
    Also tests for the two required files -- wordgame.jpg and cat.jpg.
    """
    def setUp(self):
        self.project_base_dir = os.getcwd()
        self.static_dir = os.path.join(self.project_base_dir, 'static')
        self.media_dir = os.path.join(self.project_base_dir, 'media')
    
    def test_does_static_directory_exist(self):
        """
        Tests whether the static directory exists in the correct location -- and the images subdirectory.
        Also checks for the presence of wordgame.jpg in the images subdirectory.
        """
        does_static_dir_exist = os.path.isdir(self.static_dir)
        does_images_static_dir_exist = os.path.isdir(os.path.join(self.static_dir, 'images'))
        
        self.assertTrue(does_static_dir_exist, f"{FAILURE_HEADER}The static directory was not found in the expected location. Check the instructions in the book, and try again.{FAILURE_FOOTER}")
        self.assertTrue(does_images_static_dir_exist, f"{FAILURE_HEADER}The images subdirectory was not found in your static directory.{FAILURE_FOOTER}")

    def test_does_media_directory_exist(self):
        """
        Tests whether the media directory exists in the correct location.
        Also checks for the presence of cat.jpg.
        """
        does_media_dir_exist = os.path.isdir(self.media_dir)
   
        self.assertTrue(does_media_dir_exist, f"{FAILURE_HEADER}We couldn't find the /media/ directory in the expected location. Make sure it is in your project directory (at the same level as the manage.py module).{FAILURE_FOOTER}")
   
    def test_static_and_media_configuration(self):
        """
        Performs a number of tests on your Django project's settings in relation to static files and user upload-able files..
        """
        static_dir_exists = 'STATIC_DIR' in dir(settings)
        self.assertTrue(static_dir_exists, f"{FAILURE_HEADER}Your settings.py module does not have the variable STATIC_DIR defined.{FAILURE_FOOTER}")
        
        expected_path = os.path.normpath(self.static_dir)
        static_path = os.path.normpath(settings.STATIC_DIR)
        self.assertEqual(expected_path, static_path, f"{FAILURE_HEADER}The value of STATIC_DIR does not equal the expected path. It should point to your project root, with 'static' appended to the end of that.{FAILURE_FOOTER}")
        
        staticfiles_dirs_exists = 'STATICFILES_DIRS' in dir(settings)
        self.assertTrue(staticfiles_dirs_exists, f"{FAILURE_HEADER}The required setting STATICFILES_DIRS is not present in your project's settings.py module. Check your settings carefully. So many students have mistyped this one.{FAILURE_FOOTER}")
        self.assertEqual([static_path], settings.STATICFILES_DIRS, f"{FAILURE_HEADER}Your STATICFILES_DIRS setting does not match what is expected. Check your implementation against the instructions provided.{FAILURE_FOOTER}")
        
        staticfiles_dirs_exists = 'STATIC_URL' in dir(settings)
        self.assertTrue(staticfiles_dirs_exists, f"{FAILURE_HEADER}The STATIC_URL variable has not been defined in settings.py.{FAILURE_FOOTER}")
        self.assertEqual('/static/', settings.STATIC_URL, f"{FAILURE_HEADER}STATIC_URL does not meet the expected value of /static/. Make sure you have a slash at the end!{FAILURE_FOOTER}")
        
        media_dir_exists = 'MEDIA_DIR' in dir(settings)
        self.assertTrue(media_dir_exists, f"{FAILURE_HEADER}The MEDIA_DIR variable in settings.py has not been defined.{FAILURE_FOOTER}")
        
        expected_path = os.path.normpath(self.media_dir)
        media_path = os.path.normpath(settings.MEDIA_DIR)
        self.assertEqual(expected_path, media_path, f"{FAILURE_HEADER}The MEDIA_DIR setting does not point to the correct path. Remember, it should have an absolute reference to ITECH_Word_Game/media/.{FAILURE_FOOTER}")
        
        media_root_exists = 'MEDIA_ROOT' in dir(settings)
        self.assertTrue(media_root_exists, f"{FAILURE_HEADER}The MEDIA_ROOT setting has not been defined.{FAILURE_FOOTER}")
        
        media_root_path = os.path.normpath(settings.MEDIA_ROOT)
        self.assertEqual(media_path, media_root_path, f"{FAILURE_HEADER}The value of MEDIA_ROOT does not equal the value of MEDIA_DIR.{FAILURE_FOOTER}")
        
        media_url_exists = 'MEDIA_URL' in dir(settings)
        self.assertTrue(media_url_exists, f"{FAILURE_HEADER}The setting MEDIA_URL has not been defined in settings.py.{FAILURE_FOOTER}")
        
        media_url_value = settings.MEDIA_URL
        self.assertEqual('/media/', media_url_value, f"{FAILURE_HEADER}Your value of the MEDIA_URL setting does not equal /media/. Check your settings!{FAILURE_FOOTER}")   

class databaseConfigurationTests(TestCase):
    """
    Is your database configured as the book states?
    These tests should pass if you haven't tinkered with the database configuration.
    N.B. Some of the configuration values we could check are overridden by the testing framework -- so we leave them.
    """
    def setUp(self):
        pass
    
    def does_gitignore_include_database(self, path):
        """
        Takes the path to a .gitignore file, and checks to see whether the db.sqlite3 database is present in that file.
        """
        f = open(path, 'r')
        
        for line in f:
            line = line.strip()
            
            if line.startswith('db.sqlite3'):
                return True
        
        f.close()
        return False
    
    def test_databases_variable_exists(self):
        """
        Does the DATABASES settings variable exist, and does it have a default configuration?
        """
        self.assertTrue(settings.DATABASES, f"{FAILURE_HEADER}Your project's settings module does not have a DATABASES variable, which is required. Check the start of Chapter 5.{FAILURE_FOOTER}")
        self.assertTrue('default' in settings.DATABASES, f"{FAILURE_HEADER}You do not have a 'default' database configuration in your project's DATABASES configuration variable. Check the start of Chapter 5.{FAILURE_FOOTER}")
    
    def test_gitignore_for_database(self):
        """
        If you are using a Git repository and have set up a .gitignore, checks to see whether the database is present in that file.
        """
        git_base_dir = os.popen('git rev-parse --show-toplevel').read().strip()
        
        if git_base_dir.startswith('fatal'):
            warnings.warn("You don't appear to be using a Git repository for your codebase. Although not strictly required, it's *highly recommended*. Skipping this test.")
        else:
            gitignore_path = os.path.join(git_base_dir, '.gitignore')
            
            if os.path.exists(gitignore_path):
                self.assertTrue(self.does_gitignore_include_database(gitignore_path), f"{FAILURE_HEADER}Your .gitignore file does not include 'db.sqlite3' -- you should exclude the database binary file from all commits to your Git repository.{FAILURE_FOOTER}")
            else:
                warnings.warn("You don't appear to have a .gitignore file in place in your repository. We ask that you consider this! Read the Don't git push your Database paragraph in Chapter 5.")

class adminInterfaceTests(TestCase):
    """
    A series of tests that examines the authentication functionality (for superuser creation and logging in), and admin interface changes.
    Have all the admin interface tweaks been applied, and have the two models been added to the admin app?
    """
    def setUp(self):
        """
        Create a superuser account for use in testing.
        """
        User.objects.create_superuser('testAdmin', 'email@email.com', 'adminPassword123')
        self.client.login(username='testAdmin', password='adminPassword123')

    def test_admin_interface_accessible(self):
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}The admin interface is not accessible. Check that you didn't delete the 'admin/' URL pattern in your project's urls.py module.{FAILURE_FOOTER}")  

class populationScriptTests(TestCase):
    """
    Tests whether the population script puts the expected data into a test database.
    All values that are explicitly mentioned in the book are tested.
    Expects that the population script has the populate() function, as per the book!
    """
    def setUp(self):
        """
        Imports and runs the population script, calling the populate() method.
        """
        try:
            import populate_wordgame
        except ImportError:
            raise ImportError(f"{FAILURE_HEADER}The Chapter 5 tests could not import the populate_wordgame. Check it's in the right location (the first tango_with_django_project directory).{FAILURE_FOOTER}")
        
        if 'populate' not in dir(populate_wordgame):
            raise NameError(f"{FAILURE_HEADER}The populate() function does not exist in the populate_wordgame module. This is required.{FAILURE_FOOTER}")
        
        # Call the population script -- any exceptions raised here do not have fancy error messages to help readers.
        populate_wordgame.populate()

class formClassTests(TestCase):
    """
    Do the Form classes exist, and do they contain the correct instance variables?
    """
    def test_module_exists(self):
        """
        Tests that the forms.py module exists in the expected location.
        """
        project_path = os.getcwd()
        wordgame_app_path = os.path.join(project_path, 'wordgame')
        forms_module_path = os.path.join(wordgame_app_path, 'forms.py')

        self.assertTrue(os.path.exists(forms_module_path), f"{FAILURE_HEADER}We couldn't find wordgame's new forms.py module. This is required to be created at the top of Section 7.2. This module should be storing your two form classes.{FAILURE_FOOTER}")
    
    def test_UserProfileForm_form_class(self):
        """
        Does the UserProfileForm implementation exist, and does it contain the correct instance variables?
        """
        # Check that we can import CategoryForm.
        import wordgame.forms
        self.assertTrue('UserForm' in dir(wordgame.forms), f"{FAILURE_HEADER}The class UserForm could not be found in wordgame's forms.py module. Check you have created this class in the correct location, and try again.{FAILURE_FOOTER}")

        from wordgame.forms import UserProfileForm
        userProfile = UserProfileForm()

        # Do you correctly link Category to CategoryForm?
        self.assertEqual(type(userProfile.__dict__['instance']), User, f"{FAILURE_HEADER}The UserProfileForm does not link to the Category model. Have a look in the CategoryForm's nested Meta class for the model attribute.{FAILURE_FOOTER}")

        # Now check that all the required fields are present, and of the correct form field type.
        fields = userProfile.fields

        expected_fields = {
            'username': django_fields.CharField,
            'password': django_fields.CharField,
            'sex': django_fields.ChoiceField,
            'email': django_fields.EmailField,
            'photo':django_fields.ImageField,
        }

        for expected_field_name in expected_fields:
            expected_field = expected_fields[expected_field_name]

            self.assertTrue(expected_field_name in fields.keys(), f"{FAILURE_HEADER}The field '{expected_field_name}' was not found in your CategoryForm implementation. Check you have all required fields, and try again.{FAILURE_FOOTER}")
            self.assertEqual(expected_field, type(fields[expected_field_name]), f"{FAILURE_HEADER}The field '{expected_field_name}' in CategoryForm was not of the expected type '{type(fields[expected_field_name])}'.{FAILURE_FOOTER}")

    def test_UserForm_form_class(self):
            """
            Does the UserForm implementation exist, and does it contain the correct instance variables?
            """
            # Check that we can import CategoryForm.
            import wordgame.forms
            self.assertTrue('UserForm' in dir(wordgame.forms), f"{FAILURE_HEADER}The class UserForm could not be found in wordgame's forms.py module. Check you have created this class in the correct location, and try again.{FAILURE_FOOTER}")

            from wordgame.forms import UserForm
            userForm = UserForm()

            # Do you correctly link Category to CategoryForm?
            self.assertEqual(type(userForm.__dict__['instance']), User, f"{FAILURE_HEADER}The UserForm does not link to the Category model. Have a look in the CategoryForm's nested Meta class for the model attribute.{FAILURE_FOOTER}")

            # Now check that all the required fields are present, and of the correct form field type.
            fields = userForm.fields

            expected_fields = {
                'username': django_fields.CharField,
                'password': django_fields.CharField,
                'PasswordConfirm': django_fields.CharField,
                'email': django_fields.EmailField,
            }

            for expected_field_name in expected_fields:
                expected_field = expected_fields[expected_field_name]

                self.assertTrue(expected_field_name in fields.keys(), f"{FAILURE_HEADER}The field '{expected_field_name}' was not found in your CategoryForm implementation. Check you have all required fields, and try again.{FAILURE_FOOTER}")
                self.assertEqual(expected_field, type(fields[expected_field_name]), f"{FAILURE_HEADER}The field '{expected_field_name}' in CategoryForm was not of the expected type '{type(fields[expected_field_name])}'.{FAILURE_FOOTER}")

class gamePageTests(TestCase):
    """
    Testing the basics of your game view and URL mapping.
    Also runs tests to check the response from the server.
    """
    def setUp(self):
        self.views_module = importlib.import_module('wordgame.views')
        self.views_module_listing = dir(self.views_module)       
        self.project_urls_module = importlib.import_module('ITECH_Word_Game.urls')
    
    def test_view_exists(self):
        """
        Does the game() view exist in wordgame's views.py module?
        """
        name_exists = 'game' in self.views_module_listing
        is_callable = callable(self.views_module.game)
        
        self.assertTrue(name_exists, f"{FAILURE_HEADER}The game() view for wordgame does not exist.{FAILURE_FOOTER}")
        self.assertTrue(is_callable, f"{FAILURE_HEADER}Check that you have created the game() view correctly. It doesn't seem to be a function!{FAILURE_FOOTER}")
    
    def test_mappings_exists(self):
        """
        Are the two required URL mappings present and correct?
        One should be in the project's urls.py, the second in wordgame's urls.py.
        We have the 'game' view named twice -- it should resolve to '/wordgame/'.
        """
        game_mapping_exists = False
        
        # This is overridden. We need to manually check it exists.
        for mapping in self.project_urls_module.urlpatterns:
            if hasattr(mapping, 'name'):
                if mapping.name == 'game':
                    game_mapping_exists = True
        
        self.assertTrue(game_mapping_exists, f"{FAILURE_HEADER}The game URL mapping could not be found. Check your PROJECT'S urls.py module.{FAILURE_FOOTER}")
        self.assertEquals(reverse('wordgame:game'), '/wordgame/', f"{FAILURE_HEADER}The game URL lookup failed. Check wordgame's urls.py module. You're missing something in there.{FAILURE_FOOTER}")    

class leaderboardPageTests(TestCase):
    """
    Tests to check the leaderboard view.
    We check whether the view exists, the mapping is correct, and the response is correct.
    """
    def setUp(self):
        self.views_module = importlib.import_module('wordgame.views')
        self.views_module_listing = dir(self.views_module)
    
    def test_view_exists(self):
        """
        Does the leaderboard() view exist in wordgame's views.py module?
        """
        name_exists = 'leaderboard' in self.views_module_listing
        is_callable = callable(self.views_module.leaderboard)
        
        self.assertTrue(name_exists, f"{FAILURE_HEADER}We couldn't find the view for your leaderboard view! It should be called leardboard().{FAILURE_FOOTER}")
        self.assertTrue(is_callable, f"{FAILURE_HEADER}Check you have defined your leaderboard() view correctly. We can't execute it.{FAILURE_FOOTER}")
    
    def test_mapping_exists(self):
        """
        Checks whether the leaderboard view has the correct URL mapping.
        """
        self.assertEquals(reverse('wordgame:leaderboard'), '/wordgame/leaderboard/', f"{FAILURE_HEADER}Your about URL mapping is either missing or mistyped.{FAILURE_FOOTER}")

class registrationTests(TestCase):
    """
    A series of tests that examine changes to views that take place in Chapter 9.
    Specifically, we look at tests related to registering a user.
    """
    def test_new_registration_view_exists(self):
        """
        Checks to see if the new registration view exists in the correct place, with the correct name.
        """
        url = ''

        try:
            url = reverse('wordgame:register')
        except:
            pass
        
        self.assertEqual(url, '/wordgame/register/', f"{FAILURE_HEADER}Have you created the wordgame:register URL mapping correctly? It should point to the new register() view, and have a URL of '/wordgame/register/' Remember the first part of the URL (/wordgame/) is handled by the project's urls.py module, and the second part (register/) is handled by the wordgame app's urls.py module.{FAILURE_FOOTER}")
    
    def test_registration_template(self):
        """
        Does the register.html template exist in the correct place, and does it make use of template inheritance?
        """
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'wordgame')
        template_path = os.path.join(template_base_path, 'register.html')
        self.assertTrue(os.path.exists(template_path), f"{FAILURE_HEADER}We couldn't find the 'register.html' template in the 'templates/wordgame/' directory. Did you put it in the right place?{FAILURE_FOOTER}")
      
    def test_good_form_creation(self):
        """
        Tests the functionality of the forms.
        Creates a UserProfileForm and UserForm, and attempts to save them.
        Upon completion, we should be able to login with the details supplied.
        """
        user_data = {'username': 'testuser', 'password': 'test123','PasswordConfirm': 'test123', 'email': 'test@test.com'}
        user_form = forms.UserForm(data=user_data)
        user_object = user_form.save()
        user_object.set_password(user_data['password'])
        user_object.save()    
        self.assertEqual(len(User.objects.all()), 1, f"{FAILURE_HEADER}We were expecting to see a User object created, but it didn't appear. Check your UserForm implementation, and try again.{FAILURE_FOOTER}")
        self.assertTrue(self.client.login(username='testuser', password='test123'), f"{FAILURE_HEADER}We couldn't log our sample user in during the tests. Please check your implementation of UserForm and UserProfileForm.{FAILURE_FOOTER}")
    
    def test_base_for_register_link(self):
        """
        Tests whether the registration link has been added to the base.html template.
        This should work for pre-exercises, and post-exercises.
        """
        template_login_path = os.path.join(settings.TEMPLATE_DIR, 'wordgame')
        login_path = os.path.join(template_login_path, 'login.html')
        template_str = get_template(login_path)
        self.assertTrue('Create Account' in template_str)

class loginTests(TestCase):
    """
    A series of tests for checking the login functionality of wordgame.
    """
    def test_login_url_exists(self):
        """
        Checks to see if the new login view exists in the correct place, with the correct name.
        """
        url = ''

        try:
            url = reverse('wordgame:login')
        except:
            pass
        
        self.assertEqual(url, '/wordgame/login/', f"{FAILURE_HEADER}Have you created the wordgame:login URL mapping correctly? It should point to the new login() view, and have a URL of '/wordgame/login/' Remember the first part of the URL (/wordgame/) is handled by the project's urls.py module, and the second part (login/) is handled by the wordgame app's urls.py module.{FAILURE_FOOTER}")

    def test_login_functionality(self):
        """
        Tests the login functionality. A user should be able to log in, and should be redirected to the wordgame homepage.
        """
        user_object = create_user_object()

        response = self.client.post(reverse('wordgame:login'), {'username': 'testuser', 'password': 'testabc123'})
        
        try:
            self.assertEqual(user_object.id, int(self.client.session['_auth_user_id']), f"{FAILURE_HEADER}We attempted to log a user in with an ID of {user_object.id}, but instead logged a user in with an ID of {self.client.session['_auth_user_id']}. Please check your login() view.{FAILURE_FOOTER}")
        except KeyError:
            self.assertTrue(False, f"{FAILURE_HEADER}When attempting to log in with your login() view, it didn't seem to log the user in. Please check your login() view implementation, and try again.{FAILURE_FOOTER}")

        self.assertEqual(response.status_code, 302, f"{FAILURE_HEADER}Testing your login functionality, logging in was successful. However, we expected a redirect; we got a status code of {response.status_code} instead. Check your login() view implementation.{FAILURE_FOOTER}")
        self.assertEqual(response.url, reverse('wordgame:game'), f"{FAILURE_HEADER}We were not redirected to the wordgame homepage after logging in. Please check your login() view implementation, and try again.{FAILURE_FOOTER}")


    def test_login_template_content(self):
        """
        Some simple checks for the login.html template. Is the required text present?
        """
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'wordgame')
        template_path = os.path.join(template_base_path, 'login.html')
        self.assertTrue(os.path.exists(template_path), f"{FAILURE_HEADER}We couldn't find the 'login.html' template in the 'templates/wordgame/' directory. Did you put it in the right place?{FAILURE_FOOTER}")
        
        template_str = get_template(template_path)
        self.assertTrue('<h1>Login to w[&nbsp;]rdle!</h1>' in template_str, f"{FAILURE_HEADER}We couldn't find the '<h1>Login to wordgame</h1>' in the login.html template.{FAILURE_FOOTER}")
        self.assertTrue('action="{% url \'wordgame:login\' %}"' in template_str, f"{FAILURE_HEADER}We couldn't find the url lookup for 'wordgame:login' in your login.html <form>.{FAILURE_FOOTER}")
        self.assertTrue('<button type="submit" value="login" class="btn btn-info setWidth_120">login</button>' in template_str, f"{FAILURE_HEADER}We couldn't find the submit button in your login.html template. Check it matches what is in the book, and try again.{FAILURE_FOOTER}")
    
class restrictedAccessTests(TestCase):
    """
    Some tests to test the restricted access view. Can users who are not logged in see it?
    """
    def test_restricted_url_exists(self):
        """
        Checks to see if the new restricted view exists in the correct place, with the correct name.
        """
        url = ''

        try:
            url = reverse('wordgame:restricted')
        except:
            pass
        
        self.assertEqual(url, '/wordgame/restricted/', f"{FAILURE_HEADER}Have you created the wordgame:restricted URL mapping correctly? It should point to the new restricted() view, and have a URL of '/wordgame/restricted/' Remember the first part of the URL (/wordgame/) is handled by the project's urls.py module, and the second part (restricted/) is handled by the wordgame app's urls.py module.{FAILURE_FOOTER}")
    
    def test_bad_request(self):
        """
        Tries to access the restricted view when not logged in.
        This should redirect the user to the login page.
        """
        response = self.client.get(reverse('wordgame:restricted'))
        
        self.assertEqual(response.status_code, 302, f"{FAILURE_HEADER}We tried to access the restricted view when not logged in. We expected to be redirected, but were not. Check your restricted() view.{FAILURE_FOOTER}")
        self.assertTrue(response.url.startswith(reverse('wordgame:login')), f"{FAILURE_HEADER}We tried to access the restricted view when not logged in, and were expecting to be redirected to the login view. But we were not! Please check your restricted() view.{FAILURE_FOOTER}")
    
    def test_good_request(self):
        """
        Attempts to access the restricted view when logged in.
        This should not redirect. We cannot test the content here. Only links in base.html can be checked -- we do this in the exercise tests.
        """
        create_user_object()
        self.client.login(username='testuser', password='testabc123')

        response = self.client.get(reverse('wordgame:restricted'))
        self.assertTrue(response.status_code, 200)

class logoutTests(TestCase):
    """
    A few tests to check the functionality of logging out. Does it work? Does it actually log you out?
    """
    def test_bad_request(self):
        """
        Attepts to log out a user who is not logged in.
        This should according to the book redirect you to the login page.
        """
        response = self.client.get(reverse('wordgame:logout'))
        self.assertTrue(response.status_code, 302)
        self.assertTrue(response.url, reverse('wordgame:login'))
    
    def test_good_request(self):
        """
        Attempts to log out a user who IS logged in.
        This should succeed -- we should be able to login, check that they are logged in, logout, and perform the same check.
        """
        user_object = create_user_object()
        self.client.login(username='testuser', password='testabc123')

        try:
            self.assertEqual(user_object.id, int(self.client.session['_auth_user_id']), f"{FAILURE_HEADER}We attempted to log a user in with an ID of {user_object.id}, but instead logged a user in with an ID of {self.client.session['_auth_user_id']}. Please check your login() view. This happened when testing logout functionality.{FAILURE_FOOTER}")
        except KeyError:
            self.assertTrue(False, f"{FAILURE_HEADER}When attempting to log a user in, it failed. Please check your login() view and try again.{FAILURE_FOOTER}")
        
        # Now lot the user out. This should cause a redirect to the homepage.
        response = self.client.get(reverse('wordgame:logout'))
        self.assertEqual(response.status_code, 302, f"{FAILURE_HEADER}Logging out a user should cause a redirect, but this failed to happen. Please check your logout() view.{FAILURE_FOOTER}")
        self.assertEqual(response.url, reverse('wordgame:game'), f"{FAILURE_HEADER}When logging out a user, the book states you should then redirect them to the homepage. This did not happen; please check your logout() view.{FAILURE_FOOTER}")
        self.assertTrue('_auth_user_id' not in self.client.session, f"{FAILURE_HEADER}Logging out with your logout() view didn't actually log the user out! Please check yout logout() view.{FAILURE_FOOTER}")

def create_user_object():
    """
    Helper function to create a User object.
    """
    user = User.objects.get_or_create(username='testuser',
                                      first_name='Test',
                                      last_name='User',
                                      email='test@test.com')[0]
    user.set_password('testabc123')
    user.save()

    return user

def create_super_user_object():
    """
    Helper function to create a super user (admin) account.
    """
    return User.objects.create_superuser('admin', 'admin@test.com', 'testpassword')

def get_template(path_to_template):
    """
    Helper function to return the string representation of a template file.
    """
    f = open(path_to_template, 'r')
    template_str = ""

    for line in f:
        template_str = f"{template_str}{line}"

    f.close()
    return template_str

class ModelTests(TestCase):
    """
    Tests to check whether the UserProfile model has been created according to the specification.
    """
    def test_userprofile_class(self):
        """
        Does the UserProfile class exist in wordgame.models? If so, are all the required attributes present?
        Assertion fails if we can't assign values to all the fields required (i.e. one or more missing).
        """
        self.assertTrue('UserProfile' in dir(wordgame.models))

        user_profile = wordgame.models.UserProfile()

        # Now check that all the required attributes are present.
        # We do this by building up a UserProfile instance, and saving it.
        expected_attributes = {
            'sex': '0',
            'photo': tempfile.NamedTemporaryFile(suffix=".jpg").name,
            'user': create_user_object(),
        }

        expected_types = {
            'sex': models.fields.IntegerField,
            'photo': models.fields.files.ImageField,
            'user': models.fields.related.OneToOneField,
        }

        found_count = 0

        for attr in user_profile._meta.fields:
            attr_name = attr.name

            for expected_attr_name in expected_attributes.keys():
                if expected_attr_name == attr_name:
                    found_count += 1

                    self.assertEqual(type(attr), expected_types[attr_name], f"{FAILURE_HEADER}The type of attribute for '{attr_name}' was '{type(attr)}'; we expected '{expected_types[attr_name]}'. Check your definition of the UserProfile model.{FAILURE_FOOTER}")
                    setattr(user_profile, attr_name, expected_attributes[attr_name])
        
        self.assertEqual(found_count, len(expected_attributes.keys()), f"{FAILURE_HEADER}In the UserProfile model, we found {found_count} attributes, but were expecting {len(expected_attributes.keys())}. Check your implementation and try again.{FAILURE_FOOTER}")
        user_profile.save()
    

    def test_model_admin_interface_inclusion(self):
        """
        Attempts to access the UserProfile admin interface instance.
        If we don't get a HTTP 200, then we assume that the model has not been registered. Fair assumption!
        """
        super_user = create_super_user_object()
        self.client.login(username='admin', password='testpassword')

        # The following URL should be available if the UserProfile model has been registered to the admin interface.
        response = self.client.get('/admin/wordgame/userprofile/')
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}When attempting to access the UserProfile in the admin interface, we didn't get a HTTP 200 status code. Did you register the new model with the admin interface?{FAILURE_FOOTER}")

