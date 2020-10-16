import cv2
import pytesseract

import re


def getDictionary(imageFile):

    # Mention the installed location of Tesseract-OCR in your system
    pytesseract.pytesseract.tesseract_cmd = 'C:\\msys64\\mingw64\\bin\\tesseract.exe'

    # Read image from which text needs to be extracted
    img = cv2.imread("C:\\Users\\LENOVO\\PycharmProjects\\OCRTask3\\task3\\"+imageFile)

    # Preprocessing the image starts

    # Convert the image to gray scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Performing OTSU threshold
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    # Specify structure shape and kernel size.
    # Kernel size increases or decreases the area
    # of the rectangle to be detected.
    # A smaller value like (10, 10) will detect
    # each word instead of a sentence.
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

    # Appplying dilation on the threshold image
    dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)

    # Finding contours
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_NONE)

    # Creating a copy of image
    im2 = img.copy()


    # Looping through the identified contours
    # Then rectangular part is cropped and passed on
    # to pytesseract for extracting text from it
    # Extracted text is then written into the text file
    count = 0

    text = ""

    name = ""
    date = ""
    totalAmount = ""
    email = ""

    for cnt in contours[::-1]:

        x, y, w, h = cv2.boundingRect(cnt)

        # Drawing a rectangle on copied image
        rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Cropping the text block for giving input to OCR
        cropped = im2[y:y + h, x:x + w]

        # Open the file in append mode
        #file = open("recognized.txt", "a")

        # Apply OCR on the cropped image
        text = pytesseract.image_to_string(cropped)

        if count == 0:
            #print("Name:",text.strip())
            count+=1
            name = text.strip()


        pattern = "([\d{1}\d{2}][/-]\d{2}[/-]\d{4})"

        #date = "date is 5-01-2019 on this bonda proposed a boy and married on 31-12-2030"

        #print(date)

        x = re.search(pattern, text.strip())
        if x:
            date = x.group()
            #print("Date:",x.group())

        if text.__contains__('Total') or text.__contains__('total'):
            #print("###################")

            total = []

            pattern = "(\d+.\d{2})"
            for words in text.split('\n'):
                x = re.findall(pattern, words)

                #print("TOTAL", )
                if x:
                    #print(x[-1])
                    try:
                        float(x[-1])
                        total.append(x[-1])
                    except Exception as e:
                        #print(e)
                        pass

            if total:
                #print("Total:",total[-1])
                totalAmount = total[-1]
            else:
                totalAmount = ""
                #print("Total:","NULL")

        if text.__contains__('email') or text.__contains__('Email'):
            # print("###################")

            total = []

            pattern = "\S+@\S+"
            for words in text.split('\n'):

                x = re.findall(pattern, words)

                if x:
                    #print(x)
                    email = x[0]

            #print("###################")




        #print(text)

        # Appending the text into file
        #file.write(text)
        #file.write("\n")

        # Close the file
        #file.close

    #print("NAME:",name)
    #print("DATE:",date)
    #print("TOTAL:",totalAmount)

    return dict(
        {"name":name,
         "date":date,
         "email":email,
         "total":totalAmount}
    )


#d = getDictionary("X00016469670.jpg")
#print(d)

