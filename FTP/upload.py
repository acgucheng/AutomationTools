#coding=utf-8
#import ftplib
from ftplib import FTP
import logging
import os
import json
import ftplib

class Server:
    username = "";
    password = "";
    host = "";
    directory = "";
    ftp = FTP();

    def __init__(self,serverinfo):
        self.host = serverinfo["host"];
        self.username = serverinfo["username"];
        self.password = serverinfo["password"];
        self.directory = serverinfo["directory"];
    
    def connect_server(self):
        self.ftp.connect(self.host,21,10);
        self.ftp.login(self.username,self.password);
        return self.ftp.getwelcome();

    def upload_file(self,local_path,remote_path):
        if(not self.check_dir(remote_path)):
            if(remote_path == self.directory):
                logging.error("The directory %s on %s not exists!" % (remote_path,self.host));
                return;
            else:
                try:
                    self.ftp.mkd(remote_path);
                except ftplib.error_perm:
                    logging.error("Can not create directory %s on %s!" % (remote_path,self.host));
                    logging.error(ftplib.error_perm);
                    return;
        files = os.listdir(local_path);
        self.ftp.cwd(remote_path);
        print self.ftp.pwd();
        for file in files:
            src = os.path.join(local_path, file);
            dest = os.path.join(remote_path,file);
            if(os.path.isdir(src)):
                self.upload_file(src,dest);
            else:
                src = os.path.join(local_path,file);
                with open(src,"rb") as upload_file:
                   logging.info("Uploading file : " + upload_file.name);
                   self.ftp.storbinary("STOR " + file,upload_file); 
        self.ftp.cwd("../");

    def check_dir(self,remote_dir):
        try:
            self.ftp.cwd(remote_dir);
        except ftplib.error_perm:
            return False;
        return True;


logging.basicConfig(level = logging.DEBUG);
logging.info("Reading the configuration...");
with open('servers.json','r') as cnfFile:
    servers = json.load(cnfFile);
ftp = FTP();
for serverinfo in servers:
    server = Server(serverinfo);
    logging.info("Connecting to " + server.host + "...");
    logging.info(server.connect_server());
    logging.info(server.host + " connected");    
    server.upload_file("./patch",server.directory);
