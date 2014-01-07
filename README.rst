Repo: apriori
----------------
Features
--------------
- *Python*
- ``pandas`` *Python statistical package*
Description
------------------
While working on a project to extract information from the free text fields
of aircraft maintenance records, I wanted to see if it wasn't possible to use
the structured data fields of those records to normalize the irregular
language found in the free-text fields and alleviate the added complexity of
processing them with standard NLP techniques.  Later I was able to turn this
question into a methodical investigation for a Data Mining class.  As part of
my class project, I wrote this implementation of the common apriori algorithm,
based on the description found in Han, J., Kamber, M., Pei, J. (2006).  *Data
Mining: Concepts and Techniques*, Morgan Kaufmann, p. 253.

Frequent itemset mining is a subclass of frequent pattern mining, and is used
to detect patterns of commonly co-occurring events.  A classic example of
frequent itemset mining is market basket analysis, wherein a marketing analyst
uses purchasing history data to determine which products are likely to be 
purchased together in order to make decisions about placement of goods or 
special offers.  In order to see if there were similar frequent co-occurrences
of structured data values and whether or not these patterns mapped to strong
support for references to single part names in free text fields, I adapted the
apriori algorithm to find frequently occurring sets of structured data values.
For the algorithm to work within the domain of maintenance records, certain
subtleties had to be incorporated into it.  Each maintenance record is treated
as though it were a market transaction; field-value pairs are equivalent to
purchased items.  Since a record cannot have more than one structured data
entry of the same field, when building candidate itemsets items must be withheld
from a set when their field names match another already in the set.  However,
two sequences of field-value pairings cannot be considered equal unless all
field names and their corresponding values align, so when determining itemset 
equality items must be compared by both field name and value.  This subtlety
is manifest in the different treatments of Item and Itemset hash functions, 
which are used for set construction.
