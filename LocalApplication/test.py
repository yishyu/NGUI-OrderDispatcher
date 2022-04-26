import cv2
import imutils
import pytesseract as tess
from PIL import Image
import string

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while(1):
    # Capture frame-by-frame
    ret, image = cap.read()
    # image = cv2.imread('memory/images/caz.png')
    # image = imutils.resize(image, width=300 )
    #cv2.imshow("original image", image)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("greyed image", gray_image)
    gray_image = cv2.bilateralFilter(gray_image, 11, 17, 17)
    #cv2.imshow("smoothened image", gray_image)
    edged = cv2.Canny(gray_image, 30, 200)
    #cv2.imshow("edged image", edged)
    cnts,new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    image1=image.copy()
    cv2.drawContours(image1,cnts,-1,(0,255,0),3)
    #cv2.imshow("contours",image1)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True) [:30]
    screenCnt = None
    image2 = image.copy()
    cv2.drawContours(image2,cnts,-1,(0,255,0),3)
    #cv2.imshow("Top 30 contours",image2)
    i=7
    cv2.rectangle(image, (300, 150), (900, 450), (0, 255, 0), 5)
    cv2.imshow("original image", image)
    for c in cnts:
        image2 = image.copy()
        perimeter = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * perimeter, True)
        # if len(approx) == 4:
        screenCnt = approx
        x,y,w,h = cv2.boundingRect(c)
        new_img=image[y:y+h,x:x+w]
        cv2.imshow("cropped", new_img)
        plate_im = Image.fromarray(new_img)
        text = tess.image_to_string(plate_im, config=f'--psm 11 --oem 3 -c tessedit_char_whitelist={string.digits}')

        path = './'+str(i)+'.png'
        print(f"imageid : {path} - text : {text}")
        cv2.imwrite(path, new_img)
        i+=1
        # break

    cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 3)
    cv2.waitKey(0)
cv2.destroyAllWindows()