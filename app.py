import streamlit as st
import datetime
import tempfile

def generate_html(data):
    year = data['取樣日期'].year - 1911
    taiwan_date = f"{year} 年 {data['取樣日期'].month} 月 {data['取樣日期'].day} 日"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>混凝土試體製作紀錄表</title>
        <style>
            @page {{
                size: A4 landscape;
                margin: 10mm;
            }}
            @media print {{
                html, body {{
                    width: 297mm;
                    height: 210mm;
                    margin: 5mm;
                    transform: scale(0.9);
                    transform-origin: top left;
                    overflow: hidden;
                }}
                table {{
                    page-break-inside: avoid;
                }}
                .no-print {{
                    display: none;
                }}
            }}
            body {{
                font-family: "Microsoft JhengHei", Arial, sans-serif;
                margin: 20px;
                font-size: 1.4rem;
                line-height: 1.4;
            }}
            h1 {{
                text-align: center;
                font-size: 1.8rem;
                margin-bottom: 10px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                border: 1px solid black;
                margin-bottom: 16px;
            }}
            td, th {{
                border: 1px solid black;
                padding: 8px;
                vertical-align: middle;
            }}
            .section-title {{
                width: 20%;
                font-weight: bold;
                background-color: #f0f0f0;
                font-size: 200%;
                text-align: center;
                white-space: nowrap;
            }}
            .cell-content {{
                font-size: 150%;
                text-align: left;
            }}
            .double-height {{
                height: 100px;
            }}
            button {{
                margin: 10px 0;
                padding: 8px 16px;
                background-color: #007BFF;
                color: white;
                border: none;
                cursor: pointer;
                font-size: 1.2rem;
                border-radius: 4px;
            }}
            button:hover {{
                background-color: #0056b3;
            }}
        </style>
        <script>
            function printPage() {{
                window.print();
            }}
        </script>
    </head>
    <body>
        <h1 class="no-print">混凝土試體製作紀錄表</h1>
        <button class="no-print" onclick="printPage()">🖨️ 列印本頁</button>

        <!-- 頂部基本資料 -->
        <table>
            <tr><td class="section-title">工程名稱</td><td colspan="3" class="cell-content">{data['工程名稱']}</td></tr>
            <tr><td class="section-title">業　主</td><td colspan="3" class="cell-content">{data['業主']}</td></tr>
            <tr><td class="section-title">監造單位</td><td colspan="3" class="cell-content">{data['監造單位']}</td></tr>
            <tr><td class="section-title">承包廠商</td><td colspan="3" class="cell-content">{data['承包廠商']}</td></tr>
            <tr>
                <td class="section-title">設計強度</td>
                <td class="cell-content">{data['設計強度']}</td>
                <td class="section-title">kgf/cm²</td>
                <td></td>
            </tr>
            <tr><td class="section-title">結構部位</td><td colspan="3" class="cell-content">{data['結構部位']}</td></tr>
        </table>

        <!-- 取樣日期 -->
        <table>
            <tr>
                <td class="section-title">取樣日期</td>
                <td colspan="3" class="cell-content">{taiwan_date}</td>
            </tr>
        </table>

        <!-- 試驗項目 -->
        <table>
            <tr>
                <td class="section-title" rowspan="3">試驗項目</td>
                <td class="cell-content">一、坍度</td>
                <td class="cell-content">公分</td>
                <td class="cell-content">設計坍度 {data['設計坍度']} ± {data['容許範圍']} 公分</td>
            </tr>
            <tr>
                <td class="cell-content">二、氣離子檢測值</td>
                <td class="cell-content">kg/M³</td>
                <td class="cell-content">規範值 0.15kg/M³</td>
            </tr>
            <tr>
                <td class="cell-content">三、圓柱試體製作</td>
                <td class="cell-content">Φ=15cm＊H=30cm</td>
                <td class="cell-content">{data['圓柱個數']} 個</td>
            </tr>
        </table>

        <!-- 取樣人員 -->
        <table>
            <tr class="double-height">
                <td class="section-title">取樣人員</td>
                <td colspan="3"></td>
            </tr>
        </table>
    </body>
    </html>
    """
    return html

# --- Streamlit UI ---
st.title("混凝土試體填報系統（產出網頁版 HTML）")

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
        氣離子 = st.text_input("氣離子檢測值 (kg/m³)")
        圓柱個數 = st.number_input("圓柱試體製作數量", min_value=1, value=3)
        容許範圍 = st.number_input("坍度允許誤差 ± (cm)", value=2.0)

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
