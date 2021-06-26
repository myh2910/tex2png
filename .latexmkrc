sub asy {return system("asy -o asy/ '$_[0]'");}
add_cus_dep("asy","eps",0,"asy");
add_cus_dep("asy","pdf",0,"asy");
add_cus_dep("asy","tex",0,"asy");

$pdf_mode = 1;
$pdflatex = 'pdflatex -synctex=1 %O %S; convert -density 1000 -trim %D +profile "*" %R.png';

# vim: ft=perl
