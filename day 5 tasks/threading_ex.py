import threading
import time

def task(name):
  
    print(f"Thread {name}: starting...")
    time.sleep(10)                                           # giving  a time-consuming operation
    print(f"Thread {name}: finishing.")

if __name__ == "__main__":
    print("Main thread: starting...")

    my_thread = threading.Thread(target=task, args=("A",))

    my_thread.start()

    print("Main thread: doing other work...")

    my_thread.join()

    print("Main thread: all done.")