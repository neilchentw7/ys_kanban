import streamlit as st
import tempfile
import base64

def generate_html(data):
    with open("logo.png", "rb") as img_file:
        logo_base64 = base64.b64encode(img_file.read()).decode()

    spec_text = "Φ=15cm＊H=30cm" if data['試體規格'] == "15x30" else "Φ=12cm＊H=24cm"

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
                .no-print {{ display: none; }}
            }}
            body {{
                font-family: "Microsoft JhengHei", Arial, sans-serif;
                margin: 0;
                font-size: 30pt;
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
                width: 25px;
                height: 25px;
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
                border: 4px solid black;
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
                font-size: 32pt;
            }}
            .unit-title {{
                font-weight: bold;
                font-size: 32pt;
            }}
            .cell-content {{
                font-size: 30pt;
            }}
            .align-right {{
                text-align: right;
                padding-right: 15px;
            }}
            .smaller-text {{
                font-size: 20pt;
            }}
            .item-title {{
                font-size: 32pt; /* 增大 6pt */
                height: 80px;     /* 兩行高度 */
                line-height: 1.2;
            }}
            .double-height {{
                height: 60px;
            }}
            .right-text {{
                float: right;
                font-size: 24pt;
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
            function printPage() {{ window.print(); }}
        </script>
    </head>
    <body>
        <div class="container">
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
                <tr><td class="section-title">結構<br>部位</td><td colspan="3" class="cell-content">&nbsp;</td></tr>
            </table>

            <!-- 試驗項目 -->
            <table>
                <tr>
                    <td class="section-title" rowspan="3">試驗<br>項目</td>
                    <td class="item-title">一、坍度</td>
                    <td class="cell-content">
                        <span class="right-text">(設計　　 ± 　　 公分)</span>
                    </td>
                </tr>
                <tr>
                    <td class="item-title">二、氯離子檢測值</td>
                    <td class="cell-content">
                        <span class="right-text">kg/m³</span>
                    </td>
                </tr>
                <tr>
                    <td class="item-title">三、圓柱試體製作</td>
                    <td class="cell-content">
                        <span class="smaller-text">{spec_text}</span> 數量　　　 個
                    </td>
                </tr>
            </table>

            <!-- 取樣資訊 -->
            <table>
                <tr>
                    <td class="section-title">取樣日期</td>
                    <td colspan="3" class="cell-content">民國　　　年　　　月　　　日</td>
                </tr>
                <tr class="double-height">
                    <td class="section-title">取樣<br>人員</td>
                    <td colspan="3" class="cell-content align-right">&nbsp;</td>
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
    with col2:
        承包廠商 = st.text_input("承包廠商")
        試體規格 = st.radio("圓柱試體規格", ["15x30", "12x24"], index=0)

    submitted = st.form_submit_button("產出網頁檔自行列印")

if submitted:
    data = {
        "工程名稱": 工程名稱,
        "業主": 業主,
        "監造單位": 監造單位,
        "承包廠商": 承包廠商,
        "設計強度": 設計強度,
        "試體規格": 試體規格
    }

    html_content = generate_html(data)

    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
    tmp_file.write(html_content.encode("utf-8"))
    tmp_file.close()

    with open(tmp_file.name, "rb") as f:
        st.download_button(
            label="📄 下載網頁檔自行列印",
            data=f,
            file_name="品管工地用白板.html",
            mime="text/html"
        )
