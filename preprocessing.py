import cv2


#image 1 -> the image of the dustbin before throwing in the new garbage(object of interest)
#image2 -> the image of the dustbin after throwing in the new garbage(object of interest)
#plz click images from a steady camera, else the algo wont work

image1 = cv2.imread("/Users/piyush.ku/Desktop/im1.png")
#image1 = cv2.resize(image1,None,fx=0.1, fy=0.1, interpolation = cv2.INTER_CUBIC)
image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
cv2.imshow('Draw01',image1)

image2 = cv2.imread("/Users/piyush.ku/Desktop/im2.png")
#image2 = cv2.resize(image2,None,fx=0.1, fy=0.1, interpolation = cv2.INTER_CUBIC)
image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
cv2.imshow('Draw02',image2)


image3 = cv2.subtract(image1, image2)
cv2.imshow('Draw03',image3)

(T, threshImage) = cv2.threshold(image3, 1, 255, cv2.THRESH_BINARY)
cv2.imshow('Draw04',threshImage)
cv2.imwrite('/Users/piyush.ku/Desktop/threshImage.png',threshImage)

clrimg = cv2.imread("/Users/piyush.ku/Desktop/im1.png")
abc = cv2.bitwise_and(clrimg, clrimg, mask = cv2.imread('/Users/piyush.ku/Desktop/threshImage.png', 0))
#cv2.Copy(clrimg, clrimg, threshImage)

cv2.imshow('Draw05',abc)

cv2.waitKey(0)