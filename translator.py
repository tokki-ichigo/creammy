import json
import os
import sys

# 尝试导入模糊匹配库，如果没有安装则报错提醒
try:
    from rapidfuzz import process, fuzz
except ImportError:
    print("错误：未找到 rapidfuzz 库。请在终端运行 'pip3 install rapidfuzz' 后再执行程序。")
    sys.exit()

class BrandSystem:
    def __init__(self, json_path):
        # 获取当前脚本所在文件夹的绝对路径，解决 Mac/IDLE 找不到文件的问题
        base_path = os.path.dirname(os.path.abspath(__file__))
        self.json_path = os.path.join(base_path, json_path)
        self.brands = self.load_data()

    def load_data(self):
        """加载本地 JSON 词库"""
        if os.path.exists(self.json_path):
            try:
                with open(self.json_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"读取 JSON 失败: {e}")
                return {}
        else:
            print(f"提示：未找到词库文件 {self.json_path}，将开启空词库。")
            return {}

    def translate(self, text):
        """查找逻辑"""
        if not self.brands:
            return None, 0
            
        # 1. 精确匹配
        if text in self.brands:
            return self.brands[text], 100
        
        # 2. 模糊匹配
        choices = list(self.brands.keys())
        result = process.extractOne(text, choices, scorer=fuzz.WRatio)
        
        if result:
            match_name, score, _ = result
            if score > 60:
                return self.brands[match_name], score
        
        return None, 0

# --- 程序入口 ---
if __name__ == "__main__":
    # 初始化，传入文件名
    translator = BrandSystem('brands.json')
    
    print("="*30)
    print("  日语品牌名 -> 英语名转换系统")
    print("  (输入 'q' 键退出程序)")
    print("="*30)
    
    while True:
        user_input = input("\n请输入日语品牌名 (如 シャネル): ").strip()
        
        if user_input.lower() == 'q':
            print("程序已退出。")
            break
            
        if not user_input:
            continue
            
        english_name, confidence = translator.translate(user_input)
        
        if confidence == 100:
            print(f"✨ 准确匹配: {english_name}")
        elif confidence > 60:
            print(f"🤔 你是不是在找: {english_name}? (相似度: {confidence:.0f}%)")
        else:
            print("❌ 抱歉，词库中暂无该品牌记录。")
