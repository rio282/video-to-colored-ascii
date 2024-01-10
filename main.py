import os
import cv2
import time
from PIL import Image

COMPRESSION = Image.Resampling.NEAREST


def get_colored_text(r, g, b, text):
    color_code = f"\033[38;2;{r};{g};{b}m"
    reset_code = "\033[0m"
    return f"{color_code}{text}{reset_code}"


def draw_pixel(pixel_data) -> None:
    r, g, b = pixel_data
    pixel_placeholder = "@@"

    print(get_colored_text(r, g, b, pixel_placeholder), end="", flush=True)


def resize_frame_to(image_name: str, new_size: int) -> Image:
    image = Image.open(image_name)

    # calc new size
    width_percentage = (new_size / float(image.size[0]))
    new_height = int((float(image.size[1]) * float(width_percentage)))

    # resize
    image = image.resize((new_size, new_height), COMPRESSION)
    return image


def print_frame(frame: Image) -> None:
    width, height = frame.size
    pixels = list(frame.getdata())

    os.system("cls")
    for y in range(height):
        for x in range(width):
            pixel = pixels[y * width + x]
            draw_pixel(pixel)
        print(flush=True)


def extract_video_frames(video_name: str) -> list:
    cap = cv2.VideoCapture(video_name)
    output_folder = "./frames"
    frames = []
    total_frames_amount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT));

    # check if video opened successfully
    if not cap.isOpened():
        print("Error opening video file")
        return []

    # create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # filename
        frame_filename = os.path.join(output_folder, f"frame_{len(frames) + 1}.jpg")
        frames.append(frame_filename)

        # output
        max_loader_stripes = 50
        loader_stripes = int(len(frames) / total_frames_amount * max_loader_stripes)
        loading_bar = f"[{'=' * loader_stripes}{'-' * (max_loader_stripes - loader_stripes)}]"
        print(
            f"\rLoading frame: {len(frames)}/{total_frames_amount}",
            loading_bar,
            f"{len(frames) / total_frames_amount * 100: 0.2f} %",
            end="",
            flush=True
        )

        # write
        cv2.imwrite(frame_filename, frame)

    # release & return
    cap.release()
    return frames


def play_video(video_name: str, fps: int, frame_size: int) -> None:
    frames = extract_video_frames(video_name)

    print()
    print("Video is ready to be played!")
    os.system("pause & cls")

    frame_time = 1 / fps
    for frame in frames:
        frame = resize_frame_to(frame, frame_size)
        print_frame(frame)
        time.sleep(frame_time)


def main() -> None:
    video_name = "./test_files/minions.mp4"
    frame_size = 64
    fps = 60
    play_video(video_name, fps, frame_size)


if __name__ == "__main__":
    main()
