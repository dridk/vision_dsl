show:
	textx generate query.txt --grammar dsl.tx --target dot
	dot -Tpng -O query.dot 
	display query.dot.png	
