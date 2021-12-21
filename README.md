# General information

This applcation is a part of [panelstudenta][pan] project. It is used to extract text from images and pdf files. Main app (panelstudenta) makes api call to this app,
then request is processed on another thread and result is returned via api call to main app. Therefore user must provide environment variable with appropriate 
endpoint in panelstudenta app:

```URL_PANEL=http://host:port/imgtxt/files/img_receive```

[pan]:<https://github.com/wojciechzyla/panelstudenta>
