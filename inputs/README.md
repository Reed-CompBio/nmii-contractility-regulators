## Method Inputs

### Interactome (`interactome-flybase-collapsed-evidence.txt`)

The interactome comes from [the `fly-interactome` GitHub repo](https://github.com/annaritz/fly-interactome). This interactome contains common names, FlyBaseIDs, and evidence.

```
#symbol1	symbol2	PubMedIDs	FlyBase1	FlyBase2	DBs	Evidence
128up	128up	23711155	FBgn0010339	FBgn0010339	droid	droid:human_interologs
128up	14-3-3zeta	17361185	FBgn0010339	FBgn0004907	droid	droid:human_interologs
128up	AdSS	22036573	FBgn0010339	FBgn0027493	droid	droid:MI:0007;droid:dpim_coapcomplex
128up	Ada2b	18719252	FBgn0010339	FBgn0037555	droid	droid:yeast_interologs
...
```

### Positive Nodes (`labeled-nodes.txt` and `positive-ids.txt`)

The labeled positive nodes come from different sources of evidence (e.g., Gene Ontology terms or Manning et. al. paper from 2014); some nodes appear in multiple sources. The `labeled-nodes.txt` contains, for each positive, the source of evidence:

```
#Name	FlyBaseID	Pos/Neg	Annotations
fog	FBgn0000719	Positive	gastrulation_GO0007369;apical_constriction_GO0003383;Manning2014
Rok	FBgn0026181	Positive	gastrulation_GO0007369;apical_constriction_GO0003383;Manning2014
RhoGEF2	FBgn0023172	Positive	gastrulation_GO0007369;Manning2014
...
```

The `positive-ids.txt` file is simply a list of the FlyBaseIDs:

```
FBgn0000014
FBgn0000017
FBgn0000077
...
```

### Namespace Mappers (`nodes-flybase.txt`)

Finally, we have a file of FlyBaseIDs, common names, UniprotID, and other aliases. This is used for mapping FlyBaseIDs into other namespaces.

```
FLYBASE	uniprot	Symbol	Aliases
FBgn0030647	Q9VXU5;X2JF48	CG6324	Dmel\CG6324
FBgn0014931	Q8T053	CG2678	B;Dmel\CG2678;anon-84Eb
FBgn0014930	O76206	CG2846	C;Dmel\CG2846;anon-84Ea
...
```
