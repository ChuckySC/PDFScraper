from datetime import datetime
import hashlib

from functions.universal import remove_superscripts

class Abstract():
    id = None
    title = None
    content = None
    author = None
    page = None
    abstraction_datetime = None

    def __init__(self, **kwargs):
        default_attr = dict(title=None, content=None, author=None, page=None)
        allowed_attr = list(default_attr.keys())
        default_attr.update(kwargs)
        self.__dict__.update((k,v) for k,v in default_attr.items() if k in allowed_attr)

    def get(self):
        abstract = {}

        abstract['id'] = self.get_id()
        abstract['title'] = self.get_title()
        abstract['author'] = self.get_author()
        abstract['content'] = self.get_content()
        abstract['page'] = self.get_page()
        abstract['abstraction_datetime'] = self.get_abstraction_datetime()

        return abstract
    
    def get_id(self):
        '''Return ID'''
        text = f'{self.get_abstraction_datetime()} - {self.get_title()}'
        self.id = hashlib.md5(text.encode('utf-8')).hexdigest().upper()
        return self.id

    def get_title(self):
        '''Return title'''
        return self.title
    
    def get_author(self):
        '''Return clean author(s)'''
        return remove_superscripts(str(self.author))
    
    def get_content(self):
        '''Return content'''
        return self.content
    
    def get_page(self):
        '''Return page'''
        return self.page
    
    def get_abstraction_datetime(self):
        '''Return abstraction datetime stamp'''
        return datetime.strftime(datetime.today(), '%a %d %b %Y, %I:%M%p')