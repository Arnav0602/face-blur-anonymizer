class FaceTracker:
    def __init__(self, grace_period=8):
        self.grace_period = grace_period
        self.tracked_faces = []

    def update(self, detected_boxes):
        updated_tracked = []

        for face in self.tracked_faces:
            face["matched"] = False

        for box in detected_boxes:
            match = self._find_overlapping(box)
            if match is not None:
                match["box"] = box
                match["missed"] = 0
                match["matched"] = True
            else:
                self.tracked_faces.append({"box": box, "missed": 0, "matched": True})

        for face in self.tracked_faces:
            if not face["matched"]:
                face["missed"] += 1
            if face["missed"] <= self.grace_period:
                updated_tracked.append(face)

        self.tracked_faces = updated_tracked

        return [face["box"] for face in self.tracked_faces]

    def _find_overlapping(self, box, iou_threshold=0.3):
        best_face = None
        best_iou = iou_threshold

        for face in self.tracked_faces:
            iou = self._iou(face["box"], box)
            if iou > best_iou:
                best_iou = iou
                best_face = face

        return best_face

    @staticmethod
    def _iou(box_a, box_b):
        ax, ay, aw, ah = box_a
        bx, by, bw, bh = box_b

        x1 = max(ax, bx)
        y1 = max(ay, by)
        x2 = min(ax + aw, bx + bw)
        y2 = min(ay + ah, by + bh)

        inter_w = max(0, x2 - x1)
        inter_h = max(0, y2 - y1)
        intersection = inter_w * inter_h

        area_a = aw * ah
        area_b = bw * bh
        union = area_a + area_b - intersection

        if union == 0:
            return 0
        return intersection / union