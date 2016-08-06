"""

This file is the place to write solutions for the
skills assignment called skills-sqlalchemy. Remember to
consult the exercise directions for more complete
explanations of the assignment.

All classes from model.py are being imported for you
here, so feel free to refer to classes without the
[model.]User prefix.

"""

from model import *

init_app()

# -------------------------------------------------------------------
# Part 2: Write queries


# Get the brand with the **id** of 8.
Brand.query.get(8)

# Get all models with the **name** Corvette and the **brand_name** Chevrolet.
Model.query.filter_by(name='Corvette', brand_name='Chevrolet').all()

# Get all models that are older than 1960.
db.session.query(Model).filter(Model.year < 1960).all()

# Get all brands that were founded after 1920.
db.session.query(Brand).filter(Brand.founded > 1920).all()

# Get all models with names that begin with "Cor".
Model.query.filter(Model.name.like('Cor%')).all()

# Get all brands that were founded in 1903 and that are not yet discontinued.
Brand.query.filter(Brand.founded == 1903, Brand.discontinued == None).all()

# Get all brands that are either 1) discontinued (at any time) or 2) founded 
# before 1950.
Brand.query.filter(db.or_(Brand.discontinued != None, Brand.founded < 1950)).all()

# Get any model whose brand_name is not Chevrolet.
Model.query.filter(Model.brand_name != 'Chevrolet').first()

# Fill in the following functions. (See directions for more info.)

def get_model_info(year):
    '''Takes in a year, and prints out each model, brand_name, and brand
    headquarters for that year using only ONE database query.'''

    models = Model.query.options(db.joinedload('brand')).filter(Model.year == year).all()
    for model in models:
        print model.name, model.brand_name, model.brand.headquarters

def get_brands_summary():
    '''Prints out each brand name, and each model name for that brand
     using only ONE database query.'''

    brands = Brand.query.options(db.joinedload('models')).all()
    for brand in brands:
        print brand.name.upper()
        for model in brand.models:
            print "\t" + model.name

    # I realize this prints model names multiple times, once for every year
    # they're in the table, but I can't figure out how to write the query.

    # Only models with distinct names, but then how do I organize them by brand?
    # Model.query.distinct(Model.name).all()

    # Sorted by brand, but then how do I filter out the extra models?
    # Model.query.order_by(Model.brand_name).all()

    # Just the distinct model names, but I can't seem to add the brand names?
    # db.session.query(Model.name).group_by(Model.name).all()

    # I tried this but it isn't working?
    # db.session.query(Model.brand_name, Model.name).group_by(Model.name).order_by(Model.brand_name).all()

    # It raises the following error:
    # ProgrammingError: (psycopg2.ProgrammingError) column "models.brand_name"
    # must appear in the GROUP BY clause or be used in an aggregate function

    # I guess I could make a dictionary where the key-value pairs are brands and
    # lists of models -- we talked about doing that with a defaultdict in study
    # hall -- but it doesn't seem to be within the spirit of the assessment?

# -------------------------------------------------------------------
# Part 2.5: Discussion Questions (Include your answers as comments.)

# 1. What is the returned value and datatype of ``Brand.query.filter_by(name='Ford')``?

# It returns an instance of a BaseQuery object. (You need .all() or .first() to
# actually run the query.)

# 2. In your own words, what is an association table, and what *type* of relationship
# does an association table manage?

# An association table manages a many-to-many relationship. For example, a book
# can have many genres, and a genre can have many books, but for reasons of
# normalization, we keep books in their own table and genres in their own table,
# and mediate their relationship through an association table.

# -------------------------------------------------------------------
# Part 3

def search_brands_by_name(mystr):
    """Returns a list of objects that are brands whose name contains or is equal
    to the input string."""

    results = Brand.query.filter(db.or_(Brand.name.like('%'+mystr+'%'),
                                 Brand.name == mystr)).all()
    return results


def get_models_between(start_year, end_year):
    """Returns a list of objects that are models with years that fall between
    the start year (inclusive) and end year (exclusive)."""

    results = Model.query.filter(Model.year > start_year-1, Model.year < end_year).all()
    return results
