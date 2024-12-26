import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot


cap = cv2.VideoCapture(0)  
detector = FaceMeshDetector(maxFaces=1)
plotY = LivePlot(640, 360, [20, 50], invert=True)

LEFT_EYE = [159, 145, 33, 133]  
RIGHT_EYE = [386, 374, 362, 263]  

ratioList = []
blinkCounter = 0
counter = 0
eye_shut = False  


EAR_THRESHOLD = 28  # Adjust based on testing (lower for larger eyes)
SHUT_FRAMES_THRESHOLD = 10
color = (255, 0, 255)  # Default color initialization


def calculate_eye_ratio(face, eye_indices):
    """Calculate the Eye Aspect Ratio (EAR) for a single eye."""
    top = face[eye_indices[0]]  # Top landmark
    bottom = face[eye_indices[1]]  # Bottom landmark
    left = face[eye_indices[2]]  # Left corner
    right = face[eye_indices[3]]  # Right corner

  
    length_ver, _ = detector.findDistance(top, bottom)
    length_hor, _ = detector.findDistance(left, right)

  
    return (length_ver / length_hor) * 100


while True:
    success, img = cap.read()
    if not success:
        print("Failed to capture video frame. Exiting.")
        break

    # Detect face mesh
    img, faces = detector.findFaceMesh(img, draw=False)

    if faces:
        face = faces[0]

       
        left_ratio = calculate_eye_ratio(face, LEFT_EYE)
        right_ratio = calculate_eye_ratio(face, RIGHT_EYE)
        avg_ratio = (left_ratio + right_ratio) / 2

        ratioList.append(avg_ratio)
        if len(ratioList) > 3:
            ratioList.pop(0)
        ratioAvg = sum(ratioList) / len(ratioList)

       
        if ratioAvg < EAR_THRESHOLD:  
            if not eye_shut:  
                eye_shut = True
                counter = 0
            counter += 1

            if counter > SHUT_FRAMES_THRESHOLD:
                color = (0, 0, 255)  
        else:  
            if eye_shut:  
                if counter > 0 and counter <= SHUT_FRAMES_THRESHOLD:
                    blinkCounter += 1  
                eye_shut = False
                color = (0, 255, 0)  

       
        for eye in [LEFT_EYE, RIGHT_EYE]:
            cv2.line(img, face[eye[0]], face[eye[1]], (0, 200, 0), 2) 
            cv2.line(img, face[eye[2]], face[eye[3]], (0, 200, 0), 2)  

        cvzone.putTextRect(img, f'Blink Count: {blinkCounter}', (50, 100), colorR=color)

       
        imgPlot = plotY.update(ratioAvg, color)
        img = cv2.resize(img, (640, 360))
        imgStack = cvzone.stackImages([img, imgPlot], 2, 1)
    else:
       
        color = (255, 0, 255)  
        img = cv2.resize(img, (640, 360))
        imgStack = cvzone.stackImages([img, img], 2, 1)

    cv2.imshow("Image", imgStack)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
        break

cap.release()
cv2.destroyAllWindows()
