ATTENTION! There is a quota for the number of uses per day for Google API and you can make a big money mistake if you use this code thoughtlessly

The file "textextractor.py" uses Google technology to convert an image into text and fill an Excel table with this text
To use the library, you need to have a personal Google API and give access to: tables, documents and disk.

How it works: specify the path to the image, it is sent to Google Drive, from Drive the image is read as a document, converting pixels into text (works VERY well for standard Windows fonts and combined languages ​​​​at the same time), then the document is read and returned back to the console, then optionally data processing / parsing is performed, sent to disk and entered into Google Sheets

As an example, a picture from the game Archeage was used to determine the number of people and their nicknames in order to collect attendance statistics
