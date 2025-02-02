
import pandas as pd

excel_file = r"C:\Users\admin\Desktop\大宰府プロジェクト\project\data\大宰府短歌・俳句前処理後データ.xlsx"


df = pd.read_excel(excel_file)


df = df[["句", "データ元", "年齢", "在住地"]]


json_file = "poems.json"
df.to_json(json_file, orient="records", force_ascii=False, indent=4)

print(f"データが {json_file} に変換されました！")