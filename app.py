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
                margin: 8mm;
            }}
            @media print {{
                html, body {{
                    width: 297mm;
                    height: 210mm;
                    margin: 0;
                    font-size: 11pt;
                    overflow: hidden;
                }}
                table {{
                    page-break-inside: avoid;
                }}
                tr {{
                    page-break-inside: avoid;
                }}
                .no-print {{
                    display: none;
                }}
            }}
            body {{
                font-family: "Microsoft JhengHei", Arial, sans-serif;
                margin: 10px;
                font-size: 12pt;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 10px;
            }}
            td, th {{
                border: 1px solid black;
                padding: 6px;
                vertical-align: middle;
                font-size: 110%;
            }}
            .section-title {{
                background-color: #f0f0f0;
                font-weight: bold;
                text-align: center;
                font-size: 180%;
            }}
            .unit-title {{
                font-weight: bold;
                text-align: center;
                font-size: 180%;
            }}
            .cell-content {{
                font-size: 120%;
                text-align: left;
            }}
            .double-height {{
                height: 80px;
            }}
            h1 {{
                text-align: center;
                font-size: 18pt;
                margin-bottom: 10px;
            }}
            button {{
                margin: 10px 0;
                padding: 8px 16px;
                background-color: #007BFF;
                color: white;
                border: none;
                font-size: 1.1rem;
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
        <h1 class="no-print">混凝土試體製作紀錄表</h1>
        <button class="no-print" onclick="printPage()">🖨️ 列印本頁</button>

        <!-- 表格一：基本資料 -->
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
            <tr><td class="section-title">結構部位</td><td colspan="3" class="cell-content">{data['結構部位']}</td></tr>
        </table>

        <!-- 表格二：試驗項目 -->
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

        <!-- 表格三：取樣資訊 -->
        <table>
            <tr>
                <td class="section-title">取樣日期</td>
                <td colspan="3" class="cell-content">{taiwan_date}</td>
            </tr>
            <tr class="double-height">
                <td class="section-title">取樣人員</td>
                <td colspan="3" class="cell-content"></td>
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
