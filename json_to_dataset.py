import argparse
import json
import os
import os.path as osp
import warnings
 
import PIL.Image
import yaml
import numpy as np
 
from labelme import utils
import base64
 
def main():
    warnings.warn("This script is aimed to demonstrate how to convert the\n"
                  "JSON file to a single image dataset, and not to handle\n"
                  "multiple JSON files to generate a real-use dataset.")
    parser = argparse.ArgumentParser()
    parser.add_argument('json_file')
    parser.add_argument('-o', '--out', default=None)
    args = parser.parse_args()
 
    json_file = args.json_file
    if args.out is None:
        out_dir = osp.basename(json_file).replace('.', '_')
        out_dir = osp.join(osp.dirname(json_file), out_dir)
    else:
        out_dir = args.out
    if not osp.exists(out_dir):
        os.mkdir(out_dir)
 
    count = os.listdir(json_file) 
    for i in range(0, len(count)):
        path = os.path.join(json_file, count[i])
        if os.path.isfile(path) and path.endswith('.json'):
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if data['imageData']:
                imageData = data['imageData']
            else:
                imagePath = os.path.join(os.path.dirname(path), data['imagePath'])
                with open(imagePath, 'rb') as f:
                    imageData = f.read()
                    imageData = base64.b64encode(imageData).decode('utf-8')
            img = utils.img_b64_to_arr(imageData)
            label_name_to_value = {'_background_': 0}
            for shape in data['shapes']:
                label_name = shape['label']
                if label_name in label_name_to_value:
                    label_value = label_name_to_value[label_name]
                else:
                    label_value = len(label_name_to_value)
                    label_name_to_value[label_name] = label_value
            
            # label_values must be dense
            label_values, label_names = [], []
            for ln, lv in sorted(label_name_to_value.items(), key=lambda x: x[1]):
                label_values.append(lv)
                label_names.append(ln)
            assert label_values == list(range(len(label_values)))
            
            # 新版 labelme 的 shapes_to_label 返回 (cls_mask, ins_mask) 元组
            lbl_tuple = utils.shapes_to_label(img.shape, data['shapes'], label_name_to_value)
            if isinstance(lbl_tuple, tuple):
                lbl = lbl_tuple[0] # 获取 class mask
            else:
                lbl = lbl_tuple # 兼容旧版
            
            captions = ['{}: {}'.format(lv, ln)
                for ln, lv in label_name_to_value.items()]
            
            try:
                lbl_viz = utils.draw_label(lbl, img, captions)
            except AttributeError:
                # 新版的 labelme 把可视化功能转移到了 imgviz 库
                import imgviz
                try:
                    lbl_viz = imgviz.label2rgb(
                        label=lbl,
                        image=img,
                        label_names=label_names,
                        font_size=15,
                        loc="rb"
                    )
                except Exception:
                    lbl_viz = None # 容错，如果 imgviz 依然有问题，则不生成 viz 图
            
            file_out_dir = osp.basename(count[i]).replace('.', '_')
            file_out_dir = osp.join(out_dir, file_out_dir)
            if not osp.exists(file_out_dir):
                os.makedirs(file_out_dir, exist_ok=True)
 
            PIL.Image.fromarray(img).save(osp.join(file_out_dir, 'img.png'))
            try:
                utils.lblsave(osp.join(file_out_dir, 'label.png'), lbl.astype(np.uint8))
            except AttributeError:
                # 兼容部分新版 Labelme 移除了 lblsave 的情况
                lbl_pil = PIL.Image.fromarray(lbl.astype(np.uint8), mode='P')
                lbl_pil.save(osp.join(file_out_dir, 'label.png'))
            
            if lbl_viz is not None:
                PIL.Image.fromarray(lbl_viz).save(osp.join(file_out_dir, 'label_viz.png'))
 
            with open(osp.join(file_out_dir, 'label_names.txt'), 'w', encoding='utf-8') as f:
                for lbl_name in label_names:
                    f.write(lbl_name + '\n')
 
            warnings.warn('info.yaml is being replaced by label_names.txt')
            info = dict(label_names=label_names)
            with open(osp.join(file_out_dir, 'info.yaml'), 'w', encoding='utf-8') as f:
                yaml.safe_dump(info, f, default_flow_style=False)
 
            print('Saved to: %s' % file_out_dir)
if __name__ == '__main__':
    main()
