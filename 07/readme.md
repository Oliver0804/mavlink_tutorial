# 今天針對MAVproxy進行展示
##SITL部屬
 07資料夾中有兩個檔案
 Docker 資料夾中為部署SITL的文件
 使用 docker-compose up 佈署
 請使用apt先完成docker ,docker-compose 安裝
 ```
 apt install -y docker docker-compose
 ```
運行
```
 docker-compose up 
```

## 安裝與使用mavproxy
 使用requirements.txt進行安裝pip
 ```
 pip install -r requirements.txt 
 ```

 運行mavproxy.py
 ```
 mavproxy.py --master=tcp:127.0.0.1:5760 \
 --out=udp:127.0.0.1:14550 \
 --out=udp:127.0.0.1:14551 \
 --map \
 --console 
 ```

 --master 指向設備
 --out 用於輸出 可以多組,用於地面站或是其他程序接入使用
 --map 打開地圖
 --console 打開圖形界面

### 有時候需要重起SITL CTRL+C 必重新運行
### 終端機開始有打印資訊了


##mavproxy 命令操作
1. mode [list]
2. arm 
3. module [load/list]
4. velocity [X Y Z]