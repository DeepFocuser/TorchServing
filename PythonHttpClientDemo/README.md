> # **what is it?**
  * Kubernetes 서버가 잘 동작하는지 확인하는
    간단한 Python http client 코드

> # **실행 방법**
  * 설치
    ```cmd
    pip install opencv-python
    ```
  * ex image ) python main.py --address 192.168.35.69:8000 --image sample.jpg --outimage result.mp4 --classfile class.txt --size 512 512 --thresh 0.1 --saveimage True
  * ex video ) python main.py --address 192.168.35.69:8000 --video sample.mp4 --outvideo result.mp4 --classfile class.txt --size 512 512 --thresh 0.1 --savevideo True
