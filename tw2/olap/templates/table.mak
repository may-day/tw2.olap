<%namespace name="tw" module="tw2.core.mako_util"/>
<%namespace name="omu" module="tw2.olap.mako_util"/>

<table ${tw.attrs(attrs=w.attrs)}>

<% 
   colgroup, theadrows, tbodyrows, tfootrows = w.getContent()
%>

% if colgroup:
 <colgroup>
  % for colattrs in colgroup:
    <col ${tw.attrs(attrs=colattrs)}>
  % endfor
 </colgroup>
% endif

% if theadrows:
  ${omu.etree(*theadrows)|n}
% endif

% if tfootrows:
  ${omu.etree(*tfootrows)|n}
% endif

% if tbodyrows:
  ${omu.etree(*tbodyrows)|n}
% endif

</table>

