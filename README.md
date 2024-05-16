# Pose estimation to check ergonomics

In this project I'm using the MediaPipe library to detect the keypoints of a person and I check if the wrist is in a ergonomical position

buld and run the docker container
```bash
docker build -t myflaskapp .
```

```bash
docker run -d -p 5000:5000 myflaskapp
```

run the app
```bash
python test.py
```

![image](https://github.com/enrypiff/pose_estimation/assets/139701172/f58c84e3-dac4-4187-bf73-65bcd13803b0)

![image](https://github.com/enrypiff/pose_estimation/assets/139701172/6edbf9b8-8ba2-4209-a6a9-592c0480b9b6)
