import urllib2
from HTMLParser import HTMLParser
import os.path

class LinkParser(HTMLParser):
      def __init__(self):
          self.data = []
          self.href = 0
          self.linkname = ''
          HTMLParser.__init__(self)
      def handle_starttag(self, tag, attrs):
          if tag == 'a':
              for name, value in attrs:
                  if name == 'href':
                      self.href = 1
      def handle_data(self, data):
          if self.href:
              self.linkname += data
      def handle_endtag(self,tag):
          if tag == 'a':
              self.linkname = ''.join(self.linkname.split())
              self.linkname = self.linkname.strip()
              if  self.linkname:
                  self.data.append(self.linkname)
              self.linkname = ''
              self.href = 0
      def get_result(self):
        return self.data

def downloadAndSave(url, fp):
  f = urllib2.urlopen(url)
  with open(fp, "wb") as code:
    code.write(f.read())

def download():
  cran = 'http://mirrors.ustc.edu.cn/CRAN/src/contrib/'
  linkParser = LinkParser()
  linkParser.feed(urllib2.urlopen(cran).read())
  linkParser.close()
  data = linkParser.get_result()
  packages = open('packages2.txt', 'r')
  download = 0
  for line in packages:
    pack = line.strip()
    if pack == '':
      continue
    for p in data:
      if p.split('_')[0] == pack:
        url = cran + p
        fp = 'E:/RPackages/' + p
        download = download + 1
        if not os.path.exists(fp):
          print ' '.join([p,str(download)])
          downloadAndSave(url, fp)

def files():
  packages = open('packages.txt', 'r')
  fs = []
  f_valid = set()
  f_novalid = set()
  for f in os.listdir('E:/RPackages/'):
    if f.endswith(".tar.gz"):
      fs.append(f)
  for pack in packages:
    for f in fs:
      if not cmp(f.split('_')[0].lower(), pack.strip().lower()):
        f_valid.add(f)
  for f in fs:
    if f not in f_valid:
      f_novalid.add(f)
      print f
  print str(len(f_novalid))

def main():
  download()

if __name__ == '__main__':
  main()