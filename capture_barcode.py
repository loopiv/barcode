import cv2
from pyzbar import pyzbar
import imutils

cam = cv2.VideoCapture(0)
cv2.namedWindow("Image")

def codetype(barcode):
    if barcode.startswith('WD'):
        return 'Model'
    elif barcode.startswith('ST'):
        return 'Model'
    else:
        return 'Other'

while True:
    ret, frame = cam.read()
    frame = imutils.resize(frame, width=1200)
    cv2.imshow("Image", frame)
    if not ret:
        break
    k = cv2.waitKey(1)

    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        barcodes = pyzbar.decode(frame)
        # loop over the detected barcodes
        for barcode in barcodes:
            # extract the bounding box location of the barcode and draw the
            # bounding box surrounding the barcode on the image
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            # the barcode data is a bytes object so if we want to draw it on
            # our output image we need to convert it to a string first
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type
            # draw the barcode data and barcode type on the image
            text = "{} ({})".format(barcodeData, barcodeType)
            cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 0, 255), 2)
            # print the barcode type and data to the terminal
            print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
            print(codetype(barcodeData), " = ", barcodeData)
        # show the output image
        cv2.imshow("Barcode", frame)

cam.release()
cv2.destroyAllWindows()

