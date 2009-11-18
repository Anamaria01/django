from django.db import models
    
class Author(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    dob = models.DateField()
    
    def __init__(self, *args, **kwargs):
        super(Author, self).__init__(*args, **kwargs)
        
        # Perform a check for missing params to protect against real fields
        # being added as annotations.
        if len(args) == 0:
            expected_keywords = ['dob', 'first_name', 'last_name']
            for keyword in expected_keywords:
                if keyword not in kwargs.keys():
                    raise Exception('All fields are required.  %s is missing' %
                                      keyword)
            
        
    
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author)
    
class Coffee(models.Model):
    brand = models.CharField(max_length=255, db_column="name")
    
class Reviewer(models.Model):
    reviewed = models.ManyToManyField(Book)