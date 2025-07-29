import streamlit as st
import datetime
import tempfile

def generate_html(data):
    year = data['取樣日期'].year - 1911
    taiwan_date = f"民國 {year} 年 {data['取樣日期'].month} 月 {data['取樣日期'].day} 日"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>混凝土試體製作紀錄表</title>
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
                text-align: right;       /* ✅ 取樣人員右對齊 */
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
            <h1 class="no-print">混凝土試體製作紀錄表</h1>
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
                    </
