"""
需要分析的点
1、总人口
2、男女人口比例
3、人口城镇化
4、人口增长率
5、人口老化（抚养比）

获取详细教程、获取代码帮助、提出意见建议
关注微信公众号「裸睡的猪」与猪哥联系

@Author  :   猪哥

"""
import numpy as np
import pandas as pd
import pyecharts.options as opts
from pyecharts.charts import Line, Bar, Page, Pie
from pyecharts.commons.utils import JsCode

# 人口数量excel文件保存路径
POPULATION_EXCEL_PATH = 'population.xlsx'

# 读取标准数据
DF_STANDARD = pd.read_excel(POPULATION_EXCEL_PATH)
# 自定义pyecharts图形背景颜色js
background_color_js = (
    "new echarts.graphic.LinearGradient(0, 0, 0, 1, "
    "[{offset: 0, color: '#c86589'}, {offset: 1, color: '#06a7ff'}], false)"
)
# 自定义pyecharts图像区域颜色js
area_color_js = (
    "new echarts.graphic.LinearGradient(0, 0, 0, 1, "
    "[{offset: 0, color: '#eb64fb'}, {offset: 1, color: '#3fbbff0d'}], false)"
)


def analysis_total():
    """
    分析总人口
    """
    # 1、分析总人口，画人口曲线图
    # 1.1 处理数据
    x_data = DF_STANDARD['年份']
    # 将人口单位转换为亿
    y_data = DF_STANDARD['年末总人口(万人)'].map(lambda x: "%.2f" % (x / 10000))
    # 1.2 自定义曲线图
    line = (
        Line(init_opts=opts.InitOpts(bg_color=JsCode(background_color_js)))
            .add_xaxis(xaxis_data=x_data)
            .add_yaxis(
            series_name="总人口",
            y_axis=y_data,
            is_smooth=True,
            is_symbol_show=True,
            symbol="circle",
            symbol_size=5,
            linestyle_opts=opts.LineStyleOpts(color="#fff"),
            label_opts=opts.LabelOpts(is_show=False, position="top", color="white"),
            itemstyle_opts=opts.ItemStyleOpts(
                color="red", border_color="#fff", border_width=1
            ),
            tooltip_opts=opts.TooltipOpts(is_show=False),
            areastyle_opts=opts.AreaStyleOpts(color=JsCode(area_color_js), opacity=1),
            # 标出4个关键点的数据
            markpoint_opts=opts.MarkPointOpts(
                data=[opts.MarkPointItem(name="新中国成立（1949年）", coord=[0, y_data[0]], value=y_data[0]),
                      opts.MarkPointItem(name="计划生育（1980年）", coord=[31, y_data[31]], value=y_data[31]),
                      opts.MarkPointItem(name="放开二胎（2016年）", coord=[67, y_data[67]], value=y_data[67]),
                      opts.MarkPointItem(name="2019年", coord=[70, y_data[70]], value=y_data[70])
                      ]
            ),
            # markline_opts 可以画直线
            # markline_opts=opts.MarkLineOpts(
            #     data=[[opts.MarkLineItem(coord=[39, y_data[39]]),
            #            opts.MarkLineItem(coord=[19, y_data[19]])],
            #           [opts.MarkLineItem(coord=[70, y_data[70]]),
            #            opts.MarkLineItem(coord=[39, y_data[39]])]],
            #     linestyle_opts=opts.LineStyleOpts(color="red")
            # ),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(
                title="新中国70年人口变化(亿人)",
                pos_bottom="5%",
                pos_left="center",
                title_textstyle_opts=opts.TextStyleOpts(color="#fff", font_size=16),
            ),
            # x轴相关的选项设置
            xaxis_opts=opts.AxisOpts(
                type_="category",
                boundary_gap=False,
                axislabel_opts=opts.LabelOpts(margin=30, color="#ffffff63"),
                axisline_opts=opts.AxisLineOpts(is_show=False),
                axistick_opts=opts.AxisTickOpts(
                    is_show=True,
                    length=25,
                    linestyle_opts=opts.LineStyleOpts(color="#ffffff1f"),
                ),
                splitline_opts=opts.SplitLineOpts(
                    is_show=False, linestyle_opts=opts.LineStyleOpts(color="#ffffff1f")
                ),
            ),
            # y轴相关选项设置
            yaxis_opts=opts.AxisOpts(
                type_="value",
                position="left",
                axislabel_opts=opts.LabelOpts(margin=20, color="#ffffff63"),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(width=0, color="#ffffff1f")
                ),
                axistick_opts=opts.AxisTickOpts(
                    is_show=True,
                    length=15,
                    linestyle_opts=opts.LineStyleOpts(color="#ffffff1f"),
                ),
                splitline_opts=opts.SplitLineOpts(
                    is_show=False, linestyle_opts=opts.LineStyleOpts(color="#ffffff1f")
                ),
            ),
            # 图例配置项相关设置
            legend_opts=opts.LegendOpts(is_show=False),
        )
    )
    # 2、分析计划生育执行前后增长人口
    # 2.1 数据处理
    total_1949 = DF_STANDARD[DF_STANDARD['年份'] == 1949]['年末总人口(万人)'].values
    total_1979 = DF_STANDARD[DF_STANDARD['年份'] == 1979]['年末总人口(万人)'].values
    total_2010 = DF_STANDARD[DF_STANDARD['年份'] == 2010]['年末总人口(万人)'].values
    increase_1949_1979 = '%.2f' % (int(total_1979 - total_1949) / 10000)
    increase_1979_2010 = '%.2f' % (int(total_2010 - total_1979) / 10000)
    # 2.2 画柱状图
    bar = (
        Bar(init_opts=opts.InitOpts(bg_color=JsCode(background_color_js)))
            .add_xaxis([''])
            .add_yaxis("前31年：1949-1979", [increase_1949_1979], color=JsCode(area_color_js),
                       label_opts=opts.LabelOpts(color='white', font_size=16))
            .add_yaxis("后31年：1980-2010", [increase_1979_2010], color=JsCode(area_color_js),
                       label_opts=opts.LabelOpts(color='white', font_size=16))
            .set_global_opts(
            title_opts=opts.TitleOpts(
                title="计划生育执行前31年（1949-1979）与后31年（1980-2010）增加人口总数比较（亿人）",
                pos_bottom="5%",
                pos_left="center",
                title_textstyle_opts=opts.TextStyleOpts(color="#fff", font_size=16)
            ),
            xaxis_opts=opts.AxisOpts(
                # 隐藏x轴的坐标线
                axisline_opts=opts.AxisLineOpts(is_show=False),
            ),
            yaxis_opts=opts.AxisOpts(
                # y轴坐标数值
                axislabel_opts=opts.LabelOpts(margin=20, color="#ffffff63"),
                # y 轴 轴线
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(width=0, color="#ffffff1f")
                ),
                # y轴刻度横线
                axistick_opts=opts.AxisTickOpts(
                    is_show=True,
                    length=15,
                    linestyle_opts=opts.LineStyleOpts(color="#ffffff1f"),
                ),
            ),
            legend_opts=opts.LegendOpts(is_show=False)
        )
    )
    # 3、渲染图像，将多个图像显示在一个html中
    # DraggablePageLayout表示可拖拽
    page = Page(layout=Page.DraggablePageLayout)
    page.add(line)
    page.add(bar)
    page.render('population_total.html')


def analysis_sex():
    """
    分析男女比
    """
    # 年份
    x_data_year = DF_STANDARD['年份']
    # 1、2019年男女比饼图
    sex_2019 = DF_STANDARD[DF_STANDARD['年份'] == 2019][['男性人口(万人)', '女性人口(万人)']]
    pie = (
        Pie()
            .add("", [list(z) for z in zip(['男', '女'], np.ravel(sex_2019.values))])
            .set_global_opts(title_opts=opts.TitleOpts(title="2019中国男女比", pos_bottom="bottom", pos_left="center"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
    )
    # 2、历年男性占总人数比曲线
    # （男性数/总数）x 100 ，然后保留两位小数
    man_percent = (DF_STANDARD['男性人口(万人)'] / DF_STANDARD['年末总人口(万人)']).map(lambda x: "%.2f" % (x * 100))
    line1 = (
        Line()
            .add_xaxis(x_data_year)
            .add_yaxis(
            series_name="男性占总人口比",
            y_axis=man_percent.values,
            # 标出关键点的数据
            markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="min"), opts.MarkPointItem(type_="max")]),
            # 画出平均线
            markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")])
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="中国70年(1949-2019)男性占总人数比", pos_left="center", pos_top="bottom"),
            xaxis_opts=opts.AxisOpts(type_="category"),
            # y轴显示百分比，并设置最小值和最大值
            yaxis_opts=opts.AxisOpts(type_="value", max_=52, min_=50,
                                     axislabel_opts=opts.LabelOpts(formatter='{value} %')),
            legend_opts=opts.LegendOpts(is_show=False),
        )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    )

    # 3、男女折线图
    # 历年男性人口数
    y_data_man = DF_STANDARD['男性人口(万人)']
    # 历年女性人口数
    y_data_woman = DF_STANDARD['女性人口(万人)']
    line2 = (
        Line()
            .add_xaxis(x_data_year)
            .add_yaxis("女性", y_data_woman)
            .add_yaxis("男性", y_data_man)
            .set_global_opts(
            title_opts=opts.TitleOpts(title="中国70年(1949-2019)男女人口数(万人)", pos_left="center", pos_top="bottom"),
            xaxis_opts=opts.AxisOpts(type_="category"),
        )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    )
    # 4、男女人口差异图
    # 两列相减，获得新列
    y_data_man_woman = DF_STANDARD['男性人口(万人)'] - DF_STANDARD['女性人口(万人)']
    line3 = (
        Line()
            .add_xaxis(x_data_year)
            .add_yaxis(
            series_name="男女差值",
            y_axis=y_data_man_woman.values,
            # 标出关键点的数据
            markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="min"), opts.MarkPointItem(type_="max"),
                                                    opts.MarkPointItem(type_="average")]),
            markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")])
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="中国70年(1949-2019)男女差值（万人）", pos_left="center", pos_top="bottom"),
            xaxis_opts=opts.AxisOpts(type_="category"),
            legend_opts=opts.LegendOpts(is_show=False),
        )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    )

    # 5、渲染图像，将多个图像显示在一个html中
    page = Page(layout=Page.DraggablePageLayout)
    page.add(pie)
    page.add(line1)
    page.add(line2)
    page.add(line3)
    page.render('population_sex.html')


def analysis_urbanization():
    """
    分析我国人口城镇化
    """
    # 年份
    x_data_year = DF_STANDARD['年份']
    # 2019年我国人口城镇化
    urbanization_2019 = DF_STANDARD[DF_STANDARD['年份'] == 2019][['城镇人口(万人)', '乡村人口(万人)']]
    pie = (
        Pie()
            .add("", [list(z) for z in zip(['城镇人口', '乡村人口'], np.ravel(urbanization_2019.values))])
            .set_global_opts(title_opts=opts.TitleOpts(title="2019中国城镇化比例", pos_bottom="bottom", pos_left="center", ),
                             legend_opts=opts.LegendOpts(is_show=False))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))

    )
    # 2、城镇化比例曲线
    y_data_city = DF_STANDARD['城镇人口(万人)'] / 10000
    y_data_countryside = DF_STANDARD['乡村人口(万人)'] / 10000
    line1 = (
        Line()
            .add_xaxis(x_data_year)
            .add_yaxis("城镇人口", y_data_city)
            .add_yaxis(series_name="乡村人口", y_axis=y_data_countryside,
                       # 标记线
                       markline_opts=opts.MarkLineOpts(
                           # 去除标记线的箭头
                           symbol='none',
                           label_opts=opts.LabelOpts(font_size=16),
                           data=[[opts.MarkLineItem(coord=[46, 0]),
                                  opts.MarkLineItem(name='1995', coord=[46, y_data_countryside[46]])],
                                 [opts.MarkLineItem(coord=[61, 0]),
                                  opts.MarkLineItem(name='2010', coord=[61, y_data_countryside[61]])]],
                           # opacity不透明度 0 - 1
                           linestyle_opts=opts.LineStyleOpts(color="red", opacity=0.3)
                       ),
                       # 标出关键点的数据
                       markpoint_opts=opts.MarkPointOpts(
                           data=[opts.MarkPointItem(name="1995年", coord=[46, y_data_countryside[46]],
                                                    value="%.2f" % (y_data_countryside[46])),
                                 opts.MarkPointItem(name="2010年", coord=[61, y_data_countryside[61]],
                                                    value="%.2f" % (y_data_countryside[61]))]
                       )
                       )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="中国70年(1949-2019)城乡人口曲线（亿人）", pos_left="center", pos_top="bottom"),
            xaxis_opts=opts.AxisOpts(type_="category")
        )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    )

    # 3、城镇化曲线
    y_data_urbanization = (DF_STANDARD['城镇人口(万人)'] / DF_STANDARD['年末总人口(万人)']).map(lambda x: "%.2f" % (x * 100))
    line2 = (
        Line()
            .add_xaxis(x_data_year)
            .add_yaxis(
            series_name="中国人口城镇化比例曲线",
            y_axis=y_data_urbanization.values,
            markline_opts=opts.MarkLineOpts(symbol='none', data=[opts.MarkLineItem(y=30), opts.MarkLineItem(y=70)])
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="中国(1949-2019)人口城镇化比例曲线", pos_left="center", pos_top="bottom"),
            xaxis_opts=opts.AxisOpts(type_="category"),
            # y轴显示百分比，并设置最小值和最大值
            yaxis_opts=opts.AxisOpts(type_="value", max_=100, min_=10,
                                     axislabel_opts=opts.LabelOpts(formatter='{value} %')),
            legend_opts=opts.LegendOpts(is_show=False),
        )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    )

    # 4、渲染图像，将多个图像显示在一个html中
    page = Page(layout=Page.DraggablePageLayout)
    page.add(pie)
    page.add(line1)
    page.add(line2)
    page.render('population_urbanization.html')


def analysis_growth():
    """
    分析人口增长率
    """
    # 1、三条曲线
    x_data_year = DF_STANDARD['年份']
    y_data_birth = DF_STANDARD['人口出生率(‰)']
    y_data_death = DF_STANDARD['人口死亡率(‰)']
    y_data_growth = DF_STANDARD['人口自然增长率(‰)']
    line1 = (
        Line()
            .add_xaxis(x_data_year)
            .add_yaxis("人口出生率", y_data_birth)
            .add_yaxis("人口死亡率", y_data_death)
            .add_yaxis("人口自然增长率", y_data_growth)
            .set_global_opts(
            # y轴显示百分比，并设置最小值和最大值
            yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter='{value} ‰')),
            title_opts=opts.TitleOpts(title="中国70年(1949-2019)出生率、死亡率及增长率变化", subtitle="1949-2019年，单位：‰",
                                      pos_left="center",
                                      pos_top="bottom"),
            xaxis_opts=opts.AxisOpts(type_="category"),
        )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    )
    # 2、渲染图像，将两个图像显示在一个html中
    page = Page(layout=Page.DraggablePageLayout)
    page.add(line1)
    page.render('analysis_growth.html')


def analysis_age():
    """
    分析年龄结构
    """
    new_df = DF_STANDARD[DF_STANDARD['0-14岁人口(万人)'] != 0][['年份', '0-14岁人口(万人)', '15-64岁人口(万人)', '65岁及以上人口(万人)']]
    x_data_year = new_df['年份']
    y_data_age_14 = new_df['0-14岁人口(万人)']
    y_data_age_15_64 = new_df['15-64岁人口(万人)']
    y_data_age_65 = new_df['65岁及以上人口(万人)']
    line1 = (
        Line()
            .add_xaxis(x_data_year)
            .add_yaxis("0-14岁人口", y_data_age_14)
            .add_yaxis("15-64", y_data_age_15_64)
            .add_yaxis("65岁及以上人口", y_data_age_65)
            .set_global_opts(
            # y轴显示百分比，并设置最小值和最大值
            yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter='{value}万')),
            title_opts=opts.TitleOpts(title="中国人口年龄结构变化图（万人）",
                                      pos_left="center",
                                      pos_top="bottom"),
            xaxis_opts=opts.AxisOpts(type_="category"),
        )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    )
    # 2、1982年龄结构与2019年龄结构
    age_1982 = DF_STANDARD[DF_STANDARD['年份'] == 1982][['0-14岁人口(万人)', '15-64岁人口(万人)', '65岁及以上人口(万人)']]
    age_2019 = DF_STANDARD[DF_STANDARD['年份'] == 2019][['0-14岁人口(万人)', '15-64岁人口(万人)', '65岁及以上人口(万人)']]

    pie = (
        Pie()
            .add(
            "1982",
            [list(z) for z in zip(['0-14', '15-64', '65'], np.ravel(age_1982.values))],
            center=["20%", "50%"],
            radius=[60, 80],
        )
            .add(
            "2019",
            [list(z) for z in zip(['0-14', '15-64', '65'], np.ravel(age_2019.values))],
            center=["55%", "50%"],
            radius=[60, 80],
        )
            .set_series_opts(label_opts=opts.LabelOpts(position="top", formatter="{b}: {d}%"))
            .set_global_opts(
            title_opts=opts.TitleOpts(title="中国1982、2019年年龄结构对比图", pos_left="center",
                                      pos_top="bottom"),
            legend_opts=opts.LegendOpts(
                type_="scroll", pos_top="20%", pos_left="80%", orient="vertical"
            ),
        )
    )
    # 3、抚养比曲线
    new_df = DF_STANDARD[DF_STANDARD['总抚养比(%)'] != 0][['年份', '总抚养比(%)', '少儿抚养比(%)', '老年抚养比(%)']]
    x_data_year2 = new_df['年份']
    y_data_all = new_df['总抚养比(%)']
    y_data_new = new_df['少儿抚养比(%)']
    y_data_old = new_df['老年抚养比(%)']
    line2 = (
        Line()
            .add_xaxis(x_data_year2)
            .add_yaxis(series_name="总抚养比", y_axis=y_data_all, markpoint_opts=opts.MarkPointOpts(
            data=[opts.MarkPointItem(name="1995年", coord=[22, y_data_all.values[22]],
                                     value="%.2f" % (y_data_all.values[22]))
                  ]
        ))
            .add_yaxis("少儿抚养比", y_data_new)
            .add_yaxis("老年抚养比", y_data_old)
            .set_global_opts(
            # y轴显示百分比，并设置最小值和最大值
            yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter='{value}%')),
            title_opts=opts.TitleOpts(title="中国抚养比变化曲线图",
                                      pos_left="center",
                                      pos_top="bottom"),
            xaxis_opts=opts.AxisOpts(type_="category"),
        )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    )
    # 4、渲染图像，将两个图像显示在一个html中
    page = Page(layout=Page.DraggablePageLayout)
    page.add(line1)
    page.add(line2)
    page.add(pie)
    page.render('analysis_age.html')


if __name__ == '__main__':
    # analysis_total()
    # analysis_sex()
    # analysis_urbanization()
    # analysis_growth()
    analysis_age()
