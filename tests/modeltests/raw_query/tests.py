from django.test import TestCase
from datetime import datetime
from models import Author, Book, Coffee, Reviewer

class RawQueryTests(TestCase):
    
    def setUp(self):
        self.authors = []
        self.books = []
        self.coffees = []
        self.reviewers = []
        
        self.authors.append(Author.objects.create(
            first_name="Joe",
            last_name="Smith",
            dob=datetime(year=1950, month=9, day=20),
        ))
        self.authors.append(Author.objects.create(
            first_name="Jill",
            last_name="Doe",
            dob=datetime(year=1920, month=4, day=2),
        ))
        self.authors.append(Author.objects.create(
            first_name="Bob",
            last_name="Smith",
            dob=datetime(year=1986, month=1, day=25),
        ))
        self.authors.append(Author.objects.create(
            first_name="Bill",
            last_name="Jones",
            dob=datetime(year=1932, month=5, day=10),
        ))
        
        self.books.append(Book.objects.create(
            title = 'The awesome book',
            author = self.authors[0],
        ))

        self.books.append(Book.objects.create(
            title = 'The horrible book',
            author = self.authors[0],
        ))

        self.books.append(Book.objects.create(
            title = 'Another awesome book',
            author = self.authors[0],
        ))
        
        self.books.append(Book.objects.create(
            title = 'Some other book',
            author = self.authors[2],
        ))
        
        self.coffees.append(Coffee.objects.create(brand="dunkin doughnuts"))
        self.coffees.append(Coffee.objects.create(brand="starbucks"))
        
        self.reviewers.append(Reviewer.objects.create())
        self.reviewers.append(Reviewer.objects.create())
        self.reviewers[0].reviewed.add(self.books[3])
        self.reviewers[0].reviewed.add(self.books[1])
        self.reviewers[0].reviewed.add(self.books[2])
        
    def assertSuccessfulRawQuery(self, model, query, expected_results, \
            expected_annotations=(), params=[], translations=None):
        results = model.objects.raw(query=query, params=params, \
                            translations=translations)
        self.assertProcessed(results, expected_results, expected_annotations)
        self.assertAnnotations(results, expected_annotations)
        
    def assertProcessed(self, results, orig, expected_annotations=()):
        self.assertEqual(len(results), len(orig))
        for index, item in enumerate(results):
            orig_item = orig[index]
            for annotation in expected_annotations:
                setattr(orig_item, *annotation)

            self.assertEqual(item.id, orig_item.id)

    def assertNoAnnotations(self, results):
        self.assertAnnotations(results, ())

    def assertAnnotations(self, results, expected_annotations):
        self.assertEqual(results._annotations, expected_annotations)
        
    def testSimpleRawQuery(self):
           query = "SELECT * FROM raw_query_author"
           self.assertSuccessfulRawQuery(Author, query, self.authors)