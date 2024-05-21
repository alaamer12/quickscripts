import shutil
import os
import colorama

def compy_dir(src: str, des: str) -> None:
    shutil.copytree(src, des)



if __name__ == "__main__":
    colorama.init(autoreset=True)
    src = input(colorama.Fore.BLUE + "Enter the source directory: " + colorama.Fore.RESET)
    des = input(colorama.Fore.BLUE + "Enter the destination directory: " + colorama.Fore.RESET)
    if os.path.exists(des):
        raise FileExistsError(f"Directory {des} already exists")
    compy_dir(src, des)
    print(colorama.Fore.GREEN + f"Directory {des} created successfully" + colorama.Fore.RESET)
    print("[OK]")
