I1
==

Can order have lines that have same SKU?


I2
==

https://github.com/python-leap/book/blob/master/chapter_02_repository.asciidoc
example:


@flask.route.gubbins
def allocate_endpoint():
    batches = SqlAlchemyRepository.list()
    lines = [
        OrderLine(l['orderid'], l['sku'], l['qty'])
         for l in request.params...
    ]
    allocate(lines, batches)
    session.commit()
    return 201


SqlAlchemyRepository requires session.


i3
==
Example 2

replace os.walk with new approach
for folder, _, files in os.walk(dest):

Example 3. Some end-to-end tests (test_sync.py) - use context manager



