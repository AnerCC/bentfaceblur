from retinaface import RetinaFace
import cv2 
import numpy as np
import base64
import json
from datetime import datetime

#V3 use resizingfor pixelation.
# https://sefiks.com/2021/04/27/deep-face-detection-with-retinaface-in-python/
#Recives a base64 string to "imgData" and a string to "imgName"
RESIZE_FACTOR=4
TIME=lambda:datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
COMPRESSION_LEVEL=9
QUALITY=99
def blureFace(images,vin):
      
         # Decode base64 picture to jpg file
      blurred_images=[]
      
      for index,image in enumerate(images):
         print(f"{TIME()} proccess started for image {index+1}")
         # with open('decImage.jpg', 'wb') as dec_img:
         #    dec_img.write(base64.b64decode((image)))
         try:
            # Decode the base64 string into bytes
            image_bytes = base64.b64decode(image)
            # Convert bytes to a numpy array
            image_array = np.frombuffer(image_bytes, dtype=np.uint8)
            # Decode the image
            img = cv2.imdecode(image_array, flags=cv2.IMREAD_COLOR)
         
            print(f"{TIME()} image {index+1} decoding proccess ended successfully")
         
         except:

            print(f"{TIME()}image {index+1} decoding faild")
            #returns unsupported media type error
            return 415


         # read the decoded img
         # img=cv2.imread('decImage.jpg')
         h,w=img.shape[:2]
         res_image=cv2.resize(img,(w//RESIZE_FACTOR,h//RESIZE_FACTOR))
         # img2blur=cv2.imread(img)
         
         print(f"{TIME()}sending image {index+1} for face detection")
         resp = RetinaFace.detect_faces(res_image,threshold=0.6)
         print(f"{TIME()} retinaface returnd {resp}")
         for identity in resp:
           
            try:
               facial_area = resp[identity]['facial_area']   
               print(f"{TIME()} {identity}")
               print(f"{TIME()} image {index+1} sent for full blurring")
               blurred=cv2.GaussianBlur(img,(71,71),500)

               
            except:
               print(f"{TIME()} no face detected in image {index+1}")
               break
         
            #Get detected face area from retinaFace response and assign face region to face veriable
            x1, y1, x2, y2 = facial_area
            sx1=x1*RESIZE_FACTOR
            sx2=x2*RESIZE_FACTOR 
            sy1=y1*RESIZE_FACTOR
            sy2=y2*RESIZE_FACTOR
         
            face = img[sy1:sy2, sx1:sx2]

            #blur the face region
            
            # Create circular mask of the same size as the blurred image
            mask = np.zeros_like(blurred)
            h, w = face.shape[:2]
            center = ((sx1+w//2), (sy1+h//2))
            
            cv2.ellipse(mask,center,(w//2,h//2),0,0,360, (255, 255, 255), -1)
            # cv2.circle(mask, center, radius, (255, 255, 255), -1)
            # cv2.imwrite("mask.jpg",mask)
            #create a circular blurred section
            blurred_circular = cv2.bitwise_and(blurred, mask)
            # cv2.imwrite("blurred.jpg",blurred_circular)
            
            #apply the blurred circular section into the detected face area
            blurredFace=np.where(mask!=0,blurred_circular,img)

            #apply the blured face into the sorce image
            img[sy1:sy2, sx1:sx2]=blurredFace[sy1:sy2, sx1:sx2]
            # if imgName !=None:
         _, buffer = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, QUALITY])
         # _, buffer = cv2.imencode('.png', img ,[cv2.IMWRITE_PNG_COMPRESSION, COMPRESSION_LEVEL])
         img_bytes=buffer.tobytes()
         img_base64 = base64.b64encode(img_bytes).decode('utf-8')
         blurred_images.append(img_base64)
         print(f"{TIME()} face bluring proccess ended for vehicle {vin}")
      return blurred_images

# if __name__=='__main__':
#    f=open("01VIN42342888253456989.json")
#    data=json.load(f)
#    img_name=data["Vin"]
#    img_data=data["Images"][0]

#    blureFace(img_data,img_name)
   