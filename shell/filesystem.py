#coding=utf-8
import json
class FileSystemError(Exception): pass
class FileSystem(object):
    def __init__(self,filename):
        self.filename = filename
        #self.root = self.load(filename)
        #self.pwd  = self.root
    def makeroot(self):
        self.root = {"type":"dir",
                     "fullname":"/",
                     "name":"/",
                     "items":[ ]}
    def load ( self ):
        with open(f"{self.filename}.fs","r",encoding="utf-8") as f:
            self.root = json.load(f)
            self.pwd = self.root
    def create(self,filename):
        with open(f"{filename}.fs","w",encoding="utf-8") as f:
            json.dump(self.root,f)
    def mkdir(self,name):
        if name == "..":
            raise FileSystemError("directory name can't '..' ")
        directory = self.directory(name,self.pwd)
        fullname = self.pwd["fullname"] + name + "/"
        if fullname not in [i["fullname"] for i in self.pwd["items"] if i["type"] == "dir"]:
            self.pwd["items"] += [directory]
            self.create( self.filename )
            return fullname
        else:
            raise FileSystemError(f"{fullname} in {self.pwd['fullname']}")
    def rmdir(self,name):
        fullname = self.pwd["fullname"] + name + '/'
        if fullname in [i["fullname"] for i in self.pwd["items"] if i["type"] == "dir"]:
            for i in self.pwd["items"]:
                if i["fullname"] == fullname:
                    self.pwd["items"].remove(i)
            self.create( self.filename )
            return fullname
        else:
            raise FileSystemError(f"{fullname} not in {self.pwd['fullname']}")
    def remove(self,name):
        fullname = self.pwd["fullname"] + name
        if fullname in [i["fullname"] for i in self.pwd["items"] if i["type"] == "file"]:
            for i in self.pwd["items"]:
                if i["fullname"] == fullname:
                    self.pwd["items"].remove(i)
                    break
            self.create( self.filename )
            return fullname
        else:
            raise FileSystemError(f"{fullname} not in {self.pwd['fullname']}")
    def touch(self,name):
        if "/" in name:
            raise FileSystemError("filename can't have '/'")
        File = self.file(name,self.pwd)
        fullname = self.pwd["fullname"] + name
        if fullname not in [i["fullname"] for i in self.pwd["items"] if i["type"] == "file"]:
            self.pwd["items"] += [File]
            self.create( self.filename )
            return fullname
        else:
            raise FileSystemError(f"{fullname} in {self.pwd['fullname']}")

    def directory(self,name,parent):
        parentname = parent["fullname"]
        fullname = parentname + name + "/"
        return {"type":"dir",
                "fullname":fullname,
                "name":name,
                "items":[ ]}
    def file(self,name,parent):
        parentname = parent["fullname"]
        fullname = parentname + name
        return {"type":"file",
                "fullname":fullname,
                "name":name,
                "content":""}

    def dirs(self,node):
        return [i for i in node["items"] if i["type"] == "dir"]
    def find(self,name,node):
        if name in [i["name"] for i in node["items"] if i["type"] == "dir"]:
            for n in [i for i in node["items"] if i["type"] == "dir"]:
                if n["name"] == name:
                    return n
        raise FileSystemError(f"Not found {name} in {node['fullname']}")
    def ls(self):
        return [i for i in self.pwd["items"]]
    def getcwd(self):
        return self.pwd["fullname"]
    def change_dir(self,name):
        # split it then check length 
        # first is '' is '/'
        # last  is '' is '/' 
        # else check is '..' or just name
        if name.startswith("/"):
            if name == '/':
                rt = self.root
                self.pwd = rt
                return self.pwd["fullname"]
            if name.endswith("/"):
                name = name[:-1]
            target = name[1:].split("/")
            rt = self.root
            for n in target:
                rt = self.find(n,rt)
            self.pwd = rt
            return self.pwd["fullname"]
        elif name == "..":
            funame = self.pwd["fullname"]
            if funame == "/":
                raise FileSystemError("Can't change directory to pre for /")
            else:
                target = funame[1:-1].split("/")
                #print( "..",target)
                target.pop()
                #print( "..",target)
                rt = self.root
                for n in target:
                    rt = self.find(n,rt)
                self.pwd = rt
                return self.pwd["fullname"]
        else:
            target = [name]
            #print( "else:",target )
            rt = self.pwd
            for n in target:
                rt = self.find(n,rt)
            self.pwd = rt
            return self.pwd["fullname"]
    def __repr__(self):
        return f"pwd {self.pwd['fullname']} : {[i['fullname'] for i in self.pwd['items']]}"

"""
fs = FileSystem("test")
#fs.makeroot()
#fs.create("test")
fs.load()
#fs.mkdir("test")
#fs.touch("hello")
print( fs )
fs.change_dir("/test/")
print( fs )
fs.rmdir('b')
#fs.mkdir('a')
#fs.change_dir("..")
#fs.mkdir("b")
#fs.change_dir("b")
print( fs )
"""
