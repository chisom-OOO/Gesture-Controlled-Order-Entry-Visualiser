import cv2
import mediapipe as mp
from gesture import detect_gesture
from display import draw_overlay
from orders import get_position, get_realised_pnl, get_entry_price, update_position, get_trade_log, get_price


mp_hands = mp.solutions.hands #uses hand module
mp_draw = mp.solutions.drawing_utils #drawing utility to draw the skeleton

def run():
    cap = cv2.VideoCapture(0)

    with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7) as hands:
        frame_count = 0
        current_price = 0
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb)
            gesture = 'none'

            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    gesture = detect_gesture(hand_landmarks)
            
            update_position(gesture)

            colour = (255,255,255)
            if gesture == 'pinch':
                colour = (0, 255, 0)
            elif gesture == 'spread':
                colour = (0, 0, 255)

            cv2.putText(frame, f'Gesture: {gesture.upper()}', (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, colour, 2)
            
            frame_count += 1
            if frame_count % 60 == 0 or current_price == 0:
                current_price = get_price()

            entry_price = get_entry_price()
            position = get_position()
            frame = draw_overlay(frame, position, entry_price, current_price,get_realised_pnl())
            cv2.imshow("Hand Tracker", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run()
