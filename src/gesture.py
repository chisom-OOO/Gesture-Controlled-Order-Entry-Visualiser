import cv2
import mediapipe as mp
import math

mp_hands = mp.solutions.hands #uses hand module
mp_draw = mp.solutions.drawing_utils #drawing utility to draw the skeleton

def get_distance(p1, p2):
    return math.sqrt((p1.x-p2.x)**2 + (p1.y-p2.y)**2)
#calculate distance between two hand landmarks

def detect_gesture(hand_landmarks):
    landmarks = hand_landmarks.landmark
    # storing the landmarks as the hand landmarks (21 points found my mediapipe) so you can refer to each point by index

    thumb_tip= landmarks[4]
    index_tip= landmarks[8]
    middle_tip= landmarks[12]
    ring_tip= landmarks[16]
    pinky_tip= landmarks[20]

    wrist = landmarks[0]

    pinch_distance = get_distance(thumb_tip, index_tip)
    if pinch_distance < 0.05:
        return 'pinch' #pinch detection
    #calculates if distance is less that 5% of screen width
    
    tips = [thumb_tip, index_tip, middle_tip, ring_tip, pinky_tip]
    distances = [get_distance(tip,wrist) for tip in tips]
    if all(d>0.27 for d in distances):
        return 'spread' #spread detection
    
    return 'none'
    # calculate each of the fingertips distance from the central point of the wrist
    # more than 28% of screen width
    # all() function returns true if every single distance is over threshhold
    
def run_gesture_feed():
    cap = cv2.VideoCapture(0) #0 means use firt web cam (like index positions)
#cap is a live feed object to read frames from

    with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7) as hands:
    # hand detector tracking 1 hand at most, only takes as detection if 70+% confident
    #more than 70% threshhold more likely false negatives through overfitting
    # less than 50% threshold more likely false positives through underfitting

        while cap.isOpened():
            success, frame = cap.read()
        # Webcam constantly capturing frames like video
        # grabs one frame at time in a loop
        # success tells if the read woked, frame is the image so if reading the cam is a success 
            if not success:
                break
            
            frame = cv2.flip(frame,1)
        #fixes the flipping of the feed to now act as a mirror

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb)
        # opencv stores frames in BGR by default, MediaPipe needs RGB
        # converted and passed through the detector
            gesture = 'none'
            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    gesture = detect_gesture(hand_landmarks)
                # result.multi_hand_landmarks contains 21 points MediaPipe found on hand *knucles, fingertips etc
                # if found a hand, loop through and draw all dots and ligns connecting them
        
            colour = (255,255,255)
            if gesture == "pinch":
                colour = (0,255,0) #green=long
            elif gesture == "spread":
                colour = (0,0,255) #red=short
                #OpenCV colours are BGR not RGB

            cv2.putText(frame, f'Gesture: {gesture.upper()}', (10,40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, colour, 2)
            # draws text onto frame
            cv2.imshow("Hand Tracker", frame) #renders frame in new window called hand tracker
            if cv2.waitKey(1) & 0xFF == ord("q"): # wait key waits 1 ms between frames, if Q is pressed loop breaks feed ends
                break
    
    cap.release()
    cv2.destroyAllWindows() # releases webcam so can be used by other apps and closes OpenCv completely

if __name__ == "__main__":
    run_gesture_feed()