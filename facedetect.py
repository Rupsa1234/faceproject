import cv2
import mysql.connector

# Load the Haar cascade XML file for face detection
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Connect to the MySQL database
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='mydb'
)
cursor = db.cursor()
# table_creation_query = '''CREATE table faces (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     x INT,
#     y INT,
#     width INT,
#     height INT
# )'''

# cursor.execute(table_creation_query)
# db.commit()

# Capture video from webcam or load a video file
video_capture = cv2.VideoCapture(0)  # Use 0 for webcam or provide the path to a video file

while True:
    # Read each frame of the video
    ret, frame = video_capture.read()

    # Convert the frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Perform face detection
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

    # Iterate over detected faces
    for (x, y, w, h) in faces:
        # Draw a rectangle around the detected face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Perform face recognition or authentication logic here
        # For the purpose of this example, we'll assume face authentication is successful
        authorized_user = True

        if authorized_user:
            cv2.putText(frame, 'Access Granted', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        else:
            cv2.putText(frame, 'Access Denied', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
        query = "INSERT INTO faces (x, y, width, height) VALUES (%s, %s, %s, %s)"
        values = (int(x), int(y), int(w), int(h))
        cursor.execute(query, values)
        db.commit()
    # Display the frame
    cv2.imshow('Face Login', frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close the database connection
video_capture.release()
cv2.destroyAllWindows()
cursor.close()
db.close()

