# For adding shape recognition. A useful link https://pyimagesearch.com/2016/02/08/opencv-shape-detection/
# Does not use AI so probably faster to process. For simple shapes also a better solution

import cv2
import numpy as np

if __name__ == "__main__":

    # Set webcam parameters
    cam_feed = cv2.VideoCapture(0)
    cam_feed.set(cv2.CAP_PROP_FRAME_WIDTH, 650)
    cam_feed.set(cv2.CAP_PROP_FRAME_HEIGHT, 750)

    while True:
        ret, frame = cam_feed.read()

        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Blur the image to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Detect edges using Canny edge detection
        edges = cv2.Canny(blurred, 50, 150)

        # Apply morphological opening to remove noise and clutter
        kernel = np.ones((5, 5), np.uint8)
        opening = cv2.morphologyEx(edges, cv2.MORPH_OPEN, kernel)

        # Find contours in the edges image
        contours, _ = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Create a copy of the original frame
        frame_copy = frame.copy()

        # Loop over all contours and detect shapes
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.03 * cv2.arcLength(contour, True), True)

            # Skip small contours to reduce noise
            if cv2.contourArea(approx) < 100:
                continue

            x, y, w, h = cv2.boundingRect(approx)

            # Detect and draw shapes based on number of vertices
            if len(approx) == 3 and cv2.isContourConvex(approx):
                cv2.putText(frame_copy, "Triangle", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                cv2.drawContours(frame_copy, [approx], 0, (0, 255, 0), 2)
            elif len(approx) == 4:
                aspect_ratio = float(w) / h
                if aspect_ratio >= 0.95 and aspect_ratio <= 1.05:
                    cv2.putText(frame_copy, "Square", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    cv2.drawContours(frame_copy, [approx], 0, (0, 0, 255), 2)
                else:
                    cv2.putText(frame_copy, "Rectangle", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    cv2.drawContours(frame_copy, [approx], 0, (0, 0, 255), 2)
            elif len(approx) >= 5:
                # Fit an ellipse to the contour and draw it
                if len(approx) >= 5:
                    ellipse = cv2.fitEllipse(approx)
                    cv2.putText(frame_copy, "Circle", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                    cv2.ellipse(frame_copy, ellipse, (255, 0, 0), 2)

        # Display the image
        cv2.imshow('frame', frame_copy)

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close the window
    cam_feed.release()
    cv2.destroyAllWindows()

