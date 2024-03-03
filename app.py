from flask import Flask, redirect, render_template, request, url_for
import requests
from businesses import businesses

app = Flask(__name__)
got_position = 'false'
center = {'x': 0, 'y': 0}

@app.route('/')
def home():
    return render_template("home.html", flag=got_position)

@app.route('/<lat>/<lng>')
def get_pos(lat, lng):
    global got_position
    got_position = 'true'
    center['x'] = lng
    center['y'] = lat
    return redirect(url_for('home'))

# 탄소중립포인트 설명
@app.route('/cpoints')
def cpoints():
    return render_template("cpoints.html")

# 탄소중립포인트 제도 참여 기업 정보
# 리스트에서 기업 이름을 클릭하면 /businessInfo/<name> 으로 redirect
@app.route('/businessInfo')
def business_list():
    return render_template("business_list.html", businesses=businesses)

# 선택한 기업 정보
# Gps를 이용한 사용자의 현재 위치 확인 후 기업 이름으로 지도 검색
# 해당 기업에서 실천할 수 있는 행동에 관한 정보
@app.route('/businessInfo/<name>')
def business_info(name):
    info = businesses[name]
    places = search_place(name, x=center['x'], y=center['y']) # x y 값을 gps로 받아와야 함. 현재는 이마트 기준

    return render_template("business_info.html", info=info, places=places, center=center, name=name)

# 카카오맵을 이용한 키워드 검색
# 최대 15개 항목 검색, 중심 기준 3km 반경
def search_place(name, x, y):
    searching = name
    url = 'https://dapi.kakao.com/v2/local/search/keyword.json?query={}&x={}&y={}&radius=3000&size=15'\
        .format(searching, x, y)

    headers = {
        "Authorization": f"KakaoAK {REST_API_KEY}"
    }
    places = requests.get(url, headers=headers).json()['documents']
    print(places)
    return places

if __name__ == '__main__':
    app.run(debug=True)

