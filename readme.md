>## ***serving할 모델 만들기***
torch-model-archiver --model-name facedetector --version 0.0.1 --serialized-file 512_512_ADAM_PCENTER_RES18-prepost-0021.jit --handler customhandler.py --extra-files index_to_name.json --force

>## ***실행하기***
torchserve --start --ts-config config.properties --ncs --model-store . --models facedetector.mar

>## ***중단하기***
torchserve --stop

>## ***이미지 다운로드***
curl -O https://skybiometry.com/wp-content/uploads/2016/01/grouping-1st-R-e1451909599172.jpg

>## ***결과 얻기***
curl http://localhost:8080/predictions/facedetector -T grouping-1st-R-e1451909599172.jpg
or
curl http://localhost:8080/predictions/facedetector -F "data=@grouping-1st-R-e1451909599172.jpg"

>## ***도커 빌드 및 실행***
* 도커 빌드 : ./build_image.sh -g -cv cu101 -t jonggon/torchserve_opencv:0.0.0 하거나
  * 자세한 내용은 [여기](https://github.com/pytorch/serve/tree/master/docker)
* 도커 PULL 한다
  * docker pull jonggon/torchserve_opencv

* 도커 실행
  * bash start_front.sh : 확인용
  * bash start_background.sh : 실제 서비스용

>## ***쿠버네티스(microk8s) / 헬름(helm) 설치 및 실행***
* 쿠버네티스 실행 : helm install facedetector Helm

>## ***환경***
* ubuntu 18.04 LTS / cuda version : 10.1.243
* python version : 3.6.9
* torch version : 1.8.0 / torchvision version : 0.8.2
* torch-model-archiver version  0.3.1 / torchserve version : 0.3.1

