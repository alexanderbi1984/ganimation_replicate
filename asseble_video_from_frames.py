import os
import subprocess


def assemble_videos_from_frames(folder_path, output_folder):
    for subfolder in os.listdir(folder_path):
        subfolder_path = os.path.join(folder_path, subfolder)

        if os.path.isdir(subfolder_path):
            # List all BMP files in the subfolder
            frame_files = sorted([f for f in os.listdir(subfolder_path) if f.endswith('.bmp')])

            if frame_files:
                # Construct the output video file path
                output_video_path = os.path.join(output_folder, f"{subfolder}.mp4")

                # Debugging print to show the frames found
                print(f"Frames found in {subfolder}: {frame_files}")

                # Create a temporary text file to list all frame paths
                with open(os.path.join(subfolder_path, 'file_list.txt'), 'w') as file_list:
                    for frame in frame_files:
                        file_list.write(f"file '{os.path.join(subfolder_path, frame)}'\n")

                # Create the ffmpeg command
                ffmpeg_command = [
                    r"C:\Users\Nan Bi\Downloads\ffmpeg-master-latest-win64-gpl\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe", '-r', '25', '-f', 'concat', '-safe', '0',
                    '-i', os.path.join(subfolder_path, 'file_list.txt'),
                    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', output_video_path
                ]

                print(f"Running command: {' '.join(ffmpeg_command)}")  # Debugging line

                # Execute the command
                subprocess.run(ffmpeg_command)
                print(f"Video created for {subfolder}: {output_video_path}")

# Example usage:
assemble_videos_from_frames(r"C:\pain\BioVid_Frame_224",r"C:\pain\BioVid_224_video")
