
#BEACH BUGGY GAME CONTROLLER

#Import Libraries
import cv2
import mediapipe as mp
import pyautogui
import time


mp_hands=mp.solutions.hands
mp_drawing=mp.solutions.drawing_utils
mp_drawing_styles=mp.solutions.drawing_styles

hands=mp_hands.Hands(static_image_mode=False,model_complexity=0,min_detection_confidence=0.5,min_tracking_confidence=0.5,max_num_hands=2)

#Access the webcam
video=cv2.VideoCapture(0)

while True:
    success,image=video.read()

    #To get the height and width of the webcam
    height,width,channels=image.shape

    #Draw the horizontal line
    cv2.line(image,(0,height//2),(width,height//2),(0,255,0),2)

    #Draw the vertical line
    cv2.line(image,(width//2,0),(width//2,height),(0,255,0),2)
     
    #Flip the image horizontally for selfie view display
    #convert the image from BGR to RGB
    image=cv2.cvtColor(cv2.flip(image,1),cv2.COLOR_BGR2RGB)
    
    #To improve performance, optionally mark the image as not writeable to pass by reference
    image.flags.writeable=False
    
    #process the image and find the hands
    results=hands.process(image)
    
    image.flags.writeable=True
    
    #Convert the image from RGB to BGR
    image=cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
    
    #Draw the hand annotations on the image
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            mp_drawing.draw_landmarks(image,hand_landmarks,mp_hands.HAND_CONNECTIONS)
            
            #Accessing the landmarks for detecting palm of the hand and thumbsup action

            #index_finger_mcp,pinky_mcp and wrist are used for detecting the palm of the hand
            #thumb_tip,thumb_ip and index_finger_mcp are used for detecting thumbsup action
            index_finger_mcp=hand_landmarks.landmark[5]
            pinky_mcp=hand_landmarks.landmark[17]
            wrist=hand_landmarks.landmark[0]
            thumb_tip=hand_landmarks.landmark[4]
            thumb_ip=hand_landmarks.landmark[3]
            
            #Normalize the coordinates of landmarks
            thumb_tip_x=thumb_tip.x * width
            thumb_tip_y=thumb_tip.y * height

            thumb_ip_x=thumb_ip.x * width
            thumb_ip_y=thumb_ip.y * height

            index_finger_mcp_x=index_finger_mcp.x * width
            index_finger_mcp_y=index_finger_mcp.y * height

            pinky_mcp_x=pinky_mcp.x * width
            pinky_mcp_y=pinky_mcp.y * height

            wrist_x=wrist.x * width
            wrist_y=wrist.y * height
            
            #Condition for accessing break control
            if index_finger_mcp_x < width//2 and pinky_mcp_x < width//2 and wrist_x < width//2 and index_finger_mcp_y > height//2 and pinky_mcp_y > height//2 and wrist_y > height//2:
                
                cv2.putText(image,'Break',(80,350),cv2.FONT_HERSHEY_COMPLEX,1.5,(255,0,0),3)
                pyautogui.keyDown('down')
                pyautogui.keyUp('up')
                time.sleep(0.2)
                pyautogui.keyUp('down')

            #Condition for accessing accelerator control and using special ability
            elif index_finger_mcp_x > width//2 and pinky_mcp_x > width//2 and wrist_x > width//2 and index_finger_mcp_y > height//2 and pinky_mcp_y > height//2 and wrist_y > height//2:
                if thumb_tip_y < index_finger_mcp_y and thumb_ip_y < index_finger_mcp_y:
                    cv2.putText(image,'Ability',(330,350),cv2.FONT_HERSHEY_COMPLEX,1.5,(255,0,0),3)
                    pyautogui.keyDown('space')
                    time.sleep(0.2)
                    pyautogui.keyUp('space')
                else:
                
                    cv2.putText(image,'Accelerator',(330,350),cv2.FONT_HERSHEY_COMPLEX,1.5,(255,0,0),3)
                    pyautogui.keyDown('up')
                    pyautogui.keyUp('down')
                    time.sleep(0.2)
                    pyautogui.keyUp('up')
                
            #Condition for turning left
            elif index_finger_mcp_x < width//2 and pinky_mcp_x < width//2 and wrist_x < width//2 and index_finger_mcp_y < height//2 and pinky_mcp_y < height//2 and wrist_y < height//2:
                cv2.putText(image,'Left',(100,150),cv2.FONT_HERSHEY_COMPLEX,1.5,(255,0,0),3)
                pyautogui.keyDown('left')
                pyautogui.keyUp('right')
                time.sleep(.6)
                pyautogui.keyUp('left')

            
            #Condition for turning right
            elif index_finger_mcp_x > width//2 and pinky_mcp_x > width//2 and wrist_x > width//2 and index_finger_mcp_y < height//2 and pinky_mcp_y < height//2 and wrist_y < height//2:
                cv2.putText(image,'Right',(400,150),cv2.FONT_HERSHEY_COMPLEX,1.5,(255,0,0),3)
                pyautogui.keyDown('right')
                pyautogui.keyUp('left')
                time.sleep(.6)
                pyautogui.keyUp('right')
            

    cv2.imshow("Beach_buggy",image)

    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
video.release()
cv2.destroyAllWindows()