# cdxj-explorer
A python based application to explore CDXJ files. Meant to be used with Arquivo.pt's CDXJ files, but probably works with any CDXJ files. Though it hasn't been tested with other CDX files.

## Installation

`pip install PyQt5`

## Running 

`python main.py`

## Usage

1 - Click the "Open CDX" button and browse to a local CDXJ file. You can download CDXJ files from https://arquivo.pt/cdxj

<img width="852" height="302" alt="image" src="https://github.com/user-attachments/assets/2f763819-9871-4fbe-a210-dbfa83d9aeb6" />

1.1 - Alternatively, change the "Get file from:" dropdown to "Internet" and copy a link to a CDXJ file, which you can find at https://arquivo.pt/cdxj

<img width="862" height="171" alt="image" src="https://github.com/user-attachments/assets/f401072b-0a83-4e33-b758-4a6c303ca157" />

2 - After Selecting a CDXJ file, type a URL you want to search, for example sapo.pt

<img width="460" height="181" alt="image" src="https://github.com/user-attachments/assets/c50fda91-eeb0-4b10-bb5f-7cd4cd490191" />

3 - Click the "Search" button to display the first 100 entries that match your search.

<img width="940" height="307" alt="image" src="https://github.com/user-attachments/assets/50a4692f-4e7a-498a-9b66-85ca7fc9b4f8" />

That's it.

## Notes

This isn't a well optimized project, it was just something I made for fun and it turned out to be somewhat useful. As such it may consume way too many resources, to make sure that doesn't happen avoid searching "All results" unless you're sure that the number of results is a manageable number. From my experience less than 10,000 is fine, above 10,000 it starts struggling.
It'd be also wise to avoid "All results" searches altogether if you're getting the file from the internet rather than a local file. The program makes one HTTP request per line read, so you might get blocked or accidentally cause a DoS if the number of lines is too big. It will also be horribly slow.
