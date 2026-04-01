import cv2

def calculate_pnl(position, entry_price, current_price):
    if position == "long":
        return current_price - entry_price
    if position == "short":
        return entry_price - current_price
    return 0

def draw_overlay(frame, position, entry_price, current_price, realised_pnl):
    pnl = calculate_pnl(position, entry_price, current_price)

    # Colours
    position_colour = (0, 255, 0) if position == 'long' else (0, 0, 255) if position == 'short' else (255, 255, 255)
    pnl_colour = (0, 255, 0) if pnl > 0 else (0, 0, 255) if pnl < 0 else (255, 255, 255)
    realised_colour = (0, 255, 0) if realised_pnl > 0 else (0, 0, 255) if realised_pnl < 0 else (255, 255, 255)

    # Dark background panel
    overlay = frame.copy()
    cv2.rectangle(overlay, (5, 60), (255, 220), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)

    # Text
    cv2.putText(frame, f'Position: {position.upper()}', (10, 85),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, position_colour, 2)
    cv2.putText(frame, f'Entry:    ${entry_price}', (10, 115),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(frame, f'Current:  ${current_price}', (10, 145),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(frame, f'P&L:      ${round(pnl, 2)}', (10, 175),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, pnl_colour, 2)
    cv2.putText(frame, f'Realised: ${realised_pnl}', (10, 205),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, realised_colour, 2)

    return frame