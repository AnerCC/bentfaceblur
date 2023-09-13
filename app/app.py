
from flask import Flask, request,jsonify, abort, make_response
from app.blur import blureFace
import json
import cv2 as cv
# from app.logger import create_logger
from datetime import datetime
app = Flask(__name__)
TIME=lambda:datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/blur', methods=['POST'])
# ‘/’ URL is bound with hello_world() function.

def faceBlure():
    if request.method=='POST':
    
            print(f"{TIME()} request recived")
            try:
                data=json.loads(request.data)
                
                print(f"{TIME()} data loaded from JSON")
            
            except:
                
                print(f"{TIME()} couldnt load data from JSON")
                return  make_response(jsonify(error="Couldnt load json file"), 415)
            
            images=data["images"]
            vin=data["vin"]
            
            
            print(f"{TIME()} Recived {len(images)} images of car {vin}")
            
            #send images to blur service
            res=blureFace(images,vin)
            
            print(f"{TIME()} blurFace returned {len(images)} blurred images from car {vin}")

            if res==415:
                 print(f"Couldnt decode {vin} images from JSON")
                 return make_response(jsonify(error="Couldnt decode image"), 415)

    return res

#Test url 
@app.route('/brew', methods=['GET'])
def teapot():
     
     abort(418)


    

# main driver function
# if __name__ == '__main__':
	
# 	app.run(host="0.0.0.0",port=5000, debug=True)
