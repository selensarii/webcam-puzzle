import cv2
import time
from hand_tracking import HandTracker
from puzzle import Puzzle

def main():
    cap = cv2.VideoCapture(1) 
    if not cap.isOpened():
        cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    tracker = HandTracker(detectionCon=0.8, maxHands=2)
    
    mode = "FRAME" 
    puzzle = None
    puzzle_top_left = (0, 0)
    
    dragging_idx = None
    
    while True:
        success, img = cap.read()
        if not success:
            break
            
        img = cv2.flip(img, 1)
        h, w, _ = img.shape
        img = tracker.findHands(img, draw=False)
        
        lmList1 = tracker.findPosition(img, handNo=0, draw=False)
        lmList2 = tracker.findPosition(img, handNo=1, draw=False)
        
        if mode == "FRAME":
            cv2.putText(img, "ADIM 1: CERCEVELE", (w//2 - 150, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(img, "Sag ve Sol isaret parmaklarinla koseleri belirle.", (w//2 - 300, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(img, "Cekmek icin IKI ELINLE CIMDIK yap!", (w//2 - 180, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            
            if tracker.results.multi_hand_landmarks and len(tracker.results.multi_hand_landmarks) == 2:
                if len(lmList1) > 8 and len(lmList2) > 8:
                    x1, y1 = lmList1[8][1], lmList1[8][2]
                    x2, y2 = lmList2[8][1], lmList2[8][2]
                    
                    min_x, max_x = min(x1, x2), max(x1, x2)
                    min_y, max_y = min(y1, y2), max(y1, y2)
                    
                    if max_x - min_x > 100 and max_y - min_y > 100:
                        cv2.rectangle(img, (min_x, min_y), (max_x, max_y), (0, 255, 255), 3)
                        
                        pinching1, _ = tracker.is_pinch(lmList1, draw=False)
                        pinching2, _ = tracker.is_pinch(lmList2, draw=False)
                        
                        if pinching1 and pinching2:
                            min_y, max_y = max(0, min_y), min(h, max_y)
                            min_x, max_x = max(0, min_x), min(w, max_x)
                            
                            roi = img[min_y:max_y, min_x:max_x].copy()
                            puzzle = Puzzle(roi, rows=4, cols=4)
                            puzzle_top_left = (w//2 - roi.shape[1]//2, h//2 - roi.shape[0]//2)
                            mode = "SOLVE"
                            is_dragging = False
                            cv2.waitKey(500)

        elif mode == "SOLVE":
            cv2.putText(img, "ADIM 2: BULMACAYI COZ", (w//2 - 180, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(img, "Parcalari tasi. Basa donmek icin YUMRUK yap.", (w//2 - 250, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            if tracker.is_fist(lmList1) or tracker.is_fist(lmList2):
                mode = "FRAME"
                puzzle = None
                dragging_idx = None
                cv2.waitKey(500)
                continue
                
            if puzzle:
                cursor_pos = None
                is_pinching = False
                active_lmList = None
                
                if len(lmList1) > 8:
                    cursor_pos = (lmList1[8][1], lmList1[8][2])
                    is_pinching, _ = tracker.is_pinch(lmList1, draw=False)
                    active_lmList = lmList1
                elif len(lmList2) > 8:
                    cursor_pos = (lmList2[8][1], lmList2[8][2])
                    is_pinching, _ = tracker.is_pinch(lmList2, draw=False)
                    active_lmList = lmList2
                    
                if cursor_pos:
                    hover_idx = puzzle.get_piece_at(cursor_pos[0], cursor_pos[1], puzzle_top_left[0], puzzle_top_left[1])
                    
                    if is_pinching:
                        if dragging_idx is None and hover_idx is not None:
                            dragging_idx = hover_idx
                    else:
                        if dragging_idx is not None:
                            if hover_idx is not None and hover_idx != dragging_idx:
                                puzzle.swap_pieces(dragging_idx, hover_idx)
                            dragging_idx = None

                    if not is_pinching and hover_idx is not None:
                        px = puzzle_top_left[0] + (hover_idx % puzzle.cols) * puzzle.piece_w
                        py = puzzle_top_left[1] + (hover_idx // puzzle.cols) * puzzle.piece_h
                        cv2.rectangle(img, (px, py), (px+puzzle.piece_w, py+puzzle.piece_h), (0, 0, 255), 2)

                img = puzzle.draw(img, puzzle_top_left[0], puzzle_top_left[1], dragging_idx, cursor_pos)
                
                if active_lmList:
                    tracker.is_pinch(active_lmList, draw=True, img=img)
                
                if puzzle.is_solved():
                    mode = "WIN"

        elif mode == "WIN":
            cv2.putText(img, "TEBRIKLER! COZDUN!", (w//2 - 180, h//2), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 4)
            cv2.putText(img, "Yeniden baslamak icin YUMRUK yap", (w//2 - 250, h//2 + 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            
            if tracker.is_fist(lmList1) or tracker.is_fist(lmList2):
                mode = "FRAME"
                puzzle = None
                cv2.waitKey(500)

        cv2.imshow("Webcam Puzzle", img)
        
        key = cv2.waitKey(1)
        if key == 27 or key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
