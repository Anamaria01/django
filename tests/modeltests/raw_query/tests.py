from django.test import TestCase
from datetime import datetime
from models import Author, Book, Coffee, Reviewer

from django.db.models.query import InsuficientFields
from django.db.models.sql.query import InvalidQuery

class RawQueryTests(TestCase):
    
    def __init__(self, *args, **kwargs):
        super(RawQueryTests, self).__init__(*args, **kwargs)
        self.authors = list(Author.objects.all())
        self.books = list(Book.objects.all())
        self.coffees = list(Coffee.objects.all())
        self.reviewers = list(Reviewer.objects.all())
        
    def assertSuccessfulRawQuery(self, model, query, expected_results, \
            expected_annotations=(), params=[], translations=None):
        """
        Execute the passed query against the passed model and check the output
        """
        results = model.objects.raw(query=query, params=params, \
                            translations=translations)
        self.assertProcessed(results, expected_results, expected_annotations)
        self.assertAnnotations(results, expected_annotations)
        
    def assertProcessed(self, results, orig, expected_annotations=()):
        """
        Compare the results of a raw query against expected results
        """
        self.assertEqual(len(results), len(orig))
        for index, item in enumerate(results):
            orig_item = orig[index]
            for annotation in expected_annotations:
                setattr(orig_item, *annotation)

            self.assertEqual(item.id, orig_item.id)

    def assertNoAnnotations(self, results):
        """
        Check that the results of a raw query contain no annotations
        """
        self.assertAnnotations(results, ())

    def assertAnnotations(self, results, expected_annotations):
        """
        Check that the passed raw query results contain the expected
        annotations
        """
        for result in results:
          for annotation in expected_annotations:
            self.assertTrue(hasattr(result, annotation))
        
    def testSimpleRawQuery(self):
        """
        Basic test of raw query with a simple database query
        """
        query = "SELECT * FROM raw_query_author"
        self.assertSuccessfulRawQuery(Author, query, self.authors)

    def testFkeyRawQuery(self):
        """
        Test of a simple raw query against a model containing a foreign key
        """
        query = "SELECT * FROM raw_query_book"
        self.assertSuccessfulRawQuery(Book, query, self.books)
        
    def testDBColumnHandler(self):
        """
        Test of a simple raw query against a model containing a field with 
        db_column defined.
        """
        query = "SELECT * FROM raw_query_coffee"
        self.assertSuccessfulRawQuery(Coffee, query, self.coffees)
    
    def testOrderHandler(self):
        """
        Test of raw raw query's tolerance for columns being returned in any
        order
        """
        selects = (
            ('dob, last_name, first_name, id'),
            ('last_name, dob, first_name, id'),
            ('first_name, last_name, dob, id'),
        )

        for select in selects:
            query = "SELECT %s FROM raw_query_author" % select
            self.assertSuccessfulRawQuery(Author, query, self.authors)
            
    def testTranslations(self):
        """
        Test of raw query's optional ability to translate unexpected result
        column names to specific model fields
        """
        query = "SELECT first_name AS first, last_name AS last, dob, id FROM raw_query_author"
        translations = (
            ('first', 'first_name'),
            ('last', 'last_name'),
        )
        self.assertSuccessfulRawQuery(Author, query, self.authors, translations=translations)
        
    def testParams(self):
        """
        Test passing optional query parameters
        """
        query = "SELECT * FROM raw_query_author WHERE first_name = %s"
        params = [self.authors[2].first_name]
        results = Author.objects.raw(query=query, params=params)
        self.assertProcessed(results, [self.authors[2]])
        self.assertNoAnnotations(results)
        self.assertEqual(len(results), 1)
        
    def testManyToMany(self):
        """
        Test of a simple raw query against a model containing a m2m field
        """
        query = "SELECT * FROM raw_query_reviewer"
        self.assertSuccessfulRawQuery(Reviewer, query, self.reviewers)
        
    def testExtraConversions(self):
        """
        Test to insure that extra translations are ignored.
        """
        query = "SELECT * FROM raw_query_author"
        translations = (('something', 'else'),)
        self.assertSuccessfulRawQuery(Author, query, self.authors, translations=translations)
        
    def testInsufficientColumns(self):
        query = "SELECT first_name, dob FROM raw_query_author"
        raised = False
        try:
            results = Author.objects.raw(query)
            results_list = list(results)
        except InsuficientFields:
            raised = True

        self.assertTrue(raised)
        
    def testAnnotations(self):
        query = "SELECT a.*, count(b.id) as book_count FROM raw_query_author a LEFT JOIN raw_query_book b ON a.id = b.author_id GROUP BY a.id, a.first_name, a.last_name, a.dob ORDER BY a.id"
        expected_annotations = (
            ('book_count', 3),
            ('book_count', 0),
            ('book_count', 1),
            ('book_count', 0),
        )
        self.assertSuccessfulRawQuery(Author, query, self.authors, expected_annotations)
        
    def testInvalidQuery(self):
        query = "UPDATE raw_query_author SET first_name='thing' WHERE first_name='Joe'"
        self.assertRaises(InvalidQuery, Author.objects.raw, query)
        
    def testWhiteSpaceQuery(self):
        query = "    SELECT * FROM raw_query_author"
        self.assertSuccessfulRawQuery(Author, query, self.authors)