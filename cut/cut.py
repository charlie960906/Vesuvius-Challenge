import tifffile as tf
import cv2
import os

# 定義輸入和輸出資料夾
input_folder = r'C:\Users\charl\Desktop\science\layer'  # 替換為實際的輸入資料夾路徑
output_folder = r'C:\Users\charl\Desktop\science\vesuvius_challenge\cut\output'  # 替換為實際的輸出資料夾路徑

# 確保輸出資料夾存在，若不存在則創建
os.makedirs(output_folder, exist_ok=True)

# 獲取輸入資料夾中的所有 TIFF 和 PNG 檔案
input_files = [f for f in os.listdir(input_folder) if f.endswith('.tif') or f.endswith('.png')]

# 定義裁剪區域的尺寸
crop_width, crop_height = 1500, 1000  # 替換為實際的裁剪區域尺寸

# 迴圈處理每個輸入檔案
for input_file in input_files:
    input_path = os.path.join(input_folder, input_file)
    
    if input_file.endswith('.tif'):
        with tf.TiffFile(input_path) as tif:
            pages = tif.pages
            page = pages[0]  # 選擇要裁剪的特定頁面（如果只有一頁，可以直接選取）
            image_data = page.asarray()
    elif input_file.endswith('.png'):
        image_data = cv2.imread(input_path)
        if image_data is None:
            print(f"Failed to read {input_file}")
            continue
    
    height, width = image_data.shape[:2]
    
    # 計算橫向和縱向的裁剪區域數量
    num_crops_x = width // crop_width
    num_crops_y = height // crop_height
    
    # 迴圈裁剪影像
    for i in range(num_crops_y):
        for j in range(num_crops_x):
            x0 = j * crop_width
            y0 = i * crop_height
            x1 = x0 + crop_width
            y1 = y0 + crop_height
            
            cropped_data = image_data[y0:y1, x0:x1]
            
            # 檢查裁剪後的資料是否為空
            if cropped_data.size == 0:
                print(f"Cropped data is empty for {input_file} at ({i}, {j})")
                continue
            
            # 創建輸出資料夾
            output_subfolder = os.path.join(output_folder, f"part_{i}_{j}")
            os.makedirs(output_subfolder, exist_ok=True)
            
            # 創建輸出檔案名稱
            output_file = os.path.splitext(input_file)[0]+os.path.splitext(input_file)[1]
            output_path = os.path.join(output_subfolder, output_file)
            
            # 儲存裁剪後的影像
            cv2.imwrite(output_path, cropped_data)

print("所有檔案的裁剪已完成。")
