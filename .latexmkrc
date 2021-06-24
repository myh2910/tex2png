push @extra_pdflatex_options, '-synctex=1' ;

sub asy {return system("asy -o asy/ '$_[0]'");}
add_cus_dep("asy","eps",0,"asy");
add_cus_dep("asy","pdf",0,"asy");
add_cus_dep("asy","tex",0,"asy");

$pdf_mode = 1;
$pdflatex =
	'pdflatex %O'.
		'"\\expandafter\\def\\csname sa@internal@rune\\endcsname{1}\\input{"%S"}"; '.
	'convert -density 1000 -trim %D +profile "*" png/$(basename $(dirname "%D"))/%R.png';

# vim: ft=perl
