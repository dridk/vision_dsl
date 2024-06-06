# vision_dsl
dsl prototype for vision


## Objectif : 

Faire une fonction qui converti : 

```
q="endocardite" AND bio:glycemie> 10 AND (pmsi:cim10 = 'FT43ATC' OR pmsi:cim10 = 'TRAFGRT')
```

en requete SQL DuckDB .. Mais je sais pas comment faire encore ... 
Un truc comme ca : 

```
SELECT * FROM docs 
JOIN data as bio on docs.ipp = bio.ipp AND bio.domain = 'bio' AND bio.key=
JOIN data as pmsi ON docs.ipp = pmsi.ipp AND pmsi.domain = 'pmsi'
WHERE docs.text LIKE '%endocardite%' AND (bio.gl)

```


@Bertrand : 
- Peux tu générer des tables factices avec des faux documents francais , des fausse valeurs ? Tu as un exemple dans create_db.py

@Lucas: 
- J'ai déjà fait la grammaire textx, elle est fonctionnelle. Peux tu regarder pour générer la requete SQL 

@Sacha: 
- Regarder pour l'aggregation dans une fenetre Windows glissante 
