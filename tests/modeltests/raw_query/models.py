from django.db import models
    
class Author(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    dob = models.DateField()
    
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author)
    
class Coffee(models.Model):
    brand = models.CharField(max_length=255, db_column="name")
    
class Reviewer(models.Model):
    reviewed = models.ManyToManyField(Book)