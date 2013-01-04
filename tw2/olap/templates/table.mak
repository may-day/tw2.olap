<%namespace name="tw" module="tw2.core.mako_util"/>
<table ${tw.attrs(attrs=w.attrs)}>
% for row in w.getLeadingRows():
  ${row | n}
% endfor
% for cr in range(0, w.getColumnRowCount()):
<tr>
% if w.getRowColumnCount() > 0:
   % if w.showRowColumnHeader() and cr == w.getColumnRowCount()-1:
      % for c in range(w.getRowColumnCount()):
        <th ${tw.attrs(attrs=w.getRowColumnHeaderAttrs(c))}>${w.displayRowColumnHeader(c)}</th>
      % endfor
   % else:
       <% 
          e_attrs, e_content = w.getEmptyRowDesc(cr)
       %>
       % if e_content:
       	 <th ${tw.attrs(attrs=e_attrs)}>${ e_content|n }</th>
       % else:
       	 <th ${tw.attrs(attrs=e_attrs)} />
       % endif
   % endif
% endif

% for c in range(0, w.getColumnCount()):
  % if w.showColumnRowCell(c, cr):
    <th ${tw.attrs(attrs=w.getColumnRowCellAttrs(c, cr))}>${w.displayColumnRowCell(c, cr)}</th>
  % endif
% endfor
</tr>
% endfor

% for r in range(0, w.getRowCount()):
% if w.showRow(r):
<tr>
% for rc in range(0, w.getRowColumnCount()):
  % if w.showRowColumnCell(r, rc):
    <th ${tw.attrs(attrs=w.getRowColumnCellAttrs(r, rc))}>
       <div ${tw.attrs(attrs=w.getRowColumnDivAttrs(r, rc))}>
       <% 
          e_name, e_attrs, e_content = w.getRowColumnCellDesc(r, rc)
       %>
       % if e_name == "input":
           <input ${tw.attrs(attrs=e_attrs)}>${e_content | n}
       % else:
          <${e_name} ${tw.attrs(attrs=e_attrs)}>${e_content | n}<${e_name}/>
        % endif
       </div>
    </th>
  % endif
% endfor
% for c in range(0, w.getColumnCount()):
  % if w.showCell(r, c):
    <td ${tw.attrs(attrs=w.getCellAttrs(r, c))}>${w.displayCell(r, c)|n}</td>
  % endif
% endfor
</tr>
% endif
% endfor

% for row in w.getTrailingRows():
  ${row | n}
% endfor

</table>
