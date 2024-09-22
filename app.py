from flask import Flask, render_template, request,redirect,url_for
from datetime import datetime
from dateutil.relativedelta import relativedelta

app = Flask(__name__)



# requestsモジュールのインポート
import requests
today = datetime.now()
ttt=(today + relativedelta(months=3)).strftime('%Y-%m-%d')
to=today.strftime('%Y-%m-%d')
# 送信するメッセージを定義
linemsg = f'掃除が完了しました\n清掃した日\n{to}\n次回の掃除は\n{ttt}'
# LINE Notifyのアクセストークン
token = "KUoFqErn9zNS03j3WbKoQcdKkM6ixNeXk3AbLmO70Ru" # アクセストークンに置き換えてください

#LINEメッセージ送信の関数
def LINE_message(msg):
  # APIエンドポイントのURLを定義
  url = "https://notify-api.line.me/api/notify"
  # HTTPリクエストヘッダーの設定 
  headers = {"Authorization" : "Bearer "+ token}
  # 送信するメッセージの設定
  message =  (msg)
  # ペイロードの設定
  payload = {"message" :  message}
  # POSTリクエストの使用 
  r = requests.post(url, headers = headers, params=payload)

# 関数の呼び出し

@app.route('/', methods=['GET', 'POST'])
def checklist():
    if request.method == 'POST':
        # チェックボックスのすべての項目がチェックされているか確認
        checkboxes = request.form.getlist('check')  # 'check'はチェックボックスのname属性で取得されるリスト
        if len(checkboxes) == 4:  # すべての項目がチェックされている場合
            print("すべてのチェック項目が完了しました")
            return redirect(url_for('end'))

            
        else:
            print("チェック項目がすべて完了していません")
            return "チェック項目がすべて完了していません"

    return render_template('index.html')
@app.route('/end')
def end():
    LINE_message(linemsg)

# 3か月後の日付を計算
    three_months_later = today + relativedelta(months=3)

# 日付を表示
    print(three_months_later.strftime('%Y-%m-%d'))  # 例: 2024-12-22
    return render_template("end.html",date=three_months_later.strftime('%Y-%m-%d'))

if __name__ == '__main__':
    app.run(debug=True)
