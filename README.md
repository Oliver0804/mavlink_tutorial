# mavlink_tutorial

## MavLink 介紹

### 使用環境

1. 本項目基於conda 使用3.8.16版本python進行開發測試
```
conda create -n mavlink python=3.8.16
```
2. 安裝pip相關庫
```
pip install -r requirements.txt
```

## Mavproxy 介紹

MAVProxy 是一款基於命令行的無人機飛行控制和任務規劃軟件，它主要用於MAVLink通訊協議的無人機。MAVLink是一種廣泛用於無人機的輕量級通訊協議。MAVProxy的主要功能包括：

1. 多路UDP輸出：MAVProxy能夠將接收到的MAVLink數據分流到多個UDP端口。這意味著它可以將從無人機接收的數據同時發送給多個客戶端，例如地面控制站、數據記錄工具或其他分析軟件。

2. 數據轉發和中繼：MAVProxy可以作為一個中繼站，接收來自無人機的MAVLink消息，然後轉發給其他系統或網絡。這對於遠程操作或在複雜網絡環境中工作的無人機特別有用。

3. 命令行界面：MAVProxy提供一個命令行界面，用於直接控制無人機和訪問飛行數據。這對於需要快速響應或自定義控制指令的用戶來說非常有用。

4. 擴展和模塊化：它支持通過模塊和插件進行擴展，使用者可以根據自己的需求添加新的功能或集成到更大的系統中。

5.跨平台兼容性：MAVProxy可以在多種操作系統上運行，包括Windows、Linux和macOS，這使它在不同的用戶和應用場景中具有很高的適應性。

MAVProxy是一個多功能的無人機通訊和控制工具，特別適合於需要高度自定義和靈活多變的通訊解決方案的專業用戶和開發者。

### windows 下使用 MavProxy
```
mavproxy --master=COM4 --out=127.0.0.1:14550 --out=127.0.0.1:14551
```

### ubuntu 下使用 mavproxy
```
python3 mavproxy.py --master=COM4 --out=127.0.0.1:14550 --out=127.0.0.1:14551
```
