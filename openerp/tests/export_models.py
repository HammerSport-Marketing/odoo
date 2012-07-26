# -*- coding: utf-8 -*-
from openerp.osv import orm, fields

models = [
    ('boolean', fields.boolean()),
    ('integer', fields.integer()),
    ('float', fields.float()),
    ('decimal', fields.float(digits=(16, 3))),
    ('string.bounded', fields.char('unknown', size=16)),
    ('string', fields.char('unknown', size=None)),
    ('date', fields.date()),
    ('datetime', fields.datetime()),
    ('text', fields.text()),
    ('selection', fields.selection([(1, "Foo"), (2, "Bar"), (3, "Qux")])),
    # just relate to an integer
    ('many2one', fields.many2one('export.integer')),
    ('one2many', fields.one2many('export.one2many.child', 'parent_id')),
    ('many2many', fields.many2many('export.many2many.other'))
    # TODO: function?
    # TODO: related?
    # TODO: reference?
]
for name, field in models:
    attrs = {
        '_name': 'export.%s' % name,
        '_module': 'base',
        '_columns': {
            'const': fields.integer(),
            'value': field
        },
        '_defaults': {'const': 4},
        'name_get': (lambda self, cr, uid, ids, context=None:
            [(record.id, "%s:%s" % (self._name, record.value))
             for record in self.browse(cr, uid, ids, context=context)])
    }
    NewModel = type(
        'Export%s' % ''.join(section.capitalize() for section in name.split('.')),
        (orm.Model,),
        attrs)

class One2ManyChild(orm.Model):
    _name = 'export.one2many.child'
    _module = 'base'
    # FIXME: orm.py:1161, fix to name_get on m2o field
    _rec_name = 'value'

    _columns = {
        'parent_id': fields.many2one('export.one2many'),
        'str': fields.char('unknown', size=None),
        'value': fields.integer()
    }
    def name_get(self, cr, uid, ids, context=None):
        return [(record.id, "%s:%s" % (self._name, record.value))
            for record in self.browse(cr, uid, ids, context=context)]

class One2ManyMultiple(orm.Model):
    _name = 'export.one2many.multiple'
    _module = 'base'

    _columns = {
        'const': fields.integer(),
        'child1': fields.one2many('export.one2many.child.1', 'parent_id'),
        'child2': fields.one2many('export.one2many.child.2', 'parent_id'),
    }
    _defaults = { 'const': 36 }

class One2ManyChildMultiple(orm.Model):
    _name = 'export.one2many.multiple.child'
    _module = 'base'
    # FIXME: orm.py:1161, fix to name_get on m2o field
    _rec_name = 'value'

    _columns = {
        'parent_id': fields.many2one('export.one2many.multiple'),
        'str': fields.char('unknown', size=None),
        'value': fields.integer()
    }
    def name_get(self, cr, uid, ids, context=None):
        return [(record.id, "%s:%s" % (self._name, record.value))
            for record in self.browse(cr, uid, ids, context=context)]
class One2ManyChild1(orm.Model):
    _name = 'export.one2many.child.1'
    _module = 'base'
    _inherit = 'export.one2many.multiple.child'
class One2ManyChild2(orm.Model):
    _name = 'export.one2many.child.2'
    _module = 'base'
    _inherit = 'export.one2many.multiple.child'

class Many2ManyChild(orm.Model):
    _name = 'export.many2many.other'
    _module = 'base'
    # FIXME: orm.py:1161, fix to name_get on m2o field
    _rec_name = 'value'

    _columns = {
        'str': fields.char('unknown', size=None),
        'value': fields.integer()
    }
    def name_get(self, cr, uid, ids, context=None):
        return [(record.id, "%s:%s" % (self._name, record.value))
            for record in self.browse(cr, uid, ids, context=context)]
