import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands #uses hand module
mp_draw = mp.solutions.drawing_utils #drawing utility to draw the skeleton

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

            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                # result.multi_hand_landmarks contains 21 points MediaPipe found on hand *knucles, fingertips etc
                # if found a hand, loop through and draw all dots and ligns connecting them
        
            cv2.imshow("Hand Tracker", frame) #renders frame in new window called hand tracker
            if cv2.waitKey(1) & 0xFF == ord("q"): # wait key waits 1 ms between frames, if Q is pressed loop breaks feed ends
                break
    
    cap.release()
    cv2.destroyAllWindows() # releases webcam so can be used by other apps and closes OpenCv completely

if __name__ == "__main__":
    run_gesture_feed()