
import markdown
import os

from beep import Beep

class MemPadModel:
    
  def __init__(self):
    self.__pages = []
    self.__num_pages = 0
    self.__current_page = 0
    self.__filename = ''
   
  def open(self, filename):
    "read lst mempad file"   
    self.__dir = os.path.dirname(os.path.realpath(__file__))
    str = MemPadModel.__readFile(filename)
  
    if not str.startswith('MeMpAd.'):
      import sys
      sys.exit(filename + ' is NOT a Mempad file.')
  
    index = str.index('\1')
    str = str[index:].rstrip('\0')
    arr = str.split('\0')

    pages = []
    
     
    for i, item in enumerate(arr):
      if i & 1 == 0 : # titles
        level = ord(item[0])
        title = item[1:]
      else:
        #pages.append([ len(pages), level, title, item])
        pages.append({
           "id": len(pages), 
           "level": level, 
           "title": title, 
           "content": item})
      
      
    self.__pages = pages
    self.__num_pages = len(pages)
    self.__filename = filename
     
    Beep.dispatch('new_file', self, self.__filename)

  @property
  def pages(self):
      return self.__pages
  
  def set_pages(self, pages, selected_item = None):
      self.__pages = pages
      
  
  def get_page_by_id(self, id):
      id = int(id)
      return self.__pages[id]
  
  def set_page_by_id(self, id, level, title, content):
      
      self.__pages[id] = {
           "id": id, 
           "level": level, 
           "title": title, 
           "content": content}

  def set_content_by_id(self, id, content):
      p = self.__pages[id] 
      p["content"] = content     

  def get_content_by_id(self, id):
      p = self.__pages[id] 
      return p["content"]
  
  def get_page_title(self, id):
      p = self.__pages[id] 
      return p["title"]
     
  def set_page_title(self, id, title):
      p = self.__pages[id] 
      p["title"] = title   

  def export_to_html(self,filename = None):
    "write to html"  
    
    links = ''
    pages = ''

    if not filename :
      filename = f'{self.__filename[0:-4]}.html'

    for page in self.__pages :
      id, level, title, content = page.id, page.level, page.title, page.content 
      dots = ' ' * (level - 1)
      links += f'<a href="javascript:show({id})">{dots}{title}</a>\n'
     
      if title[:-4] != '.ini' :
        content = markdown.markdown(content)
      pages += f'<div id="id{id}">{content}</div>\n'

    html = MemPadModel.__readFile(self.__dir + '/assets/template.html')
    css = MemPadModel.__readFile(self.__dir + '/assets/mempad.css')
    js = MemPadModel.__readFile(self.__dir + '/assets/mempad.js')
    html = html.format(links=links, pages = pages, css = css, js = js)

    
    f = open(filename, 'w', encoding='utf-8')
    f.write(html)
    f.close()
    
  def get_data(self):
      return str(self.__num_pages) + ' pages'
  @property
  def num_pages(self):
      return self.__num_pages

  @property
  def current_page(self):
      return self.__current_page
  
  @staticmethod
  def __readFile(filename) :
    "read file"  
    f = open(filename, 'r', encoding='utf-8')
    str = f.read()
    f.close()  
    return str

 

  def add_page_child(self, parent_id, title):
      found = False
      new_pages = []

      for page in self.pages:
        new_pages.append({
          "id": len(new_pages), 
          "level": page['level'], 
          "title": page['title'], 
          "content": page['content']})
        
        if page['id'] == parent_id:
          found = True
          self.__current_page = len(new_pages)
          new_pages.append({
          "id": len(new_pages), 
          "level": page['level'] + 1, 
          "title": title, 
          "content": ''})
               
      if found:
        self.__pages = new_pages

      return found
  
  def _______add_page_after(self, page_id, title):
    found = False
    page_level = 0
    added = False
    new_pages = []

    for page in self.pages:
      new_pages.append({
        "id": len(new_pages), 
        "level": page['level'], 
        "title": page['title'], 
        "content": page['content']})
      
      if page['id'] == id:
        found = True
        page_level = page['level']

        new_pages.append({
        "id": len(new_pages), 
        "level": page['level'] + 1, 
        "title": title, 
        "content": ''})
              
    if found:
      self.__pages = new_pages

    return found
  
  def delete_page(self, page_id):
      self.__pages = [page for page in self.__pages if page["id"] != page_id]

 