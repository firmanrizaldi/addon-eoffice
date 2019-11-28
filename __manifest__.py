{
    'version': '0.3',
    'name': 'eoffice',
    'depends': ['base','mail'],
    'author'  :'vitraining.com',
    'category': 'Other',
    'data': [
        'views/eo_menu.xml',
        'views/doc.xml',
        'views/doc_template.xml',
        'data/ir_sequence.xml',
        'data/doc_type.xml',
    	'data/doc_template.xml',
        'security/ir.model.access.csv',
        'security/record_rules.xml',
        'reports/doc.xml',
    ],    
    'description': """
Description
==================
aplikasi e-office

""",
    'installable':True,

}
