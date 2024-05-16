import cv2
import requests
import numpy as np
import io



def main():
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        _, img_encoded = cv2.imencode('.jpg', frame)
        # Convert the encoded image to bytes
        img_bytes = img_encoded.tobytes()

        # Create a BytesIO object from the bytes
        img_io = io.BytesIO(img_bytes)
        # response = requests.post('http://localhost:5000/check_ergonomics', files={'image': ('image.jpg', img_bytes, 'image/jpeg')})
        response = requests.post('http://localhost:5000/check_ergonomics', files={'image': ('image.jpg', img_io, 'image/jpeg')})

        if response.status_code == 200:
            data = response.json()

            # Get the size of the image
            height, width = frame.shape[:2]

            # Extract the keypoints from the response and rescale them to the size of the image
            keypoints = [cv2.KeyPoint(landmark['x'] * width, landmark['y'] * height, 6) for landmark in data['landmarks']]

            # Draw the keypoints on the frame
            frame = cv2.drawKeypoints(frame, keypoints, outImage=np.array([]), color=(0, 255, 0),
                                                     flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

            # Display the ergonomic status on the frame
            status = "Ergonomic" if data['is_ergonomic'] else "Not Ergonomic"
            cv2.putText(frame, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)


        else:
            print(f"Request failed with status code {response.status_code}")

        cv2.imshow('Webcam', frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    cap.release()

if __name__ == "__main__":
    main()