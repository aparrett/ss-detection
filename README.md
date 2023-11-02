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

**Important note on paths**
The easiest way to deal with the different file paths is to save your python script and the video in the same folder and change into that folder in the terminal. To do that you can use the `cd` command. For example, if you're in `C:\Users\aparr` and your files are all saved in `C:\Users\aparr\Documents` you can enter `cd Documents` into your terminal and press `Enter` and now you will be executing the python command from that folder instead. If that's the case, you don't need to add `Documents/` to your python command or your filePath in the script because you're already in that folder.


## Results

You can view the results of the script in the folder you executed the script from in your terminal. There will be a folder called `logs/yourVideoname` with a `log.txt` file and images of each frame in which motion was detected. The `log.txt` file will have a list of timestamps of the frames with detected motion.

If you run the script on the same video multiple times, you will get duplicate files created and duplicate logs in `log.txt`. If you're testing different thresholds, you will probably want to delete your logs/yourVideoName folder after every run.

Sometimes you may find that it doesn't look like there is a meteor in the image. It would still worth be visiting that timestamp in the video because it could be showing the very beginning or very end of a faint meteor.

## Customization

- The thresholds can be adjusted to your liking if the script is not detecting all of the meteors or if there are too many false positives. Just be careful that you're not excluding faint meteors.
- If you're playing with the thresholds, it can be useful to change showVideo from `False` to `True` so that you can see the video detecting (or not detecting) meteors as it plays. I'm not sure how the performance of this will be with longer videos, though.

## Noise

If you have a noisy image that is getting a lot of false positives, trying using a blur threshold of 15 and difference threshold of 20. This will 