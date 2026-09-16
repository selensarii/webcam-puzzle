import cv2
import numpy as np
import random

class Puzzle:
    def __init__(self, img, rows=4, cols=4):
        self.img = img
        self.rows = rows
        self.cols = cols
        self.h, self.w = img.shape[:2]
        self.piece_w = self.w // self.cols
        self.piece_h = self.h // self.rows
        self.pieces = []
        self.solved_order = []
        self.current_order = []
        self._create_pieces()
        self._shuffle_pieces()

    def _create_pieces(self):
        idx = 0
        for r in range(self.rows):
            for c in range(self.cols):
                y1, y2 = r * self.piece_h, (r + 1) * self.piece_h
                x1, x2 = c * self.piece_w, (c + 1) * self.piece_w
                piece_img = self.img[y1:y2, x1:x2].copy()
                self.pieces.append({
                    'id': idx,
                    'img': piece_img,
                    'correct_r': r,
                    'correct_c': c
                })
                self.solved_order.append(idx)
                idx += 1

    def _shuffle_pieces(self):
        self.current_order = self.solved_order.copy()
        random.shuffle(self.current_order)

    def draw(self, bg_img, top_left_x, top_left_y, dragging_idx=None, drag_pos=None):
        for r in range(self.rows):
            for c in range(self.cols):
                grid_idx = r * self.cols + c
                piece_id = self.current_order[grid_idx]
                if grid_idx == dragging_idx:
                    continue
                piece_img = self.pieces[piece_id]['img']
                px = top_left_x + c * self.piece_w
                py = top_left_y + r * self.piece_h
                if py >= 0 and py + self.piece_h <= bg_img.shape[0] and px >= 0 and px + self.piece_w <= bg_img.shape[1]:
                    bg_img[py:py+self.piece_h, px:px+self.piece_w] = piece_img
                    cv2.rectangle(bg_img, (px, py), (px+self.piece_w, py+self.piece_h), (255, 255, 255), 1)

        if dragging_idx is not None and drag_pos is not None:
            piece_id = self.current_order[dragging_idx]
            piece_img = self.pieces[piece_id]['img']
            cx, cy = drag_pos
            px = cx - self.piece_w // 2
            py = cy - self.piece_h // 2
            if py >= 0 and py + self.piece_h <= bg_img.shape[0] and px >= 0 and px + self.piece_w <= bg_img.shape[1]:
                bg_img[py:py+self.piece_h, px:px+self.piece_w] = piece_img
                cv2.rectangle(bg_img, (px, py), (px+self.piece_w, py+self.piece_h), (0, 255, 0), 2)
        return bg_img

    def get_piece_at(self, x, y, top_left_x, top_left_y):
        rel_x = x - top_left_x
        rel_y = y - top_left_y
        if 0 <= rel_x < self.w and 0 <= rel_y < self.h:
            c = rel_x // self.piece_w
            r = rel_y // self.piece_h
            return r * self.cols + c
        return None

    def swap_pieces(self, idx1, idx2):
        if idx1 is not None and idx2 is not None and idx1 != idx2:
            self.current_order[idx1], self.current_order[idx2] = self.current_order[idx2], self.current_order[idx1]

    def is_solved(self):
        return self.current_order == self.solved_order
