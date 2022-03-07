import threading
import time

# 子執行緒的工作函數
def job():
    result = ''
    while result != 'input Quit':
        result = input()
        print('result', result)
        time.sleep(1)

# 建立一個子執行緒
t = threading.Thread(target = job)

# 執行該子執行緒
t.start()

# 主執行緒繼續執行自己的工作
for i in range(10):
  print("Main thread:", i)
  time.sleep(1)

# 等待 t 這個子執行緒結束
t.join()

print("Done.")