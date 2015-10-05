CS = 30  # セルのサイズ
SCR_RECT = Rect(0, 0, CS*19, CS*19)  # スクリーンサイズ
NUM_ROW = SCR_RECT.height / CS   # フィールドの行数
NUM_COL = SCR_RECT.width / CS  # フィールドの列数
EMPTY, BLACK = 0, 1  # EMPTYとBLACKの定数
WHITE = 2 # WHITE(相手)の定数
