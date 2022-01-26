function txt = displayCoordinates(~,info)
    x = info.Position(1);
    y = info.Position(2);
    load gm_table.mat
    nst=find(utmx==x & utmy==y)
    txt = [ num2str(x) ' | ' num2str(y);BM(nst) ]
%     app.ListStationListBox.Value=BM(nst)
end