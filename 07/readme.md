# 今天針對MAVproxy進行展示

操作過程影片 https://youtu.be/a15DjRs6aJU

## SITL佈署

 07資料夾中有兩個檔案
 
 Docker 資料夾中為部署SITL的文件
 
 使用 docker-compose up 佈署，如果以完成安裝可直接進行第二步
 
 1. 請使用apt先完成docker ,docker-compose 安裝
 ```
 apt install -y docker docker-compose
 ```
2. 運行
```
 docker-compose up 
```

## 安裝與使用mavproxy
 使用requirements.txt進行安裝pip
 ```
 1. pip install -r requirements.txt 
 ```
 
requirements.txt存放於本github目錄中

 2. 運行mavproxy.py
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
 
圖形化介面

![](https://github.com/Oliver0804/mavlink_tutorial/blob/main/07/pic/%E6%88%AA%E5%9C%96%202023-05-31%20%E4%B8%8B%E5%8D%881.23.34.png)

![](https://github.com/Oliver0804/mavlink_tutorial/blob/main/07/pic/%E6%88%AA%E5%9C%96%202023-05-31%20%E4%B8%8B%E5%8D%881.23.56.png)


 - 有時候需要重起SITL CTRL+C 必重新運行
 -  終端機開始有打印資訊了


## mavproxy 命令操作
### 命令介紹
1. mode [mode/null]

Available modes:  dict_keys(['STABILIZE', 'ACRO', 'ALT_HOLD', 'AUTO', 'GUIDED', 'LOITER', 'RTL', 'CIRCLE', 'POSITION', 'LAND', 'OF_LOITER', 'DRIFT', 'SPORT', 'FLIP', 'AUTOTUNE', 'POSHOLD', 'BRAKE', 'THROW', 'AVOID_ADSB', 'GUIDED_NOGPS', 'SMART_RTL', 'FLOWHOLD', 'FOLLOW', 'ZIGZAG', 'SYSTEMID', 'AUTOROTATE', 'AUTO_RTL'])
| 飛行模式 | 高度控制 | 位置控制 | 位置感測器 | 總結 |
|----------|----------|----------|----------|------|
| Acro | - | - | - | 保持態度，不自我平衡 |
| Airmode | - | -/+ | - | 實際上不是一種模式，而是一種特性 |
| Alt Hold | s | + | - | 保持高度並自我平衡滾動和俯仰 |
| Auto | A | A | Y | 執行預定的任務 |
| AutoTune | s | A | Y | 自動的俯仰和橫滾程序，以改善控制迴圈 |
| Brake | A | A | Y | 使無人機立即停止 |
| Circle | s | A | Y | 自動繞著前方的點旋轉 |
| Drift | - | + | Y | 類似於穩定模式，但與飛機一樣協調偏航和滾動 |
| Flip | A | A | - | 升高並完成自動翻轉 |
| FlowHold | s | A | - | 使用光流進行位置控制 |
| Follow | s | A | Y | 跟隨另一架無人機 |
| Guided | A | A | Y | 導航到由地面站指定的單個點 |
| Heli_Autorotate | A | A | Y | 用於傳統直升機的緊急情況。僅限直升機。目前只有SITL。 |
| Land | A | s | (Y) | 將高度降至地面水平，嘗試直接下降 |
| Loiter | s | s | Y | 保持高度和位置，使用GPS進行移動 |
| PosHold | s | + | Y | 類似於盤旋，但當搖桿不在中心時，手動滾動和俯仰 |
| RTL | A | A | Y | 返回到起飛位置，可能還包括著陸 |
| Simple/Super Simple | - | - | Y | 添加到飛行模式的插件，使用駕駛員視角而不是偏航方向 |
| SmartRTL | A | A | Y | RTL，但追蹤路徑返回 |
| Sport | s | s | - | Alt-hold，但當搖桿在中心時保持俯仰和滾動 |
| Stabilize | - | + | - | 自我平衡滾動和俯仰軸 |

注意 不同的設備提供的mode有所不同，在不同的設備起飛流程也有差別

2. arm [<check|uncheck|list|throttle|safetyon|safetyoff|safetystatus|bits|prearms>]
3. module [load <module_name>/list]
4. velocity [X Y Z]

### 命令介紹
![](https://github.com/Oliver0804/mavlink_tutorial/blob/main/07/pic/%E6%88%AA%E5%9C%96%202023-05-31%20%E4%B8%8B%E5%8D%881.24.19.png)
這邊主要使用MAVproxy中所提供令命進行，如果要使用python/C++SDK等程序控制也沒問題。可同時主要是mavproxy.py運行時候有待<--out=udp:127.0.0.1:14550> 參數

#### 起飛程序
1. mode guided
2. arm throttle
3. takeoff 20
#### 移動相對位置
GUIDED> velocity

GUIDED> Usage: velocity x y z (m/s)

1. velocity 10 0 0 //前進10m
2. velocity 10 10 0 //前進10m向右10m 同時

#### 繞圈
1. rc 3 1500
2. mode circle
3. 
這邊如果沒將油門rc ch-3 推到1500 在旋轉過程中會持續下降

#### RTL
1. mode rtl

如果高度低於15m，設備會先拉高到預設高度後，才執行RTL


