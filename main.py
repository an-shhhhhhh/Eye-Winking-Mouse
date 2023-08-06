import cv2
import mediapipe as mp
import pyautogui

cam = cv2.VideoCapture(0)#this function captures our video until the function is running
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True) #it detects the face and then the eye , so that we could make things work with just a wink
screen_w, screen_h = pyautogui.size()

while True:
    _, frame = cam.read()
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #converts the frame that is being i.e. our video to rgb colour so that it becomes easy for detection
    output = face_mesh.process(rgb_frame) #it processes the frame
    landmark_points = output.multi_face_landmarks  # our face has several landmark points, so after detecting and processing, the landmark points are marked
    # print(landmark_points)
    frame_h, frame_w, _ = frame.shape
    if landmark_points:
        landmarks = landmark_points[0].landmark  # till now we had the feature of detecting multi faces seen on the screen, but now we will detect the 1st face which is seen, hence we have put an index of 0
        for id, landmark in enumerate(landmarks[474:478]): #the range is specified to select one of the eyes,and the enumerate function will further select only one of the landmarks among the four landmarks of the eye
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            if id == 1:
                screen_x = screen_w / frame_w * x #it chnages the frame size
                screen_y = screen_h / frame_h * y
                pyautogui.moveTo(screen_x, screen_y)

            left = [landmarks[145], landmarks[159]]
            for landmark in left:
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame, (x,y), 3, (0, 255, 255)) # draws a circle on the frame with center x,y and radius 3, and colour rgb with red =0, green = 255, b = 0
            # print(left[0].y - left[1].y)
            if(left[0].y - left[1].y)<0.004:#difference between two landmarks, i.e, the upper lid and lowerlid landmrk, if the difference between both the landmarks reaches a certain range, then then it is to be considered as clicked
                # print('click')
                pyautogui.click()
                pyautogui.sleep(1)
            # print(x, y)


    cv2.imshow('Eye Controlled Mouse', frame)  # imshow is image show
    cv2.waitKey(1)
