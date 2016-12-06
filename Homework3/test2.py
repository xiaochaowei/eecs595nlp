from dependencyData import DependencyData

d = DependencyData()
datum = [[u'ROOT', None, None],
[u'majority', u'nn', 2],
[u'opinion', u'nsubj', 6],
[u'in', u'prep', 2],
[u'this', u'det', 5],
[u'case', u'pobj', 3],
[u'notes', u'root', 0],
[u'that', u'mark', 17],
[u'california', u'poss', 11],
[u"'s", u'possessive', 8],
[u'continual', u'amod', 11],
[u'invocation', u'nsubjpass', 17],
[u'of', u'prep', 11],
[u'worthless', u'amod', 14],
[u'remedies', u'pobj', 12],
[u'is', u'auxpass', 17],
[None, None, None],
[u'buttressed', u'ccomp', 6],
[u'by', u'prep', 17],
[u'the', u'det', 20],
[u'experience', u'pobj', 18],
[u'of', u'prep', 20],
[u'other', u'amod', 23],
[u'states', u'pobj', 21]]

print d.sort_datum(datum)
