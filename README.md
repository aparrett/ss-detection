# Shooting Star Detector

## Instructions (Windows)

#### 1. Install Python

https://www.python.org/downloads/

#### 2. Install opencv

Run this command: `pip3 install opencv-python`

#### 3. Copy the contents of `main.py` into a file on your own computer.

You can name the file whatever you want but the file extension must be `.py`

#### 4. Change the `filePath` at the top of the file to the path of your video file. 

Example: 

```py
filePath = "Documents/my-video.mp4"
```

#### 5. Open terminal and run the script with this command:
```sh
python main.py
```

Be sure to replace `main.py` with whatever you saved the script as. If your terminal is not in the same directory where you saved the script, you will have to put the path to the file. For example, if your terminal is at `C:\Users\aparr` and your script is in the `Documents` folder, you would use `python Documents/main.py`. The same pattern applies to the `filePath` at the top of the script. If your terminal is at `C:\Users\aparr` and your file is in the `Documents` folder, make sure to put `Documents/my-video.mp4` as your filePath.


## Results

You can view the results of the script in the folder you executed the script from in your terminal. There will be a folder called `logs` with a `log.txt` file and images of each frame in which motion was detected. The `log.txt` file will have a list of timestamps of the frames with detected motion.
