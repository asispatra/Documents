#
# File Name: csv2xlsx.py
#
# Date: April 16, 2020
# Author: Asis Kumar Patra
# Purpose:
#
#

# Write your python code here.

import sys
import csv
import xlsxwriter
from xlsxwriter.utility import xl_range_abs, xl_range, xl_rowcol_to_cell



def getData(data, level, newdata):
  global stack
  global xrow
  global xcol

  if level < dims:
    key_list=sorted(data.keys(), key=int)
    key_len=len(key_list)
    for key in key_list:
      newdata[key] = {}
      stack.append(key)
      getData(data[key], level + 1, newdata[key])
      stack.pop()
  else:
    print(stack)
    xcol = bxcol
    for index, element in enumerate(stack):
      if xrow == bxrow:
        worksheet.merge_range(xrow - 2, xcol, xrow - 1, xcol, dims_name[index], HC_merge_format)
      worksheet.write(xrow, xcol, element, CC_caption_format)
      xcol = xcol + 1

    key_list=sorted(data.keys(), key=int)
    for metric in metrics:
      if xrow == bxrow:
        worksheet.merge_range(xrow -2, xcol, xrow -2, xcol + len(key_list) - 1, metric, HR_merge_format)
      for key in key_list:
        if xrow == bxrow:
          worksheet.write(xrow - 1, xcol, "Run%s" % (key), RC_caption_format)
        worksheet.write(xrow, xcol, float(data[key][metric]), cell_format)
        xcol = xcol + 1
      SROW = xrow
      SCOL = xcol - len(key_list)
      EROW = xrow
      ECOL = xcol - 1
      cell_range = xl_range(SROW, SCOL, EROW, ECOL)
      if xrow == bxrow: # sparklines
        worksheet.merge_range(xrow - 2, xcol, xrow - 1, xcol, '%s \nsparklines' %(metric), BLUE_merge_format)
      worksheet.add_sparkline(xrow, xcol, {'range': cell_range,
                                          'high_point': True,
                                          'low_point': True})
      xcol = xcol + 1

      if xrow == bxrow and len(FORMULAs) > 0:
        worksheet.merge_range(xrow -2, xcol, xrow -2, xcol + len(FORMULAs) - 1, metric, GREEN_merge_format)
      for FORMULA in FORMULAs:
        if xrow == bxrow:
          worksheet.write(xrow - 1, xcol, FORMULA, GREEN_caption_format)
        if FORMULAs[FORMULA_INDEX] == FORMULA:
          newdata[metric] = "='%s'!%s" % (WORKSHEET_SHORT, xl_rowcol_to_cell(xrow, xcol))
        worksheet.write_formula(xrow, xcol, '=%s(%s)' % (str(FORMULA), cell_range), GREEN_cell_format)
        xcol = xcol + 1

      if xrow == bxrow and len(CUSTOM_FORMULAs) > 0:
        worksheet.merge_range(xrow -2, xcol, xrow -2, xcol + len(CUSTOM_FORMULAs) - 1, metric, GREEN_merge_format)
      for idx, FORMULA in enumerate(CUSTOM_FORMULAs):
        F=''
        for V in FORMULA:
          if isinstance(V, int):
            F='%s%s' % (F, xl_rowcol_to_cell(xrow, xcol + V - idx))
          else:
            F='%s%s' % (F, V)
        if xrow == bxrow:
          H=''
          for V in FORMULA:
            if isinstance(V, int):
              H='%s%s' % (H, FORMULAs[V])
            else:
              H='%s%s' % (H, V)
          worksheet.write(xrow - 1, xcol, H, GREEN_caption_format)
        worksheet.write_formula(xrow, xcol, '=%s' % (str(F)), GREEN_cell_format)
        xcol = xcol + 1

    xrow = xrow + 1

FORMULAs=['MIN', 'MAX', 'AVERAGE', 'GEOMEAN', 'MODE', '_xlfn.VAR.S', '_xlfn.STDEV.S']
FORMULA_INDEX=2
CUSTOM_FORMULAs=[
[-1, '/', -7],
[-1, '/', -6],
[-1, '/', -5],
[-1, '/', -4],
]

def plotData(data, level, caption):
  global WS
  global xrow
  global xcol
  #print(level)
  if level < (dims - 2):
    for key in data.keys():
      #print(key)
      plotData(data[key], level + 1, "%s%s=%s " % (caption, dims_name[level], key))
  else:
    # xrow: current row
    # xcol: current column
    # drow: delta row shift
    # dcol: delta column shift
    # brow: base row
    # bcol: base column
    # dmrow: metric wise delta row shift, the maximum will be taken
    # bmcol: metric wise base col
    drow = 0
    brow = xrow
    bcol = xcol

    bmcol = bcol
    for metric in metrics:
      finalcaption = "%s|| Metric: %s" % (caption, metric)
      #print(finalcaption)
      xrow = brow
      xcol = bmcol

      isFirst = True
      isFirstDataCell = True
      dmrow = 0
      dcol = 0
      isFirstCol = True
      worksheet.write(xrow, xcol, finalcaption, bold_format)
      column_chart = workbook.add_chart({'type': 'column'})
      xrow = xrow + 1
      dmrow = dmrow + 1
      for row in data.keys():
        dmrow = dmrow + 1

        if isFirst == True:
          isFirst = False
          xcol = xcol+1 # Skips the first column for HC
          dcol = dcol + 1

          # Header row
          dmrow = dmrow + 1
          HR_start_row = xrow
          xrow = xrow + 1

          HR_end_row = xrow - 1

          # Column Captions
          dmrow = dmrow + 1
          #print("  ", end='')
          xcol = xcol+1 # Skips the first column for Column caption
          HR_start_col = xcol
          dcol = dcol + 1
          for col in data[row].keys():
            #print("%s " % str(col), end='')
            worksheet.write(xrow, xcol, str(col), RC_caption_format)
            xcol = xcol+1
            dcol = dcol + 1
          #print()
          xrow = xrow + 1
          HR_end_col = xcol - 1
          worksheet.merge_range(HR_start_row, HR_start_col, HR_end_row, HR_end_col, dims_name[level + 1], HR_merge_format)

        xcol = bmcol
        # Header Column
        if isFirstCol:
          isFirstCol = False
          HC_start_row = xrow
          HC_start_col = xcol
        xcol = xcol+1

        #print("%s " % str(row), end='')
        worksheet.write(xrow, xcol, str(row), CC_caption_format)
        xcol = xcol+1
        if isFirstDataCell:
          isFirstDataCell = False
          CF_start_row = xrow
          CF_start_col = xcol
        S_start_row = xrow
        S_start_col = xcol
        for col in data[row].keys():
          #print("%s " % str(data[row][col][metric]), end='')
          #worksheet.write(xrow, xcol, str(data[row][col][metric]))
          #worksheet.write(xrow, xcol, data[row][col][metric], cell_format)
          worksheet.write_formula(xrow, xcol, data[row][col][metric], cell_format)
          xcol = xcol+1
        #print()
        xrow = xrow + 1
        S_end_row = xrow - 1
        S_end_col = xcol - 1
        #cell_range = xl_range_abs(S_start_row, S_start_col, S_end_row, S_end_col)
        #column_chart.add_series({'values': '=Sheet1!%s' % (cell_range)})
        #column_chart.add_series({'values': [WS, S_start_row, S_start_col, S_end_row, S_end_col]})

      HC_end_row = xrow - 1
      HC_end_col = HC_start_col
      worksheet.merge_range(HC_start_row, HC_start_col, HC_end_row, HC_end_col, dims_name[level], HC_merge_format)
      CF_end_row = xrow - 1
      CF_end_col = xcol - 1
      #print(CF_start_row, CF_start_col, CF_end_row, CF_end_col)
      worksheet.conditional_format(
          CF_start_row,
          CF_start_col,
          CF_end_row,
          CF_end_col,
          {'type': '3_color_scale',
            'min_color': "#63BE7B",
            'mid_color': "#FFEB84",
            'max_color': "#F8696B"})

      chart_row = CF_start_row
      chart_col = CF_start_col
      category_start_row = CF_start_row
      category_start_col = CF_start_col - 1
      category_end_row = CF_start_row + dmrow - 2 -2
      category_end_col = CF_start_col - 1

      #print("### Chart:")
      while chart_col < (CF_start_col + dcol - 2):
        #print("=>> ### " , end='')
        #print(chart_row-2, chart_col, chart_row-1, chart_col)
        column_chart.add_series({
          #'name': [WS, chart_row-2, chart_col, chart_row-1, chart_col],
          'name': '=%s!%s' % (WS, xl_range_abs(chart_row-2, chart_col, chart_row-1, chart_col)),
          #'name': '=%s!%s' % (WS, xl_range_abs(chart_row-1, chart_col, chart_row-1, chart_col)),
          'categories': [WS, category_start_row, category_start_col -1, category_end_row, category_end_col],
          'values': [WS, CF_start_row, chart_col, CF_start_row + dmrow - 2 -2, chart_col]
        })
        #print("name:", chart_row-1, chart_col)
        #print("categories:", category_start_row, category_start_col, category_end_row, category_end_col)
        #print("values:", CF_start_row, chart_col, CF_start_row + dmrow - 2 -2, chart_col)
        column_chart.set_legend({'position': 'bottom'})
        column_chart.set_title ({
          'name': finalcaption,
          'name_font': {
            #'name': 'Calibri',
            'name': 'Calibri (Body)',
            #'color': 'blue',
            'size': 14,
            'bold': 0
          }
        })
        column_chart.set_y_axis({'name': 'Latency(usec)'})
        #column_chart.set_y_axis({'name': 'Sample length (mm)'})
        #column_chart.set_style(1)
        chart_col = chart_col + 1
      worksheet.insert_chart(HR_start_row, xcol + 1, column_chart)
      #print()
      if drow < dmrow:
        drow = dmrow
      bmcol = bmcol + dcol + 2 + 8
    xrow = brow + drow + 3 + 5
    xcol = bcol

    #quit()


if len(sys.argv) != 3:
  print("Usage: `%s <FILENAME> <LIST>`" % (str(sys.argv[0])))
  quit()

FILENAME=str(sys.argv[1])
LIST=str(sys.argv[2])

workbook = xlsxwriter.Workbook('%s_%s.xlsx' % (FILENAME, FORMULAs[FORMULA_INDEX]))
GREEN_merge_format = workbook.add_format({
  'bold': 1,
  'border': 1,
  'align': 'center',
  'valign': 'vcenter',
  'bg_color': '#9BBB59'})
BLUE_merge_format = workbook.add_format({
  'bold': 1,
  'border': 1,
  'align': 'center',
  'valign': 'vcenter',
  'bg_color': '#B1A0C7'})
HR_merge_format = workbook.add_format({
  'bold': 1,
  'border': 1,
  'align': 'center',
  'valign': 'vcenter',
  'bg_color': '#f79646'})
HC_merge_format = workbook.add_format({
  'bold': 1,
  'border': 1,
  'align': 'center',
  'valign': 'vcenter',
  'bg_color': '#95b3d7'})
GREEN_caption_format = workbook.add_format({
  'bold': 1,
  'border': 1,
  'align': 'center',
  'bg_color': '#C4D79B'})
RC_caption_format = workbook.add_format({
  'bold': 1,
  'border': 1,
  'align': 'center',
  'bg_color': '#fabf8f'})
CC_caption_format = workbook.add_format({
  'bold': 1,
  'border': 1,
  'align': 'center',
  'bg_color': '#dce6f1'})
cell_format = workbook.add_format({
  'border': 1,
  'num_format': '0.00'})
GREEN_cell_format = workbook.add_format({
  'border': 1,
  'num_format': '0.00',
  'bg_color': '#EBF1DE'})
bold_format = workbook.add_format({
  'bold': 1})

f = open(LIST)
reader = csv.reader(f, delimiter=' ')
for row in reader:
 WORKSHEET=row[0]
 HEADER_CSV=row[1]
 DATA_CSV=row[2]

 WS=WORKSHEET
 WORKSHEET_SHORT='%s_runs' % (WORKSHEET)

 print("### HEADER_CSV: %s" % (HEADER_CSV))
 print("### DATA_CSV: %s" % (DATA_CSV))

 dims_name=[]
 metrics=[]

 f = open(HEADER_CSV)
 reader = csv.reader(f, delimiter=',')
 for row in reader:
  #print(row)
  isIterationFound=False
  for FIELD in row:
    if FIELD == "iteration":
      isIterationFound = True
    elif isIterationFound == False:
      dims_name.append(FIELD)
    else:
      metrics.append(FIELD)

 dims=len(dims_name)

 data = {}
 f = open(DATA_CSV)
 reader = csv.reader(f, delimiter=',')
 #j=0
 for row in reader:
  #print(row)
  current = data
  i = 0
  for col in row:
    if i < (dims + 1):
      if col not in current:
        current[col] = {}
      current = current[col]
    else:
      current[metrics[dims +1 -i]] = col
    i = i + 1
 #print(data)

 worksheet = workbook.add_worksheet(WORKSHEET_SHORT)


 xrow = 0 # Row: 5
 xcol = 0 # Col: 1
 row_Headers=2
 col_Headers=dims
 xrow = xrow + row_Headers
 worksheet.freeze_panes(xrow, xcol + col_Headers)
 bxrow = xrow # base xrow
 bxcol = xcol # Base xcol
 stack = []

 newdata= {}

 getData(data, 0, newdata)
 #print(newdata)

 #############################################################################
 worksheet = workbook.add_worksheet(WS)


 xrow = 1 # Row: 5
 xcol = 0 # Col: 1

 plotData(newdata, 0, "")


#worksheet.write(xrow, xcol, 'Hello world')
workbook.close()
