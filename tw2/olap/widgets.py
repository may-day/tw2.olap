import tw2.core as twc
import logging

log = logging.getLogger(__name__)

class DisplayInfo(object):
    def __init__(self, disp):
        try:
            disp = int(disp)
        except:
            disp = 0
        self.countChildren = disp & 0xffff
        self.isDrilledDown = (disp & 0x10000) != 0
        self.isSameParentAsPrev = (disp & 0x20000) != 0
        
class Table(twc.Widget):

    template = "tw2.olap.templates.table"
    mdxresult = twc.Param("An IMDXResult object.")
    properties = twc.Param("A list of properties to load from the result cells")
    showTrigger = twc.Param("Show or hide +/- trigger", default=False)
    showSpan = twc.Param("Show or hide spanning cells", default=False)
    showRowColumnHeaders = twc.Param("Show or hide column headers of row head", default=False)
    colHeaderMap = twc.Param("Optionally substitute columns header names as by this mapping")

    resources = [
        twc.CSSLink(modname="tw2.olap", filename="static/table.css"),
        twc.Link(id="do_collapse", modname="tw2.olap", filename="static/do-collapse.gif"),
        twc.Link(id="do_expand", modname="tw2.olap", filename="static/do-expand.gif"),
        twc.Link(id="do_nothing", modname="tw2.olap", filename="static/do-nothing.gif")
        ]

    css_class = "olaptable"

    def prepare(self):
        super(Table, self).prepare()
        res=self.mdxresult
        axistuple = []
        try:
            axis=0
            while True:
                axistuple.append(res.getAxisTuple(axis))
                axis += 1
        except:
            pass

        self.slices = res.getSlice(properties=self.properties)
        self.axistuple = axistuple
        #import pdb; pdb.set_trace()
        maxhier=self.getRowColumnCount()
        if maxhier > 1 and not self.showSpan:
            self.spanning( self.axistuple[1], 0, maxhier, 0, self.getRowCount())

        maxhier=self.getColumnRowCount()
        if maxhier > 1 and not self.showSpan:
            self.spanning( self.axistuple[0], 0, maxhier, 0, self.getColumnCount())

    def getContent(self):
        colgroup = []
        theadrows = self.getLeadingRows()
        tfootrows = []
        tbodyrows = []

        cr_count = self.getColumnRowCount()
        rc_count = self.getRowColumnCount()
        cc = self.getColumnCount()

        # thead
        for cr in range(cr_count):
            if self.showColumnHeaderRow(cr):
                row_attrs = {}
                ths = []
                if rc_count > 0:
                    if self.showRowColumnHeader() and cr == cr_count-1:
                        for c in range(self.getRowColumnCount()):
                            ths.append( ("th", self.getRowColumnHeaderAttrs(c), 
                                         self.displayRowColumnHeader(c)) )
                    else:
                        ths.append( self.getEmptyRowDesc(cr) )
                for c in range(cc):
                    if self.showColumnRowCell(c, cr):
                        ths.append( ("th", self.getColumnRowCellAttrs(c, cr), 
                                     self.displayColumnRowCell(c, cr)))
   
                theadrows.append(("tr", row_attrs, ths))


        # tbody
        for r in range(self.getRowCount()):
            if self.showRow(r):
                row_attrs = {}
                tds = []
                # row header cells
                for rc in range(rc_count):
                    if self.showRowColumnCell(r, rc):
                        td_attrs = self.getRowColumnCellAttrs(r, rc)
                        div_attrs = self.getRowColumnDivAttrs(r, rc)
                        div = ("div", div_attrs, self.getRowColumnCellDesc(r, rc))
                        tds.append(("th", td_attrs, div))

                # data cells
                for c in range(cc):
                    if self.showCell(r, c):
                        tds.append(("td", self.getCellAttrs(r, c), self.displayCell(r, c)))

                tbodyrows.append(("tr", row_attrs, tds))

        # tfoot
        tfootrows = self.getTrailingRows()

        if tfootrows:
            tfootrows = ("tfoot", {}, tfootrows)

        if theadrows:
            theadrows = ("thead", {}, theadrows)

        if tbodyrows:
            tbodyrows = ("tbody", {}, tbodyrows)

        return colgroup, theadrows, tbodyrows, tfootrows
        
    def getColumnCount(self):
        return len(self.axistuple[0])

    def getColumnRowCount(self):
        
        tup = self.axistuple[0][0]
        if isinstance(tup, list):
            return len(tup)
        return 1

    def getRowCount(self):
        if self.slices:
            if isinstance(self.slices[0], list):
                return len(self.slices)
            return 1
        return 0

    def getRowColumnCount(self):
        try:
            tup = self.axistuple[1][0]
            if isinstance(tup, list):
                return len(tup)
            return 1
        except:
            return 0

    def showColumnHeaderRow(self, row):
        return True

    def getColumnRowCell(self, column, row):
        cell=self.axistuple[0][column]
        if isinstance(cell, list):
            cell=cell[row]
        return cell

    def showColumnRowCell(self, column, row):
        cell=self.getColumnRowCell(column, row)
        return getattr(cell, "_tw2_span", 1) > 0

    def getColumnRowCellAttrs(self, column, row):
        cell=self.getColumnRowCell(column, row)
        span=getattr(cell, "_tw2_span", 1)
        attrs = {"class":"column-heading-even" if column%2 == 0 else "column-heading-odd"}
        if span > 1:
            attrs["colspan"]=span
            attrs["class"] = "column-heading-span"
        return attrs

    def displayColumnRowCell(self, column, row):
        cell=self.getColumnRowCell(column, row)
        caption = cell.Caption
        if self.colHeaderMap:
            return self.colHeaderMap.get(caption, caption)
        return caption
            

    def getRowColumnCell(self, row, col):
        cell=self.axistuple[1][row]
        if isinstance(cell, list):
            cell = cell[col]
        return cell

    def showRowColumnCell(self, row, col):
        cell=self.getRowColumnCell(row, col)
        return getattr(cell, "_tw2_span", 1) > 0
 
    def getRowColumnCellDesc(self, row, col):
        e_name = "input"
        e_attrs = self.getRowColumnInputAttrs(row, col)
        e_content = self.displayRowColumnCell(row, col)
        return e_name, e_attrs, e_content

    def getRowColumnCellAttrs(self, row, col):
        cell=self.getRowColumnCell(row, col)
        span=getattr(cell, "_tw2_span", 1)
        attrs = {"class":"row-heading-even" if row%2 == 0 else "row-heading-odd"}
        if span > 1:
            attrs["rowspan"]=span
            attrs["class"] = "row-heading-span"
        return attrs

    def getRowColumnDivAttrs(self, row, col):
        cell=self.getRowColumnCell(row, col)
        level = getattr(cell, "LNum", "0")
        attrs = {"style":"margin-left: %sem" % level}
        return attrs

    def getRowColumnInputAttrs(self, row, col):
        cell=self.getRowColumnCell(row, col)
        di = DisplayInfo(getattr(cell, "DisplayInfo", "0"))
        #log.info(cell.Caption + " - dispinfo:" + getattr(cell, "DisplayInfo", "0") + ", dd:"+ (di.isDrilledDown and "YES" or "NO"))
        attrs = {"border":"0", "width":"9", "type":"image", "height":"9"}
        if di.countChildren and self.showTrigger:
            attrs["src"] =self.resources.do_collapse.link if di.isDrilledDown else self.resources.do_expand.link
        else:
            attrs["src"] =self.resources.do_nothing.link
        return attrs

    def displayRowColumnCell(self, row, col):
        cell=self.getRowColumnCell(row, col)
        return cell.Caption

    def showCell(self, row, col):
        return True

    def getCellAttrs(self, row, col):
        attrs = {"class":"cell-even" if row%2 == 0 else "cell-odd"}
        return attrs

    def getCell(self, row, col):
        if self.slices:
            if isinstance(self.slices[0], list):
                cell=self.slices[row][col]
            else:
                cell=self.slices[col]
            return cell
        return None

    def displayCell(self, row, col):
        cell = self.getCell(row,col)
        if isinstance(self.properties, basestring):
           return cell
        return "override displayRowColumnCell and assemble your cell display"
        return None
    def showRowColumnHeader(self):
        return self.showRowColumnHeaders

    def getRowColumnHeaderAttrs(self, col):
        return {"class":"heading-heading"}

    def displayRowColumnHeader(self, col):
        cell=self.axistuple[1][0]
        if isinstance(cell, list):
            cell = cell[col]
        #import pdb; pdb.set_trace()
        return cell._Hierarchy

    def showRow(self, row):
        """
        Do i want to display that row?
        """
        return True

    def getLeadingRows(self):
        return []

    def getTrailingRows(self):
        return []

    def getEmptyRowDesc(self, row):
        attrs = {"colspan":self.getRowColumnCount()}
        return attrs, None

    def spanning(self, src, hier, maxhier, start, end):
        i = start
        startcellspan = None
        if hier == maxhier:
            return
        while i < end:
            cell = src[i][hier]
            if startcellspan == None:
                startcellspan = cell
                startcellspan._tw2_span = 1
            elif startcellspan.UName == cell.UName:
                startcellspan._tw2_span += 1
                cell._tw2_span = 0
            else:
                startcellspan = cell
                startcellspan._tw2_span = 1
                self.spanning(src, hier+1, maxhier, start, i)
                start = i
                
            i+=1
            
        self.spanning(src, hier+1, maxhier, start, i)
