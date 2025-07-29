import streamlit as st
import datetime
import tempfile
import base64

def generate_html(data):
    # 將 logo.png 轉為 Base64
    with open("logo.png", "rb") as img_file:
        logo_base64 = base64.b64encode(img_file.read()).decode()

    year = data['取樣日期'].year - 1911
    taiwan_date = f"民國 {year} 年 {data['取樣日期'].month} 月 {data['取樣日期'].day} 日"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>品管工地用白板</title>
        <style>
            @page {{
                size: A4 landscape;
                margin: 5mm;
            }}
            @media print {{
                html, body {{
                    width: 100%;
                    height: 100%;
                    margin: 0;
                    font-size: 30pt;
                    display: block;
                    zoom: 90%;
                    overflow: hidden;
                }}
                .no-print {{
                    display: none;
                }}
            }}
            body {{
                font-family: "Microsoft JhengHei", Arial, sans-serif;
                margin: 0;
                font-size: 30pt;
                display: block;
                text-align: center;
            }}
            .container {{
                width: 100%;
                margin: 0 auto;
            }}
            .header {{
                display: flex;
                align-items: center;
                justify-content: center;
                margin-bottom: 10px;
            }}
            .header img {{
                width: 20px;
                height: 20px;
                margin-right: 8px;
            }}
            .header span {{
                font-size: 20pt;
                font-weight: bold;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 3px;
                border: 2px solid black;
            }}
            td, th {{
                border: 2px solid black;
                padding: 2px;
                vertical-align: middle;
                font-size: 30pt;
                text-align: center;
            }}
            .section-title {{
                background-color: #f0f0f0;
                font-weight: bold;
                text-align: center;
                font-size: 32pt;
            }}
            .unit-title {{
                font-weight: bold;
                text-align: center;
                font-size: 32pt;
            }}
            .cell-content {{
                font-size: 30pt;
                text-align: center;
            }}
            .align-right {{
                text-align: right;
                padding-right: 15px;
            }}
            .smaller-text {{
                font-size: 20pt;
            }}
            .item-title {{
                font-size: 26pt;
            }}
            .double-height {{
                height: 60px;
            }}
            h1 {{
                text-align: center;
                font-size: 32pt;
                margin: 4px 0;
            }}
            button {{
                margin: 5px 0;
                padding: 5px 10px;
                background-color: #007BFF;
                color: white;
                border: none;
                font-size: 1rem;
                border-radius: 4px;
                cursor: pointer;
            }}
        </style>
        <script>
            function printPage() {{
                window.print();
            }}
        </script>
    </head>
    <body>
        <div class="container">
            <!-- Logo + 公司名稱 -->
            <div class="header">
                <img src="data:image/png;base64,{logo_base64}" alt="Logo">
                <span>禹盛混凝土有限公司</span>
            </div>

            <h1 class="no-print">品管工地用白板列印</h1>
            <button class="no-print" onclick="printPage()">🖨️ 列印本頁</button>

            <!-- 基本資料 -->
            <table>
                <tr><td class="section-title">工程名稱</td><td colspan="3" class="cell-content">{data['工程名稱']}</td></tr>
                <tr><td class="section-title">業 主</td><td colspan="3" class="cell-content">{data['業主']}</td></tr>
                <tr><td class="section-title">監造單位</td><td colspan="3" class="cell-content">{data['監造單位']}</td></tr>
                <tr><td class="section-title">承包廠商</td><td colspan="3" class="cell-content">{data['承包廠商']}</td></tr>
                <tr>
                    <td class="section-title">設計強度</td>
                    <td class="cell-content">{data['設計強度']}</td>
                    <td class="unit-title">kgf/cm²</td>
                    <td></td>
                </tr>
                <tr><td class="section-title">結構<br>部位</td><td colspan="3" class="cell-content">{data['結構部位']}</td></tr>
            </table>

            <!-- 試驗項目 -->
            <table>
                <tr>
                    <td class="section-title" rowspan="3">試驗<br>項目</td>
                    <td class="item-title">一、坍度</td>
                    <td class="cell-content">
                        實測 {data['坍度實測']} 公分 
                        <span class="smaller-text">(設計 {data['設計坍度']} ± {data['容許範圍']:.2f} 公分)</span>
                    </td>
                </tr>
                <tr>
                    <td class="item-title">二、氯離子檢測值</td>
                    <td class="cell-content">
                        實測 {data['氣離子']} kg/M³ 
                        <span class="smaller-text">(規範值 0.15 kg/M³)</span>
                    </td>
                </tr>
                <tr>
                    <td class="item-title">三、圓柱試體製作</td>
                    <td class="cell-content">
                        <span class="smaller-text">Φ=15cm＊H=30cm</span> 數量 {data['圓柱個數']} 個
                    </td>
                </tr>
            </table>

            <!-- 取樣資訊 -->
            <table>
                <tr>
                    <td class="section-title">取樣日期</td>
                    <td colspan="3" class="cell-content">{taiwan_date}</td>
                </tr>
                <tr class="double-height">
                    <td class="section-title">取樣<br>人員</td>
                    <td colspan="3" class="cell-content align-right">{data['取樣人員']}</td>
                </tr>
            </table>
        </div>
    </body>
    </html>
    """
    return html


# --- Streamlit UI ---
st.title("品管工地用白板列印")

with st.form("input_form"):
    col1, col2 = st.columns(2)
    with col1:
        工程名稱 = st.text_input("工程名稱")
        業主 = st.text_input("業主")
        監造單位 = st.text_input("監造單位")
        設計強度 = st.text_input("設計強度 (kgf/cm²)")
        設計坍度 = st.number_input("設計坍度值 (cm)", value=18.0)
    with col2:
        承包廠商 = st.text_input("承包廠商")
        結構部位 = st.text_input("結構部位")
        氣離子 = st.text_input("氯離子檢測值 (kg/m³)")
        圓柱個數 = st.number_input("圓柱試體製作數量", min_value=1, value=3)
        容許範圍 = st.number_input("坍度允許誤差 ± (cm)", value=2.0, format="%.2f")

    坍度實測 = st.text_input("實測坍度值 (公分)")
    取樣日期 = st.date_input("取樣日期", value=datetime.date.today())
    取樣人員 = st.text_input("取樣人員")

    submitted = st.form_submit_button("產出 HTML")

if submitted:
    data = {
        "工程名稱": 工程名稱,
        "業主": 業主,
        "監造單位": 監造單位,
        "承包廠商": 承包廠商,
        "設計強度": 設計強度,
        "結構部位": 結構部位,
        "取樣日期": 取樣日期,
        "設計坍度": 設計坍度,
        "容許範圍": 容許範圍,
        "坍度實測": 坍度實測,
        "氣離子": 氣離子,
        "圓柱個數": 圓柱個數,
        "取樣人員": 取樣人員
    }

    html_content = generate_html(data)

    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
    tmp_file.write(html_content.encode("utf-8"))
    tmp_file.close()

    with open(tmp_file.name, "rb") as f:
        st.download_button(
            label="📄 下載 HTML 網頁檔",
            data=f,
            file_name="試體紀錄表.html",
            mime="text/html"
        )
