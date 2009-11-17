"""
>>> from models.publication import Publication
>>> from models.article import Article
>>> from django.contrib.auth.views import Site

>>> p = Publication(title="FooBar")
>>> p.save()
>>> p
<Publication: Publication object>

>>> from django.contrib.sites.models import Site
>>> current_site = Site.objects.get_current()
>>> current_site
<Site: example.com>

# Regression for #12168: models split into subpackages still get M2M tables

>>> a = Article(headline="a foo headline")
>>> a.save()
>>> a.publications.add(p)
>>> a.sites.add(current_site)
>>> a.save()

>>> a = Article.objects.get(id=1)
>>> a
<Article: Article object>
>>> a.id
1
>>> a.sites.count()
1

"""


