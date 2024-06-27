import csv
import os
import reader

imageFolder = "barcodes"
#print(os.listdir(imageFolder))
fields = ["ISBN", "Title", "Author(s)", "Page Count", "Notes"]

with open('books.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=",", quoting=csv.QUOTE_NONNUMERIC)
    csvwriter.writerow(fields)
    for filename in os.listdir(imageFolder):
        f = os.path.join(imageFolder, filename)
        if os.path.isfile(f):
            #print(f)
            book = reader.BarcodeReader(f)
            #print(book)
            csvwriter.writerow(book)

    csvfile.close()
