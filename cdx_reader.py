from abc import ABC, abstractmethod
import os
import urllib3

class CDXReader(ABC):

    @abstractmethod
    def getFileSize(self):
        pass

    @abstractmethod
    def getNextStartOfLineCursor(self):
        pass
    
    @abstractmethod
    def readLine(self):
        pass
    
    @abstractmethod
    def seek(self,cursor):
        pass

    @abstractmethod
    def tell(self):
        pass

    @abstractmethod
    def close(self):
        pass

class CDXFileReader(CDXReader):
    def __init__(self, path_to_cdx_file):
        self.f = open(path_to_cdx_file,"r")

    def getFileSize(self):
        self.f.seek(0, os.SEEK_END)
        return self.f.tell()

    def seek(self,cursor):
        self.f.seek(cursor)

    def tell(self):
        return self.f.tell()

    def getNextStartOfLineCursor(self):
        self.f.readline()
        return self.f.tell()
    
    def readLine(self):
        return self.f.readline()
    
    def close(self):
        self.f.close()

class CDXURLReader(CDXReader):
    def __init__(self, url_to_cdx_file):
        self.url = url_to_cdx_file
        self.http = urllib3.PoolManager()
        self.cursor = 0
        self.chunkSize=1000
        self.fileSize = int(self.http.request('HEAD', self.url).headers.get("Content-length"))

    def getFileSize(self):
        return self.fileSize

    def seek(self,cursor):
        self.cursor = cursor

    def tell(self):
        return self.cursor

    def getNextStartOfLineCursor(self):
        reply = self.http.request('GET', self.url, headers={'Range':'bytes={0}-{1}'.format(self.cursor,(self.cursor+self.chunkSize))}).data.decode('utf-8')
        while len(reply.split('\n')) < 2:
            if(self.cursor + self.chunkSize >= self.fileSize):
                self.cursor = self.fileSize
                return self.cursor
            self.chunkSize += self.chunkSize
            reply = self.http.request('GET', self.url, headers={'Range':'bytes={0}-{1}'.format(self.cursor,(self.cursor+self.chunkSize))}).data.decode('utf-8')
        self.cursor += len(reply.split('\n')[0])+1
        return self.cursor
    
    def readLine(self):
        reply = self.http.request('GET', self.url, headers={'Range':'bytes={0}-{1}'.format(self.cursor,(self.cursor+self.chunkSize))}).data.decode('utf-8')
        while len(reply.split('\n')) < 2:
            if(self.cursor + self.chunkSize >= self.fileSize):
                self.cursor = self.fileSize
                return reply
            self.chunkSize += self.chunkSize
            reply = self.http.request('GET', self.url, headers={'Range':'bytes={0}-{1}'.format(self.cursor,(self.cursor+self.chunkSize))}).data.decode('utf-8')
        self.cursor += len(reply.split('\n')[0])+1
        return reply.split('\n')[0] + '\n'
    
    def close(self):
        pass
