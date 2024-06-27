import cv2
import requests
from pyzbar.pyzbar import decode


# central method to read barcode image, query the detected ISBN through Google Books, and retrieve data from there
# the retrieved data is then formatted into a list that's then written to a csv spreadsheet
def BarcodeReader(image):
    ISBN = ""
    lookupURL = "https://www.googleapis.com/books/v1/volumes?q=isbn:"

    # placeholder list used for cases where a barcode is unreadable or not found in Google Books
    # the first value returns the path to the image file the barcode was supposed to be in
    UNKNOWN_BARCODE = [str(image), "--UNKNOWN--", "--UNKNOWN--", "--UNKNOWN--"]

    print("-" * len(lookupURL))

    # read the image in numpy array using cv2
    img = cv2.imread(image)

    # decode the barcode image, but only return the first barcode
    try:
        ISBNBarcode = decode(img)[0]
    except IndexError:
        print(f'CANNOT READ BARCODE @ {str(image)}')
        return UNKNOWN_BARCODE

    # if not detected then print an error message and return UNKNOWN_BARCODE data
    if not ISBNBarcode:
        print(f'CANNOT READ BARCODE @ {str(image)}')
        return UNKNOWN_BARCODE
    else:
        # return barcode's data as a string of numbers
        if ISBNBarcode.data != "":
            # set the ISBN
            ISBN = str(ISBNBarcode.data)[2:-1]
            print(f'Barcode: {ISBN}')
            print(f'Barcode Type: {ISBNBarcode.type}')


    # connect to Google Books API, query for detected ISBN, and begin to extract info:
    lookupURL += ISBN
    print(f'URL: {lookupURL}')

    r = requests.get(url=lookupURL)

    data = r.json()

    # in case where ISBN query fails, return unknown barcode list
    if not data:
        print("Could not fetch data. Try again!")
        return UNKNOWN_BARCODE

    # return unknown barcode placeholder in case where Google Books API *has* the ISBN, but no valid data on it
    elif data.get("items") is None:
        print("Barcode decoded, data unavailable. Make sure this is a valid ISBN!")
        return UNKNOWN_BARCODE

    # on successful query with valid data available, retrieve said data and format it for use in spreadsheet csv
    else:
        return retrieveandformat_GoogleBooks(ISBN, lookupURL, data)


def retrieveandformat_GoogleBooks(book_id, link, jsondata):
    # retrieve data from returned Google Books's JSON, format into list that can be used to make a csv row
    # uncomment below fields as needed, but beware not all are always used for every book, so you may need to create helper
    # methods that can format missing data into placeholder text
    title = jsondata["items"][0]["volumeInfo"]["title"]
    print(f'Title: {title}')
    authors = jsondata["items"][0]["volumeInfo"]["authors"]
    print(f'Author(s): {listAuthors(authors)}')
    # publisher = data["items"][0]["volumeInfo"]["publisher"]
    # publishedDate = data["items"][0]["volumeInfo"]["publishedDate"]
    # desc = data["items"][0]["volumeInfo"]["description"]
    # print(f'Description: {desc}')
    # pubDate = jsondata["items"][0]["volumeInfo"]["publishedDate"]
    # print(f'Published Date: {pubDate}')
    pageCount = jsondata["items"][0]["volumeInfo"]["pageCount"]
    print(f'Page Count: {pageCountCheck(pageCount)}')
    # avgRating = data["items"][0]["volumeInfo"]["averageRating"]
    # image = data["items"][0]["volumeInfo"]["imageLinks"]["thumbnail"]
    print("-" * len(link))
    return [book_id, title, listAuthors(authors), pageCountCheck(pageCount)]


def listAuthors(authors):
    # list authors' names so that they fit into one cell, with a newline after each name (except the last one)
    text = ""
    if len(authors) > 0:
        i = 0
        while i < len(authors)-1:
            text += authors[i] + "\n"
            i += 1
        text += authors[i]
        return text
    else:
        return "--CHECK MANUALLY--"


def pageCountCheck(count):
    # for cases where page count is 0 or unknown, tell user to check manually
    if (count <= 0) or (count is None):
        return "--CHECK MANUALLY--"
    else:
        return count

def showBarcodeOnImg(image, barcode, decoded_barcode):
    # optional code to display each detected barcode as an image
    (x, y, w, h) = barcode.rect

    # put a rectangle in the image to highlight the barcode
    cv2.rectangle(image, (x - 10, y - 10),
                  (x + w + 10, y + h + 10),
                  (255, 0, 0), 2)
    cv2.putText(image, decoded_barcode, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 0, 0), 20)

    # scale down the final image so it's not so ridiculously hueg
    imgSmol = cv2.resize(image, (0, 0), fx=0.15, fy=0.15)
    cv2.imshow("Scanned Barcode, press any key to close...", imgSmol)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


