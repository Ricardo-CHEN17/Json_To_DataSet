import matplotlib
# 【关键修复】强制使用无界面后端 Agg，完美绕过 Qt 报错崩溃问题
matplotlib.use('Agg') 

from labelme import LabelFile
import numpy as np
import matplotlib.pyplot as plt
import os
import glob  # 【新增】引入 glob 库用于查找所有文件

# --- 颜色参数配置 (保持原样，未作任何改动) ---
LINE_COLOR = (0.5, 0, 0)   # 暗红色 (Matplotlib RGB 范围是 0~1)
OUTLINE_COLOR = 'black'
LINE_WIDTH = 1           # 线条粗细
NODE_RADIUS = 12           # 节点大小 (s参数)
# -------------------

# 【新增】创建 output 文件夹（如果不存在则自动创建）
os.makedirs("output", exist_ok=True)

# 【新增】获取当前目录下所有的 .json 文件
json_files = glob.glob("*.json")

if not json_files:
    print("❌ 当前目录下没有找到任何 .json 文件，请确认脚本与 json 放在同一文件夹。")
else:
    print(f"✅ 共发现 {len(json_files)} 个 .json 文件，开始批量处理...")

# 【新增】循环处理每一个 json 文件
for json_file in json_files:
    print(f"正在处理: {json_file} ...")

    # 1. 读取标注文件和原始图片
    lf = LabelFile()
    lf.load(json_file)
    img_path = os.path.join(os.path.dirname(json_file), lf.image_path)

    # 用 matplotlib 读入原始图像
    img = plt.imread(img_path)

    # 2. 创建画布并绘制
    height, width = img.shape[:2]
    # 你设定的 DPI 保留为 300
    dpi = 300  
    figsize = width / float(dpi), height / float(dpi)

    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    ax.imshow(img, cmap='gray')  # 展示底图

    # 关闭坐标轴和多余的白边
    ax.axis('off')
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

    # 3. 遍历标注文件进行绘制 (你的原始逻辑)
    for shape in lf.shapes:
        pts = np.array(shape['points'], dtype=np.int32)
        shape_type = shape['shape_type']

        # --- 画连线 ---
        if shape_type in ['linestrip', 'polygon']:
            x_vals = pts[:, 0]
            y_vals = pts[:, 1]
            
            if shape_type == 'polygon' and len(pts) > 2:
                x_vals = np.append(x_vals, x_vals[0])
                y_vals = np.append(y_vals, y_vals[0])
                
            ax.plot(x_vals, y_vals, 
                    color=LINE_COLOR, 
                    linewidth=LINE_WIDTH, 
                    antialiased=True, 
                    solid_capstyle='round')

        # --- 画顶点 ---
        if len(pts) > 0:
            ax.scatter(pts[:, 0], pts[:, 1], 
                       s=NODE_RADIUS, 
                       color=LINE_COLOR, 
                       zorder=10)

    # 4. 保存最终高清无损图
    # 【新增】使用与 json 文件相同的名称，保存到 output 文件夹中
    base_name = os.path.splitext(os.path.basename(json_file))[0]
    output_filename = os.path.join("output", f"{base_name}.png")
    
    plt.savefig(output_filename, format='png', bbox_inches='tight', pad_inches=0, dpi=dpi)
    plt.close() # 释放内存，为下一张图做准备

print("🎉 全部处理完成！请在 output 文件夹中查看生成的图片。")