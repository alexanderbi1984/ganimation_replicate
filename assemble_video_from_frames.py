import os
import subprocess


def assemble_videos_from_frames(folder_path, output_folder):
    # for subfolder in os.listdir(folder_path):
    #     folder_path = os.path.join(folder_path, subfolder)
    # print(folder_path)
    # print(output_folder)
    if os.path.isdir(folder_path):
        folder_name = os.path.basename(folder_path)

        # List all BMP files in the subfolder
        frame_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.bmp')])

        if frame_files:
            # Construct the output video file path
            output_video_path = os.path.join(output_folder, f"{folder_name}.mp4")

            # # Debugging print to show the frames found
            # print(f"Frames found in {folder_name}: {frame_files}")

            # Create a temporary text file to list all frame paths
            with open(os.path.join(folder_path, 'file_list.txt'), 'w') as file_list:
                for frame in frame_files:
                    file_list.write(f"file '{os.path.join(folder_path, frame)}'\n")

            # Create the ffmpeg command
            ffmpeg_command = [
                r"W:\Nan\ffmpeg-master-latest-win64-gpl\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe", '-r', '25', '-f', 'concat', '-safe', '0',
                '-i', os.path.join(folder_path, 'file_list.txt'),
                '-c:v', 'libx264', '-pix_fmt', 'yuv420p', output_video_path
            ]

            # print(f"Running command: {' '.join(ffmpeg_command)}")  # Debugging line

            # Execute the command
            subprocess.run(ffmpeg_command)
            print(f"Video created for {folder_name}: {output_video_path}")
        else:
            print(f"No frames found in {folder_name}")
    else:
        print("Folder does not exist")

# Example usage:
# assemble_videos_from_frames(r"W:\Nan\ganimation_replicate\results\frames\frame_det_00_000202-082809_m_26-PA2-050",r"W:\Nan\ganimation_replicate\results\frames")
