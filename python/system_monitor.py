import os
from datetime import datetime

def check_disk():
    return os.popen("df -h").read()

def check_memory():
    return os.popen("free -h").read()

def write_log(data):
    with open("system.log", "a") as f:
        f.write(data + "\n")

def main():
    print("Running system monitor...")

    disk = check_disk()
    memory = check_memory()

    log_entry = f"{datetime.now()}\n{disk}\n{memory}\n"

    write_log(log_entry)

    print("Log written successfully!")

if __name__ == "__main__":
    main()