# ISBNBarcodeReader-Writer

For whatever reason, you've taken a bunch of photos of the barcodes on all your unneeded books? Great, you'll need them for this!
This tool will use computer vision to read all those barcodes, decode them to ISBNs, and fetch information about each ISBN's corresponding book. This information is then written to a convenient csv spreadsheet file, which you can hand out to wherever you plan to send your books!

Dependencies
Recommended Python 3.11+, as well as opencv and pyzbar.

Running
Simply put all your barcode photos into the ``barcodes`` folder, and then run the ``iterateImages.py`` file in a terminal.

