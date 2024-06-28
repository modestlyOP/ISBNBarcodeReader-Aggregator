# ISBNBarcodeReader-Writer

You don't want to use an app or website on your phone to look up ISBNs... and you've taken a bunch of photos of the barcodes on all your unneeded books? Great, you'll need them for this!

This tool will use computer vision to read all those barcodes, decode them to ISBNs, and fetch information (via Google Books) about each ISBN's corresponding book. This information is then written to a convenient csv spreadsheet, which you can hand out to wherever you plan to send your books!


## Dependencies
Recommended Python 3.11+, as well as opencv and pyzbar.


## Running
Simply put all your barcode photos into the ``barcodes`` folder, and then run the ``iterateImages.py`` file in a terminal.
After a completed run, you will find a newly-written csv file in the same folder the script was run in. 

