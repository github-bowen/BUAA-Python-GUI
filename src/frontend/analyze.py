# -*- coding = utf-8 -*-
# @Time :2022/8/15 19:26
# @Author:banana889
# @File : analyze.py

from PyQt5.QtWidgets import QMainWindow, QGridLayout
from PyQt5.QtChart import *
from src.backend.species import *
from src.backend.Module import *

from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter



class AnalyzeWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user

    def refresh(self):
        self.create_piechart()
        self.create_Serieschart()
        self.init_Ui()
        self.show()

    def init_Ui(self):
        self.setWindowTitle("数据分析")
        self.setGeometry(100, 100, 1280, 600)
        analyzGrid=QGridLayout(self)
        analyzGrid.setSpacing(25)
        analyzGrid.addWidget(self.chartview1,0,1)
        analyzGrid.addWidget(self.chartview2,0,2)
        widget=QWidget()
        widget.setLayout(analyzGrid)
        self.setCentralWidget(widget)

    def create_piechart(self):
        series = QPieSeries()
        data = self.user.getTaskSpeciesOfToday()
        # todo 下面这句注释掉
        # data = {Species.work:0, Species.sport : 20, Species.fun:30, Species.other : 22, Species.study:40}

        for k in data.keys():
            series.append(speciesDict[k], data[k])

        dv = list(data.values())
        for i in range(5):
            slice0 = QPieSlice()
            slice0 = series.slices()[i]
            slice0.setLabelVisible(dv[i] != 0)

        # slice1 = QPieSlice()
        # slice1 = series.slices()[1]
        # slice1.setLabelVisible(True)
        #
        # slice2 = QPieSlice()
        # slice2 = series.slices()[2]
        # slice2.setLabelVisible(True)
        #
        # slice3 = QPieSlice()
        # slice3 = series.slices()[3]
        # slice3.setLabelVisible(True)
        #
        # slice4 = QPieSlice()
        # slice4 = series.slices()[4]
        # slice4.setLabelVisible(True)


        chart = QChart()
        chart.legend().hide()
        chart.addSeries(series)
        chart.createDefaultAxes()
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle("今日任务种类统计图")

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        self.chartview1 = QChartView(chart)
        self.chartview1.setRenderHint(QPainter.Antialiasing)
        # chartview.setStyleSheet("QLabel{color:#015F17}")

        #self.setCentralWidget(chartview)

    # 绘制折线图
    def create_Serieschart(self):
        chart = QChart()
        chart.setTitle("最近7天任务完成数量统计图")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        # chart.setAnimationOptions(QChart.)
        chart.legend().hide()

        line_series = QLineSeries()  # Using line charts for this example
        data = self.user.getTaskNumOfLastWeek()
        days:[datetime.datetime] = list(data.keys())
        x_values = [1, 2, 3, 4, 5, 6, 7]
        y_values = list(data.values())

        # y_values = [1, 2, 4, 3, 1, 3, 5]
        for value in range(0, len(x_values)):
            line_series.append(x_values[value], y_values[value])
        chart.addSeries(line_series)  # Add line series to chart instance

        axis_x = QCategoryAxis(
            chart, labelsPosition=QCategoryAxis.AxisLabelsPositionOnValue)
        axis_x.setTickCount(8)
        for i in range(7):
            axis_x.append(days[i].strftime("%m-%d"), i + 1)
        chart.setAxisX(axis_x)
        line_series.attachAxis(axis_x)

        axis_y = QValueAxis()
        axis_y.setMin(0)
        axis_y.setMax(max(y_values) + 1)
        axis_y.setLabelFormat("%d")
        chart.setAxisY(axis_y)
        line_series.attachAxis(axis_y)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        v_box = QVBoxLayout()
        v_box.addWidget(chart_view)

        chart.legend().hide()
        # chart.createDefaultAxes()
        chart.setAnimationOptions(QChart.SeriesAnimations)

        self.chartview2 = QChartView(chart)
        self.chartview2.setRenderHint(QPainter.Antialiasing)

        #self.setCentralWidget(chartview)

# user = User("test")
# App = QApplication(sys.argv)
# window = AnalyzeWindow(user)
# sys.exit(App.exec_())
